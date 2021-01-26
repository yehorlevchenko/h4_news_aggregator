import psycopg2
from psycopg2.extras import execute_values
import settings
import traceback
import sys


num_of_days_kept = 3
removal_query = f"""
    WITH DELETED AS (
        DELETE FROM news 
        WHERE NOW() - published_date > '{num_of_days_kept} days' 
        RETURNING id
    )
    DELETE FROM news_to_tags WHERE news_id IN (SELECT id FROM DELETED)
    RETURNING id
"""

dsn = settings.DSN
try:
    with psycopg2.connect(dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(removal_query)
            print(f"Deleted {cursor.rowcount} entries from [news_to_tags]")
except Exception as ex:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(f'{"".join(traceback.format_exception(exc_type, exc_value, exc_tb))}')
    raise ex
else:
    print('OK')

