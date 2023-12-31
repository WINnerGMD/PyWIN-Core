from src.repositories.database_repo import SQLAlchemyRepo
from src.models.gauntlets import GauntletsModel
"""For easy import"""


GauntletsRepository = SQLAlchemyRepo(GauntletsModel)

