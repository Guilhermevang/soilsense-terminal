import time
from typing import Callable

import inquirer
from restRepositories.soilsense import FeaturesRestRepository
from models import UserModel
from .basePage import BasePage
from rich.table import Table
from rich.live import Live



class ListFeaturesPage(BasePage):
    """
    Página de busca de talhões
    """
    def __init__(self, featuresRestRepository:FeaturesRestRepository) -> None:
        super().__init__()
        self._featuresRestRepository:FeaturesRestRepository = featuresRestRepository
        self.features:list[dict] = []
        self.page_limit:int = 1
        self.page = 1
        self.table_settings = {
            'title': f'Meus talhões',
            'title_justify': "center",
            'expand': True
        }
        self.table = Table(**self.table_settings)

    def run(self, clear:Callable) -> None:
        self.table.add_column('ID', justify="left", no_wrap=True, style="green")
        self.table.add_column('HASH', justify="left", no_wrap=True, style="white")
        
        self.list_user_features()

        with Live(self.table, auto_refresh=False) as live:
            pages_range = range(int(len(self.features) / self.page_limit))
            for page_index in pages_range:
                self.page = page_index+1
                self.fill_table()
                live.refresh()
                # self.table = Table(**self.table_settings)
                time.sleep(.5)

        # self.console.print(table)

        time.sleep(10)

    def fill_table(self) -> None:
        start_index:int = (self.page - 1) * self.page_limit
        final_index:int = self.page * self.page_limit

        for feature in self.features[start_index:final_index]:
            # if table.row_count == self.page_limit: break
            feature_id:int = feature['id']
            feature_hash:int = feature['feature_hash']
            # print(feature_id, '|', feature_hash)
            self.table.add_row(str(feature_id), str(feature_hash))

    def list_user_features(self) -> None:
        try:
            r = self._featuresRestRepository.list_user_features(authorization=UserModel._access_token)
            self.features = r
        except:
            return