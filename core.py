import os
import time

from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware

import logger
from logger import info, warning, console

logger.StartLog()
time.sleep(1)
console.print("[purple] Building C part ... [/]", justify="center")
console.print(
    "[yellow bold] Сonfiguration... [/]",
    justify="center",
)
console.print("[green bold] src.gdPS started [/]", justify="center")
import uvicorn
from fastapi import Depends, Request, status
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import system
from src.api import app as api_app
from src.gd.rate.rate_levels import router as router_rate
from src.gd.accounts import router as router_accounts
from src.gd.comments.comments import router as router_comments
from src.gd.comments.posts import router as router_posts
from src.gd.levels.levels import router as router_levels
from src.gd.levels.level_packs import router as router_levelpack
from src.gd.misc.likes import router as router_likes
from src.gd.music.musix import router as router_music
from src.gd.rewards.chest import router as router_chest
from src.gd.scores.scores import router as router_scores

from plugins.origins import router as router_origins
from src.services.levels import LevelService
from src.services.user import UserService

if system.pluginloader:
    for i in os.listdir("plugins"):
        if i != "origins.py" and i != "__pycache__":
            if i.endswith(".py"):
                i = i[:-3]
            info(f"plugin load {i}")
            exec(f"import plugins.{i}")

fastapi = FastAPI(
    docs_url=f"{system.path}/swagger",
    redoc_url=None,
    title="PyWIN Core",
    summary="For developers and testers",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@fastapi.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Error": "Name field is missing"}),
    )


fastapi.mount(app=api_app, path='/v2')
fastapi.include_router(router_origins)
fastapi.include_router(router_accounts)
fastapi.include_router(router_levels)
fastapi.include_router(router_levelpack)
fastapi.include_router(router_comments)
fastapi.include_router(router_posts)
fastapi.include_router(router_likes)
fastapi.include_router(router_music)
fastapi.include_router(router_scores)
fastapi.include_router(router_rate)
fastapi.include_router(router_chest)
fastapi.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@fastapi.get(system.path, response_class=HTMLResponse)
async def message(req: Request):
    levels = await LevelService.get_total_levels(db=db)
    users = await UserService.get_total_users(db=db)
    if levels["status"] == "ok" and users["status"] == "ok":
        return templates.TemplateResponse(
            "database_page.html",
            {"request": req, "users": users["count"], "levels": levels["count"]},
        )
    else:
        return templates.TemplateResponse(
            "error.html", {"request": req, "error": levels["details"]}
        )


fastapi.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])


@fastapi.on_event("startup")
async def startup():
    info("Server Started")


if __name__ == "__main__":
    warning("server started only by localhost")
    uvicorn.run(app=fastapi)
