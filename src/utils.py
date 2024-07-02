import time
from rich.console import Console
import os
from content.asciiart import ascii_art
from tasks import Tasks
import contract
import menu


os.system("cls")

space_between = "       "

class Basics:
    def __init__(self):
        self.console = Console()
        self.tasks = Tasks()

    def start(self):
        self.console.print(ascii_art, justify="center", style="#009C34 bold")

        pre_tasks = [
            contract.PreTask(task=Tasks.fetchSatellitesTLE, label="Buscando satélites disponíveis"),
        ]

        with self.console.status("[purple bold]Iniciando programa...[/purple bold]", spinner="simpleDots") as status:
          while pre_tasks:
              task = pre_tasks.pop(0)
              status.update(f"{task.loading}", spinner=task.spinner)
              task.execute(status, task)
              self.console.log(task.complete)

        options = [
            "Rastrear Satélites",
            "Sensoriamento Remoto",
            "Finalizar",
        ]

        menu_ex = menu.Menu(options)
        user_choice = menu_ex.launch(response="String")
        self.console.print(f"Você selecionou [ {menu_ex.selected} ], {user_choice}")

        # self.console.print(
        #     "Rastrear Satélites",
        #     space_between,
        #     "[purple bold]> Sensoriamento Remoto <[/purple bold]",
        #     space_between,
        #     "Finalizar",
        #     justify="center",
        #     style="#B0DAFF"
        # )