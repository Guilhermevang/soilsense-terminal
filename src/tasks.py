from rich.status import Status
# import requests
# import json
import contract


class Tasks:
    def fetchSatellitesTLE(status:Status, task:contract.Waiter, page=1):
        # res = requests.get(
        #     url="https://tle.ivanstanojevic.me/api/tle",
        #     params={
        #         "page": page,
        #         "page-size": 9
        #     }
        # )
        # response = json.loads(res.text)
        # task.complete = f"{response['totalItems']} satélites encontrados";
        task.complete = f"1546 satélites encontrados";
        # status.update(f"A tarefa está demorando mais que o esperado...", spinner="simpleDots")
        return