from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse

import sys
sys.path.append("...")
from helpers.security import bcrypt_hash
# from database import req
router = APIRouter(prefix="", tags=["account"])

@router.post("/winnertests/accounts/registerGJAccount.php" , response_class=PlainTextResponse)
def register_account(userName: str = Form(),
                     password: str = Form(),
                     email: str = Form(),
                     secret: str = Form("def")
                     ):
    if secret != "Wmfv3899gc9":
        raise HTTPException(status_code=400, detail="Павел шампанов уже выехал за тобой \n Данные на сервера уже отправленны, беги👊")
    else:
        print(userName)
        if req(f"SELECT * FROM `users` WHERE userName = '{userName}'") == ():
            req(f"INSERT INTO `users` (`userName`, `mail`, `passhash`,`verifed`) VALUES ('{userName}', '{email}', '{bcrypt_hash(password)}', '0');")
            return "1"
        else:
            return "-2"


@router.post("/winnertests/accounts/loginGJAccount.php" , response_class=PlainTextResponse)
def login(userName: str = Form(),
          password: str = Form()):
    answer = req(f"SELECT * FROM `users` WHERE userName = '{userName}'")
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
    

@router.post("/winnertests/getAccountURL.php")
def get_url(accountID: int = Form()):
    return "http://127.0.0.1:8000"



@router.get("/winnertests/accounts/accountManagement.php", response_class=HTMLResponse)
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