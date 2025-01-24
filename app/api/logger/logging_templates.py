import logging

logger = logging.getLogger("test_case")


def log_info(action: str, message: str, **kwargs):
    if kwargs:
        # Добавляем доп значения в логи (иначе не отображаются)
        message += " | " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"[SUCCESS] {action} - {message}")


def log_warning(action: str, message: str, **kwargs):
    if kwargs:
        message += " | " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.warning(f"[WARNING] {action} - {message}")


def log_error(action: str, message: str, exc_info=False, **kwargs):
    if kwargs:
        message += " | " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.error(f"[ERROR] {action} - {message}", exc_info=exc_info)
