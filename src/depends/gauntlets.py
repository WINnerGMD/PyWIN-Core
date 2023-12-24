from src.repositories.database_repo import SQLAlchemyRepo
from src.models.gauntlets import GauntletsModel
"""For easy import"""


class GauntletsRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = GauntletsModel
