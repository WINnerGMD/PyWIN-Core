from origins import PyWIN
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
        app.alert("MEMHAUSE LOH EBANIY")
        run += 1

@app.command()
def config_get():
    app.alert(app.config_opener())


    
if __name__ == "__main__":
    app.start()