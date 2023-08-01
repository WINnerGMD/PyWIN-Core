from plugins.origins import PyWIN



app  = PyWIN("zemon", "121212j1")



@app.command()
def test_func():
    app.alert("Hello i am zemon")