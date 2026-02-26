import asyncio
import aiogram
from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import handlers.keyboard as kb
from ollama.ollama_service import OllamaAi
from config import OLLAMA_MODEL, GREET_MESSAGE
from ollama.histories import add_to_history, give_history
import json
from config import DATA
import os

router = Router()
ollama = OllamaAi()


@router.message()
async def handle_message(message: Message):
    user = message.from_user
    print(f"User: {message.text}")
    await add_to_history(user, "user", message.text)
    history = await give_history(user)
    model = await ollama.get_model(user)
    response = await ollama.ask_mistral(user, model, history)
    await add_to_history(user, "assistant", response)
    await message.answer(response)
