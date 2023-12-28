from src.repositories.database_repo import SQLAlchemyRepo
from src.models.dailychests import ChestsModel

"""For easy import"""


class ChestsRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = ChestsModel
