from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse
from src.utils.crypt import checkValidGJP2
from src.schemas.list.service.post import UploadList
from src.services.lists import ListService
from config import system

router = APIRouter(prefix="", tags=["Lists"], default_response_class=PlainTextResponse)


@router.post(f"{system.path}/uploadGJLevelList.php")
async def upload_lists(req: Request,
                       gjp2: str = Form(),
                       accountID: int = Form(),
                       listName: str = Form(),
                       listDesc: str = Form(default=""),
                       listLevels: str = Form(),
                       difficulty: int = Form(),
                       ):
    if await checkValidGJP2(accountID, gjp2=gjp2):
        service_schema = UploadList(
            accountID=accountID,
            listName=listName,
            listDesc=listDesc,
            listLevelsID=listLevels,
            difficultyIcon=difficulty
        )
        list_id = await ListService.upload_list(service_schema)
        return str(list_id)


@router.post(f"{system.path}/getGJLevelLists.php")
async def Get_lists(
        req: Request,
        string: str = Form(default=None, alias="str"),
        page: int = Form(default=None),
        type: int = Form(default=None),
        accountID: int = Form(default=None),
        diff: int | str = Form(default=None),
        star: int = Form(default=None),
                    ):
    print(await req.form())

