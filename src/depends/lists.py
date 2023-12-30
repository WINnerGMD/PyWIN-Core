from src.repositories.database_repo import SQLAlchemyRepo
from src.models.lists import ListModel

"""For easy import"""


class ListRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = ListModel
