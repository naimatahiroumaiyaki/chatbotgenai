# app/main.py
from fastapi import FastAPI, Request
from app.api import chatbot_route, auth_routes
from app.core.db import connect_db, disconnect_db
from app.services.chat_service import ensure_bot_user
from app.core.db import db
from fastapi.responses import JSONResponse
from app.services.auth import verify_token

from fastapi.middleware.cors import CORSMiddleware
#from app.api import auth_routes
app = FastAPI(title="Chatbot API", version="0.1.0")

##


app = FastAPI()

# include the routes
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])



# Inclure le router
app.include_router(chatbot_route.router, prefix="/api", tags=["api"])

##

# Montage des routes
app.include_router(chatbot_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


@app.on_event("startup")
async def on_start():
    await connect_db()
    # créer l'utilisateur BOT si absent
    await ensure_bot_user()

@app.on_event("shutdown")
async def on_shutdown():
    await disconnect_db()


PUBLIC_PATHS = ["/auth/login", "/auth/register"]

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header  or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"details": "Token manquant"})
    token = auth_header.split(" ")[1]

    try:
        user_id = verify_token(token)
        request.state.user_id = user_id
    except:
        return JSONResponse(status_code=401, content={"detail": "Token invalide ou expiré "})
    return await call_next(request) 






app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)















