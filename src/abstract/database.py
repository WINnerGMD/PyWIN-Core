from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ScalarResult


class AbstractSQLAlchemy[T](ABC):
    @staticmethod
    @abstractmethod
    async def add_one(model: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_byid(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def find_byfield(self, data: dict) -> ScalarResult:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_by_field(self, field: Any) -> int:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def find_bySTMT(stmt: Any) -> ScalarResult:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, values: dict) -> T:
        raise NotImplementedError
