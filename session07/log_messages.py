import random
from logger_setup import setup_logging

def process_data(data):
    if data < 0:
        raise ValueError("Data cannot be negative!")
    return data * 2

def log_messages(logger):
    logger.debug("Starting the logging process.")

    numbers = [random.randint(-10, 10) for _ in range(5)]
    logger.info(f"Generated numbers: {numbers}")

    for number in numbers:
        try:
            logger.info(f"Processing number: {number}")
            result = process_data(number)
            logger.info(f"Processed result: {result}")
        except ValueError as e:
            logger.error(f"Error processing number {number}: {e}")

    logger.debug("Finished the logging process.")