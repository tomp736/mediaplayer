from typing import Dict, List
import requests
from pymp_common.services.ConfigService import ConfigService

class FeApiService:
        
    feapi_host = ConfigService.feapi_host
    feapi_port = ConfigService.feapi_port
    
    @staticmethod
    def get_thumb_url(id: str) -> str:
        return f"http://{FeApiService.feapi_host}:{FeApiService.feapi_port}/thumb/{id}"
    
    @staticmethod
    def get_meta_url(id: str) -> str:
        return f"http://{FeApiService.feapi_host}:{FeApiService.feapi_port}/meta/{id}"
        
    @staticmethod
    def get_media_url(id: str) -> str:
        return f"http://{FeApiService.feapi_host}:{FeApiService.feapi_port}/media/{id}"
    
    @staticmethod
    def get_media_list_url() -> str:
        return f"http://{FeApiService.feapi_host}:{FeApiService.feapi_port}/media/list"
    
    @staticmethod
    def get_media_index_url() -> str:
        return f"http://{FeApiService.feapi_host}:{FeApiService.feapi_port}/media/index"
    
    @staticmethod
    def get_thumb(id) -> str:
        thumbUrl = FeApiService.get_thumb_url(id)
        response = requests.get(thumbUrl)
        return response.text
    
    @staticmethod
    def get_meta(id) -> Dict[str, str]:
        metaUrl = FeApiService.get_meta_url(id)
        response = requests.get(metaUrl)
        metadictionary = response.json()
        return metadictionary
    
    @staticmethod
    def get_media_list() -> List[str]:
        url = FeApiService.get_media_list_url()
        response = requests.get(url)
        list = response.json()
        return list
    
class ThumbService:
        
    thumb_host = ConfigService.thumb_host
    thumb_port = ConfigService.thumb_port
    
    # thumbs
    @staticmethod
    def get_thumb_url(id: str) -> str:
        return f"http://{ThumbService.thumb_host}:{ThumbService.thumb_port}/thumb/{id}"
    
    @staticmethod
    def get_thumb_check_url(id: str) -> str:
        return f"http://{ThumbService.thumb_host}:{ThumbService.thumb_port}/thumb/check/{id}"
    
    @staticmethod
    def get_thumb(id) -> str:
        thumbUrl = ThumbService.get_thumb_url(id)
        response = requests.get(thumbUrl)
        return response.text
    
class MetaService:
        
    meta_host = ConfigService.meta_host
    meta_port = ConfigService.meta_port
    
    # meta
    @staticmethod
    def get_meta_url(id: str) -> str:
        return f"http://{MetaService.meta_host}:{MetaService.meta_port}/meta/{id}"
    
    @staticmethod
    def get_meta_check_url(id: str) -> str:
        return f"http://{MetaService.meta_host}:{MetaService.meta_port}/meta/check/{id}"
    
    @staticmethod
    def get_meta(id) -> Dict[str, str]:
        metaUrl = MetaService.get_meta_url(id)
        response = requests.get(metaUrl)
        metadictionary = response.json()
        return metadictionary

    
class MediaService:
        
    media_host = ConfigService.media_host
    media_port = ConfigService.media_port
        
    @staticmethod
    def get_media_url(id: str) -> str:
        return f"http://{MediaService.media_host}:{MediaService.media_port}/media/{id}"
    
    @staticmethod
    def get_media_list_url() -> str:
        return f"http://{MediaService.media_host}:{MediaService.media_port}/media/list"
    
    @staticmethod
    def get_media_index_url() -> str:
        return f"http://{MediaService.media_host}:{MediaService.media_port}/media/index"
    
    @staticmethod
    def get_media_index():
        url = MediaService.get_media_index_url()
        requests.get(url)
    
    @staticmethod
    def get_media_list() -> List[str]:
        url = MediaService.get_media_list_url()
        response = requests.get(url)
        list = response.json()
        return list
