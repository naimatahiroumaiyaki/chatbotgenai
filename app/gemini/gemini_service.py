# app/services/gemini_service.py
from google import genai

client = genai.Client(api_key="AIzaSyBnhFgcSTEsuZs7RQ07HkfFRZe8s56Oh4M")

def get_gemini_reply(message: str) -> str:
    """
    Utilise gemini pour générer une réponse à partir d'un message.
    """
    try:
        response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=message,
)
        
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"
