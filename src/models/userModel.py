import json
import time
import jwt
from utils import Utils

class UserModel:
    _email          :str = None
    _access_token   :str = None
    _active         :bool = False
    _keep_alive     :bool = False
        
    def __init__(self) -> None:
        self.email          :str = UserModel._email
        self.access_token   :str = UserModel._access_token
        self.active         :bool = UserModel._active
        self.keep_alive     :bool = UserModel._keep_alive
        self.utils = Utils()

    def keep_session_alive(self, keep_alive:bool=True) -> None:
        self.keep_alive = UserModel._keep_alive = keep_alive
        
        if not keep_alive:
            self.unset_session()
            return

        self.write_session_file()

    def write_session_file(self) -> None:
        dictionary = {
            'email': self.email,
            'access_token': self.access_token
        }

        json_dictonary = json.dumps(dictionary, indent=4)
        with open('session.json', 'w', encoding='utf8') as outfile:
            outfile.write(json_dictonary)

    def set_session_from_file(self) -> None:
        try:
            self.active = UserModel._active = False
            path:str = 'session.json'
            json_dictionary = self.utils.readJsonFile(path=path)
            self.email = UserModel._email = json_dictionary['email']
            self.access_token = UserModel._access_token = json_dictionary['access_token']
            if not self.access_token:
                return
            self.check_token_expiration()
            self.active = UserModel._active = True
        except FileNotFoundError:
            return
        except:
            raise

    def check_token_expiration(self) -> None:
        try:
            jwt.get_unverified_header(self.access_token)
        except jwt.ExpiredSignatureError:
            self.access_token = UserModel._access_token = None
            self.write_session_file()
            raise
        except:
            self.access_token = UserModel._access_token = None
            self.write_session_file()
            raise Exception('Houve um erro ao decodificar a chave de acesso')
        
    def unset_session(self) -> None:
        self.access_token   = UserModel._access_token   = None
        self.active         = UserModel._active         = False
        self.keep_alive     = UserModel._keep_alive     = False
        self.write_session_file()