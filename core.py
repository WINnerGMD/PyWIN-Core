import os
import uvicorn
from fastapi import Depends, Request
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from config import system
from database import get_db
from gd.rate.rate_levels import router as router_rate
from gd.accounts.accounts import router as router_accounts
from gd.accounts.page import router as router_acc_page
from gd.api.get_levels import router as router_api_levels
from gd.api.get_user import router as router_api_users
from gd.comments.comments import router as router_comments
from gd.comments.posts import router as router_posts
from gd.levels.levels import router as router_levels
from gd.misc.likes import router as router_likes
from gd.music.musix import router as router_music
from gd.rewards.chest import router as router_chest
from gd.scores.scores import router as router_scores
from logger import info, warning
from plugins.origins import router as router_origins
from services.levels import LevelService
from services.user import UserService

if system.pluginloader:
    for i in os.listdir("plugins"):
        if i != "origins.py" and i != "__pycache__":
            if i.endswith(".py"):
                i = i[:-3]
            info(f"plugin load {i}")
            exec(f"import plugins.{i}")

fastapi = FastAPI(
    docs_url="/swagger",
    redoc_url=None,
    title="PyWIN Core",
    summary="For developers and testers",
)

fastapi.include_router(router_origins)
fastapi.include_router(router_accounts)
fastapi.include_router(router_levels)
fastapi.include_router(router_acc_page)
fastapi.include_router(router_comments)
fastapi.include_router(router_posts)
fastapi.include_router(router_likes)
fastapi.include_router(router_music)
fastapi.include_router(router_scores)
fastapi.include_router(router_rate)
fastapi.include_router(router_chest)
fastapi.include_router(router_api_levels)
fastapi.include_router(router_api_users)
fastapi.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@fastapi.get(system.path, response_class=HTMLResponse)
async def message(req: Request, db=Depends(get_db)):
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


@fastapi.on_event("startup")
async def startup():
    info("Server Started")


if __name__ == "__main__":
    warning("server started only by localhost")
    uvicorn.run(app=fastapi)
