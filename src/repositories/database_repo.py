from abc import ABC, abstractmethod
from database import async_session_maker
from sqlalchemy import insert, select


class AbstractRepo(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_byid(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepo(AbstractRepo):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        """Method for get all items from DB """
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.all()

    async def find_byid(self, id: int):
        """Method for get one item by id"""
        async with async_session_maker() as session:
            stmt = select(self.model).filter(self.model.id == id)
            res = await session.execute(stmt)
            return res.first()
