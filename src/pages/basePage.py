from rich.console import Console
from utils import Utils

class BasePage:
    """
    Página base
    """
    def __init__(self) -> None:
        self.console = Console()
        self.utils = Utils()