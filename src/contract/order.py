from rich.console import Console

import contract

class Order:
    def __init__(
        self,
        label:str="Rodando tarefas",
        color:str="purple bold",
        spinner:str="simpleDots"
    ) -> None:
        self.console = Console()
        self.label = label
        self.color = color
        self.colored_label = f'[{color}]{label}[/{color}]'
        self.spinner = spinner
        self.tasks:list[contract.Waiter] = []

    def add(self, *tasks):
        self.tasks.append(*tasks)
        return self
    
    def remove(self, index:int=0) -> contract.Waiter:
        return self.tasks.pop(index)

    def start(self):
        with self.console.status(self.colored_label, spinner=self.spinner) as status:
            while self.tasks:
                task = self.remove()
                status.update(f"{task.loading}", spinner=task.spinner)
                task.execute(status, task)
                self.console.log(task.complete)
        return self

                # "[purple bold]Iniciando programa...[/purple bold]"
                # "simpleDots"