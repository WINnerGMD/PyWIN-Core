from src.repositories.database_repo import SQLAlchemyRepo
from src.models.user import UsersModel

"""For easy import"""


UsersRepository = SQLAlchemyRepo(UsersModel)
