import asyncio
from multiprocessing import Process

import uvicorn

from app.bot.bot_app import start_bot
from migrate import initialize_database, create_tables, insert_token_and_user_id


def run_fastapi():
    """Запускает сервер FastAPI."""
    print("Запуск FastAPI...")
    uvicorn.run("app.api.fast_api_app:app", host="127.0.0.1", port=8000, reload=True)


async def run_bot():
    """Запускает Telegram-бота."""
    print("Запуск Telegram-бота...")
    await start_bot()


def main():
    # Запускаем миграции
    initialize_database()
    create_tables()
    insert_token_and_user_id()

    # Создаём отдельный процесс для FastAPI
    fastapi_process = Process(target=run_fastapi)
    fastapi_process.start()

    # Запускаем Telegram-бот в основном процессе
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
