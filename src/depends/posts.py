from src.repositories.database_repo import SQLAlchemyRepo
from src.models.posts import PostsModel

"""For easy import"""


class PostsRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = PostsModel
