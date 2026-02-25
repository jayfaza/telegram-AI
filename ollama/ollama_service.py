import aiohttp
import json
from config import OLLAMA_URL, OLLAMA_MODEL, DATA
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class OllamaAi:
    def __init__(self):
        """Url для общения с локальным сервером и модель"""
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.user = None

    async def ask(self, prompt: str) -> str:
        """Данные для отправки запроса серверу с ollama"""
        payload = {"model": self.model, "prompt": prompt, "stream": False}

        try:
            """Открываем сессию для дальнешего подключение куда-либо"""
            async with aiohttp.ClientSession() as session:
                """Отправляем запрос ollama"""
                async with session.post(self.url, json=payload) as resp:
                    """Если сервер ответил без ошибок"""
                    if resp.status == 200:
                        """Возвращаем ответ нейросети"""

                        result = await resp.json()
                        print(result.get("model"))
                        print(result.get("response"))

                        return result.get("response", "No answer")
                    else:
                        return f"Error {resp.status}"

        except:
            return "Ollama is not running. Run: ollama serve"

    async def get_models(self) -> list:
        models_list = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:11434/api/tags") as resp:
                    raw_models = await resp.json()
                    models = raw_models["models"]
                    for model in models:
                        model = model["name"]
                        models_list.append(model)
            return models_list
        except:
            print("No response")

    async def build_keyboard(self):
        models = await self.get_models()
        models_kb = []
        buttons = [InlineKeyboardButton(text="Закрыть ❌", callback_data="remove_msg")]
        for model in models:
            models_kb.append(
                [InlineKeyboardButton(text=model, callback_data=f"model_{model}")]
            )
        models_kb.append(buttons)
        models_keyboard = InlineKeyboardMarkup(inline_keyboard=models_kb)

        return models_keyboard

    """
    async def ask_with_history(self, history):
        payload = {"model": self.model, "messages": history, "stream": False}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/chat", json=payload
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("message", {}).get("content", "Нет ответа")
                    else:
                        return f"Ошибка {resp.status}"
        except:
            return "Ollama не запущена"
    """

    async def ask_with_history(self, user, history):
        with open(DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
        if user.username in data:
            model = data[user.username]["model"]
            self.model = model
        payload = {"model": model, "messages": history, "stream": False}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/chat", json=payload
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        print(
                            f"{self.model}: {result.get("message", "none").get("content", "none")}"
                        )
                        return result.get("message", "none").get("content", "none")
                    else:
                        print(f"Server is down: {resp.status}")
        except:
            return "ollama is not running"
