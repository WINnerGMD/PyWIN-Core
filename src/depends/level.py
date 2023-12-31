from src.repositories.database_repo import SQLAlchemyRepo
from src.models.levels import LevelModel

"""For easy import"""


LevelsRepository = SQLAlchemyRepo(LevelModel)