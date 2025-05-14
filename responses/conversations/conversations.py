import json
import requests
from starlette.responses import JSONResponse
from fastapi import status
from config.config import OLLAMA_CONFIG
from utils.ollamaclient import ASYNC_CLIENT, SYNC_CLIENT
from models.models import CreateConversationRequest
from database.mysql import mysql

async def get_user_conversation_list(user_email: str):
    try:
        conversations = await mysql.get_user_conversations(user_email=user_email)
        content = None
        if len(conversations) != 0:
            content = {'conversations': conversations}
        return JSONResponse(
            content=content,
            status_code=status.HTTP_200_OK
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )

def get_full_conversation(conversation_id: str):
    pass

async def create_conversation(request: CreateConversationRequest):
    try:
        new_id = await mysql.create_conversation(request=request)

        return JSONResponse(
            content=new_id,
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )