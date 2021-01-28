import psycopg2
from psycopg2.extras import execute_values
from api_processor import BaseAPIProcessor
from settings import generic


class NYAPIProcessor(BaseAPIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
        self.api_key = generic.NYT_API_KEY
        self.news_fields = ["title", "abstract", "slug_name", "published_date",
                            "url", "source", "des_facet", "per_facet",
                            "org_facet", "geo_facet", "ttl_facet",
                            "topic_facet", "porg_facet", "multimedia"]
        self.tag_names = {
            "des_facet": "topic",
            "org_facet": "organisation",
            "per_facet": "person",
            "geo_facet": "geo"
        }

    def _clean_data(self, raw_data):
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
        clean_news = list()
        raw_news = raw_data['results']
        if not raw_news:
            raise RuntimeError("No news in received data")

        for item in raw_news:
            item = {k: v for k, v in item.items()
                    if k in self.news_fields}
            item['source_api'] = "nyt"
            item['slug_name'] = item['slug_name'].lower()
            item['media_url'] = None
            item['media_copyright'] = None
            if item.get('multimedia'):
                normal_media = [m for m in item['multimedia']
                                if m["format"] == "Normal"]
                if normal_media:
                    item['media_url'] = normal_media[0]["url"]
                    item['media_copyright'] = normal_media[0]["copyright"]
            # del (item['multimedia'])
            item['internal_source'] = item.pop('source')
            clean_news.append(item)
        return clean_news

    def _save_data(self, clean_news):
        news_query = """
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
        VALUES (%(source_api)s, %(title)s, %(abstract)s, %(slug_name)s, 
                %(published_date)s, %(url)s, %(internal_source)s, %(media_url)s,
                %(media_copyright)s)
        ON CONFLICT ON CONSTRAINT original_news 
        DO NOTHING
        RETURNING id;
        """
        tags_query = """
        INSERT INTO tags (
            source_api,
            tag_name,
            tag_group
        )
        VALUES %s
        ON CONFLICT (source_api, tag_name, tag_group) 
        DO 
            UPDATE SET
                source_api = EXCLUDED.source_api
        RETURNING id;
        """
        news_to_tags_query = """
        INSERT INTO news_to_tags (
            news_id,
            tag_id
        )
        VALUES %s;
        """
        dsn = self.dsn
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cursor:
                for item in clean_news:
                    # TODO: exception handling
                    cursor.execute(news_query, item)
                    if cursor.rowcount == 0:
                        continue
                    news_id = cursor.fetchone()
                    tags = list()
                    for category in self.tag_names:
                        raw_tags = item[category]
                        if not raw_tags:
                            continue
                        tags.extend([('nyt', tag, self.tag_names[category])
                                     for tag in raw_tags])
                    if not tags:
                        continue
                    # TODO: exception handling
                    execute_values(cursor, tags_query, tags)
                    if cursor.rowcount != len(tags):
                        print(item)
                        raise RuntimeError(f"Tags not saved: got {cursor.rowcount}, has {len(tags)}")

                    tags_id = [row[0] for row in cursor.fetchall()]
                    news_and_tags = [(news_id, tag) for tag in tags_id]
                    # TODO: exception handling
                    execute_values(cursor, news_to_tags_query,
                                   news_and_tags)


if __name__ == '__main__':
    from time import sleep
    t = NYAPIProcessor()
    while True:
        t.refresh_data()
        sleep(350)
