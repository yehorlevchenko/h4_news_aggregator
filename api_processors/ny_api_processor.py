import psycopg2
from api_processor import APIProcessor


class NYAPIProcessor(APIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
        self.api_key = "6LWMg0c19nLU7dKwBR6QRXQ5A6elwqmp"
        self.news_fields = ["slug_name", "section", "subsection", "title",
                            "abstract", "url", "source", "published_date",
                            "multimedia", "des_facet", "per_facet",
                            "org_facet", "geo_facet", "ttl_facet",
                            "topic_facet", "porg_facet"]


    def _clean_data(self, raw_data):
        """
        Will get explicit data from API (list of dicts), remove unnecessary
        fields from each entry, and prepare a list of tuples for saving
        to the DB.
        Values order for tuple: "nyt", title, abstract, slug_name,
        published_date, url, internal_source, media_url.
        :param raw_data:
        :return:
        """
        # TODO: update in accordance with docstring
        news_field_for_tuple = ('source', 'title', 'abstract', 'slug_name',
                                'published_date', 'url', 'internal_source')
        clean_data = list()

        raw_news = raw_data['results']
        if not raw_news:
            raise RuntimeError("No news in received data")

        for item in raw_news:
            clean_data_for_item = [item.get(field)
                                   for field in news_field_for_tuple]

            try:
                multimedia = item['multimedia']
                media_url = multimedia[0]['url']
            except KeyError:
                media_url = ''
            except TypeError:
                media_url = ''

            clean_data_for_item.append(media_url)
            clean_data.append(tuple(clean_data_for_item))

        return clean_data

    def _save_data(self, data_to_save):
        query = """
        INSERT INTO news (
            source_api,
            title,
            abstract,
            slug_name,
            published_date,
            url,
            internal_source,
            media_url
        )
        VALUES (%s);
        """
        raise NotImplementedError


if __name__ == '__main__':
    t = NYAPIProcessor()
    t.refresh_data()
