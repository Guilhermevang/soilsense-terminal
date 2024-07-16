from ..baseRestRepository import BaseRestRepository

class FeaturesRestRepository(BaseRestRepository):
    """
    Esse repositório REST fará requisições à API SoilSense (interna) na rota /v1/Features
    """
    def __init__(self, base_url:str='') -> None:
        super().__init__(base_url=base_url)

    def checkFeatureFromHash(self, hash:str) -> bool:
        """
        Verifica se Feature já está salva com base no HASH calculado
        """
        r = self.get('v1/Features/check', params={
            'hash': hash,
        })

        if r.Data == True:
            return True

        return False
    
    def insertFeatures(self, feature_collection):
        """
        Insere uma coleção de Features
        """
        r = self.post('v1/Features', body=feature_collection)

        if r.Success and r.Data:
            return True
        
        return False