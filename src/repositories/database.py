from typing import Any
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import insert, select, update, func
from sqlalchemy.engine import ScalarResult
from src.schemas.errors import SQLAlchemyNotFound
from src.abstract.database import AbstractSQLAlchemy


class SQLAlchemyRepo[T](AbstractSQLAlchemy):
    """Repository class for SQLAlchemy databases."""

    def __init__(self, model: T, session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def __str__(self) -> T:
        return self.model

    async def add_one(self, model: T) -> T:
        """
        Method for add one item to DB

        Return item
        """

        self.session.add(model)
        return model

    async def find_all(self) -> list[T]:
        """
        Method for get all items from DB

        Return sqlalchemy model
        """
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        result = res.scalars().all()
        if result == []:
            return result
        else:
            raise SQLAlchemyNotFound

    async def find_byid(self, id: int) -> T:
        """
        Method for get one item by id

        Return model
        """
        stmt = select(self.model).filter(self.model.id == id)
        res = await self.session.execute(stmt)
        result = res.scalars().first()
        if result is not None:
            return result
        else:
            raise SQLAlchemyNotFound

    async def find_byfield(self, data: dict) -> ScalarResult:
        """
        Method for get one item by field

        Return model
        """
        stmt = select(self.model).filter(data)
        res = await self.session.execute(stmt)
        return res.scalars()

    async def find_bySTMT(self, stmt: Any) -> ScalarResult:
        """
        Method get already created statement to get db items

        Return model
        """
        res = await self.session.execute(stmt)
        return res.scalars()

    async def count(self) -> int:
        stmt = select(func.count(self.model.id))
        result = await self.session.scalar(stmt)
        return result

    async def count_by_field(self, field: Any) -> int:
        stmt = select(func.count(self.model.id).filter(field))
        result = await self.session.scalar(stmt)
        return result

    async def update(self, id: int, values: dict) -> None:
        """
        Method to update one item

        Return none
        """
        stmt = update(self.model).filter(self.model.id == id).values(values)
        await self.session.execute(stmt)

    async def delete(self, id: int) -> None:
        """
        Method to delete one item

        Return none
        """
        stmt = select(self.model).filter(self.model.id == id)
        await self.session.delete(stmt)
