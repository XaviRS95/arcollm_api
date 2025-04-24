import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config.config import API_CONFIG
from routers.llm.llm import llm_router
from routers.metadata.metadata import metadata_router

app = FastAPI(title=API_CONFIG['name'])

app.include_router(llm_router)
app.include_router(metadata_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG['middleware_allow_origins'],
    allow_credentials=True,
    allow_methods=API_CONFIG['middleware_allow_methods'],
    allow_headers=API_CONFIG['middleware_allow_headers'],
)

@app.middleware("http")
async def request_handling(request: Request, call_next):
    start_time = time.time()
    endpoint = str(request.url)
    method = request.method
    response = await call_next(request)
    status_code = response.status_code
    process_time = time.time() - start_time
    response.headers['Client-IP'] = request.client.host
    response.headers['X-Process-Time'] = str(process_time)

    return response