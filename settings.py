import os
from dotenv import load_dotenv

load_dotenv()

# https://nytimes.com/ API KEY
# --------------------------------------
NYT_API_KEY = os.getenv('NYT_API_KEY')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
