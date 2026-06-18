from config import *

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, CopyTextButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Клавиатура
def admin_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Статистика', callback_data='a_stats')
    builder.button(text='Рассылка', callback_data='a_mailing')
    builder.button(text='Поиск пользователя', callback_data='a_finduser')
    builder.button(text='< Назад', callback_data='start')

    builder.adjust(2, 1, 1)

    return builder.as_markup()

# Текст
def admin_text(telegram_id):
    text = f"""Админ панель - {telegram_id}"""

    return text

# Хендлеры
@router.callback_query(F.data == 'adminpanel')
async def admin_callback(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    await callback.message.edit_text(text=admin_text(telegram_id), reply_markup=admin_kb())
