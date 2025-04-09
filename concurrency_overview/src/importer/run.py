import logging
import requests
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typer import Typer
from multiprocessing import cpu_count
from src.logging import setup_logging
from src import db

api_url= "http://api:8000"
fetch_endpoint = f"{api_url}/fetch"
raw_endpoint = f"{api_url}/get_raw_data"

setup_logging()

logger = logging.getLogger(__name__)

app = Typer()

def collect_data():
    try:
        response=requests.post(fetch_endpoint)
        response.raise_for_status()
        return response.json()
    except Exception as exp:
        raise exp


@app.command()
def fetch(total_pages:int, num_processes:int = cpu_count):
    assert num_processes <= (2*cpu_count), "The max of threads must not exceed the number of cores * 2"
    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        for _ in range(1,total_pages):
            executor.submit(collect_data)
    
    logger.info("processed!")


def process_data(skip:int =0, limit:int=1000):
    try:
        response = requests.get(f"{raw_endpoint}?skip={skip}&limit={limit}")
        response.raise_for_status()
        data = response.json()["data"]
        new_data = []
        for item in data:
            new_data.append({
            "firstname": item["firstname"],
            "lastname": item["lastname"],
            "email": item["email"],
            "phone": item["phone"]
            })
        db.get_collection("processed_data").insert_many(new_data)

    except:
        raise

@app.command()
def process(total_pages:int=10, limit:int=1000,num_processes:int = cpu_count):
    assert num_processes <= (2*cpu_count), "The max of threads must not exceed the number of cores * 2"
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for page in range(total_pages):
            executor.submit(process_data, limit*page, limit)
    
    logger.info("processed!")



