from config import *

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, CopyTextButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.database.requests import get_user, create_user
from src.bot.utils import generate_link

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


# Хендлеры
@router.message(Command('start'))
async def start_handler(message: Message):

    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    username = message.from_user.username

    user = await get_user(telegram_id)

    if not user:
        user = await create_user(telegram_id=telegram_id, username=username, link_name=generate_link())
    
    await message.answer(text = await start_text(full_name, telegram_id), reply_markup = await start_kb(telegram_id))


@router.callback_query(F.data == 'start')
async def start_callback(callback: CallbackQuery):
    full_name = callback.from_user.full_name
    telegram_id = callback.from_user.id

    await callback.message.edit_text(text = await start_text(full_name, telegram_id), reply_markup = await start_kb(telegram_id))