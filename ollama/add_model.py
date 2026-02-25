import os
import json
import asyncio
from config import DATA


async def save_model(user, model):
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    if user.username not in data:
        data[user.username] = {}

    data[user.username]["model"] = model

    try:
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Модель {model} сохранена для пользователя {user.username}")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
