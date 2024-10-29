# Синхронная версия
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# from app.core.config import settings
#
#
# DATABASE_URL = settings.DATABASE_URL  # у нас в settings'ах нет такого урла, но можно было бы добавить, поменяв драйвер на psycopg2
#
# engine = create_engine(DATABASE_URL)
#
# sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
#
# def get_db():
#     db = sync_session_maker()
#     try:
#         yield db
#     finally:
#         db.close()

# Асинхронная версия
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(settings.ASYNC_DATABASE_URL)  # создали движок БД
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)  # передали наш движок в создатель сессий


class Base(DeclarativeBase):
    pass

async def get_async_session():
    async with async_session_maker() as session:
        yield session