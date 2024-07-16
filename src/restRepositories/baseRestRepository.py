import json
import requests
from contract import exceptions

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
    
    def get(self, route:str='', params:dict={}) -> BaseRestResponse:
        """
        Método GET
        """
        try:
            res = requests.get(
                url=f"{self.BASE_URL}/{route}",
                params=params,
                verify=False # NÃO RECOMENDADO...
            )
            response = json.loads(res.text)
            return self.BaseRestResponse(**response)
        except:
            raise exceptions.RestException('[ERROR] GET: Houve um erro')
        
    def post(self, route:str='', body:dict={}) -> BaseRestResponse:
        """
        Método POST
        """
        try:
            res = requests.post(
                url=f"{self.BASE_URL}/{route}",
                json=body,
                verify=False
            )
            response = json.loads(res.text)
            return self.BaseRestResponse(**response)
        except:
            raise exceptions.RestException('[ERROR] POST: Houve um erro')