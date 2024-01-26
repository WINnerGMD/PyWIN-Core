from sqlalchemy import MetaData
from .. models.actions import ActionsModel
from .. models.comments import CommentsModel
from .. models.dwlevels import FeaturedLevelsModel
from .. models.gauntlets import GauntletsModel
from .. models.levels import LevelModel
from .. models.mappacks import MapPacksModel
from .. models.messages import MessagesModel
from .. models.posts import PostsModel
from .. models.roles import RolesModel
from .. models.songs import SongsModel
from .. models.user import UsersModel
from .. models.dailychests import ChestsModel
from .lists import ListModel
metadata_obj = MetaData()

#
# metadata_obj.create_all(tables=[ListModel])