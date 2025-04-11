import logging
from pymongo import MongoClient
from shared.settings import Settings
from shared.logging import setup_logging

setup_logging()

config = Settings()
logger = logging.getLogger(__name__)

def get_database(name:str=config.mongoDatabase):
    """Returns a collection from the MongoDB database."""
    logger.info(f"Connecting to MongoDB database {name}...")
    client = MongoClient(config.mongoUri)
    assert client is not None, "MongoDB client not found"
    logger.info("Connected to MongoDB server.")

    db = client[name]
    assert db is not None, f"Database {name} not found"
    logger.info(f"Connected to database {name}.")
    return db