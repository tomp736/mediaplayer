
from typing import Dict, Union
import requests
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.http_request_factory import media_registry_request_factory


class MediaRegistryProviderRemote(MediaRegistryProvider):
    
    def register_(self, serviceinfo: Dict):
        self.register(serviceinfo["id"],
                      serviceinfo["scheme"],
                      serviceinfo["host"],
                      serviceinfo["port"])
    
    def register(self, id, scheme, host, port):
        registerRequest = media_registry_request_factory.register(
            id,
            scheme,
            host,
            port
        )
        s = requests.Session()
        return s.send(registerRequest.prepare()) 
    
    def registerMedia(self, mediaId, serviceId):
        registerRequest = media_registry_request_factory.register_media(
            mediaId,
            serviceId
        )
        s = requests.Session()
        return s.send(registerRequest.prepare())   
    
    def remove(self, serviceId: str) -> Union[int, None]:
        pass
    
    def removeMedia(self, mediaId: str) -> bool:
        return False
    
    def getMediaIndex(self) -> Union[Dict[str, str], None]:
        pass
    
    def getMediaServices(self) -> Union[Dict[str, str], None]:
        pass
    
    def getMediaService(self, mediaId: str) -> Union[str, None]:
        pass