# app/services/chatbot_service.py
from app.gemini.gemini_service import get_gemini_reply

def generate_reply(message: str) -> str:
    """
    Appelle gemini pour obtenir une réponse intelligente.
    """
    return get_gemini_reply(message)

