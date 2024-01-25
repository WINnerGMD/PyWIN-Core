from src.repositories.database import SQLAlchemyRepo
from src.models.dailychests import ChestsModel

"""For easy import"""


ChestsRepository = SQLAlchemyRepo(ChestsModel)
