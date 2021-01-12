import requests
import logging


class APIProcessor:
    def __init__(self):
        self.url = ""
        self.api_key = ""
        self.offset = 20
        self.limit = 20
        # TODO: make logging module and use it
        self._init_logger()

    def _init_logger(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - {self.__class__.__name__} - %(message)s',
                                      "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler('api.log')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.log.addHandler(fh)
        self.log.addHandler(ch)

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
            clean_data = self._clean_data(raw_data=new_data)
        except Exception as e:
            self.log.error(f'refresh_data - '
                           f'failed to clean data: '
                           f'{e}')
            return False

        try:
            self._save_data(data_to_save=clean_data)
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
            "offset": self.offset
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
            raise RuntimeError(f'{response.status_code}: {response.text}')

        return response.json()

    def _clean_data(self, raw_data):
        raise NotImplementedError

    def _save_data(self, data_to_save):
        pass


if __name__ == '__main__':
    t = APIProcessor()
    t.refresh_data()

