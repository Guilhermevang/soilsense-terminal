import json
import time
from ..baseRestRepository import BaseRestRepository
from contract import exceptions

class SignInResponse:
    def __init__(self, access_token:str, success:bool, errors:list[str]):
        self.access_token:str = access_token
        self.success:bool = success
        self.errors:list[str] = errors

class SessionRestRepository(BaseRestRepository):
    """
    Esse repositório REST fará requisições à API SoilSense (interna) na rota /v1/Session
    """
    def __init__(self, base_url:str='') -> None:
        super().__init__(base_url=base_url)


    def signIn(self, email:str, password:str):
        """
        Realiza o Login
        """
        try:
            r = self.post('v1/session/sign-in', body={
                'email': email,
                'password': password
            })

            signInResponse = SignInResponse(**r.Data)
            return signInResponse
        except exceptions.RestException:
            print('Houve um erro REST')