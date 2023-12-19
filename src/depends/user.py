from src.repositories.database_repo import SQLAlchemyRepo
from src.models.user import UsersModel

"""For easy import"""


class UsersRepository(SQLAlchemyRepo):
    """User Database Repository for easy import"""

    model = UsersModel
