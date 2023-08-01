from fastapi import FastAPI, Request,Body, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
from plugins.origins import app
from services.user import *
from database import get_db, engine




models.Base.metadata.create_all(bind=engine)
from gd.levels.levels import router as router_levels
from gd.accounts.accounts import router as router_accounts
from gd.accounts.page import router as router_acc_page
# from gd.rate.rate_levels import router as router_rates
# from gd.levels.likes import router as router_likes
from gd.levels.upload import router as router_upload
# from win.main import router as router_pywin
# from gd.music.songs import router as router_music
# from gd.scores.scores import router as router_scores
# from route_manager import default_route , plugin_management
# from route_manager import router as plugin_router
from  gd.comments.comments import router as router_comments
import os
import uvicorn
from config import pluginload
import json
if pluginload == True:
    for i in os.listdir("plugins"):
        if i != "origins.py" and i != "__pycache__":
            if i.endswith('.py'):
                i = i[:-3]
            # plugin_management(i)
            exec(f"import plugins.{i}")
        
fastapi = FastAPI()

fastapi.include_router(router_levels)
fastapi.include_router(router_accounts)
fastapi.include_router(router_acc_page)
fastapi.include_router(router_comments)
# fastapi.include_router(router_rates)
# fastapi.include_router(router_likes)
fastapi.include_router(router_upload)
# fastapi.include_router(router_music)
# fastapi.include_router(plugin_router)
# fastapi.include_router(router_pywin)
# fastapi.include_router(router_scores)
@fastapi.get("/", )
# @default_route()
async def message( db: Session = Depends(get_db)):
    # UserService().register_user(db=db)
    # print(UserService().get_user_byid(db, id=1))
    # return UserService().get_user_byid(db, id=1)
    return str(UserService().get_user_byid(db, id=3))
    # return """
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="UTF-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <title>PyWIN Core</title>
    # </head>
    # <body style="background-color: rgb(32, 37, 36);">
    #     <div style="background-color: rgb(55, 48, 66); text-align: center; width:100vh; height: 500px; border-radius: 15px; margin-left: 25%; margin-top: 5%;">
    #         <h1 style="padding: 25px; font-family: Arial, Helvetica, sans-serif; color: white;">PyWIN Core Успешно припаркован</h1>
    #         <h2 style="color: white; font-family: Arial, Helvetica, sans-serif;">Привет🚀 <br>Если ты не админ, я кажется знаю что ты тут делаешь... <br> Ну давай, устрой тест драйв)</h2>
    #         <a href="https://pywin.pw/gdps" style="text-decoration: none; color: white; margin-top: 100px;">PyWIN EcoSystem</a>
    #     </div>
    # </body>
    # </html>
    # """


if __name__ == '__main__':
    uvicorn.run(app="core:fastapi", reload=True)