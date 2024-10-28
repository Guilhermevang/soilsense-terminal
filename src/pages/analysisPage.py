import time
from typing import Callable

import inquirer
from restRepositories.soilsense import FeaturesRestRepository
from models import UserModel
from .basePage import BasePage
from rich.table import Table
from rich.live import Live
from contract import exceptions



class AnalysisPage(BasePage):
    """
    Página de análise/métricas de talhões
    """
    def __init__(self, featuresRestRepository:FeaturesRestRepository) -> None:
        super().__init__()
        self._featuresRestRepository:FeaturesRestRepository = featuresRestRepository
        self.features:list[dict] = []
        self.selected_feature:str = None
        self.selected_process_types:list[str] = None

    def run(self, clear:Callable) -> None:
        self.list_user_features()

        options = [
            inquirer.List(
                'selected_feature',
                message='Escolha um talhão para processar',
                choices=[feature['feature_hash'] for feature in self.features]
            ),
            inquirer.Checkbox(
                'selected_process_types',
                message='Selecione os dados você gostaria de obter (espaço)',
                choices=[
                    ('Visão de satélite', 'TRUE_COLOR'),
                    ('NDVI (Saúde das plantas)', 'NDVI'),
                    ('NDVI em preto e branco', 'BLACK_AND_WHITE_NDVI'),
                    ('Falsa cor', 'FALSE_COLOR')
                ]
            )
        ]

        r = inquirer.prompt(options)
        self.selected_feature = r['selected_feature']
        self.selected_process_types = r['selected_process_types']

        self.console.print(f'Você escolheu o talhão (HASH) "{self.selected_feature}"')
        self.console.print(f'Você escolheu o obter os seguintes dados: "{self.selected_process_types}"')

        self.start_processing_image()
        self.fetch_processing_results()

        time.sleep(5)

    def list_user_features(self) -> None:
        try:
            r = self._featuresRestRepository.list_user_features(authorization=UserModel._access_token)
            self.features = r
        except:
            return
        
    def start_processing_image(self):
        try:
            if self.selected_process_types is None or self.selected_feature is None:
                raise exceptions.InvalidValue('Nenhuma HASH ou tipo de processamento foi fornecido.')
            
            content = {
                'feature_hash': self.selected_feature,
                'image_processing_type': self.selected_process_types
            }

            self._featuresRestRepository.start_processing_image(authorization=UserModel._access_token)
        except:
            return
    
    def fetch_processing_results(self):
        return