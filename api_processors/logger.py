import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s: [%(asctime)s] %(funcName)s %(message)s')

fh = logging.FileHandler('advanced.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
