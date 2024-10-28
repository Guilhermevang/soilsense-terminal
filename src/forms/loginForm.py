import re
import time
from typing import Callable, Tuple

import inquirer
import inquirer.errors
from .baseForm import BaseForm
from contract import exceptions
from restRepositories.soilsense import SessionRestRepository
import contract
from rich.status import Status
from models import UserModel

class LoginForm(BaseForm):
    """
    Formulário de Login
    """
    def __init__(self, sessionRestRepository:SessionRestRepository) -> None:
        super().__init__()
        self._sessionRestRepository:SessionRestRepository = sessionRestRepository
        self.password:str = None
    
    def run(self, clear:Callable):
        try:
            self.run_form()

            order = contract.Order('Autenticando usuário...')
            (order
             .add(*[contract.Waiter(task=self.fetch_sign_in, label='Autenticando usuário')])
             .start()
             .then(success='Usuário autenticado com sucesso!', failure='Não foi possível autenticar o usuário.')
            )

            time.sleep(1)

            if order.failed:
                clear()
                self.run(clear)
        except:
            clear()
            self.console.print('\nHouve um erro não tratado, por favor reinicie o programa e tente novamente\n', style='#F47174 bold')
            raise
        pass

    def run_form(self):
        self.console.set_window_title('SoilSense - Entrar')
        self.console.print('Entrar', style="#ffffff bold")

        form = [
            inquirer.Text(
                'email',
                message='E-mail',
                default=UserModel._email,
                autocomplete=['@gmail.com', '@hotmail.com', '@outlook.com'],
                validate=self.email_validation
            ),
            inquirer.Password(
                'password',
                message='Senha',
                echo='*'
            ),
            inquirer.Checkbox(
                'keep-session-alive',
                message='Pressione espaço para continuar conectado',
                choices=[('Manter conectado?', True)]
            )
        ]

        answers = inquirer.prompt(form)

        UserModel._email = answers['email'].strip()
        UserModel._keep_alive = True if len(answers['keep-session-alive']) is 1 else False
        self.password = answers['password']
        pass

    def email_validation(self, answers, current):
        if not re.match(r'^[a-zA-Z0-9._%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', current.strip()):
            raise inquirer.errors.ValidationError('', reason='E-mail inválido')
        
        return True

    def fetch_sign_in(self, status:Status, task:contract.Waiter):
        r = self._sessionRestRepository.signIn(email=UserModel._email, password=self.password)

        if r.success == False:
            task.complete = 'Não foi possivel autenticar o usuário'
            raise exceptions.InvalidValue('Usuário não autenticado')

        task.complete = 'Autenticação completa'
        UserModel._access_token = r.access_token
        UserModel._active = True
        if UserModel._keep_alive == True:
            UserModel().keep_session_alive()
        pass