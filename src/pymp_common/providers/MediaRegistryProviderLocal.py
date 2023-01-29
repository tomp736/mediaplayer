
from typing import Dict, Union
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.redis import media_service_da
from pymp_common.dataaccess.redis import media_source_da


class MediaRegistryProviderLocal(MediaRegistryProvider):
    
    def register_(self, serviceinfo: Dict):
        self.register(serviceinfo["id"],
                      serviceinfo["scheme"],
                      serviceinfo["host"],
                      serviceinfo["port"])
    
    def register(self, serviceId, scheme, host, port) -> bool:
        media_service_da.hset(serviceId, scheme, host, port)
        return True
    
    def registerMedia(self, mediaId, serviceId) -> bool:
        media_source_da.hset(mediaId, serviceId)
        return True
    
    def remove(self, serviceId: str) -> Union[int, None]:
        return media_service_da.hdel(serviceId)
    
    def removeMedia(self, mediaId: str) -> bool:
        media_source_da.hdel(mediaId)
        return True
    
    def getMediaServices(self) -> Union[Dict[str, str], None]:
        return media_service_da.hgetall()
    
    def getMediaService(self, mediaId: str) -> Union[str, None]:
        return media_source_da.hget(mediaId)
    
    def getMediaIndex(self) -> Union[Dict[str, str], None]:
        return media_source_da.hgetall()
