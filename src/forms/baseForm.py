from rich.console import Console
from utils import Utils

class BaseForm:
    """
    Formulário base
    """
    def __init__(self) -> None:
        self.console = Console()
        self.utils = Utils()