import os
from logging.config import dictConfig
from datetime import datetime

# Определяем директорию, где находится текущий файл и поднимаемся выше
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Создаём путь к папке logs рядом с файлом
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Создаём директорию для логов
os.makedirs(LOG_DIR, exist_ok=True)

# Конфигурация логгера
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, f'app_{datetime.now().strftime("%Y-%m-%d")}.log'),
            'encoding': 'utf-8',
            'level': 'DEBUG',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def setup_logging():
    dictConfig(LOGGING)
