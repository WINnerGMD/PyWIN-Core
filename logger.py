from rich.console import Console
import threading
from utils.gdform import formatted_date


console = Console()


def console_start():
    """/"""

    #         request = console.input("")
    #         spliter = request.split(" ")
    #         if prefix in spliter[0]:
    #             run = True
    #             command = spliter[0].replace(prefix,"")
    #             args = int(len(spliter) - 1)
    #             spliter.pop(0)
    #             if args == 0:
    #                 for i in self.command_start.ZeroArgs:
    #                     if i["func_name"] == command:
    #                         run = False
    #                         try:
    #                             i["func"]()
    #                         except:
    #                             pass
    #                 if run == True:
    #                     print(f"Команда не найдена")
    #             elif args == 1:
    #                 run = True
    #                 for i in self.command_start.OneArgs:
    #                     if i["func_name"] == command:
    #                         try:
    #                             i["func"](spliter[0])
    #                             run = False
    #                         except:
    #                             pass
    #                 if run == True:
    #                     print("Команда не найдена")

    #             elif args == 2:
    #                 run = True
    #                 for i in self.command_start.TwoArgs:
    #                     if i["func_name"] == command:
    #                         try:
    #                             i["func"](spliter[0])
    #                             run = False
    #                         except:
    #                             pass
    #                 if run == True:
    #                     print("Команда не найдена")
    #         else:
    #             print("неизвестный запрос")


console_th = threading.Thread(target=console_start, name="console")
console_th.start()


def warning(message):
    # if config.logger_warning:
        console.print(
            f"[bold yellow][WARNING][/bold yellow] - {formatted_date()} / {message}",
        )


def info(message):
    # if config.logger_info:
        console.print(
            f"[bold green][INFO][/bold green] - {formatted_date()} / {message}",
        )


def error(message):
    # if config.logger_error:
        console.print(
            f"[bold red][ERROR][/ bold red] - {formatted_date()} / {message}",
        )


def alert(message, plugin_name):
    console.print(
        f"[bold red]{plugin_name}[/ bold red] - {formatted_date()} / {message}",
    )
