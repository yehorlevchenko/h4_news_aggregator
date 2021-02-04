import os

from dotenv import load_dotenv

load_dotenv()

# https://nytimes.com/ API KEY
# --------------------------------------
NYT_API_KEY = os.getenv('NYT_API_KEY')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')
