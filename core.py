from fastapi import FastAPI, Request,Body
from fastapi.responses import PlainTextResponse, HTMLResponse

from gd.levels import router as router_levels
from gd.accounts.accounts import router as router_accounts

from plugins.origins import app
app = FastAPI()

app.include_router(router_levels)
app.include_router(router_accounts)



@app.get("/", response_class=HTMLResponse)
async def message():
    answer = """<!DOCTYPE html>
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
    return answer
