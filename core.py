from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from gd.levels.levels import router as router_levels
from gd.accounts.accounts import router as router_accounts
from gd.accounts.page import router as router_acc_page
from gd.api.get_levels import router as router_api_levels
from gd.api.get_user import router as router_api_users
from logger import info
from gd.levels.likes import router as router_likes
from gd.levels.upload import router as router_upload
from gd.music.musix import router as router_music
from gd.scores.scores import router as router_scores
from  gd.comments.comments import router as router_comments
from gd.comments.posts import router as router_posts
from asade.verified import router as router_verified_asade
from helpers import rate
from config import path
import os 
import uvicorn
from config import pluginload
if pluginload == True:
    for i in os.listdir("plugins"):
        if i != "origins.py" and i != "__pycache__":
            if i.endswith('.py'):
                i = i[:-3]
            exec(f"import plugins.{i}")
        
fastapi = FastAPI()

fastapi.include_router(router_levels)
fastapi.include_router(router_accounts)
fastapi.include_router(router_acc_page)
fastapi.include_router(router_comments)
fastapi.include_router(router_api_levels)
fastapi.include_router(router_api_users)
fastapi.include_router(router_posts)
fastapi.include_router(router_likes)
fastapi.include_router(router_upload)
fastapi.include_router(router_music)
fastapi.include_router(router_verified_asade)
fastapi.include_router(router_scores)
import logger
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

@fastapi.get(path, response_class=HTMLResponse )
@cache(expire=60)
async def message():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PyWIN Core</title>
    </head>
    <body style="background-color: rgb(32, 37, 36);">
        <div style="background-color: rgb(55, 48, 66); text-align: center; width:100vh; height: 500px; border-radius: 15px; margin-left: 25%; margin-top: 5%;">
            <h1 style="padding: 25px; font-family: Arial, Helvetica, sans-serif; color: white;">PyWIN Core Успешно припаркован</h1>
            <h2 style="color: white; font-family: Arial, Helvetica, sans-serif;">Привет🚀 <br>Если ты не админ, я кажется знаю что ты тут делаешь... <br> Ну давай, устрой тест драйв)</h2>
            <a href="https://pywin.pw/gdps" style="text-decoration: none; color: white; margin-top: 100px;">PyWIN EcoSystem</a>
        </div>
    </body>
    </html>
    """


@fastapi.on_event('startup')
async def startup():
    info('Server Started')

if __name__ == '__main__':
    uvicorn.run(app="core:fastapi", host="fhgd.store")


