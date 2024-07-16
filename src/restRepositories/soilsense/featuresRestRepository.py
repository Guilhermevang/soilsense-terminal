from ..baseRestRepository import BaseRestRepository
from contract import exceptions

class FeaturesRestRepository(BaseRestRepository):
    """
    Esse repositório REST fará requisições à API SoilSense (interna) na rota /v1/Features
    """
    def __init__(self, base_url:str='') -> None:
        super().__init__(base_url=base_url)

    def checkFeatureFromHash(self, hash:str, authorization:str=None) -> bool:
        """
        Verifica se Feature já está salva com base no HASH calculado
        """
        r = self.get('v1/Features/check', params={
            'hash': hash,
        }, authorization=authorization)

        if r.Code is 200:
            return r.Data
            
        match r.Code:
            case 401:
                raise exceptions.NotAuthorized(r.Data if r.Data is not None else 'Autorização necessária')
            case _:
                raise exceptions.CommonBaseException('Houve um erro não tratado')
    
    def insertFeatures(self, feature_collection):
        """
        Insere uma coleção de Features
        """
        r = self.post('v1/Features', body=feature_collection)

        if r.Success and r.Data:
            return True
        
        return False