import asyncio
import logging
import requests
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, wait
from typer import Typer
from multiprocessing import cpu_count
from shared.logging import setup_logging
from shared import db

api_url= "http://api:8000"
fetch_endpoint = f"{api_url}/fetch"
raw_endpoint = f"{api_url}/get_raw_data"

setup_logging()

logger = logging.getLogger(__name__)

app = Typer()

def collect_data(api_url:str=api_url):
    """Fetches data from FakerAPI and saves it to MongoDB."""
    try:
        logger.info("Fetching data from the API...")
        fetch_endpoint = f"{api_url}/fetch"
        response=requests.post(fetch_endpoint)
        logger.info(f"Response: {response}")
        response.raise_for_status()
        return response.json()
    except Exception as exp:
        logger.error(f"Error fetching data: {exp}")
        raise exp


@app.command()
def fetch(total_pages:int,api_url:str=api_url):
    """Fetches data from FakerAPI and saves it to MongoDB."""
    logger.info("Starting fetch process...")
    with ThreadPoolExecutor() as executor:
        logger.info(f"Fetching {total_pages} pages...")
        futures = []
        for page in range(total_pages):
            logger.info(f"Fetching page {page}...")
            futures.append(executor.submit(collect_data, api_url))
        for future in as_completed(futures):
            logger.info(f"Page {page} fetched successfully.")
            logger.info(f"Result: {future.result()}")
    logger.info("Waiting for all processes to complete...")
    executor.shutdown(wait=True)
    logger.info("All processes completed!")

async def process_page(page:int, limit:int, endpoint:str):
    """Processes a single page of data."""
    try:
        logger.info(f"Processing page {page}...")
        response = requests.get(f"{endpoint}/get_raw_data?skip={page * limit}&limit={limit}")
        logger.info(f"Response: {response}")
        response.raise_for_status()
        data = response.json()
        new_data :list[dict]= []
        for item in data:
            new_data.append({
            "firstname": item["firstname"],
            "lastname": item["lastname"],
            "email": item["email"],
            })
        logger.info(f"Processed {len(new_data)} items...")
        if new_data:
            db.get_database().processed_data.insert_many(new_data)
        logger.info(f"Inserted {len(new_data)} items into processed_data collection.")
        return new_data
    except Exception as exp:
        logger.error(f"Error processing page {page}: {exp}")
        raise exp



async def process_data(total_pages:int, limit:int, endpoint:str):
    """Processes data from MongoDB and saves it to a new collection."""

    logger.info("Starting data processing...")
    assert total_pages > 0, "Total pages must be greater than 0"
    assert limit > 0, "Limit must be greater than 0"
    logger.info(f"Fetching {total_pages} pages of raw data...")

    asyncio.gather(*[
        process_page(page, limit, endpoint) for page in range(total_pages)
    ])

    logger.info("Waiting for all processes to complete...")


@app.command()
def process(total_pages:int=10, limit:int=1000, num_processes:int=cpu_count(), api_url:str=api_url):
    """Processes data from MongoDB and saves it to a new collection."""
    assert total_pages > 0, "Total pages must be greater than 0"
    assert limit > 0, "Limit must be greater than 0"
    assert num_processes > 0, "Number of processes must be greater than 0"  
    assert num_processes <= 2 * cpu_count(), "Number of processes must be less than or equal to the number of CPUs"
    logger.info("Starting process...")
    asyncio.run(process_data(total_pages, limit, api_url))
    logger.info("Process completed!")
    