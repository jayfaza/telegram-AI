import asyncio
from aiogram import F, Router
from aiogram.types import Message
from ollama.ollama_service import OllamaAi
from ollama.profiles import get_profile
from ollama.histories import give_history
import os

router = Router()
ollama = OllamaAi()


@router.message(F.text == "Модель 📖")
async def chose_model(message: Message):
    models_kb = await ollama.build_keyboard()
    await message.answer("Выберите модель:", reply_markup=models_kb)


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
    await message.answer(history_text)


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


@router.message(F.text == "Профиль 🪪")
async def profile(message: Message):
    user = message.from_user
    text = await get_profile(user)
    await message.answer(text)
