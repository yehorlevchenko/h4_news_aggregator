import logging


class ApiLogger:
    def __init__(self, parent):
        self.parent = parent
        self._init_logger(self.parent.__class__.__name__)

    def _init_logger(self, name):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(message)s',
                                      "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler('api.log')
        fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.log.addHandler(fh)
        self.log.addHandler(ch)

    def debug(self, msg, *args, **kwargs):
        self.log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log.critical(msg, *args, **kwargs)


my_log = logging.getLogger('custom')


