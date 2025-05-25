from logger_setup import setup_logging
from log_messages import log_messages

if __name__ == "__main__":
    logger = setup_logging()
    log_messages(logger)