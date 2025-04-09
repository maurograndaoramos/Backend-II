import asyncio
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from typer import Typer
from multiprocessing import cpu_count
from src.logging import setup_logging
from src import db
import pandas as pd

api_url= "http://api:8000"
processed_endpoint = f"{api_url}/get_processed_data"

setup_logging()

logger = logging.getLogger(__name__)

app = Typer()

async def collect_data():
    try:
        response= await requests.post(processed_endpoint)
        response.raise_for_status()
        return response.json()
    except Exception as exp:
        raise exp

async def export_to_csv():
    data = await collect_data()
    df = pd.DataFrame(data)    
    df.to_csv("output.csv")
    logger.info("processed!")

@app.command()
def export():
    asyncio.run(export_to_csv())
   
