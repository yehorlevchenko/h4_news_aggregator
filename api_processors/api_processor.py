import requests
import logging
from logger import logger


class APIProcessor:
    def __init__(self):
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/podcasts.json"
        self.api_key = "6LWMg0c19nLU7dKwBR6QRXQ5A6elwqmp"
        self.offset = 20
        self.limit = 20
        # TODO: make logging module and use it
        # self.log = logging.getLogger(__name__)

    def refresh_data(self):
        logger.info(f'{__name__} - start')

        try:
            new_data = self._get_data()
        except Exception as e:
            logger.error(f'{__name__} - failed to get data from API: {e}')
            return False

        try:
            clean_data = self._clean_data(raw_data=new_data)
        except Exception as e:
            logger.error(f'{__name__} - failed to clean data: {e}')
            return False

        try:
            self._save_data(data_to_save=clean_data)
        except Exception as e:
            logger.error(f'{__name__} - failed to say data: {e}')
            return False
        logger.info(f'{__name__} - Done')
        return True

    def _get_data(self):
        req_params = {
            "api-key": self.api_key,
            "offset": self.offset
        }
        try:
            response = requests.get(self.url, params=req_params)
        except Exception as e:
            logger.error(f'{__name__} - failed to make a request: {e}')
            raise e
        if response.status_code != 200:
            logger.error(f'{__name__} - received {response.status_code} ')
            raise RuntimeError(f'{response.status_code}: {response.text}')

        return response.json()

    def _clean_data(self, raw_data):
        raise NotImplementedError

    def _save_data(self, data_to_save):
        pass


if __name__ == '__main__':
    t = APIProcessor()
    t.refresh_data()

