from .. abstract.logger import AbstractConsole
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import time


class ConsoleRepository(AbstractConsole):

    def __init__(self):
        self.console = rich.console.Console()

    def warn(self, text: str) -> None:
        self.console.log(f"[bold yellow] WARN: [/bold yellow] {text} ")

    def info(self, text: str) -> None:
        self.console.log(f"[bold green] INFO: [/bold green] {text} ")

    def alert(self, text: str) -> None:
        self.console.log(f"[bold red] ALERT: [/bold red] {text} ")
