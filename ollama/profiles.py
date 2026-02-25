import asyncio
import json
import os
from config import DATA

file_path = "/home/jayfaza/projects/telegram-bot/data.json"


async def get_profile(user):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        if str(user.username) in data:
            model = data[str(user.username)]["model"]
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
Current model: llama3.1:8b 
"""

    model = "llama3.1:8b"
    await save_user(user, model)
    return text


async def save_user(user, model):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            users = json.load(f)
            print(users)

    except FileNotFoundError:
        print("fileNotFound")
        users = {}

    username = str(user.username)

    if "prompt" not in users[username]:
        prompt = "ТЫ ПОЛЕЗНЫЙ ПОМОЩНИК HubertAI"
    if "prompt" in users[username]:
        prompt = users[username]["prompt"]

    users[str(user.username)] = {
        "id": user.id,
        "name": user.first_name,
        "username": user.username if user.username else "None",
        "model": model,
        "prompt": prompt,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
