import aiohttp
import json
from config import OLLAMA_URL, OLLAMA_MODEL, DATA, MODELS_LIST
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv()
MISTRAL = os.getenv("MISTRAL")

from ollama.profiles import grub_prompt


class OllamaAi:
    def __init__(self):
        """Url для общения с локальным сервером и модель"""
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.user = None
        self.mistral = Mistral(api_key=MISTRAL)

    async def get_models(self) -> list:
        return MODELS_LIST

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

    async def ask_mistral(self, user, model, history):
        username = str(user.username)
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

        if username in data:
            prompt = (
                data[username]["prompt"]
                if "prompt" in data[username]
                else "Ты вежливый и приятный"
            )
        history = [
            {
                "role": "system",
                "content": f"Твоя роль: {prompt}, Запомни без коментов и отвечай в соответствии с ним",
            },
            *history,
        ]
        resp = self.mistral.chat.complete(model=model, messages=history)
        response = resp.choices[0].message.content
        print(f"{model}: {response}")
        return response

    async def get_model(self, user):
        username = str(user.username)
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if username in data:
                    model = (
                        data[username]["model"]
                        if data[username]["model"]
                        else "mistral-tiny"
                    )
                    return model
                model = "mistral-tiny"
                return model

        except:
            data = {}
            model = "mistral-tiny"
            return model
