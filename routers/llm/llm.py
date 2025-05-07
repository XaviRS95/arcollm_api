from fastapi import APIRouter
from config.config import API_CONFIG
from models.models import ChatRequest
#from utils.decorators import execution_handler
from responses.llm import llm as llm_responses

llm_router = APIRouter()

@llm_router.get("/api/models_list")
def list_models():
    response = llm_responses.ollama_model_list()
    return response

@llm_router.post("/api/async_chat_request")
async def async_chat_request(request: ChatRequest):
    return await llm_responses.async_chat_request(request=request)

@llm_router.post("/api/sync_chat_request")
def sync_chat_request(request: ChatRequest):
    return llm_responses.sync_chat_request(request=request)