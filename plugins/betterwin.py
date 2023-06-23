from origins import PyWIN
import time
app = PyWIN("betterwin","origins")
@app.command("hui")
def test_func(arg):
    app.alert(f"hello {arg}")

@app.command("hui")
def Memhouse_loh():
    run = 0
    while run <= 10:
        time.sleep(1)
        app.alert("MEMHAUSE LOH EBANIY")
        run += 1


app.test()


app.start()