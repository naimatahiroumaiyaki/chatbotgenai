from app.core.db import db
from app.services.message_service import save_message,generate_reply, create_room



BOT_EMAIL = "bot@local"
BOT_NAME = "Bagri Bot"

async def ensure_bot_user():
    bot = await db.user.find_unique(where={"email": BOT_EMAIL})
    if not bot:
        bot = await db.user.create(
            data={
                "name": BOT_NAME,
                "email": BOT_EMAIL,
                "role": "BOT"
            }
        )
    return bot



async def handle_chat(user_id: str, message: str, room_id: str) -> str:
    if not room_id:

    # 1) sauver le message utilisateur
        room = await create_room(user_id)
        room_id = room.id
    await save_message(user_id=user_id, room_id=room_id, content=message)    

    # 2) générer la réponse
    
    reply =  generate_reply(message)

    # 3) sauver la réponse du BOT (en tant qu'utilisateur BOT)
    bot = await ensure_bot_user()
    await save_message(user_id=bot.id, room_id=room_id, content=reply)

    return {
        "roomId": room_id,
        "reply": reply
    }

