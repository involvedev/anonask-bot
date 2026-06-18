from src.bot.database.db import engine, SessionLocal
from src.bot.database.models import Base, User, Stats

from sqlalchemy import select


# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Получить юзера по айди
async def get_user(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
# Создать юзера в бд
async def create_user(
    telegram_id: int,
    username: str | None,
    link_name: str
):
    async with SessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            username=username,
            link_name=link_name,
        )

        session.add(user)
        await session.commit()

        return user