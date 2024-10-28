import re
import json
import os
import time
from typing import Callable, Literal

import inquirer

from restRepositories.soilsense import FeaturesRestRepository
from .baseForm import BaseForm
import contract
from rich.status import Status
from rich.progress import Progress
from models import UserModel


class InsertFeaturesForm(BaseForm):
    """
    Formulário de inserção de talhão
    """
    def __init__(self, featuresRestRepository:FeaturesRestRepository) -> None:
        super().__init__()
        self._featuresRestRepository:FeaturesRestRepository = featuresRestRepository
        
        self.file_path          :str = None
        self.file_content       :str | any = None
        self.hash               :str = None
        self.feature_type       :Literal['Feature', 'FeatureCollection'] = None
        self.features           :list[any] = []
        self.pending_features   :list[any] = []
    
    def run(self, clear:Callable):
        self.run_form()

        tasks = [
            contract.Waiter(task=self.set_file_content, label='Extraindo dados do arquivo'),
            contract.Waiter(task=self.check_for_type, label='Verificando tipo da coleção'),
            contract.Waiter(task=self.check_for_features, label='Verificando existência das features'),
            contract.Waiter(task=self.insert_pending_features, label='Inserindo talhões pendentes'),
        ]

        order = contract.Order('Validando dados do talhão...')
        order.add(*tasks).start().then()

        time.sleep(2)
        
        pass

    def run_form(self) -> None:
        form = [
            inquirer.Text('file_path', message='Arraste o arquivo (GEOJson) ou insira o caminho completo', validate=self.file_path_verification)
        ]

        answers = inquirer.prompt(form)

        self.file_path = re.sub(r'(^\"|\"$)', '', answers['file_path'].strip())
        self.console.print(f'Endereço do arquivo (talhão): {self.file_path}')

    def file_path_verification(self, answers, current) -> bool:
        current = re.sub(r'(^\"|\"$)', '', current.strip())
        if not re.match(r'^.+\.\w+$', current):
            raise inquirer.errors.ValidationError('', reason='Caminho inválido')

        return True
    
    def set_file_content(self, status:Status, task:contract.Waiter):
        self.file_content = self.utils.readJsonFile(self.file_path)
        task.complete = 'Dados do arquivo extraídos com sucesso'
        time.sleep(1)
        pass

    def check_for_type(self, status:Status, task:contract.Waiter):
        # Se não possuir conteudo no arquivo -> gerar erro
        if len(self.file_content) <= 0:
            raise Exception('O arquivo possívelmente se encontra nulo')
        
        self.feature_type = self.file_content['type']
        task.complete = f'Tipo: {self.feature_type}'
        time.sleep(1)
        pass

    def check_for_features(self, status:Status, task:contract.Waiter):
        """
        Itera por todos talhões e verifica quais já estão salvos, assim como os pendentes
        """
        # Cria uma lista com as Features
        if self.feature_type == 'FeatureCollection':
            self.features = self.file_content['features']
        else:
            self.features = [self.file_content]

        # Armazena o número total de -> features, features que já estão salvas no AWS S3, além dos talhões que deverão ser salvos
        total_features  :int = len(self.features)
        total_saved     :int = 0

        for (index, feature) in enumerate(self.features):
            # Calcula o HASH do talhão com base nas coordenadas
            self.calculate_hash(index)

            # Verifica se talhão existe requisitando API passando o HASH calculado
            feature_exists:bool = self.check_feature_from_hash()

            # Se existir incrementa os talhões salvos, se não, adiciona talhão na lista de pendências
            if feature_exists:
                total_saved += 1
            else:
                self.pending_features.append(feature)

            task.loading = f'{index+1} de {total_features} talhões verificados'
            status.update(task.loading)
            
        # Atualiza o texto
        task.complete = f'{total_saved} de {total_features} talhões já existem'
        pass

    def calculate_hash(self, feature_index:int):
        """
        Calcula o HASH de acordo com as coordenadas do talhão
        """
        self.hash = self.utils.calculateHash(json.dumps(self.features[feature_index]['geometry']['coordinates'][0], indent=None, separators=(',', ':')))
        pass

    def check_feature_from_hash(self) -> bool:
        if len(self.hash) <= 0:
            raise Exception('HASH vazio')
        
        r:bool = self._featuresRestRepository.check_feature_from_hash(self.hash, authorization=UserModel._access_token)
        return r
    
    def insert_pending_features(self, status:Status, task:contract.Waiter):
        if len(self.pending_features) == 0:
            task.complete = 'Não há talhões para inserir'
            return

        properties = self.file_content['properties'] if 'properties' in self.file_content else None
        if self.feature_type == 'Feature':
            properties = None

        feature_collection = {
            'type': 'FeatureCollection',
            'features': self.pending_features,
            'properties': properties
        }

        # Inserir as Features pendentes
        r:bool = self._featuresRestRepository.insert_features(feature_collection, authorization=UserModel._access_token)
        if r == True:
            task.complete = 'Talhões pendentes inseridos com sucesso'
        else:
            task.complete = 'Não foi possivel inserir os talhões pendentes'