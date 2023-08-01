from plugins.origins import PyWIN
from route_manager import route_config
from fastapi.responses import HTMLResponse
from helpers.helper import get_stats
app = PyWIN("musix", "t1212121_12mssd")



@app.command()
def test_func():
    app.alert("test_func")

@app.command()
def routes():
    app.alert(route_config)

@app.router.get('/suka', response_class=HTMLResponse)
def shprot():
    stat = get_stats()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мама я сайт создал</title>
</head>
<body>
    <div id="overview">
        <h1>Статистика</h1>
        <p>Игроков: {stat['users'][0]['count(*)']}</p>
        <p>Уровней: {stat['levels'][0]['count(*)']}</p>
    </div>
</body>
</html>"""