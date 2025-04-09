from http.client import HTTPException
import logging
from fastapi import FastAPI
import requests
from logging import setup_logging
from api.settings import Settings
from src import db

config = Settings()

api = FastAPI(
    title="Concurrency Overview",
    description="A simple API to demonstrate the differences between concurrency models.",
    version="0.1.0",
)

setup_logging()
logger = logging.getLogger(__name__)

@api.post("/fetch")
async def fetch_and_save() -> dict[str, str]:
    """Fetches data from FakerAPI and saves it to MongoDB."""
    try:
        response = requests.get(config.faker_api_url)
        response.raise_for_status()
        data = response.json()["data"]
        await db.get_collection("raw_data").insert_many(data)
        logger.info(f"Fetched and saved {len(data)} items.")
        return {"message": f"Fetched and saved {len(data)} items."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/get_raw_data")
async def get_all_raw_data(skip:int=0,limit:int=1000) -> list[dict]:
    """Retrieves all raw data from MongoDB."""
    try:
        data = await db.get_collection("raw_data").find().to_list(length=limit)
        return data
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/get_processed_data/")
async def get_all_processed_data() -> list[dict]:
    """Retrieves all raw data from MongoDB."""
    try:
        data = await db.get_collection("processed_data").find().to_list(length=None)
        return data
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
