from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from database import db
from config import  path

router = APIRouter(tags=["rate"], prefix="")



@router.post(path=f'{path}/suggestGJStars20.php',response_class=PlainTextResponse)
def suggestGJStars(accountID: str = Form(), feature: str = Form(), levelID: str = Form(), stars: str = Form()):
    answer = db(f"SELECT * FROM `users` WHERE `id` = {accountID}")
    user_obj = answer[0]
    if user_obj['role'] == 1:
        return "1"
    elif user_obj['role'] == 2:
        print(type(stars))
        if stars == "1":
            if feature == "0":
                db(f"UPDATE `levels` SET `starAuto` = 1, `stars` = 1, `rate` = 0 WHERE `id` = {levelID}")
            elif feature == "1":
                db(f"UPDATE `levels` SET `starAuto` = 1, `stars` = 1, `rate` = 1 WHERE `id` = {levelID}")
        elif int(stars) <= 9 and int(stars) >= 2:
            if int(stars) <= 3:
                difficulty = int(stars) - 1
            else: 
                if int(stars) in [4,5]:
                    difficulty = 3
                elif int(stars) in [6,7]:
                    difficulty = 4
                elif int(stars) in [8,9]:
                    difficulty = 5
            print(difficulty)
            if feature == "0":
                db(f"UPDATE `levels` SET `starAuto` = 0, `stars` = {int(stars)},`difficulty` =  {difficulty}, `rate` = 0 WHERE `id` = {levelID}")
            elif feature == "1":
                db(f"UPDATE `levels` SET `starAuto` = 0, `stars` = {int(stars)},`difficulty` =  {difficulty}, `rate` = 1 WHERE `id` = {levelID}")

        # elif stars == "3":
        #     if feature == "0":
        #         db(f"UPDATE `levels` SET `starAuto` = 0, `stars` = 3,`difficulty` = 2, `rate` = 0 WHERE `id` = {levelID}")
        #     elif feature == '1':
        #         db(f"UPDATE `levels` SET `starAuto` = 0, `stars` = 3,`difficulty` = 2, `rate` = 1 WHERE `id` = {levelID}")
        # db(f"UPDATE `levels` SET `stars` = '1', `difficulty` = '1', `rate` = '1' WHERE `id` = 3;")
        return "1"
    else:
        return "-2"
    print()