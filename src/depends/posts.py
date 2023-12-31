from src.repositories.database_repo import SQLAlchemyRepo
from src.models.posts import PostsModel

"""For easy import"""


PostsRepository = SQLAlchemyRepo(PostsModel)
