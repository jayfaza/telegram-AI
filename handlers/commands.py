import asyncio
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from ollama.profiles import get_profile
import handlers.keyboard as kb
from config import GREET_MESSAGE

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user
    await get_profile(user)

    greet = await message.answer(GREET_MESSAGE, reply_markup=kb.reply_kb)


@router.message(Command("menu"))
async def menu(message: Message):
    message = await message.answer(text="меню открыто 📁", reply_markup=kb.reply_kb)
