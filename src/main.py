import os
import time
from typing import Callable
import jwt
from rich import pretty
from restRepositories.soilsense import FeaturesRestRepository, SessionRestRepository
import utils
import forms
from dotenv import load_dotenv
import urllib3
from models import UserModel
import rich
import inquirer


urllib3.disable_warnings()
load_dotenv()
pretty.install()

class Main:
    _mode:str = None
    
    def __init__(
        self,
        featuresRestRepository: FeaturesRestRepository,
        sessionRestRepository: SessionRestRepository,
    ) -> None:
        self.featuresRestRepository:FeaturesRestRepository = featuresRestRepository
        self.sessionRestRepository:SessionRestRepository = sessionRestRepository
        self.window:utils.Window = utils.Window()
    
    def login(self):
        # Inicia uma nova 'janela'
        try:
            UserModel().set_session_from_file()
            if not UserModel._active:
                authForm = forms.LoginForm(sessionRestRepository=self.sessionRestRepository)
                self.window.run(authForm.run)
            else:
                if not UserModel._access_token:
                    UserModel._active = False
                    self.login()
        except jwt.ExpiredSignatureError:
            rich.print('Sessão expirada. Entre novamente.')
            time.sleep(2)
            self.login()
        except:
            rich.print('Houve um erro não tratado ao autenticar o usuário, por favor tente novamente mais tarde.\n')
            time.sleep(2)
            self.login()
            raise

        self.run()

    def run(self):
        options = [
            inquirer.List(
                "mode",
                message="Escolha uma opção",
                choices=[
                    ("Inserir novos talhões", "new"),
                    ("Analisar talhões", "analysis"),
                    ("Sair", "logoff")
                ]
            )
        ]

        def mode_selector(clear:Callable):
            r = inquirer.prompt(options)
            Main._mode = r['mode']

        self.window.run(mode_selector)

        match self._mode:
            case 'new':
                fieldForm = forms.FieldForm(featuresRestRepository=self.featuresRestRepository)
                self.window.run(fieldForm.run)
                self.run()
            case 'analysis':
                self.run()
            case 'logoff':
                UserModel().unset_session()
                self.login()

if __name__ == '__main__':
    default_email_address = os.getenv('DEFAULT_EMAIL')
    if default_email_address is not None:
        UserModel._email = default_email_address

    Main(
        featuresRestRepository=FeaturesRestRepository(base_url=os.getenv('API_SOILSENSE__BASE_URL')),
        sessionRestRepository=SessionRestRepository(base_url=os.getenv('API_SOILSENSE__BASE_URL'))
    ).login()