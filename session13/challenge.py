from fastapi import FastAPI, Request
import time
import logging

app = FastAPI()

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url} completed_in={process_time:.2f}ms status_code={response.status_code}")
    return response

# Error Handling Middleware
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logging.error(f"Unhandled error: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Performance Optimization: Use async endpoints and database queries

@app.get("/fast")
async def fast_endpoint():
    await asyncio.sleep(0.1)  # Simulate async work
    return {"message": "Fast response"}

