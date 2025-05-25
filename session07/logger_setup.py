import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    file_handler = TimedRotatingFileHandler("daily.log", when="midnight", interval=1)
    file_handler.suffix = "%Y-%m-%d"
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger