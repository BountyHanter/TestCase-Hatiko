from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import CallbackFilter


async def start(message: Message, state: FSMContext):
    """
    Функция обработки команды /start
    """
    await state.clear()
    message_text = 'Бот создан для тестового задания \\- Проверка IMEI\\.'
    button_text = 'Проверить IMEI'

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=button_text,
            callback_data=CallbackFilter(foo='check_imei').pack())
    )
    button = builder.as_markup()
    await message.answer(message_text, reply_markup=button)
