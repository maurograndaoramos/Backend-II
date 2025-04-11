import asyncio
import csv
import logging
import requests
from typer import Typer
from shared.logging import setup_logging

api_url= "http://api:8000"

setup_logging()

logger = logging.getLogger(__name__)

app = Typer()

def collect_data(api_url:str=api_url):
    try:
        logger.info("Fetching data from the API...")
        endpoint = f"{api_url}/get_processed_data"
        response= requests.get(endpoint)
        logger.info(f"Response: {response}")
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data)} items from the API.")
        return data
    except Exception as exp:
        logger.error(f"Error fetching data: {exp}")
        raise exp

async def export_to_csv(api_url:str=api_url):
    """Fetches data from the API and saves it to a CSV file."""
    logger.info("Fetching data from the API...")
    data = collect_data(api_url)
    logger.info(f"Fetched {len(data)} items from the API.")
    logger.info("Saving data to CSV...")
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["firstname", "lastname", "email"])
        for item in data:
            writer.writerow(item.values())
    logger.info("Data saved to output.csv")
    logger.info("Data processing complete!")

@app.command()
def export(api_url:str=api_url):
    """Export data to CSV."""
    logger.info("Starting export process...")
    asyncio.run(export_to_csv(api_url))
    logger.info("Export process complete!")
   