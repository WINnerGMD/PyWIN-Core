from src.repositories.database_repo import SQLAlchemyRepo
from src.models.lists import ListModel

"""For easy import"""


ListRepository = SQLAlchemyRepo(ListModel)
