import logging

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def log(message):
    logger.log(logging.INFO, message)
