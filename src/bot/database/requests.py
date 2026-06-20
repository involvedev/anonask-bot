from src.bot.database.db import engine, SessionLocal
from src.bot.database.models import Base, User, Stats, Message

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

# Получить юзера по его ссылке
async def get_tgid_by_link(link_name: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User.telegram_id).where(
                User.link_name == link_name
            )
        )

        return result.scalar_one_or_none()
    
# Сохранение сообщения
async def create_message(receiver_id: int, text: str):
    async with SessionLocal() as session:
        result = Message(receiver_id = receiver_id, text = text)

        session.add(result)
        await session.commit()

        return result
    
# TEST TEST TEST
async def debug_users():
    async with SessionLocal() as session:
        result = await session.execute(select(User))

        users = result.scalars().all()

        for user in users:
            print(
                f"id={user.telegram_id} "
                f"username={user.username} "
                f"link={user.link_name}"
            )