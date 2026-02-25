import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import commands_router, profile_router, messages_router, callback_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def delete_webhook():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook removed")


async def start():
    await delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(commands_router)
    dp.include_router(profile_router)
    dp.include_router(messages_router)
    dp.include_router(callback_router)
    asyncio.run(start())
