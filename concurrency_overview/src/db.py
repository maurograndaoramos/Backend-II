from pymongo import MongoClient
from api.settings import Settings

config = Settings()
def get_collection(name:str):

    client = MongoClient(config.mongoUri)

    assert client

    database = getattr(client,config.mongoDatabase)

    assert database

    return database[name]
