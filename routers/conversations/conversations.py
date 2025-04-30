from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from config.config import API_CONFIG
from models.models import CreateConversationRequest
#from utils.decorators import execution_handler


conversations_router = APIRouter()

@conversations_router.get('/api/conversations_list')
def conversations_list(email: str):
    # return get_user_conversation_list(email=email)
    pass

@conversations_router.get('/api/conversation')
def get_full_conversation(conversation_id: str):
    # return get_full_conversation(conversation_id=conversation_id)
    pass

@conversations_router.post('/api/conversation')
def create_conversation(request: CreateConversationRequest):
    # return create_conversation(request = request)
    pass





