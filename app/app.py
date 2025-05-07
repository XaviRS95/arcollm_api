import time
import traceback
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config.config import API_CONFIG
from routers.llm.llm import llm_router
from routers.metadata.metadata import metadata_router
from utils.loggers import endpoint_info_logger, endpoint_error_logger

app = FastAPI(title=API_CONFIG['name'])

#ROUTERS:
app.include_router(llm_router)
app.include_router(metadata_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG['middleware_allow_origins'],
    allow_credentials=True,
    allow_methods=API_CONFIG['middleware_allow_methods'],
    allow_headers=API_CONFIG['middleware_allow_headers'],
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    func_name = request.scope.get("endpoint", None)
    func_name = func_name.__name__ if func_name else "unknown"

    error_trace = str(exc)

    stack_summary = traceback.extract_tb(exc.__traceback__)
    # Get the last call in the stack (where error originated)
    if stack_summary:
        last_call = stack_summary[-1]
        file_name = last_call.filename
        line_number = last_call.lineno
        function_name = last_call.name
    else:
        file_name = function_name = "unknown"
        line_number = -1

    endpoint_error_logger.error({
        "date": datetime.now(timezone.utc).isoformat(),
        "endpoint": func_name,
        "origin": {
            "client": request.scope['client'],
            "scheme": request.scope['scheme'],
            "method": request.scope['method']
        },
        "status_code": 500,
        "file_name": file_name,
        "function_name": function_name,
        "line_number": line_number,
        "error_trace": error_trace
    })

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

#Middleware to generate statistics logs:
@app.middleware("http")
async def log_request_data(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        execution_time = round((time.time() - start_time) * 1000, 2)  # in ms
        log_data = {
            "date": datetime.now(timezone.utc).isoformat(),
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "execution_time_ms": execution_time
        }
        endpoint_info_logger.debug(log_data)
        return response
    except HTTPException as http_exc:
        func_name = request.scope.get("endpoint", None)
        func_name = func_name.__name__ if func_name else "unknown"

        # Get a simplified error trace (only exception type and message)
        error_trace = str(http_exc)

        endpoint_error_logger.error({
            "date": datetime.now(timezone.utc).isoformat(),
            "url": str(request.url),
            "status_code": http_exc.status_code,
            "function": func_name,
            "error_trace": error_trace
        })

        return JSONResponse(
            status_code=http_exc.status_code,
            content={"detail": http_exc.detail}
        )



