from typing import Any
from abc import ABC, abstractmethod
from database import async_session_maker
from sqlalchemy import insert, select, update
from sqlalchemy.engine import Result
from src.schemas.errors import SQLAlchemyNotFound

class AbstractRepo[T](ABC):
    @staticmethod
    @abstractmethod
    async def add_one(model: T) -> T:
        raise NotImplementedError

    async def find_all(self) -> list[T]:
        raise NotImplementedError

    async def find_byid(self, id: int) -> T:
        raise NotImplementedError

    async def find_byfield(self, data: dict) -> Result:
        raise NotImplementedError

    @staticmethod
    async def find_bySTMT(stmt: Any) -> Result:
        raise NotImplementedError

    async def update(self, id: int, values: dict) -> T:
        raise NotImplementedError


class SQLAlchemyRepo[T](AbstractRepo):
    """Repository class for SQLAlchemy databases."""

    def __init__(self, model: T):
        self.model = model

    def __str__(self) -> T:
        return self.model

    @staticmethod
    async def add_one(model: T) -> T:
        """
        Method for add one item to DB

        Return item
        """
        async with async_session_maker() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)  # Actual identify refresh
            return model

    async def find_all(self) -> list[T]:
        """
        Method for get all items from DB

        Return sqlalchemy model
        """
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_byid(self, id: int) -> T:
        """
        Method for get one item by id

        Return model
        """
        async with async_session_maker() as session:
            stmt = select(self.model).filter(self.model.id == id)
            res = await session.execute(stmt)
            result = res.scalars().first()
            if result is not None:
                return result
            else:
                raise SQLAlchemyNotFound

    async def find_byfield(self, data: dict) -> Result:
        """
        Method for get one item by field

        Return model
        """
        async with async_session_maker() as session:
            stmt = select(self.model).filter(data)
            res = await session.execute(stmt)
            return res

    @staticmethod
    async def find_bySTMT(stmt: Any) -> Result:
        """
        Method get already created statement to get db items

        Return model
        """
        async with async_session_maker() as session:
            res = await session.execute(stmt)
            return res

    async def update(self, id: int, values: dict) -> None:
        """
        Method to update one item

        Return none
        """
        async with async_session_maker() as session:
            stmt = update(self.model).filter(self.model.id == id).values(values)
            await session.execute(stmt)
            await session.commit()

    async def delete(self, id: int) -> None:
        """
        Method to delete one item

        Return none
        """
        async with async_session_maker() as session:
            stmt = select(self.model).filter(self.model.id == id)
            await session.delete(stmt)
            await session.commit()
