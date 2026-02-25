import aiohttp
import json
from config import OLLAMA_URL, OLLAMA_MODEL, DATA
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from ollama.profiles import grub_prompt


class OllamaAi:
    def __init__(self):
        """Url для общения с локальным сервером и модель"""
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.user = None

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

    async def ask_with_history(self, user, history):
        with open(DATA, "r", encoding="utf-8") as f:
            data = json.load(f)

        if user.username in data:
            model = data[user.username]["model"]
            self.model = model

        prompt = await grub_prompt(user)
        messages = [
            {
                "role": "system",
                "content": f"Твоя роль: {prompt}, Запомни без коментов и отвечай в соответствии с ним",
            },
            *history,
        ]
        payload = {"model": model, "messages": messages, "stream": False}
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
            print("ERROR ERROR")
            return "ollama is not running"
