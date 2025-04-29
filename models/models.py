from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

class CreateConversationRequest(BaseModel):
    email: str
    messages: List
    model = str

class AsyncClientRequestOllama(BaseModel):
    messages: List
    model: str

class SyncClientRequestOllama(BaseModel):
    message: str
    model: str
