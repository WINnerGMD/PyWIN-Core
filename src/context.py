from database import async_session_maker
from src.abstract.context import AbstractContext, AbstractDatabase, AbstractServices
from src.services import UserService, LevelService, CommentsService, PostCommentsService
from src.repositories.database import SQLAlchemyRepo
from src.depends.logs import Console
from fastapi import Request
from src.models import (
    UsersModel, LevelModel, PostsModel, CommentsModel,
    SongsModel, GauntletsModel, MapPacksModel, RolesModel,
    MessagesModel, FeaturedLevelsModel, ListModel, ActionsModel
)


class Services(AbstractServices):
    def __init__(self, ctx: AbstractContext):
        self.users = UserService(ctx)
        self.levels = LevelService(ctx)
        self.posts = PostCommentsService(ctx)
        self.comments = CommentsService(ctx)


class Database(AbstractDatabase):
    def __init__(self, session):
        self.session = session
        self.users = SQLAlchemyRepo(UsersModel, session)
        self.levels = SQLAlchemyRepo(LevelModel, session)
        self.posts = SQLAlchemyRepo(PostsModel, session)
        self.comments = SQLAlchemyRepo(CommentsModel, session)
        self.songs = SQLAlchemyRepo(SongsModel, session)
        self.gauntlets = SQLAlchemyRepo(GauntletsModel, session)
        self.mappacks = SQLAlchemyRepo(MapPacksModel, session)
        self.roles = SQLAlchemyRepo(RolesModel, session)
        self.messages = SQLAlchemyRepo(MessagesModel, session)
        self.featured = SQLAlchemyRepo(FeaturedLevelsModel, session)
        self.lists = SQLAlchemyRepo(ListModel, session)
        self.actions = SQLAlchemyRepo(ActionsModel, session)


class UoWContext(AbstractContext):
    def __init__(self, request: Request = None):
        self.request = request
        self._session_factory = async_session_maker
        self._is_active = False

    @property
    def is_active(self) -> bool:
        return self._is_active

    async def __aenter__(self):
        self.session = self._session_factory()
        self.console = Console
        self.database = Database(self.session)
        self.services = Services(self)
        self._is_active = True
        return self

    async def __aexit__(self, exc_type, *args):
        self._is_active = False
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()

