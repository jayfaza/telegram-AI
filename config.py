import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.1:8b"
DATA = "/home/jayfaza/projects/telegram-bot/data.json"
GREET_MESSAGE = """👋 Привет!  

Рад(а) видеть тебя в нашем сообществе!  
Я – HubertAI – твой персональный помощник: готов отвечать на вопросы, делиться полезными ресурсами и помогать решать любые задачи.  

Не стесняйся задавать вопросы, пробовать команды и просто общаться – я всегда на связи!  

🚀 Давай сделаем этот опыт ярким и полезным!"""
