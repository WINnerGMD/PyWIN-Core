from abc import abstractmethod, ABC
from typing import Type
from src.repositories.database import AbstractSQLAlchemy
import src.services as services
from .logger import AbstractConsole


class AbstractDatabase(ABC):
    users: Type[AbstractSQLAlchemy]
    levels: Type[AbstractSQLAlchemy]
    comments: Type[AbstractSQLAlchemy]
    posts: Type[AbstractSQLAlchemy]


class AbstractServices(ABC):
    users: Type[services.UserService]
    levels: Type[services.LevelService]
    comments: Type[services.CommentsService]
    posts: Type[services.PostCommentsService]

class AbstractContext(ABC):
    database = AbstractDatabase
    console = AbstractConsole
    services = AbstractServices

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError
