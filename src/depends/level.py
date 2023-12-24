from src.repositories.database_repo import SQLAlchemyRepo
from src.models.levels import LevelModel

"""For easy import"""


class LevelsRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = LevelModel
