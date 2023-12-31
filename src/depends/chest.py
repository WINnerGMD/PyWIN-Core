from src.repositories.database_repo import SQLAlchemyRepo
from src.models.dailychests import ChestsModel

"""For easy import"""


ChestsRepository = SQLAlchemyRepo(ChestsModel)
