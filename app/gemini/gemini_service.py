# app/services/gemini_service.py
from google import genai
import os
import json

##
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#check if the API key is set 
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
client = genai.Client(api_key=GEMINI_API_KEY)

with open("bagri_knowledge.json", "r", encoding="utf-8") as f:

    data = json.load(f)

bagri_knowledge = f"""
    Tu es un assistant virtuel pour la Banque Agricole du Niger (BAGRI).
Voici des informations officielles :
Nom : {data['organization']['name']}
Siège : {data['head_office']['address']}
Téléphones : {', '.join(data['head_office']['phones'])}
Site web : {data['head_office']['website']}
Réseau : {data['network']['agencies_count']} agences présentes dans {data['network']['coverage']}
Produits : {', '.join(data['products_services']['particuliers'] + data['products_services']['professionnels'])}
Horaires par défaut : {data['hours']['default_local_time']['monday']} (lun–ven)
Directeurs : {data}
"""


def get_gemini_reply(message: str) -> str:
    """
    Utilise gemini pour générer une réponse à partir d'un message.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config={
                "system_instruction": bagri_knowledge  # Ajout de l’instruction système
            }
        ) 
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"



""" messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": message}
 ]"""
      

        
    