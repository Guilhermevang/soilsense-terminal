import json
import time
import requests
from urllib3 import HTTPResponse
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
    
    def get(self, route:str='', params:dict={}, headers:dict={}, authorization:str=None) -> BaseRestResponse:
        """
        Método GET
        """
        try:
            if authorization is not None:
                headers['Authorization'] = f'Bearer {authorization}'

            res = requests.get(
                url=f"{self.BASE_URL}/{route}",
                params=params,
                verify=False, # NÃO RECOMENDADO...
                headers=headers
            )
            # print(f'BaseRestRepository [GET] -> Resposta crua: {res.__dict__}')
            # time.sleep(10)
            if hasattr(res, 'text'):
                response = json.loads(res.text)
                return self.BaseRestResponse(**response)
            else:
                data = res.reason if 'reason' in res else None
                response = self.BaseRestResponse(Data=data, Code=res.status_code, Success=None, DataAsString=None)
                return response
        except:
            raise exceptions.RestException('[ERROR] GET: Houve um erro')
        
    def post(self, route:str='', body:dict={}, headers:dict={}, authorization:str=None) -> BaseRestResponse:
        """
        Método POST
        """
        try:
            if authorization is not None:
                headers['Authorization'] = f'Bearer {authorization}'

            res = requests.post(
                url=f"{self.BASE_URL}/{route}",
                json=body,
                verify=False, # NÃO RECOMENDADO...
                headers=headers
            )
            # print(f'BaseRestRepository [GET] -> Resposta crua: {res.__dict__}')
            # time.sleep(10)
            if hasattr(res, 'text'):
                response = json.loads(res.text)
                return self.BaseRestResponse(**response)
            else:
                data = res.reason if 'reason' in res else None
                response = self.BaseRestResponse(Data=data, Code=res.status_code, Success=None, DataAsString=None)
                return response
        except:
            raise exceptions.RestException('[ERROR] POST: Houve um erro')