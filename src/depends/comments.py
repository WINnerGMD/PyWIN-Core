from src.repositories.database_repo import SQLAlchemyRepo
from src.models.comments import CommentsModel

"""For easy import"""


class CommentsRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = CommentsModel
