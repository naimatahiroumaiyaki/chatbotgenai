# app/core/config.py
import os
from dotenv import load_dotenv
print(os.getenv("GEMINI_API_KEY"))
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

gemini_API_KEY = os.getenv("GEMINI_API_KEY")
