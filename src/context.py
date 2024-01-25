from database import async_session_maker
from src.abstract.context import AbstractContext, AbstractDatabase, AbstractServices
from src.services import UserService, LevelService, CommentsService, PostCommentsService
from src.services import LevelService
from src.repositories.database import SQLAlchemyRepo
from src.depends.logs import Console
from fastapi import Request
from src.models import *


class Services(AbstractServices):
    def __init__(self, ctx: AbstractContext):
        self.users = UserService(ctx)
        self.levels = LevelService(ctx)
        self.posts = PostCommentsService(ctx)
        self.comments = CommentsService(ctx)


class Database(AbstractDatabase):

    def __init__(self, session):
        self.users = SQLAlchemyRepo(UsersModel, session)
        self.levels = SQLAlchemyRepo(LevelModel, session)
        self.posts = SQLAlchemyRepo(PostsModel, session)


class UoWContext(AbstractContext):

    def __init__(self, request: Request):
        self.request = request
        self._session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self._session_factory()
        self.console = Console
        self.database = Database(self.session)
        self.services = Services(self)
        return self

    async def __aexit__(self, exc_type, *args):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
