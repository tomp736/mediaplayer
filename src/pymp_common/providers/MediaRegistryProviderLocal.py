
import logging
from typing import Dict
from typing import Union
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.redis import media_service_da
from pymp_common.dataaccess.redis import media_source_da


class MediaRegistryProviderLocal(MediaRegistryProvider):
        
    def __repr__(self) -> str:
        return f"MediaRegistryProviderLocal()"

    def loginfo(self, message):
        logging.info(f"{self.__repr__}{message}")

    def register_(self, serviceinfo: Dict):
        self.register(serviceinfo["id"],
                      serviceinfo["scheme"],
                      serviceinfo["host"],
                      serviceinfo["port"])

    def register(self, serviceId, scheme, host, port) -> bool:
        media_service_da.hset(serviceId, scheme, host, port)
        return True

    def register_media(self, mediaId, serviceId) -> bool:
        media_source_da.hset(mediaId, serviceId)
        return True

    def remove(self, serviceId: str) -> Union[int, None]:
        return media_service_da.hdel(serviceId)

    def remove_media(self, mediaId: str) -> bool:
        media_source_da.hdel(mediaId)
        return True

    def get_media_services(self) -> Union[Dict[str, str], None]:
        return media_service_da.hgetall()

    def get_media_service(self, mediaId: str) -> Union[str, None]:
        return media_source_da.hget(mediaId)

    def get_media_index(self) -> Union[Dict[str, str], None]:
        return media_source_da.hgetall()
