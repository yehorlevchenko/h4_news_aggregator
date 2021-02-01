import psycopg2
from psycopg2.extras import execute_values
from settings.generic import *
from custom_logging.main_logger import MainLogger
import schedule
import time


log = MainLogger('Deleter')
old_news = 3
removal_query = f"""
    WITH DELETED AS (
        DELETE FROM news 
        WHERE CURRENT_TIMESTAMP - published_date > '{old_news} days' 
        RETURNING id
    )
    DELETE FROM news_to_tags WHERE news_id IN (SELECT id FROM DELETED)
    RETURNING id
"""
dsn = f"host={POSTGRES_HOST} " \
      f"port={POSTGRES_PORT} " \
      f"dbname={POSTGRES_DB_NAME} " \
      f"user={POSTGRES_USER} " \
      f"password={POSTGRES_PASSWORD}"


def clean_old_news():
    with psycopg2.connect(dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(removal_query)
            log.info(f'Rows deleted!')


schedule.every().day.at("00:01").do(clean_old_news)
while True:
    schedule.run_pending()
    time.sleep(1)
