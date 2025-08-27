# app/core/config.py
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

gemini_API_KEY = os.getenv("GEMINI_API_KEY")
print(os.getenv("GEMINI_API_KEY"))
#https://github.com/naimatahiroumaiyaki/chatbotgenai.git
#link to send to Ousmane