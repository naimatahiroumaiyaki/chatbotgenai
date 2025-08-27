from app.core.db import db
import bcrypt

async def register_user(name: str, email: str, password: str):
    existing = await db.user.find_unique(where={"email": email})
    if existing:
        raise ValueError("Email déjà utilisé")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_password = hashed_password.decode("utf-8")


    user = await db.user.create(
        data={
            "name": name,
            "email": email,
            "password": hashed_password,   
            "role": "HUMAN"
        }
    )
    return user


async def login_user(email: str, password: str):
    user = await db.user.find_unique(where={"email": email})
    if not user:
        raise ValueError("Identifiants invalides")
    
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise ValueError("Mot de passe incorect")
    return user 
