import re
import time
from typing import Callable, Tuple
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
        self.username       :str = None
        self.password       :str = None
    
    def run(self, clear:Callable):
        try:
            self.setCredentials()
            order = contract.Order('Autenticando usuário...')
            (order
             .add(*[contract.Waiter(task=self.fetchSignIn, label='Autenticando usuário')])
             .start()
             .then(success='Usuário autenticado com sucesso')
            )
            time.sleep(1)
        except exceptions.InvalidValue:
            clear()
            self.console.print('\nE-mail ou senha incorretos\n', style='#F47174 bold')
            self.run(clear)
        except:
            clear()
            self.console.print('\nHouve um erro não tratado, por favor reinicie o programa e tente novamente\n', style='#F47174 bold')
            raise
        finally:
            prev_email = UserModel._email
            self.__init__(sessionRestRepository=self._sessionRestRepository)
            UserModel._email = prev_email
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
        if UserModel._email is None:
            email = self.console.input(f'Endereço de e-mail: ')
        else:
            email = self.console.input(f'Endereço de e-mail ({UserModel._email}):')
            if (email is None or email is ''):
                email = UserModel._email
                # self.console.print(f'E-mail que será utilizado: {email}')
        match = re.search('^[a-zA-Z0-9._%±]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', email)

        if match is None:
            raise exceptions.InvalidValue('E-mail inválido')
            
        UserModel._email = email
        pass

    def setPassword(self):
        password = self.console.input('Senha: ', password=True)
        self.password = password
        pass

    def fetchSignIn(self, status:Status, task:contract.Waiter):
        r = self._sessionRestRepository.signIn(email=UserModel._email, password=self.password)

        if r.success == False:
            task.complete = 'Não foi possivel autenticar o usuário'
            raise exceptions.InvalidValue('Usuário não autenticado')

        task.complete = 'Autenticação completa'
        UserModel._access_token = r.access_token
        UserModel._active = True
        pass