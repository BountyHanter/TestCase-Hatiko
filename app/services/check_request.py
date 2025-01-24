import os
from datetime import datetime
from typing import Union

import httpx

import logging

logger = logging.getLogger("test_case")

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")


def format_unix_timestamp(timestamp: int) -> str:
    if timestamp:
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return "Не указано"


async def request_check_imei(device_id: str, service_id: int = 6) -> Union[str, dict]:
    """
    Асинхронный запрос проверки IMEI через сервис

    :param device_id: IMEI телефона
    :param service_id: айди сервиса (в моём случае 6 - Xiaomi)
    :return: Данные об устройстве или результат запроса
    """

    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        'Authorization': f'Bearer {SERVICE_TOKEN}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    payload = {
        "deviceId": device_id,
        "serviceId": service_id
    }

    logger.debug(f"[DEBUG] payload - {payload}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()

            properties = data.get("properties", {})
            if not properties:
                return "Ответ от API не содержит данных об устройстве"

            return {
                "status": "ok",
                "detail": {
                    "Название устройства": properties.get("deviceName"),
                    "Код модели": properties.get("modelCode"),
                    "IMEI 1": properties.get("imei"),
                    "IMEI 2": properties.get("imei2"),
                    "Серийный номер": properties.get("serial"),
                    "Номер разблокировки": properties.get("unlockNumber"),
                    "Блокировка активации (Mi)": properties.get("miActivationLock"),
                    "SKU номер": properties.get("skuNumber"),
                    "Страна покупки": properties.get("purchaseCountry"),
                    "Гарантийный статус": properties.get("warrantyStatus"),
                    "Дата производства": format_unix_timestamp(properties.get("productionDate")),
                    "Дата доставки": format_unix_timestamp(properties.get("deliveryDate")),
                    "Дата активации": format_unix_timestamp(properties.get("activationDate")),
                }
            }
        elif response.status_code == 422:
            logger.debug(f"[DEBUG] Сервер вернул ошибку 422 - инфо: {response.text}")

            return {
                "status": "error",
                "detail": "IMEI не от Xiaomi",
            }

        else:
            logger.debug(f"[DEBUG] Сервер вернул ошибку {response.status_code} - инфо: {response.text}")

            return {
                "status": "error",
                "detail": f"Ошибка {response.status_code}: {response.text}",
            }
