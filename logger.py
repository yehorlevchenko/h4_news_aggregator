import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler('api_processor.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)

bh = logging.FileHandler('api_processor.log')
bh.setLevel(logging.INFO)
bh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(bh)
logger.addHandler(ch)

