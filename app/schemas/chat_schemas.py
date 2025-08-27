from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    room_id: Optional[str] = None


class ChatResponse(BaseModel):
    roomId: str
    reply: str
