from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime
from config.config import OLLAMA_CONFIG

class ChatMessage(BaseModel):
    content: str
    role: Literal["user", "assistant", "system"]

class CreateConversationRequest(BaseModel):
    email: str
    messages: List[ChatMessage]
    model: str

class ChatRequest(BaseModel):
    messages: Optional[List[ChatMessage]] = None
    message: Optional[ChatMessage] = None
    options: dict
    model: str
