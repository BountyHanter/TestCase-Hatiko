from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.bot_utils import check_white_list, check_imei_on_backend
from app.bot.states import MainState


async def bot_check_imei_start(query: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=None
    )
    message = 'Введите IMEI\\!'
    await query.message.answer(message)
    await state.set_state(MainState.check_imei)


async def bot_check_imei_request(message: Message, state: FSMContext):
    check_user = await check_white_list(message.from_user.id)
    if check_user == 'error':
        await message.answer('Возникла ошибка при проверке юзера')
        await state.clear()
        return
    elif not check_user:
        await message.answer('У вас нет доступа')
        await state.clear()
        return

    check_imei = await check_imei_on_backend(message.text)
    if check_imei == 'error':
        await message.answer('Возникла ошибка при проверке IMEI')
        await state.clear()
        return

    await message.answer(check_imei)
    await state.clear()
