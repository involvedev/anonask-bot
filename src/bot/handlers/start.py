from config import *

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, CopyTextButton
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from src.bot.database.requests import get_user, create_user, get_tgid_by_link, debug_users
from src.bot.utils import generate_link, MessageState

router = Router()

# Клавиатура
async def start_kb(telegram_id):

    user = await get_user(telegram_id)
    link = f"""https://t.me/{BOT_USERNAME}?start={user.link_name}"""

    builder = InlineKeyboardBuilder()
    builder.button(text='Скопировать ссылку', copy_text=CopyTextButton(text=link))
    builder.button(text='Статистика', callback_data='stats')
    if telegram_id in ADMINS:
        builder.button(text='Админ панель', callback_data='adminpanel')

    builder.adjust(1, 1, 1)

    return builder.as_markup()


# Текст
async def start_text(full_name: str, telegram_id: int):
    user = await get_user(telegram_id)
    link = f"""https://t.me/{BOT_USERNAME}?start={user.link_name}"""

    text = f"""Привет! <b>{full_name}</b>

Начни получать анонимные сообщения прямо сейчас!

<b><blockquote>Твоя ссылка: {link}</blockquote></b>
"""
    return text

async def sendmessage_text():
    text = f"""Отправьте ваше сообщение"""

    return text


# Хендлеры
@router.message(Command('start'))
async def start_handler(message: Message, command: CommandObject, state: FSMContext):

    await debug_users()

    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    username = message.from_user.username

    user = await get_user(telegram_id)

    if not user:
        user = await create_user(telegram_id=telegram_id, username=username, link_name=generate_link())

    if command.args:
        receiver = await get_tgid_by_link(command.args)

        await state.update_data(receiver=receiver)
        await state.set_state(MessageState.waiting_message)
        await message.answer(text= await sendmessage_text())

        return

    else:
        await message.answer(text = await start_text(full_name, telegram_id), reply_markup = await start_kb(telegram_id))


@router.callback_query(F.data == 'start')
async def start_callback(callback: CallbackQuery):
    full_name = callback.from_user.full_name
    telegram_id = callback.from_user.id

    await callback.message.edit_text(text = await start_text(full_name, telegram_id), reply_markup = await start_kb(telegram_id))

@router.message(MessageState.waiting_message)
async def waiting_message_handler(message: Message, state: FSMContext):

    data = await state.get_data()
    receiver_tg_id = data["receiver"]

    await message.bot.send_message(chat_id=receiver_tg_id, text=message.text)

    await state.clear()