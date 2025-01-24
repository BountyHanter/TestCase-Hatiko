from aiogram.filters.callback_data import CallbackData


class CallbackFilter(CallbackData, prefix='my'):
    foo: str
