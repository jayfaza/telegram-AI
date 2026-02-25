import asyncio
from aiogram.types import Message

user_messages = {}


async def save_message(user_id, message, user_messages):
    """Сохраняет сообщение пользователя"""
    user_messages[user_id] = message


async def get_message(user_id):
    """Получает сообщение пользователя"""
    return user_messages.get(user_id)


async def delete_message(user_id):
    """Удаляет сообщение пользователя из словаря"""
    if user_id in user_messages:
        del user_messages[user_id]
