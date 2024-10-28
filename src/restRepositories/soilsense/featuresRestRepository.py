from ..baseRestRepository import BaseRestRepository
from contract import exceptions

class FeaturesRestRepository(BaseRestRepository):
    """
    Esse repositório REST fará requisições à API SoilSense (interna) na rota /v1/Features
    """
    def __init__(self, base_url:str='') -> None:
        super().__init__(base_url=base_url)

    def check_feature_from_hash(self, hash:str, authorization:str=None) -> bool:
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
    
    def insert_features(self, feature_collection, authorization:str=None):
        """
        Insere uma coleção de Features
        """
        r = self.post('v1/Features', body=feature_collection, authorization=authorization)

        if r.Success and r.Data:
            return True
        
        return False

    def list_user_features(self, authorization:str=None) -> list[dict]:
        """
        Busca todas as Features do usuário autenticado
        """
        r = self.get('v1/Features/list', authorization=authorization)

        if r.Code is 200:
            return r.Data
        
        raise exceptions.CommonBaseException('Houve um erro não tratado')
    
    def start_processing_image(self, body:dict, authorization:str=None) -> dict:
        """
        Inicia o processamento da imagem (do talhão)

        Retorno: { 'folder': 'str' }
        """
        r = self.post('v1/Process', authorization=authorization)

        if r.Code is 200:
            return {
                'folder': r.Data
            }
        
        raise exceptions.CommonBaseException('Houve um erro não tratado')

    def fetch_processing_result(self, guid_folder:str, image_names:list[str], authorization:str=None):
        """
        Busca o resultado do processamento do talhão

        Retorno: None
        """
        search_params = {
            'folder': guid_folder,
            'images': image_names
        }
        
        r = self.get('v1/Process', params=search_params, authorization=authorization)

        if r.Code is 200:
            return r.Data
        
        raise exceptions.CommonBaseException('Houve um erro não tratado')