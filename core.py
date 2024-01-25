import os
import time
from src import init_app
import logger
time.sleep(1)
# console.print("[purple] Building C part ... [/]", justify="center")
# console.print(
#     "[yellow bold] Сonfiguration... [/]",
#     justify="center",
# )
# console.print("[green bold] GDPS started [/]", justify="center")

from config import system

if system.pluginloader:
    for i in os.listdir("plugins"):
        if i != "origins.py" and i != "__pycache__":
            if i.endswith(".py"):
                i = i[:-3]
            exec(f"import plugins.{i}")

app = init_app()


