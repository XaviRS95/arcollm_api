from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from config.config import API_CONFIG
from models.models import CreateConversationRequest
#from utils.decorators import execution_handler
from responses.conversations import conversations


conversations_router = APIRouter()

@conversations_router.get('/api/user_conversations/{user_email}')
async def user_conversations(user_email: str):
    response =  await conversations.get_user_conversation_list(user_email=user_email)
    return response

@conversations_router.get('/api/conversation/{conversation_id}')
async def get_full_conversation(conversation_id: str):
    # return await get_full_conversation(conversation_id=conversation_id)
    pass

@conversations_router.post('/api/conversation')
async def create_conversation(request: CreateConversationRequest):
    response = await conversations.create_conversation(request = request)
    return response




