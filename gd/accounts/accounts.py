from fastapi import APIRouter, Form, HTTPException,Request,Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
# from database import req
from sqlalchemy.orm import Session
from services.user import UserService
from config import path
from route_manager import default_route
from database import get_db

router = APIRouter(prefix="", tags=["account"])

@router.post(f"{path}/accounts/registerGJAccount.php" , response_class=PlainTextResponse)
@default_route()
def register_account(userName: str = Form(),
                     password: str = Form(),
                     email: str = Form(),
                     secret: str = Form(default=""),
                     db: Session = Depends(get_db)):
    if secret == "":
        raise HTTPException(401,'Паша шампанов уже едет за тобой')
    service_response = UserService().register_user(db=db, userName=userName, password=password,mail=email)
    return str(service_response['code'])
@router.post(f"{path}/accounts/loginGJAccount.php" , response_class=PlainTextResponse)
@default_route()
def login(userName: str = Form(),
          password: str = Form(),
          db: Session = Depends(get_db)):
    service_response = UserService().login_user(userName=userName, password=password, db=db)

    if "error" in service_response["message"]:
        return str(service_response['code'])
    else:
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
    

@router.post(f"{path}/getAccountURL.php")
@default_route()
async def get_url(req: Request):
    print(await req.body())
    return "https://gdpshelper.xyz"


# @router.post(f'{path}/requestUserAccess.php')
# @default_route()
# def requestUserAccess(accountID: str = Form()):
#     try:
#         accountID = int(accountID)
#     except:
#         raise HTTPException(401,"к тебе уже паша шампанов летит")
#     answer = db(f"SELECT * FROM `users` WHERE `id` = {accountID} and `role` > 0;",)
#     if answer != []:
#         return 1
#     else:
#         return -1
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