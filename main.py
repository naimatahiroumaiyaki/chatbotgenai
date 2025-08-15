# app/main.py
from fastapi import FastAPI
from app.api import chatbot_route

app = FastAPI(title="Chatbot API", version="0.1.0")

# Montage des routes
app.include_router(chatbot_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
