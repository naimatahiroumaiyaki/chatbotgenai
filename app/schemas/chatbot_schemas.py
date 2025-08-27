# app/schemas/chatbot_schemas.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    roomId: str
    reply: str












''''
#conversation

class CreateConversationRequest(BaseModel):
    user_id:str


class AddMessageRequest(BaseModel):
    message_test:str
    '''