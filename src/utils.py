# import time
from rich.console import Console
import os
from content.asciiart import ascii_art
from tasks import Tasks
import contract
# import pytermgui as ptg

os.system("cls")


space_between = "    "

class Basics:
    def __init__(self):
        self.console = Console()
        self.order = contract.Order
        self.tasks = Tasks()

    def start(self):
        self.console.print(ascii_art, justify="center", style="#009C34 bold")

        pre_tasks = [
            contract.Waiter(task=Tasks.fetchSatellitesTLE, label="Buscando satélites disponíveis"),
        ]

        order = self.order(label="Iniciando programa...")
        order.add(*pre_tasks).start()

        options = [
            "[1] Rastrear Satélites",
            space_between,
            "[2] Sensoriamento Remoto",
            space_between,
            "[3] Finalizar",
        ]

        self.console.print(
            *options,
            justify="center",
            style="#B0DAFF"
        )