import asyncio
from aiogram import F, Router, types
from ollama.ollama_service import OllamaAi
from ollama.add_model import save_model
from aiogram.filters import StateFilter
from bstates import PromptStates
from aiogram.fsm.context import FSMContext
import os

router = Router()
ollama = OllamaAi()


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


@router.callback_query(F.data == "remove_msg")
async def remove_models_msg(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
