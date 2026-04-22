import time

from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse   
from api import user_router, ticket_router

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):

    is_under_maintenance = True
    if is_under_maintenance:
        return JSONResponse(status_code=503, content={"massage": "Kechirasiz, serverda texnik ishlar olib borilmoqda."})
    
    user_agent = request.headers.get("user_agent", "").lower()
    if "postman" in user_agent:
        print("Diqqat: Dasturchi Postman orqali API ga kirdi!")

    print(f"Request: {request.method} {request.url}")
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    print(f"Response: {end_time - start_time} seconds")
    response.headers["X-Process-Time"] = str(end_time - start_time)
    response.headers["X-App-Version"] = "1.0.0"

    return response


# @app.middleware("http")
# async def add_app_version_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["X-App-Version"] = "1.0.0"
#     return response

# @app.middleware("http")
# async def browser_spy(request: Request, call_next):
#     user_agent = request.headers.get("user_agent", "").lower()
#     if "postman" in user_agent:
#         print("Diqqat: Dasturchi Postman orqali API ga kirdi!")

#     response = await call_next(request)
#     return response

# @app.middleware("http")
# async def maintenance_mode(request: Request, call_next):
#     is_under_maintenance = True
#     if is_under_maintenance:
#         return JSONResponse(status_code=503, content={"massage": "Kechirasiz, serverda texnik ishlar olib borilmoqda."})
#     response = await call_next(request)
#     return response

app.include_router(user_router)
app.include_router(ticket_router)