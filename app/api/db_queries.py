import secrets
import sqlite3
from sqlite3 import IntegrityError, OperationalError

import aiosqlite
from fastapi import HTTPException, status

from app.api.logger.logging_templates import log_error, log_warning
from migrate import DB_FILE

conn = sqlite3.connect(DB_FILE, check_same_thread=False)  # Позволяет использовать один и тот же объект соединения из разных потоков

def generate_token():
    return secrets.token_hex(16)


async def save_token_to_db(token):
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(
                "INSERT INTO tokens (token) VALUES (?)",
                (token,)
            )
            await db.commit()
    except OperationalError as e:
        log_error(
            action="Сохранение токена в бд",
            message="Ошибка базы данных",
            detail=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )


async def save_user_to_db(user_id):
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute(
                "INSERT INTO white_list (user_id) VALUES (?)",
                (user_id,)
            )
            await db.commit()
    except IntegrityError:
        log_warning(
            action="Сохранение юзера в бд",
            message='Юзер уже есть в базе',
            user_id=user_id
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID уже существует в White List"
        )
    except OperationalError as e:
        log_error(
            action="Сохранение юзера в бд",
            message="Ошибка базы данных",
            detail=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )


async def get_token_from_db(token):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute(
            "SELECT token FROM tokens WHERE token = ? AND is_active = 1", (token,)
        )
        result = await cursor.fetchone()
    return result


async def get_user_id(user_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute(
            "SELECT user_id FROM white_list WHERE user_id = ?", (user_id,)
        )
        result = await cursor.fetchone()
    return result
