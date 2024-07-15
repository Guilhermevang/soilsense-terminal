from rich.console import Console
from rich import pretty
from utils import *


pretty.install()

# Apresentação inicial
intro = Basics()

# Inicia uma nova 'janela' e roda o código dentro de 'intro'
window = Window()
window.run(intro.runPreTasks)