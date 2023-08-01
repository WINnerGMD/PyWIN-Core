from fastapi import APIRouter, Form, HTTPException, Request,Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
from helpers.security import bcrypt_hash
from database import get_db
from sqlalchemy.orm import Session
from services.user import UserService
from sql import models
import json
from config import path
from config import path
from route_manager import default_route
from objects.schemas import UpdateStats
router = APIRouter(prefix="", tags=["account"])


@router.post(f"{path}/getGJUserInfo20.php", response_class=PlainTextResponse)
def get_userInfo(accountID: str = Form(),targetAccountID: str = Form(), db: Session = Depends(get_db)):
        user_obj = UserService().get_user_byid(db=db, id=accountID)
        iconkit = user_obj.iconkits

        # rank = db.query(models.User).filter(models.User.stars > user_obj.stars).all()
        response = f'1:{user_obj.userName}:2:{user_obj.id}:13:{user_obj.coins}:17:{user_obj.usr_coins}:10:{iconkit["color1"]}:11:{iconkit["color2"]}:3:{user_obj.stars}:46:{user_obj.diamonds}:4:{user_obj.demons}:8:{user_obj.cp}:18:0:19:0:50:0:20:UCZoN2WLAooS6uhREa9Cgpwg:21:{iconkit["accIcon"]}:22:{iconkit["accShip"]}:23:{iconkit["accBall"]}:24:{iconkit["accBird"]}:25:{iconkit["accDart"]}:26:{iconkit["accRobot"]}:28:{iconkit["accGlow"]}:43:{iconkit["accSpider"]}:48:1:30:47981:16:{user_obj.id}:31:0:44::45:devexit:49:{user_obj.role}:29:1'
        return response
    
    

# @router.post(f"{path}/getGJUsers20.php", response_class=PlainTextResponse)
# @default_route()
# def get_users(str: str = Form()):
#     try:
#         search_obj = int(str)
#         result = db(f"SELECT * FROM `users` WHERE `id` = {search_obj} or `userName` LIKE '{search_obj}';")
#     except:
#         search_obj = str
#         result = db(f"SELECT * FROM `users` WHERE `userName` LIKE '{search_obj}';")
#     if result != []:
#         user_obj = result[0]
#         return f"1:{user_obj['userName']}:2:{user_obj['id']}:13:{user_obj['coins']}:17:{user_obj['usr_coins']}:9:{'1'}:10:{'5'}:11:{'1'}:14:{'1'}:15:{'9'}:16:{user_obj['id']}:3:{user_obj['stars']}:8:{user_obj['cp']}:4:{user_obj['demons']}#999:0:10"
    


# @router.post(f'{path}/getGJAccountComments20.php', response_class=PlainTextResponse)
# @default_route()
# def get_commands(accountID = Form()):
#     return "1~134~2~TmV3IExldmVsIGRhbmdlciBqdW5nbGUh~3~1~4~100~11~2~9~6 months~6~1745624|2~QWxsZWdpYW5jZSAxMDAl~4~2~9~6 months~6~1744292|2~SUNEWCAxMDAlIDop~4~1~9~6 months~6~1743608|2~T2ggeWVhaCBDYXRhIGFuZCBUVVAgMTAwJQ==~4~1~9~7 months~6~1742661|2~Mi4xMSBpcyBvdXQgOik=~4~43~9~2 years~6~1295890|2~SSBsaWtlIGhvdyBzb21lb25lIGRpc2xpa2UgYm90dGVkIG1vc3Qgb2YgbXkgY29tbWVudHMgOikgU2hvd3MgdGhhdCBJJ20uLi5mQW1PdVM=~4~16~9~2 years~6~1279970|2~TmVjcm9wb2xpeCBpbiAyMTYgYXR0IGluIHByYWN0aWNl~4~14~9~2 years~6~1264265|2~IkhpIEx1bmEi~4~15~9~3 years~6~1246506|2~TyB3YWl0IG15IDUwdGggZGVtb24gd2FzIGdvaW5nIHRvIGJlIEJ1Y2sgRm9yY2UsIG5vdCByZWFsbHkgY2VsZWJyYXRvcnkuLi4=~4~7~9~3 kafifs~6~1238082#67:0:10"


@router.post(f'{path}/updateGJUserScore22.php', response_class=PlainTextResponse)
@default_route()
def updateGJUserScore22(accountID: str = Form(),stars: str = Form(),
                        demons: str = Form(),diamonds: str = Form(),
                        coins: str = Form(),userCoins: str = Form(),
                        accIcon: str = Form(),accShip: str = Form(),
                        accBall: str = Form(),accBird: str = Form(),
                        accDart:str = Form(),accRobot: str = Form(),
                        accGlow:str = Form(),accSpider: str = Form(),
                        accExplosion:str = Form(), gjp: str = Form(),
                        color1: str = Form(), color2: str = Form(),
                        db: Session = Depends(get_db)
                        ):
    iconkit = {"color1": int(color1), "color2":  int(color2), "accBall":  int(accBall), "accBird":  int(accBird), "accDart":  int(accDart), "accGlow":  int(accGlow), "accIcon":  int(accIcon), "accShip":  int(accShip), "accRobot":  int(accRobot), "accSpider":  int(accSpider), "accExplosion":  int(accExplosion)}
    result = UpdateStats(id=accountID,stars=stars, demons=demons,diamonds=diamonds,coins=coins,usr_coins=userCoins, iconkits=iconkit)
    print(result)
    UserService().update_user(db=db, data=result)
    print(gjp)
    
#     db(f"UPDATE `users` SET  `iconkit` = '{iconkit}',`stars`='{stars}',`diamonds`='{diamonds}',`coins`='{coins}',`usr_coins`='{userCoins}',`demons`='{demons}' WHERE `id` = {accountID} ")
    return accountID