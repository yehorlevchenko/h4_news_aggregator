import psycopg2
from psycopg2.extras import execute_values
from api_processor import BaseAPIProcessor
import h4_news_aggregator.settings


class NYAPIProcessor(BaseAPIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
        self.api_key = "WwOAsikuTWoGBxTLRXk2AIC7h212ffPF"
        self.news_fields = ["title", "abstract", "slug_name", "published_date",
                            "url", "source"]
        self.tag_fields = ["des_facet", "per_facet", "org_facet",
                           "geo_facet", "ttl_facet", "topic_facet",
                           "porg_facet"]
        self.tag_names = {
            "des_facet": "topic",
            "org_facet": "organisation",
            "per_facet": "person",
            "geo_facet": "geo"
        }
        self.cleaned_tags = None
        self.cleaned_news = None

    def _clean_news(self, raw_news):
        """
        Will get explicit data from API (list of dicts), remove unnecessary
        fields from each entry, and prepare a list of tuples for saving
        to the DB.
        Values order for tuple: "nyt", title, abstract, slug_name,
        published_date, url, internal_source, media_url.
        :param raw_news:
        :return:
        """

        # TODO: update in accordance with docstring
        clean_data = list()
        raw_news = raw_news['results']
        if not raw_news:
            raise RuntimeError("No news in received data")
        for item in raw_news:
            cleaned_data = ["nyt"]
            cleaned_data.extend([item[k] for k in self.news_fields
                                 if k in item])
            if not item.get('multimedia'):
                cleaned_data.extend([None, None])
            else:
                normal_media = [m for m in item['multimedia']
                                if m["format"] == "Normal"]
                if not normal_media:
                    cleaned_data.extend([None, None])
                cleaned_data.extend([normal_media[0]["url"],
                                     normal_media[0]["copyright"]])

            clean_data.append(tuple(cleaned_data))

        return clean_data

    def _clean_tags(self, raw_tags):
        tags = list()
        raw_tags = raw_tags["results"]

        if not raw_tags:
            raise RuntimeError("No tags in received data")

        for item in raw_tags:

            for key, tag_name in self.tag_names.items():
                tag = tuple(["nyt", tag_name, item.get(key)])
                tags.append(tag)
        return tags

    def _save_news(self, data_to_save):
        query = """
        INSERT INTO news (
            source_api,
            title,
            abstract,
            slug_name,
            published_date,
            url,
            internal_source,
            media_url,
            media_copyright
        )
        VALUES %s;
        """
        dsn = "dbname=news_api user=yehorlevchenko"
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cursor:
                execute_values(cursor, query, data_to_save)

    def _save_tags(self, data_to_save):
        query = """
        INSERT INTO tags (
            source_api,
            name,
            group
        )
        VALUES %s;
        """
        dsn = "dbname=news_api user=yehorlevchenko"
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cursor:
                execute_values(cursor, query, data_to_save)

    def _clean_data(self, raw_data):
        self.cleaned_tags = self._clean_tags(raw_data)
        self.cleaned_news = self._clean_news(raw_data)


if __name__ == '__main__':
    t = NYAPIProcessor()
    t.refresh_data()