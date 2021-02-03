import psycopg2
import settings
from datetime import datetime
from main_logger import MainLogger

log = MainLogger('Deleter')

query_for_delete = """
    DELETE FROM news_to_tags 
	WHERE news_id IN ( 
	SELECT news.id
	FROM news JOIN news_to_tags ON news_to_tags.news_id=news.id
	WHERE CURRENT_DATE - news.published_date > '3 days')
	RETURNING tag_id;

DELETE FROM news 
        WHERE CURRENT_DATE - published_date > '3 days'
        RETURNING id;
"""
try:
    with psycopg2.connect(user=settings.USER_NAME,
                              password=settings.PASSWORD,
                              database="news_api") as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_for_delete)
            log.info(f'Rows deleted!')
except Exception as e:
    raise ValueError("Cannot delete from database")