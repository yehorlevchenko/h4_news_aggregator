import psycopg2
import schedule
import time
from settings.generic import *


def db_clean():
    delete_old_news_and_tags = """
    DELETE FROM tags
    WHERE tags.id IN 
        (SELECT tag_id
        FROM news_to_tags
        WHERE news_to_tags.news_id IN 
            (SELECT id
            FROM news   
            WHERE news.published_date < CURRENT_TIMESTAMP - INTERVAL '72 hours'
            )
        );

    DELETE FROM news_to_tags
    WHERE news_to_tags.news_id IN 
        (SELECT id
        FROM news   
        WHERE news.published_date < CURRENT_TIMESTAMP - INTERVAL '72 hours'
        );

    DELETE FROM news
    WHERE news.published_date < CURRENT_TIMESTAMP - INTERVAL '72 hours';
    """
    with psycopg2.connect(dbname=POSTGRES_DB_NAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute(delete_old_news_and_tags)

    print('DB is cleaned!')


schedule.every().day.at("00:00").do(db_clean)

while True:
    schedule.run_pending()
    time.sleep(1)

