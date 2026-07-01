import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, DB_DSN
import db
from handlers import menu_router, welcome_router, buttons_router

logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "REPLACE_WITH_YOUR_TOKEN":
        raise RuntimeError("BOT_TOKEN is not set. Please set the BOT_TOKEN in environment or config.py")

    # تهيئة Pool لقاعدة البيانات
    await db.init_db_pool(DB_DSN)
    await db.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # تسجيل الروترات (routers)
    dp.include_router(menu_router)
    dp.include_router(welcome_router)
    dp.include_router(buttons_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await db.close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())
