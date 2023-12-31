from src.repositories.database_repo import SQLAlchemyRepo
from src.models.comments import CommentsModel

"""For easy import"""


CommentsRepository = SQLAlchemyRepo(CommentsModel)