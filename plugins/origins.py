import requests
import json
import threading
from rich.console import Console
import inspect
import os
# Main plugin parser file
#Не советую что либо тут изменять. Тут также летят запросы на сервер,
#по этому со сломаным модулем, ошибки могут не регаться,
#и вы не сможете расширенно управлять ядром


console = Console()

class PyWIN:

    class command_sys:
        ZeroArgs = []
        OneArgs = []
        TwoArgs = []
        ThreeArgs = []

        def __init__(self):
            pass


    token = None
    name = None
    verify_status = 0
    prefix = "!"
    command_start = command_sys()
    def __init__(self,name,token):
        self.token = token
        self.name = name

    def start(self):
        try:
            answer = requests.post("http://127.0.0.1:2000/plugins/verify", json={"token": self.token}, headers={"user-agent": self.token}).text
            if answer == 'originsOMG':
                self.verify_status = 1
        except Exception as e:
            print(f"что то пошло не так ...")

        console_th = threading.Thread(target=self.__console, name="console")
        console_th.start()
    def reset_method(self , func):
        def wrapper(*args):
            print("hui")
            func(*args)
        return wrapper
    def __console(self):
        console = Console()
        prefix = "/"
        while True:
                request = console.input("")
                spliter = request.split(" ")
                if prefix in spliter[0]:
                    command = spliter[0].replace(prefix,"")
                    args = int(len(spliter) - 1)
                    spliter.pop(0)
                    if args == 0:
                        for i in self.command_start.ZeroArgs:
                            run = True
                            if i["func_name"] == command:
                                try:
                                    i["func"]()
                                    run = False
                                except:
                                    pass
                        if run == True:
                            print("Команда не найдена")
                    elif args == 1:
                        for i in self.command_start.OneArgs:
                            run = True
                            if i["func_name"] == command:
                                try:
                                    i["func"](spliter[0])
                                    run = False
                                except:
                                    pass
                        if run == True:
                            print("Команда не найдена")

                    elif args == 2:
                        for i in self.command_start.TwoArgs:
                            run = True
                            if i["func_name"] == command:
                                try:
                                    i["func"](spliter[0])
                                    run = False
                                except:
                                    pass
                        if run == True:
                            print("Команда не найдена")
                else:
                    print("неизвестный запрос")
                
    # def __console(self):
    #     asyncio.run(self.__console_async())
    def command(self):
        def wrapper(func):
            arguments = tuple(inspect.getfullargspec(func))[0]
            if int(len(arguments)) == 0:
                self.command_start.ZeroArgs.append({"func_name": func.__name__, "func": func})
            elif int(len(arguments)) == 1:
                self.command_start.OneArgs.append({"func_name": func.__name__, "func": func,"args": arguments})
            elif int(len(arguments)) == 2:
                self.command_start.TwoArgs.append({"func_name": func.__name__, "func": func,"args": arguments})
            elif int(len(arguments)) == 3:
                self.command_start.ThreeArgsArgs.append({"func_name": func.__name__, "func": func,"args": arguments})
            else:
                raise ValueError("Number of arguments is very big")
            # self.doit.append({"func_name": func.__name__, "func": func,"args": arguments})
        return wrapper
    def alert(self, message):
        console.print(f"[red]{self.name}: {message}[/red]")

    def config_opener(self):
        if self.verify_status == 1:
            with open("./config.json", "r") as f:
                jsontext = json.loads(f.read())
            return jsontext
        else:
            print("Функция с конфигом не работает ибо ваш мод ")
            return -1
    def config_rebuild(self,content):
        if self.verify_status == 1:
            with open("./config.json", "w") as f:
                json.dump(content, f, indent=4)
                return "успешно"
        else:
            print("Функция с конфигом не работает ибо ваш мод ")
    def test(self):
        print(self.command_start.ZeroArgs)
        print(self.command_start.OneArgs)
# print(app.opener())
# app.rebuild({'database': {'host': 'localhoedededest', 'port': 3306, 'name': '', 'password': '', 'database': ''}})
app = PyWIN("origins","origins")

@app.command()
def refresh():
    
    app.alert("Server closed")
    exit()


@app.command()
def server_start():
    def open_server():
        app.alert("Server started!")
        os.system("uvicorn core:app --reload")
    console_th = threading.Thread(target=open_server, name="server")
    console_th.start()


if __name__ == "__main__":
    app.start()
else:
    app.start()
