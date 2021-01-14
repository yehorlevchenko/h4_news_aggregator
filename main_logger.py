import logging


class MainLogger(logging.Logger):
    def __init__(self, parent):
        super().__init__(parent.__class__.__name__)
        self.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(message)s',
                                      "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler('api.log')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.addHandler(fh)
        self.addHandler(ch)


if __name__ == '__main__':
    from api_processors.ny_api_processor import NYAPIProcessor
    from api_processors.api_processor import APIProcessor
    t = NYAPIProcessor()
    my_log = MainLogger(t)
    my_log.error('error')
    my_log.info('info')
    t2 = APIProcessor()
    my_log2 = MainLogger(t2)
    my_log2.error('error')
    my_log2.info('info')


