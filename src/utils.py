# import time
import time
from typing import Callable, Literal
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
        self.tasks = Tasks()

    def runPreTasks(self, clear:Callable):
        pre_tasks = [
            contract.Waiter(task=Tasks.fetchSatellitesTLE, label="Buscando satélites disponíveis"),
        ]

        order = contract.Order(label="Iniciando programa...")
        (order
            .add(*pre_tasks)
            .start()
            .then(
                success="Pronto",
                failure="Houve um erro"
            ))
        
        if order.failed:
            return

        time.sleep(1)

        clear()

        # options = [
        #     "[1] Rastrear Satélites",
        #     space_between,
        #     "[2] Sensoriamento Remoto",
        #     space_between,
        #     "[3] Finalizar",
        # ]

        # self.console.print(
        #     *options,
        #     justify="center",
        #     style="#B0DAFF"
        # )

class Window:
    def __init__(self):
        self.console = Console()
        self.top_art = {
            'ascii': ascii_art,
            'color': '#009C34',
            'weight': 'bold',
            'align': 'left'
        }

    def setArt(self, ascii, align:Literal['default', 'left', 'center', 'right', 'full']='default', color=None, weight='bold'):
        """ Define a arte que será exibida no topo do console """
        self.top_art['ascii'] = ascii
        self.top_art['align'] = align
        self.top_art['color'] = color
        self.top_art['weight'] = weight

    def clear(self):
        """ Limpa o console e desenha o cabeçalho novamente """
        os.system('cls')
        self.draw() # Desenha o cabeçalho novamente

    def draw(self):
        """ Desenha o cabeçalho e tudo que for importante """
        self.console.print(
            self.top_art['ascii'],
            justify=self.top_art['align'],
            style=f"{self.top_art['color']} {self.top_art['weight']}"
        )

    def run(self, window:Callable):
        """ Roda a janela """
        self.draw()
        window(clear=self.clear) # Chama a função de Callback passando o método que limpa a tela