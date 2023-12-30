from sqlalchemy import MetaData
from src.models.actions import ActionsModel
from src.models.comments import CommentsModel
from src.models.dwlevels import FeaturedLevelsModel
from src.models.gauntlets import GauntletsModel
from src.models.levels import LevelModel
from src.models.mappacks import MapPacksModel
from src.models.messages import MessagesModel
from src.models.posts import PostsModel
from src.models.roles import RolesModel
from src.models.songs import SongsModel
from src.models.user import UsersModel
from src.models.dailychests import ChestsModel
from .lists import ListModel
metadata_obj = MetaData()

#
# metadata_obj.create_all(tables=[ListModel])