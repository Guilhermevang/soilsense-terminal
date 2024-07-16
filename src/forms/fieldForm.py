import re
import json
import os
import time
from typing import Callable, Literal

from restRepositories.soilsense import FeaturesRestRepository
from .baseForm import BaseForm
import contract
from rich.status import Status


class FieldForm(BaseForm):
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
        self.getFieldFile()

        tasks = [
            contract.Waiter(task=self.setFileContent, label='Extraindo dados do arquivo'),
            # contract.Waiter(task=self.calculateHash, label='Calculando HASH do arquivo com base nas coordenadas'),
            contract.Waiter(task=self.checkForType, label='Verificando tipo da coleção'),
            contract.Waiter(task=self.checkForFeatures, label='Verificando existência das features'),
            contract.Waiter(task=self.insertPendingFeatures, label='Inserindo talhões pendentes'),
        ]

        order = contract.Order('Validando dados do talhão...')
        order.add(*tasks).start().then()
        pass

    def getFieldFile(self):
        value = self.console.input('Arraste o arquivo do talhão (GEOJson): ')
        value = re.sub('(^\"|\"$)', '', value) # Remove as aspas do inicio e fim
        self.file_path = value
        self.console.print(f'Endereço do arquivo (talhão): {self.file_path}')
        pass
    
    def setFileContent(self, status:Status, task:contract.Waiter):
        self.file_content = self.utils.readJsonFile(self.file_path)
        task.complete = 'Dados do arquivo extraídos com sucesso'
        time.sleep(1)
        pass

    def checkForType(self, status:Status, task:contract.Waiter):
        # Se não possuir conteudo no arquivo -> gerar erro
        if len(self.file_content) <= 0:
            raise Exception('O arquivo possívelmente se encontra nulo')
        
        self.feature_type = self.file_content['type']
        task.complete = f'Tipo: {self.feature_type}'
        time.sleep(1)
        pass

    def checkForFeatures(self, status:Status, task:contract.Waiter):
        # Cria uma lista com as Features
        if self.feature_type == 'FeatureCollection':
            self.features = self.file_content['features']
        else:
            self.features = [self.file_content]

        # Armazena o número total de -> features, features que já estão salvas no AWS S3, além dos talhões que deverão ser salvos
        total_features  :int = len(self.features)
        total_saved     :int = 0
        
        for (index, feature) in enumerate(self.features):
            self.calculateHash(index)
            feature_exists:bool = self.checkFeatureFromHash()

            # Se existir incrementa no número de Features salvas, caso contrário adiciona a Feature ao final da lista de Features pendentes
            if feature_exists:
                total_saved += 1
            else:
                # Atualiza a lista de Features pendentes, apenas os talhões que ainda não foram inseridos
                self.pending_features.append(feature)

            task.loading = f'{index+1}/{total_features} talhões verificados'
            status.update(f"{task.loading}", spinner=task.spinner)
            
        # Atualiza o texto
        task.complete = f'{total_saved}/{total_features} Talhões já existem'
        pass

    def calculateHash(self, feature_index:int):
        """
        Calcula o HASH de acordo com as coordenadas do talhão
        """
        self.hash = self.utils.calculateHash(json.dumps(self.features[feature_index]['geometry']['coordinates'][0], indent=None, separators=(',', ':')))
        pass

    def checkFeatureFromHash(self) -> bool:
        if len(self.hash) <= 0:
            raise Exception('HASH vazio')
        
        r:bool = self._featuresRestRepository.checkFeatureFromHash(self.hash)
        return r
    
    def insertPendingFeatures(self, status:Status, task:contract.Waiter):
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
        r:bool = self._featuresRestRepository.insertFeatures(feature_collection)
        if r == True:
            task.complete = 'Talhões pendentes inseridos com sucesso'
        else:
            task.complete = 'Não foi possivel inserir os talhões pendentes'