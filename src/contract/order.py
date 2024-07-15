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
        self.failed:bool = False

    def add(self, *tasks):
        if tasks.count == 1:
            self.tasks.append(*tasks)
        else:
            self.tasks.extend(tasks)
        return self
    
    def remove(self, index:int=0) -> contract.Waiter:
        return self.tasks.pop(index)

    def start(self):
        # try:
        with self.console.status(self.colored_label, spinner=self.spinner) as status:
            while self.tasks:
                task = self.remove()
                status.update(f"{task.loading}", spinner=task.spinner)
                task.execute(status, task)
                self.console.log(task.complete)
        #     self.failed = False
        # except:
        #     self.failed = True
        # finally:
        return self
    
    def then(self, success:str="Pronto", failure:str="A execução falhou"):
        if self.failed:
            self.console.log(failure, style="#F47174 bold")
        else:
            self.console.log(success, style="#ACD1AF bold")