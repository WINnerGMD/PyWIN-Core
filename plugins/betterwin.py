from plugins.origins import PyWIN
import time


app = PyWIN("betterwin","originsssss")


@app.command()
def test_func(arg):
    app.alert(f"hello {arg}")

@app.command()
def Memhouse_loh():
    run = 0
    while run <= 2:
        time.sleep(1)
        app.alert("MEMHAUSE LOH")
        run += 1

@app.command()
def config_get():
    app.alert(app.config_opener())


@app.command()
def robot():
    app.alert("Бип-Боп запускаю сервер🐬")
    app.alert("Сервер работает в штатном режиме!")

app.test()
if __name__ == "__main__":
    app.start()