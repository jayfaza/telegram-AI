import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.messages import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def delete_webhook():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook removed")


async def start():
    await delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(router)
    asyncio.run(start())
