from typing import Any
from abc import ABC, abstractmethod
from database import async_session_maker
from sqlalchemy import insert, select, update


class AbstractRepo(ABC):
    @staticmethod
    @abstractmethod
    async def add_one(model: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_byid(self, id: int):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def findall_bySTMT(stmt: Any) -> Any:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def findfirst_bySTMT(stmt: Any) -> Any:
        raise NotImplementedError


class SQLAlchemyRepo(AbstractRepo):
    model = None

    @staticmethod
    async def add_one(model: Any) -> Any:
        """
        Method for add one item to DB

        Return item
        """
        async with async_session_maker() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)  # Actual identify refresh
            return model

    async def find_all(self) -> Any:
        """
        Method for get all items from DB

        Return sqlalchemy model
        """
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_byid(self, id: int) -> Any:
        """
        Method for get one item by id

        Return model
        """
        async with async_session_maker() as session:
            stmt = select(self.model).filter(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalars().first()

    async def find_byfield(self, data: dict):
        """
        Method for get one item by field

        Return model
        """
        async with async_session_maker() as session:
            stmt = select(self.model).filter(data)
            res = await session.execute(stmt)
            return res.scalars().first()

    @staticmethod
    async def findall_bySTMT(stmt: Any) -> Any:
        """
        Method get already created statement to get db items

        Return model
        """
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return res.scalars().all()

    @staticmethod
    async def findfirst_bySTMT(stmt: Any) -> Any:
        """
        Method get already created statement to get db item

        Return model
        """
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return res.scalars().first()

    async def update(self, id: int, values: dict) -> Any:
        """
        Method to update one item

        Return refresh model
        """
        async with async_session_maker() as session:
            stmt = update(self.model).filter(self.model.id == id).values(values)
            res = await session.execute(stmt)
            await session.commit()
            return res
