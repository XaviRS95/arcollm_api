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

class ChatRequest(BaseModel):
    messages: Optional[List[ChatMessage]]
    options: dict
    model: str

