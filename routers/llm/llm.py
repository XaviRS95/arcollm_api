from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from config.config import API_CONFIG
#from utils.decorators import execution_handler
from responses.llm import ollama_async_client_request, ollama_model_list, ollama_sync_client_request

llm_router = APIRouter()

@llm_router.get("/api/models_list")
async def list_models():
    response = await ollama_model_list()
    return response

@llm_router.post("/api/async_generate")
async def async_generate(request: dict):
    message = request['prompt']
    model = request['model']
    async def event_stream():
        async for chunk in ollama_async_client_request(message=message, model=model):
            yield chunk
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={'Transfer-Encoding': 'chunked'})

@llm_router.post("/api/sync_generate")
def sync_generate(request: dict):
    message = request['prompt']
    model = request['model']
    code = ollama_sync_client_request(message=message, model=model)
    return JSONResponse(
        content=code,
        status_code=status.HTTP_202_ACCEPTED
    )