from luhn import verify


def is_valid_imei(imei: str) -> bool:
    """
    Проверяет валидность IMEI с использованием библиотеки luhn.
    """
    return verify(imei)
