import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


async def check_imei_on_backend(imei):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/check-imei",
                params={"imei": imei},
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
                timeout=10.0
            )

        if response.status_code == 200:
            data = response.json()
            return insert_backslashes(data['message'])
        elif response.status_code == 418:
            # Обработка чайника =)
            return "IMEI с ошибкой"
        else:
            print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}")
            return 'error'
    except httpx.RequestError as exc:
        print(str(exc))
        # Обработка сетевых ошибок
        return 'error'


async def check_white_list(user_id):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/api/white-list",
                params={"user_id": user_id},
                headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
                timeout=10.0
            )

        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            return False
        else:
            print(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}")
            return 'error'
    except httpx.RequestError as exc:
        # Обработка сетевых ошибок
        return "error"


#  Мой давний скрипт для экранирования
def insert_backslashes(s, chars='_[]()~>#+-=|{}.!'):
    result = ''

    for ch in s:
        if ch in chars:
            result += '\\' + ch
        else:
            result += ch

    return result


if __name__ == "__main__":
    async def main():
        # Тестируем функцию check_imei_on_backend
        imei_test = "869061067345126"  # Пример IMEI
        print("Тестирование check_imei_on_backend...")
        imei_result = await check_imei_on_backend(imei_test)
        print(f"Результат: {imei_result}\n")

        # Тестируем функцию check_white_list
        user_id_test = "123"  # Пример user_id
        print("Тестирование check_white_list...")
        white_list_result = await check_white_list(user_id_test)
        print(f"Результат: {white_list_result}\n")

    asyncio.run(main())