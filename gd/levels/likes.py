from fastapi import APIRouter,Form
from fastapi.responses import PlainTextResponse
from database import db
from config import path
router = APIRouter()


@router.post(f'{path}/likeGJItem211.php', response_class=PlainTextResponse)
def likeItem211(itemID: str = Form(), type: str = Form(), accountID:str =  Form(), like: str = Form()):
    if type == '1':
        result = int(db(f"SELECT * FROM `levels` WHERE `id` = '{itemID}'")[0]['likes'])

        total_likes = result -1 if like == "0" else result +1
        print(total_likes)
        db(f"UPDATE `levels` SET `likes` = '{total_likes}' WHERE `id` = '{itemID}'")
    return "1"

