from fastapi import FastAPI, HTTPException
import aiohttp
import asyncio

app = FastAPI()

async def simulated_io_task():
    await asyncio.sleep(1)
    return "Data fetched!"

@app.get("/async-data")
async def get_data():
    result = await simulated_io_task()
    return {"message": result}

async def fetch_data_source_1():
    await asyncio.sleep(2)
    return "Data from source 1"

async def fetch_data_source_2():
    await asyncio.sleep(3)
    return "Data from source 2"

@app.get("/concurrent-data")
async def get_concurrent_data():
    data1, data2 = await asyncio.gather(
        fetch_data_source_1(),
        fetch_data_source_2()
    )
    return {"source_1": data1, "source_2": data2}

async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Error fetching {url}")
            return await response.text()

@app.post("/scrape")
async def scrape_urls(urls: list[str]):
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs provided")

    try:
        html_contents = await asyncio.gather(*(fetch_html(url) for url in urls))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"html_contents": html_contents}