from config import *

from aiogram import Router, F
from aiogram.types import CallbackQuery, CopyTextButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Клавиатура
def stats_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Скопировать ссылку', copy_text=CopyTextButton(text='test'))
    builder.button(text="< Назад", callback_data='start')
    
    builder.adjust(1)

    return builder.as_markup()

# Текст
def stats_text(username: str):
    text = f"""<b>Статистика - @{username}

За всё время:
<blockquote>Получено сообщений:
Отправленно сообщений:</blockquote>

Что бы увеличить свою статистику отправляйте и получайте больше сообщений:
link</b>
"""
    return text

# Хендлеры
@router.callback_query(F.data == 'stats')
async def stats_callback(callback: CallbackQuery):
    username = callback.from_user.username

    await callback.message.edit_text(text=stats_text(username), reply_markup=stats_kb())
