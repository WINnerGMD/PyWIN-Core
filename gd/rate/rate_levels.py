from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from database import db


router = APIRouter(tags=["rate"], prefix="")



@router.post(path='/winnertests/suggestGJStars20.php',response_class=PlainTextResponse)
def suggestGJStars(accountID: str = Form()):
    answer = db(f"SELECT * FROM `users` WHERE `id` = {accountID}")
    user_obj = answer[0]
    if user_obj['role'] == 1:
        print("отправил модерации")
        return "1"
    elif user_obj['role'] == 2:
        print("рэйтнул")
        return "1"
    else:
        print('ебаное уебище')
        return "-2"