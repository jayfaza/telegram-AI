import asyncio
from aiogram import F, Router
from aiogram.filters import StateFilter
from bstates import PromptStates
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ollama.ollama_service import OllamaAi
from ollama.profiles import get_profile, grub_prompt, save_prompt
from ollama.histories import give_history
import handlers.keyboard as kb
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


@router.message(F.text == "Сменить промпт ⌨️")
async def change_prompt(message: Message, state: FSMContext):
    await state.set_state(PromptStates.waiting_for_prompt)
    user = message.from_user
    current_prompt = await grub_prompt(user)
    await message.answer(
        text=f"Текущий промпт\n{current_prompt}", reply_markup=kb.close_kb
    )


@router.message(PromptStates.waiting_for_prompt)
async def set_prompt(message: Message, state: FSMContext):
    prompt = message.text
    user = message.from_user
    await save_prompt(user, prompt)
    await message.answer(f"Новый промпт\n{prompt}")
    await state.clear()
