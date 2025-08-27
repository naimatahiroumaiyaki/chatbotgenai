from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat
from app.services.message_service import get_room_messages, delete_message_in_room
from fastapi.encoders import jsonable_encoder
from app.services import message_service
#from datetime import datetime, timedelta
from app.core.db import db
from app.services.auth import verify_token 

router = APIRouter()

'''@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message vide.")
    reply = await handle_chat(req.user_id, req.message)
    return ChatResponse(reply=reply)
'''
@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, user_id: str = Depends(verify_token)):
    result = await handle_chat(user_id, payload.message, payload.room_id)
    return result




@router.get("/chat")
async def get_chats(room_id: str = Query(..., description="Room ID to get messages")):
    messages = await get_room_messages(room_id)
    return jsonable_encoder(messages)


@router.delete("/rooms/{room_id}/messages/{message_id}")
async def delete_message_in_room(room_id: str, message_id: str, user_id: str):
    deleted = await message_service.delete_message_in_room(message_id, room_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found or you don't have permission to delete it")
    return {"message": "Message deleted successfully"}




@router.put("/rooms/{room_id}/messages/{message_id}")
async def update_message(room_id: str, message_id: str, user_id: str, new_content: str = Body(..., embed=True)):
    message = await db.message.find_first(
        where={"id": message_id, "roomId": room_id, "userId": user_id}
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found or not yours")

    from datetime import datetime, timedelta, timezone
    created_at = message.createdAt
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    else:
        created_at = created_at.astimezone(timezone.utc)

    if datetime.now(timezone.utc) - created_at > timedelta(hours=24):
        raise HTTPException(status_code=403, detail="You can only edit a message within 24 hours")

    return await db.message.update(
        where={"id": message_id},
        data={"content": new_content}
    )


