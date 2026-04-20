import time

from fastapi import FastAPI, Request    
from api import user_router, ticket_router

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    print(f"Response: {end_time - start_time} seconds")
    response.headers["X-Process-Time"] = str(end_time - start_time)
    return response


app.include_router(user_router)
app.include_router(ticket_router)