import secrets

from aiogram.fsm.state import State, StatesGroup

# Состояния
class MessageState(StatesGroup):
    waiting_message = State()

# Генерация уникальной ссылки для пользователя
def generate_link():
    return secrets.token_urlsafe(8)