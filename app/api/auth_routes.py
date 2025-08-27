from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.autho_schema import UserRegister, UserLogin, UserOut
from app.services.auth_service import register_user, login_user
from app.services.auth import create_access_token, verify_token
from datetime import timedelta
from app.core.db import db

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(payload: UserRegister):
    try:
        user = await register_user(payload.name, payload.email, payload.password)
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(payload: UserLogin):
    try:
        # 1) Authentifier l'utilisateur
        user = await login_user(payload.email, payload.password)

        # 2) Vérifier/créer la room
        room = await db.room.find_first(where={"userId": user.id})
        if not room:
            room = await db.room.create(data={"userId": user.id})
        room_id = room.id

        # 3) Générer le token JWT
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": user.id}, 
            expires_delta=access_token_expires
        )

        # 4) Retourner la réponse
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "room_id": room_id
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
