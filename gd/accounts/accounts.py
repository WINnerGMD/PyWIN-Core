from fastapi import APIRouter, Form, HTTPException,Request,Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
# from database import req
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models
from services.user import UserService
from config import path
from route_manager import default_route
from database import get_db
from helpers.security import chechValid
from services.perms import PermissionService
from helpers.security import bcrypt_hash
router = APIRouter(prefix="", tags=["account"])

@router.post(f"{path}/accounts/registerGJAccount.php" , response_class=PlainTextResponse)
@default_route()
async def register_account(userName: str = Form(),
                     password: str = Form(),
                     email: str = Form(),
                     secret: str = Form(default=""),
                     db: AsyncSession = Depends(get_db)):
    if secret == "":
        raise HTTPException(401,'Паша шампанов уже едет за тобой')
    service_response = await UserService().register_user(db=db, userName=userName, password=password,mail=email)
    return str(service_response['code'])


@router.post(f"{path}/accounts/loginGJAccount.php" , response_class=PlainTextResponse)
@default_route()
async def login(userName: str = Form(),
          password: str = Form(),
          db: AsyncSession = Depends(get_db)):
    service_response = await UserService().login_user(userName=userName, password=password, db=db)

    if "error" in service_response["message"]:
        print(str(service_response))
        return str(service_response['code'])
    else:
        print(f"{service_response['id']},{service_response['id']}")
        return f"{service_response['id']},{service_response['id']}"
    # answer = db(f"SELECT * FROM `users` WHERE userName = '{userName}'")
    # if answer != ():
    #     for user in answer:
    #         pass
    #     passhash = bcrypt_hash(password)
    #     print(passhash)
    #     print(user["passhash"])
    #     if user["passhash"] == passhash:
    #         id = user["id"]
    #         return f"{id},{id}"
    #     else:
    #         return "-11"
    # else:
    #     return "-11"
    

@router.post(f"{path}/getAccountURL.php", response_class=PlainTextResponse)
@default_route()
async def get_url(req: Request):
    print(await req.body())
    return "http://127.0.0.1:8000"

@router.post(f'/database/accounts/backupGJAccountNew.php',response_class=PlainTextResponse)
async def backup(saveData:str = Form(), password:str =Form(), userName: str = Form(), db: AsyncSession = Depends(get_db)):
    usersData = (await db.execute(select(models.Users).filter(models.Users.userName == userName))).scalars().first()
    if usersData != None:

        if bcrypt_hash(password) == usersData.passhash:
            
            with open(f'gd/accounts/backups/{userName}.pw', "w") as f:
                f.write(saveData)
            return "1"
    else:
        return "-1"

@router.post(f'/database/accounts/syncGJAccountNew.php',response_class=PlainTextResponse)
async def sync(userName:str = Form(), password: str = Form(),db: AsyncSession = Depends(get_db)):
    usersData = (await db.execute(select(models.Users).filter(models.Users.userName == userName))).scalars().first()
    if usersData != None:

        if bcrypt_hash(password) == usersData.passhash:

            try:
                with open(f'gd/accounts/backups/{userName}.pw', "r") as f:
                    backup = f.read()
                return f"{backup};21;30;a;a"
            except:
                return "-1"
        else:
            return "-1"
    else:
        pass
@router.post(f'{path}/requestUserAccess.php')
@default_route()
def get_user_access(gjp: str = Form(),accountID: str = Form(), db: AsyncSession = Depends(get_db)):
    if chechValid(id=accountID,gjp=gjp, db=db)  == True:
        return PermissionService().request_access(id = accountID, db=db)
    else:
        return "0"


@router.get(f"{path}/accounts/accountManagement.php", response_class=HTMLResponse)
def accountManagement():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDPS Manager</title>
</head>
<body style="background-color: rgb(32, 37, 36);">
    <div style="background-color: rgb(55, 48, 66); text-align: center; width:100vh; height: 500px; border-radius: 15px; margin-left: 25%; margin-top: 5%;">
        
    </div>
</body>
</html>"""