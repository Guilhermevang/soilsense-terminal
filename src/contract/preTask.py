import typing


class PreTask:
    def __init__(self, task:typing.Callable, label:str):
        self.execute = task
        self.loading = label
        self.complete = None
        self.spinner = "simpleDots"