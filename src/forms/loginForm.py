import re
import time
from typing import Callable
from .baseForm import BaseForm
from contract import exceptions
from restRepositories.soilsense import SessionRestRepository
import contract
from rich.status import Status

class LoginForm(BaseForm):
    """
    Formulário de Login
    """
    def __init__(self, sessionRestRepository:SessionRestRepository) -> None:
        super().__init__()
        self._sessionRestRepository:SessionRestRepository = sessionRestRepository
        self.email:str = None
        self.username:str = None
        self.password:str = None
        self.access_token:str = None
    
    def run(self, clear:Callable):
        try:
            self.setCredentials()
            order = contract.Order('Autenticando usuário...')
            (order
             .add(*[contract.Waiter(task=self.fetchSignIn, label='Autenticando usuário')])
             .start()
             .then(success='Usuário autenticado com sucesso')
            )
            time.sleep(2)
        except exceptions.InvalidValue:
            clear()
            self.console.print('\nE-mail ou senha incorretos\n', style='#F47174 bold')
            self.run(clear)
        except:
            clear()
            self.console.print('\nHouve um erro não tratado, por favor reinicie o programa e tente novamente\n', style='#F47174 bold')
        finally:
            prev_email = self.email
            self.__init__(sessionRestRepository=self._sessionRestRepository)
            self.email = prev_email
        pass

    def setCredentials(self):
        self.console.set_window_title('SoilSense - Entrar')
        self.console.print('Entrar', style="#ffffff bold")
        self.setEmailAddress()
        self.setPassword()
        pass

    def setUser(self):
        username = self.console.input('Nome de usuário: ')
        match = re.search('^[A-Za-z][A-Za-z0-9_]{7,29}$', username)

        if match is None:
            raise exceptions.InvalidValue('Nome de usuário inválido')
            
        self.username = username
        pass

    def setEmailAddress(self):
        email:str = None
        if self.email is None:
            email = self.console.input(f'Endereço de e-mail: ')
        else:
            email = self.console.input(f'Endereço de e-mail ({self.email}):')
            if (email is None or email is ''):
                email = self.email
                # self.console.print(f'E-mail que será utilizado: {email}')
        match = re.search('^[a-zA-Z0-9._%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email)

        if match is None:
            raise exceptions.InvalidValue('E-mail inválido')
            
        self.email = email
        pass

    def setPassword(self):
        password = self.console.input('Senha: ', password=True)
        self.password = password
        pass

    def fetchSignIn(self, status:Status, task:contract.Waiter):
        r = self._sessionRestRepository.signIn(email=self.email, password=self.password)

        if r.success == False:
            task.complete = 'Não foi possivel autenticar o usuário'
            raise exceptions.InvalidValue('Usuário não autenticado')

        task.complete = 'Autenticação completa'
        self.access_token = r.access_token
        pass