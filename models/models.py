from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime
from config.config import OLLAMA_CONFIG

class ChatMessage(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]

class CreateConversationRequest(BaseModel):
    title: str
    user_mail: str
    model: str

class ChatRequest(BaseModel):
    conversation_id: Optional[str]
    messages: Optional[List[ChatMessage]]
    options: dict
    model: str
    user_mail: str

class CreateMessageRequest(BaseModel):
    conversation_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    user_mail: str
