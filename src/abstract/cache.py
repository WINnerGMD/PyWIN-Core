from abc import ABC, abstractmethod
from typing import Any


class AbstractRedis(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def set(self, response: Any, key: str, ttl: int = 10) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_startswith(self, value: str) -> None:
        raise NotImplementedError
