from ..repositories.database import SQLAlchemyRepo
from ..models.dailychests import ChestsModel

"""For easy import"""


ChestsRepository = SQLAlchemyRepo(ChestsModel)
