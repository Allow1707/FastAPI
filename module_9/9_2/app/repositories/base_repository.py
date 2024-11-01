from abc import ABC, abstractmethod
from typing import Tuple, Any

from sqlalchemy import select, insert, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        query: ReturningInsert[tuple[Any]] | ReturningInsert[Any] = insert(self.model).values(**data).returning(self.model)
        print(f"add_one_query: {query}")
        res = await self.session.execute(query)
        return res.scalar_one()

    async def find_all(self):
        query: Select[tuple[Any]] | Select[Any] = select(self.model)
        print(f"find_all_query: {query}")
        result = await self.session.execute(query)
        return result.scalars().all()