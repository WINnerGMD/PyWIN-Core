import requests
import json
import threading
from rich.console import Console
import inspect
import sys
import time
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
    __endpoins = []
    run_console = True
    token = None
    name = None
    verify_status = 0
    prefix = "!"
    command_start = command_sys()
    def __init__(self,name,token):
        self.token = token
        self.name = name
    def main_start(self):
        console_th = threading.Thread(target=self.__console, name="console")
        console_th.start()

        cache.route_config = self.__endpoins

        return console_th


    def __console(self):
        console = Console()
        prefix = "/"
        console.print('hello')
        while self.run_console:
                request = console.input("")
                spliter = request.split(" ")
                if prefix in spliter[0]:
                    run = True
                    command = spliter[0].replace(prefix,"")
                    args = int(len(spliter) - 1)
                    spliter.pop(0)
                    if args == 0:
                        for i in self.command_start.ZeroArgs:
                            if i["func_name"] == command:
                                run = False
                                try:
                                    i["func"]() 
                                except:
                                    pass
                        if run == True:
                            print(f"Команда не найдена")
                    elif args == 1:
                        run = True
                        for i in self.command_start.OneArgs:
                            if i["func_name"] == command:
                                try:
                                    i["func"](spliter[0])
                                    run = False
                                except:
                                    pass
                        if run == True:
                            print("Команда не найдена")

                    elif args == 2:
                        run = True
                        for i in self.command_start.TwoArgs:
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
        self.alert("emergency shutdown")
        time.sleep(3)
        self.alert("emergency shutdown")
        self.run_console = True

        # self.__emergency_console()

    def __emergency_console(self):
        self.__console()
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
        


    # def error(error_code = "server closed"):
# print(app.opener())
# app.rebuild({'database': {'host': 'localhoedededest', 'port': 3306, 'name': '', 'password': '', 'database': ''}})
app = PyWIN("sdssdsd","\sdsdsd")




# if __name__ == "plugins.origins":
#     app.main_start()
