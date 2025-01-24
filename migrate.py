import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "db.sqlite")

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


# Функция для создания таблиц
def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создание таблицы токенов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    )
    ''')

    # Создание таблицы белого списка
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS white_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE 
    )
    ''')

    conn.commit()
    conn.close()
    print("Миграции выполнены успешно.")


def insert_token_and_user_id():
    if not ADMIN_TOKEN:
        print("ADMIN_TOKEN не найден в переменных окружения. Проверьте файл .env.")
        return

    USER_ID = os.getenv("TG_USER_ID")  # Забираем user_id из переменных окружения
    if not USER_ID:
        print("TG_USER_ID не найден в переменных окружения. Проверьте файл .env.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Вставляем токен в таблицу `tokens`
        cursor.execute("INSERT INTO tokens (token) VALUES (?)", (ADMIN_TOKEN,))
        print(f"Токен {ADMIN_TOKEN} успешно добавлен в базу данных.")
    except sqlite3.IntegrityError:
        print("Токен уже существует в базе данных.")

    try:
        # Вставляем user_id в таблицу `white_list`
        cursor.execute("INSERT INTO white_list (user_id) VALUES (?)", (USER_ID,))
        print(f"User ID {USER_ID} успешно добавлен в White List.")
    except sqlite3.IntegrityError:
        print(f"User ID {USER_ID} уже существует в White List.")
    finally:
        conn.commit()  # Фиксируем изменения
        conn.close()

# Проверка, существует ли файл базы данных
def initialize_database():
    if not os.path.exists(DB_FILE):
        print(f"База данных {DB_FILE} не найдена, создаём новую...")
        open(DB_FILE, 'w').close()  # Создаём пустой файл базы данных
    else:
        print(f"База данных {DB_FILE} уже существует.")


if __name__ == '__main__':
    initialize_database()
    create_tables()
    insert_token_and_user_id()
