# app/api/chatbot_routes.py
from fastapi import APIRouter, HTTPException
from app.services.message_service import generate_reply
from app.schemas.chatbot_schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")
    
    reply = generate_reply(req.message)
    return ChatResponse(reply=reply)
