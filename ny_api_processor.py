import psycopg2
from psycopg2.extras import execute_values
from api_processors.api_processor import BaseAPIProcessor
import settings


class NYAPIProcessor(BaseAPIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
        self.api_key = settings.NYT_API_KEY
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

    def _clean_tags(self, raw_news):
        clean_tags = list()
        raw_news = raw_news['results']
        if not raw_news:
            raise RuntimeError("No tags in received data")
        for item in raw_news:
            cleaned_data = {k: v for k, v in item.items()
                            if k in self.tag_fields}


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
        list_of_tags = list()
        for item in data_to_save:
            for type, tags in item.items():
                list_of_tags.extend([('nyt', tag, self.tag_names[type])
                                       for tag in tags])

        dsn = "dbname=news_api user=yehorlevchenko"
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cursor:
                execute_values(cursor, query, data_to_save)



if __name__ == '__main__':
    t = NYAPIProcessor()
    t.refresh_data()

