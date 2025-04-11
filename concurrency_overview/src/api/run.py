import logging
import requests
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from api.models import ProcessedData, RawData
from src.shared.logging import setup_logging
from src.shared import db
from src.shared.settings import Settings


config = Settings()

api = FastAPI(
    title="Concurrency Overview",
    description="A simple API to demonstrate the differences between concurrency models.",
    version="0.1.0",
)

setup_logging()
logger = logging.getLogger(__name__)


@api.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

@api.post("/fetch")
async def fetch_and_save() -> dict[str, str]:
    """Fetches data from FakerAPI and saves it to MongoDB."""
    try:
        response = requests.get(config.faker_api_url)
        response.raise_for_status()
        data = response.json()["data"]
        logger.info(f"Fetched {len(data)} items from the API.")
        client_db = db.get_database()
        logger.info(f"Saving {len(data)} items to the database...")
        client_db['raw_data'].insert_many(data)
        logger.info("Data saved to the database.")
        logger.info(f"Fetched and saved {len(data)} items.")
        return {"message": f"Fetched and saved {len(data)} items."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/get_raw_data")
async def get_all_raw_data(skip:int=0,limit:int=1000) -> list[RawData]:
    """Retrieves all raw data from MongoDB."""
    try:
        logger.info(f"Retrieving raw data from MongoDB with skip={skip} and limit={limit}.")
        data = db.get_database().raw_data.find().to_list(length=limit)
        if skip > 0:
            data = data[skip:]
        logger.info(f"Retrieved {len(data)} items from MongoDB.")

        result = []
        for item in data:
            result.append(RawData(
                _id=str(item["_id"]),
                id=item["id"],
                uuid=item["uuid"],
                firstname=item["firstname"],
                lastname=item["lastname"],
                username=item["username"],
                password=item["password"],
                email=item["email"],
                ip=item["ip"],
                macAddress=item["macAddress"],
                website=item["website"],
                image=item["image"]
            ))

        return result
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/get_processed_data/")
async def get_all_processed_data() -> list[ProcessedData]:
    """Retrieves all raw data from MongoDB."""
    try:
        logger.info("Retrieving processed data from MongoDB.")
        data = db.get_database().processed_data.find().to_list(length=None)
        result = [
            ProcessedData(
                firstname=item["firstname"],
                lastname=item["lastname"],
                email=item["email"],
            ) for item in data
        ]
        return result
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
