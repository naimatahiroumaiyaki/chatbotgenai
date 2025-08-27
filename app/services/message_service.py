# app/services/chatbot_service.py
from sqlalchemy import true
from app.gemini.gemini_service import get_gemini_reply
from app.core.db import db
from prisma.errors import PrismaError

def generate_reply(message: str) -> str:
    """
    Appelle gemini pour obtenir une réponse intelligente.
    """
    return get_gemini_reply(message)



async def save_message(user_id: str, content: str, room_id: str = None):
    # Si pas de room_id fourni, utiliser le user_id comme room_id
    if not room_id:
        # créer une room unique par utilisateur si elle n'existe pas
        room = await db.room.upsert(
            where={"userId": user_id},
            update={},
            create={"userId": user_id}
        )
        room_id = room.id

    return await db.message.create(
        data={
            "userId": user_id,
            "roomId": room_id,
            "content": content
        }
    )


async def get_room_messages(room_id: str):
    return await db.message.find_many(
        where={"roomId": room_id},
        order={"createdAt": "asc"}  
    )

async def create_room(user_id: str):
    room = await db.room.create(
    data={
        "name": f"Room for user {user_id}",
        "userId": user_id
    }
)
    return room



async def delete_message_in_room(message_id:str,room_id:str, user_id:str):
    try:
        message = await db.message.find_first(
            where={
                "id":message_id,
                "roomId": room_id,
                "userId": user_id
                }

        )

        if not message:
            return False
        await db.message.delete(
            where={"id": message_id}
        )
        
        return db.message.delete(
            where={"id": message_id}
        )
        return true


    except PrismaError:
        return False
 










