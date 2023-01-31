
import logging
from typing import Dict
from typing import Union
import requests
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.http_request_factory import media_registry_request_factory
from pymp_common.dataaccess.redis import media_source_da

class MediaRegistryProviderRemote(MediaRegistryProvider):
        
    def __repr__(self) -> str:
        return f"MediaRegistryProviderRemote()"

    def loginfo(self, message):
        logging.info(f"{self.__repr__}{message}")
    
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
    
    def register_media(self, mediaId, serviceId):
        registeryRequest = media_registry_request_factory.register_media(
            mediaId,
            serviceId
        )
        s = requests.Session()
        return s.send(registeryRequest.prepare())   
    
    def get_media_index(self) -> Union[Dict[str, str], None]:
        registeryRequest = media_registry_request_factory.list_media()
        s = requests.Session()
        resistryResponse = s.send(registeryRequest.prepare())         
        return resistryResponse.json()
    
    def remove(self, serviceId: str) -> Union[int, None]:
        raise Exception("NOT SUPPORTED")
    
    def remove_media(self, mediaId: str) -> bool:
        raise Exception("NOT SUPPORTED")
    
    # TODO - VALIDATE CLIENT ACCESS TO REDIS
    def get_media_services(self) -> Union[Dict[str, str], None]:
        return media_source_da.hgetall()
    
    # TODO - VALIDATE CLIENT ACCESS TO REDIS
    def get_media_service(self, mediaId: str) -> Union[str, None]:
        return media_source_da.hget(mediaId)