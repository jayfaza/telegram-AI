import asyncio
import aiogram
from time import *
from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import handlers.keyboard as kb
from ollama.ollama_service import OllamaAi
from config import OLLAMA_MODEL, GREET_MESSAGE
from ollama.profile import (
    get_profile,
    give_history,
    save_history,
    add_to_history,
    save_user,
    save_model,
)
import json
from config import DATA
import os

router = Router()
ollama = OllamaAi()  # удобный класс для общения с ollama


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    ollama.user = user
    await get_profile(user, ollama.model)

    greet = await message.answer(GREET_MESSAGE, reply_markup=kb.reply_kb)


@router.message(F.text == "Профиль 🪪")
async def profile(message: Message):
    user = message.from_user
    text = await get_profile(user, ollama.model)
    await message.answer(text)


@router.callback_query(F.data.startswith("model_"))
async def set_model(callback: types.CallbackQuery):
    model_name = callback.data.split("model_")[1]
    print(f"model_name: {model_name}")
    ollama.model = model_name
    user = callback.from_user
    await save_model(user, model_name)
    await callback.message.edit_text(f"Модель установлена: {model_name}")
    await asyncio.sleep(1.5)
    await callback.message.delete()


@router.message(F.text == "Очистить историю 📝")
async def clear_history(message: Message):
    user = message.from_user
    username = user.username if user.username else "no_username"
    variable_history_path = (
        f"/home/jayfaza/projects/telegram-bot/history/{user.id}_{username}.json"
    )
    print(variable_history_path)
    if os.path.exists(variable_history_path):
        os.remove(variable_history_path)
    await message.answer(text="История стёрта")


@router.message(F.text == "Модель 📖")
async def chose_model(message: Message):
    models_kb = await ollama.build_keyboard()
    await message.answer("Выберите модель:", reply_markup=models_kb)


@router.callback_query(F.data == "remove_msg")
async def remove_models_msg(callback: types.CallbackQuery):
    await callback.message.delete()


@router.message(F.text == "История 📝")
async def watch_history(message: Message):
    user = message.from_user
    history = await give_history(user)
    history_text = "📝 **История чата:**\n\n"

    for item in history:
        if isinstance(item, dict):
            role = item.get("role", "unknown")
            content = item.get("content", "")

            emoji = "👤" if role == "user" else "🤖"
            history_text += f"{emoji} {content}\n\n"

            if len(history_text) > 3000:
                history_text += "...\n\n(история слишком длинная)"
                break

    # Отправляем историю
    await message.answer(history_text)


@router.message()
async def handle_message(message: Message):
    user = message.from_user
    print(f"User: {message.text}")

    await add_to_history(user, "user", message.text)

    history = await give_history(user)

    response = await ollama.ask_with_history(user, history)

    await add_to_history(user, "assistant", response)

    await message.answer(response)
