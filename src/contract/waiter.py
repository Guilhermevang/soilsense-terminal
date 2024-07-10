import typing


class Waiter:
    def __init__(self, task:typing.Callable, label:str):
        self.task = task
        self.loading = label
        self.complete = None
        self.spinner = "simpleDots"

    def execute(self, *kwargs):
        return self.task(*kwargs)