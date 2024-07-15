import json
import requests

class BaseRestRepository:
    """
    Esse será o repositorio BASE
    """
    def __init__(self, base_url:str='') -> None:
        self.BASE_URL = base_url

    class BaseRestResponse:
        def __init__(self, Data, Code, Success, DataAsString) -> None:
            self.Data:any = Data
            self.Code:int = Code
            self.Success:bool = Success
            self.DataAsString:str = DataAsString
    
    def get(self, url:str='', params:dict={}) -> BaseRestResponse:
        """
        Método GET
        """
        try:
            res = requests.get(
                url=f"{self.BASE_URL}/{url}",
                params=params,
                verify=False # NÃO RECOMENDADO...
            )
            response = json.loads(res.text)
            return self.BaseRestResponse(**response)
        except:
            raise Exception('[ERROR] GET: Houve um erro')
        
    def post(self, url:str='', body:dict={}) -> BaseRestResponse:
        """
        Método POST
        """
        try:
            res = requests.post(
                url=f"{self.BASE_URL}/{url}",
                json=body,
                verify=False
            )
            response = json.loads(res.text)
            return self.BaseRestResponse(**response)
        except:
            raise Exception('[ERROR] POST: Houve um erro')