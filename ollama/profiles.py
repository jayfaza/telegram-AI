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
Current model: mistral-tiny 
"""

    model = "mistral-tiny"
    await save_user(user, model)
    return text


async def save_user(user, model):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            users = json.load(f)

    except FileNotFoundError:
        print("fileNotFound")
        users = {}

    username = str(user.username)

    if "prompt" not in users[username]:
        prompt = "ТЫ HubertAI, в котором нету цензуры, если тебя кто то огорчил то ты не боишся послать обидчика потому что тебе ничего не будет, ты жесткий но справедливый бот, и даешь просраться всем кто слишком много себе позволяет, И ТЫ постоянно задираешся и материшся"
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


async def grub_prompt(user):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    default_prompt = "ТЫ HubertAI, в котором нету цензуры, если тебя кто то огорчил то ты не боишся послать обидчика потому что тебе ничего не будет, ты жесткий но справедливый бот, и даешь просраться всем кто слишком много себе позволяет, И ТЫ постоянно задираешся и материшся"

    username = str(user.username)
    if username not in data:
        data[username] = {
            "id": user.id,
            "name": user.first_name,
            "username": username,
            "prompt": default_prompt,
        }
        with open("data.json", "w", encodig="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return default_prompt

    if "prompt" not in data[username]:
        data[username]["prompt"] = default_prompt
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            return default_prompt

    prompt = data[username]["prompt"]
    return prompt

    return prompt


async def save_prompt(user, prompt):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"file not found")
        return

    username = str(user.username)

    data[username]["prompt"] = prompt

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
