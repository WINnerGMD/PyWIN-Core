import os
import time
from .src import init_app

time.sleep(1)
# console.print("[purple] Building C part ... [/]", justify="center")
# console.print(
#     "[yellow bold] Сonfiguration... [/]",
#     justify="center",
# )
# console.print("[green bold] GDPS started [/]", justify="center")

from .src.config import system



app = init_app()
