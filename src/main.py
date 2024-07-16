import os
import time
from typing import Callable
from rich import pretty
from restRepositories.soilsense import FeaturesRestRepository, SessionRestRepository
import utils
import forms
from dotenv import load_dotenv
import urllib3
from models import UserModel
from rich import print
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
        if not UserModel._active:
            authForm = forms.LoginForm(sessionRestRepository=self.sessionRestRepository)
            self.window.run(authForm.run)

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

        def modeSelector(clear:Callable):
            r = inquirer.prompt(options)
            Main._mode = r['mode']

        self.window.run(modeSelector)

        match self._mode:
            case 'new':
                fieldForm = forms.FieldForm(featuresRestRepository=self.featuresRestRepository)
                self.window.run(fieldForm.run)
                self.run()
            case 'analysis':
                self.run()
                pass
            case 'logoff':
                UserModel._active = False
                pass

if __name__ == '__main__':
    default_email_address = os.getenv('DEFAULT_EMAIL')
    if default_email_address is not None:
        UserModel._email = default_email_address

    Main(
        featuresRestRepository=FeaturesRestRepository(base_url=os.getenv('API_SOILSENSE__BASE_URL')),
        sessionRestRepository=SessionRestRepository(base_url=os.getenv('API_SOILSENSE__BASE_URL'))
    ).login()