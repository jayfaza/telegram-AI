import asyncio
import json
import os
from config import DATA

file_path = "/home/jayfaza/projects/telegram-bot/data.json"


async def get_profile(user, model):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        if str(user.id) in data:
            text = f"""Здравствуй снова, {user.first_name}! 
👤 Профиль:
ID: {user.id}
Name: {user.first_name}
Username: @{user.username if user.username else 'нет'}
Current model: {model}
"""
            await save_user(user, model)
            return text

    text = f"""Приветствую тебя, {user.first_name}! 
👤 Профиль:
ID: {user.id}
Name: {user.first_name}
Username: @{user.username if user.username else 'нет'}
Current model: {model}
"""

    await save_user(user, model)
    return text


async def save_user(user, model):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            users = json.load(f)

    except FileNotFoundError:
        users = {}

    users[str(user.username)] = {
        "id": user.id,
        "name": user.first_name,
        "username": user.username if user.username else "None",
        "model": model,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


async def give_history(user):
    os.makedirs("/home/jayfaza/projects/telegram-bot/history/", exist_ok=True)

    username = user.username if user.username else "no_username"
    filename = f"/home/jayfaza/projects/telegram-bot/history/{user.id}_{username}.json"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Ошибка загрузки истории: {e}")
        return []


async def save_history(user, data):
    """Сохраняет историю чата"""
    os.makedirs("/home/jayfaza/projects/telegram-bot/history/", exist_ok=True)

    username = user.username if user.username else "no_username"
    filename = f"/home/jayfaza/projects/telegram-bot/history/{user.id}_{username}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def add_to_history(user, role, content):
    """Добавляет одно сообщение в историю"""
    history = await give_history(user)

    if len(history) > 20:
        history = history[-20:]

    history.append({"role": role, "content": content})

    await save_history(user, history)
    return history


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
