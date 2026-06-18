from config import *

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, CopyTextButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Клавиатура
def start_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Скопировать ссылку', copy_text=CopyTextButton(text='test'))
    builder.button(text='Статистика', callback_data='stats')

    builder.adjust(1, 1)

    return builder.as_markup()


# Текст
def start_text(full_name: str):
    text = f"""Привет {full_name}

Начни получать анонимные сообщения прямо сейчас!

Твоя ссылка:
"""
    return text


# Хендлеры
@router.message(Command('start'))
async def start_handler(message: Message):
    full_name = message.from_user.full_name
    
    await message.answer(text=start_text(full_name), reply_markup=start_kb())


@router.message(F.data == 'start')
async def start_callback(callback: CallbackQuery):
    full_name = callback.from_user.full_name
    
    await callback.message.edit_text(text=start_text(full_name), reply_markup=start_kb())