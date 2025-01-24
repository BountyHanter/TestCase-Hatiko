import logging

from fastapi import FastAPI, HTTPException, Depends
from starlette import status

from .db_queries import generate_token, save_token_to_db, get_user_id, save_user_to_db
from app.api.utils import authenticate
from app.services import is_valid_imei
from app.services import request_check_imei
from migrate import ADMIN_TOKEN
from .logger.logging_config import setup_logging
from .logger.logging_templates import log_error, log_warning, log_info

app = FastAPI()

setup_logging()

logger = logging.getLogger("test_case")


@app.post("/api/check-imei")
async def check_imei(imei: str, token: str = Depends(authenticate)):
    if imei is None or imei == "":
        log_error(
            action="Проверка IMEI",
            message="Не передан IMEI",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IMEI обязателен",
        )

    is_valid = is_valid_imei(imei)

    if not is_valid:
        log_warning(
            action="Проверка IMEI",
            message="IMEI не прошёл проверку валидности",
            imei=imei,
        )

        #  Надеюсь вы поймаете смешинку на этом моменте =) (Не для продакшна естественно)
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Кривой IMEI"
        )

    log_info(
        action='Проверка IMEI',
        message="IMEI прошёл проверку валидности",
        imei=imei,
    )

    result = await request_check_imei(imei)

    if result['status'] == 'error':
        log_warning(
            action="Запрос проверки IMEI на стороннем сервисе",
            message="Сервис вернул ошибку",
            imei=imei,
            detail=result['detail'],
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Сервис проверки IMEI вернул ошибку"
        )

    log_info(
        action='Проверка IMEI',
        message="Сервис вернул данные о устройстве",
        detail=result['detail'],
    )

    return {
        "status": "ok",
        "message": result['detail']
    }


@app.get("/api/white-list")
async def white_list(user_id: str, token_data: dict = Depends(authenticate)):
    if user_id is None or user_id == "":
        log_warning(
            action="Проверка юзера в White List",
            message="Айди не передан"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID обязателен",
        )

    is_valid_user = await get_user_id(user_id)
    logger.debug(f"[DEBUG] Проверка юзера - {user_id}")

    if not is_valid_user:
        log_warning(
            action="Проверка юзера в White List",
            message="Юзера нет в White List",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Юзер не имеет доступа",
        )

    log_info(
        action="Проверка юзера в White List",
        message="Юзер прошёл проверку",
        user_id=user_id,
    )

    return {"status": "ok"}


@app.post("/api/white-list/save")
async def white_list_save(user_id: str, token_data: dict = Depends(authenticate)):
    if user_id is None or user_id == "":
        log_warning(
            action="Добавление юзера в White List",
            message="Айди не передан"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID обязателен",
        )

    await save_user_to_db(user_id=user_id)

    log_info(
        action="Добавление юзера в White List",
        message="Юзер сохранён в базу",
        user_id=user_id,

    )

    return {"status": "ok"}


@app.post("/api/auth")
async def auth(admin_token: str):
    if admin_token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не верный админ токен",
        )

    new_token = generate_token()
    logger.debug(f"[DEBUG] Новый токен - {new_token}")

    await save_token_to_db(new_token)

    return {"status": "ok", "token": new_token}
