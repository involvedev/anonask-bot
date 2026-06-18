from src.bot.database.db import engine
from src.bot.database.models import Base


# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def user_initialization():
    pass