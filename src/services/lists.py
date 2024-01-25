from src.schemas.list.service.post import UploadList
from src.schemas.list.service.get import GetList
from src.depends.lists import ListModel
from src.depends.user import UsersModel
from src.helpers.rate import Difficulty, Rate
from sqlalchemy import select
class ListService:

    @staticmethod
    async def upload_list(scheme: UploadList) -> int:
        """"Service function to upload new list """
        user_model: UsersModel = await UsersRepository().find_byid(scheme.accountID)  # getting current user

        list_model = ListModel(
            name=scheme.listName,
            desc=scheme.listDesc,
            authorID=scheme.accountID,
            authorName=user_model.userName,
            levels=scheme.listLevelsID,
            likes=0,
            downloads=0,
            difficultyIcon=scheme.difficultyIcon,
            is_feature=False
        )
        await ListRepository.add_one(list_model)
        return list_model.id


    @staticmethod
    async def get_lists(scheme: GetList):
        stmt = select(ListModel)

        if scheme.diff != "-":
            match scheme.diff:
                case -1:
                    stmt = stmt.filter(ListModel.is_feature == False)

