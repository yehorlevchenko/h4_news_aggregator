import psycopg2
from api_processors.api_processor import APIProcessor


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
        required_fields = ("source_api", "title", "abstract", "slug_name",
            "published_date", "url", "internal_source", "media_url")

        clean_data = list()
        raw_news = raw_data['results']
        if not raw_news:
            raise RuntimeError("No news in received data")
        for item in raw_news:
            cleaned_data = {k: v for k, v in item.items()
                            if k in self.news_fields}
            clean_data.append(cleaned_data)

        result_data = list()

        for item in clean_data:
            tuple_data = list()
            for field in required_fields:
                if field in item:
                    tuple_data.append(item[field])
                else:
                    if field == "source_api":
                        tuple_data.append("nyt")
                    elif field == "internal_source":
                        tuple_data.append(item["source"])
                    elif field == "media_url":
                        media_list = item["multimedia"]
                        if media_list is None:
                            tuple_data.append(None)
                        else:
                            for media in media_list:
                                if media["format"] == "Normal":
                                    tuple_data.append(media["url"])
            result_data.append(tuple(tuple_data))
        return result_data

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
