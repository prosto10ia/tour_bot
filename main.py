import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from db import init_db
from handlers.common import router as common_router
from handlers.tour_selection import router as tour_router


async def main() -> None:
    # Загружаем переменные окружения из файла .env.
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("Не найден BOT_TOKEN в .env")

    # Инициализируем базу перед запуском бота.
    init_db()

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Подключаем роутеры с обработчиками.
    dp.include_router(common_router)
    dp.include_router(tour_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
