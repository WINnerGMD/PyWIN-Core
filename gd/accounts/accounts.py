from fastapi import APIRouter, Form, HTTPException,Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from helpers.security import bcrypt_hash
# from database import req
from database import db
from config import path
router = APIRouter(prefix="", tags=["account"])

@router.post(f"{path}/accounts/registerGJAccount.php" , response_class=PlainTextResponse)
def register_account(userName: str = Form(),
                     password: str = Form(),
                     email: str = Form(),
                     secret: str = Form("def")
                     ):
    if secret != "Wmfv3899gc9":
        raise HTTPException(status_code=400, detail="Павел шампанов уже выехал за тобой \n Данные на сервера уже отправленны, беги👊")
    else:
        print(userName)
        if db(f"SELECT * FROM `users` WHERE userName = '{userName}'") == ():
            db(f"INSERT INTO `users` (`userName`, `mail`, `passhash`,`verifed`) VALUES ('{userName}', '{email}', '{bcrypt_hash(password)}', '0');")
            return "1"
        else:
            return "-2"


@router.post(f"{path}/accounts/loginGJAccount.php" , response_class=PlainTextResponse)
def login(userName: str = Form(),
          password: str = Form()):
    answer = db(f"SELECT * FROM `users` WHERE userName = '{userName}'")
    if answer != ():
        for user in answer:
            pass
        passhash = bcrypt_hash(password)
        print(passhash)
        print(user["passhash"])
        if user["passhash"] == passhash:
            id = user["id"]
            return f"{id},{id}"
        else:
            return "-11"
    else:
        return "-11"
    

@router.post(f"{path}/getAccountURL.php")
async def get_url(req: Request):
    print(await req.body())
    return "https://gdpshelper.xyz"


@router.post(f'{path}/requestUserAccess.php')
def requestUserAccess(accountID: str = Form()):
    answer = db(f"SELECT * FROM `users` WHERE `id` = {accountID} and `role` > 0;")
    if answer != []:
        return 1
    else:
        return -1
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