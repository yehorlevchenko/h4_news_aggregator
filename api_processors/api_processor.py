import requests

from api_logger import MainLogger
from settings import *


class BaseAPIProcessor:
    def __init__(self):
        self.dsn = f"host={POSTGRES_HOST} " \
                   f"port={POSTGRES_PORT} " \
                   f"dbname={POSTGRES_DB_NAME} " \
                   f"user={POSTGRES_USER} " \
                   f"password={POSTGRES_PASSWORD}"
        self.url = ""
        self.api_key = ""
        self.offset = 0
        self.limit = 10
        # TODO: make logging module and use it
        self.log = MainLogger(self)

    def refresh_data(self):
        self.log.info(f'refresh_data - '
                      f'Start')
        try:
            new_data = self._get_data()
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to get data from API: '
                           f'{e}')
            return False

        try:
            clean_news = self._clean_data(raw_data=new_data)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to clean data: '
                           f'{e}')
            return False

        try:
            self._save_data(clean_news)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to save data: '
                           f'{e}')
            return False
        self.log.info(f'refresh_data - '
                      f'Done')
        return True

    def _get_data(self):
        req_params = {
            "api-key": self.api_key,
            "offset": self.offset,
            "limit": self.limit
        }
        try:
            response = requests.get(self.url, params=req_params)
        except Exception as e:
            self.log.error(f'_get_data - '
                           f'failed to make a request: '
                           f'{e}')
            raise e
        if response.status_code != 200:
            self.log.error(f'_get_data - '
                           f'received {response.status_code}')
            raise RuntimeError(
                f'{response.status_code}: {response.text}')

        return response.json()

    def _clean_data(self, raw_data):
        raise NotImplementedError

    def _save_data(self, data_to_save):
        raise NotImplementedError


if __name__ == '__main__':
    t = BaseAPIProcessor()
    t.refresh_data()

