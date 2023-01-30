
from typing import Dict, Union
import requests
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.http_request_factory import media_registry_request_factory
from pymp_common.dataaccess.redis import media_source_da

class MediaRegistryProviderRemote(MediaRegistryProvider):
    
    def register_(self, serviceinfo: Dict):
        self.register(serviceinfo["id"],
                      serviceinfo["scheme"],
                      serviceinfo["host"],
                      serviceinfo["port"])
    
    def register(self, id, scheme, host, port):
        registeryRequest = media_registry_request_factory.register(
            id,
            scheme,
            host,
            port
        )
        s = requests.Session()
        return s.send(registeryRequest.prepare()) 
    
    def registerMedia(self, mediaId, serviceId):
        registeryRequest = media_registry_request_factory.register_media(
            mediaId,
            serviceId
        )
        s = requests.Session()
        return s.send(registeryRequest.prepare())   
    
    def getMediaIndex(self) -> Union[Dict[str, str], None]:
        registeryRequest = media_registry_request_factory.list_media()
        s = requests.Session()
        resistryResponse = s.send(registeryRequest.prepare())         
        return resistryResponse.json()
    
    def remove(self, serviceId: str) -> Union[int, None]:
        raise Exception("NOT SUPPORTED")
    
    def removeMedia(self, mediaId: str) -> bool:
        raise Exception("NOT SUPPORTED")
    
    # TODO - VALIDATE CLIENT ACCESS TO REDIS
    def getMediaServices(self) -> Union[Dict[str, str], None]:
        return media_source_da.hgetall()
    
    # TODO - VALIDATE CLIENT ACCESS TO REDIS
    def getMediaService(self, mediaId: str) -> Union[str, None]:
        return media_source_da.hget(mediaId)