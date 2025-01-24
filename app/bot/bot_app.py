import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from app.bot import bot_logger
from app.bot.bot_commands import set_commands
from app.bot.bot_handlers.check_imei_handler import bot_check_imei_request, bot_check_imei_start
from app.bot.bot_handlers.start_handler import start
from app.bot.callbacks import CallbackFilter
from app.bot.states import MainState

load_dotenv()


async def start_bot():

    # Получаем токен из .env
    token = os.getenv('TG_BOT_TOKEN')
    if not token:
        raise ValueError("TOKEN не найден в .env")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    await set_commands(bot)
    dp = Dispatcher()
    bot_logger.bot_logger()

    async def say_something(message: Message):
        await message.answer(r"""Нажми /start чтобы проверить IMEI""", reply_markup=None)

    dp.message.register(start, CommandStart())

    dp.callback_query.register(bot_check_imei_start, CallbackFilter.filter(F.foo == 'check_imei'))

    dp.message.register(bot_check_imei_request, MainState.check_imei)

    dp.message.register(say_something)

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем сообщения, которые получил бот до запуска
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("An error occurred: ", e)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())
