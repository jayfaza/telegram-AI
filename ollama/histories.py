import os
import json
import asyncio


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
