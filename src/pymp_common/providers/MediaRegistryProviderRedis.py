
import json
from typing import Dict
from typing import Union
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.redis import media_service_info_da
from pymp_common.dataaccess.redis import media_service_media_da

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer
from pymp_common.dto.MediaRegistry import ServiceInfo


class MediaRegistryProviderRedis(MediaRegistryProvider):

    def __init__(self):
        if pymp_env.get_servertype() & PympServer.MEDIAREGISTRY_SVC:
            self.status = False
        else:
            self.status = True
        self.is_readonly = media_service_info_da.is_redis_readonly_replica()

    def __repr__(self) -> str:
        return "MediaRegistryProviderRedis()"

    def readonly(self):
        return self.is_readonly
    
    def get_status(self) -> bool:
        return self.status

    # SERVICEID => SERVICEINFO{}

    def get_service_info(self, service_id: str) -> Union[ServiceInfo, None]:
        service_info = media_service_info_da.hget(service_id)
        if service_info:
            return ServiceInfo.from_dict(service_info)
        return None

    def get_all_service_info(self) -> Union[Dict[str, ServiceInfo], None]:
        service_infos = media_service_info_da.hgetall()
        dict = {}
        if service_infos:
            for service_id, service_info in service_infos.items():
                dict[service_id] = ServiceInfo.from_dict(json.loads(service_info))
        return dict
    
    def set_service_info(self, service_id, service_info: ServiceInfo) -> bool:
        media_service_info_da.hset(
            service_id,
            service_info.service_proto,
            service_info.service_host,
            service_info.service_port)
        return True

    def del_service_info(self, service_id) -> Union[int, None]:
        return media_service_info_da.hdel(service_id)

    # SERVICEID => MEDIAINFO{}
    def set_service_media(self, service_id: str,  media_id: str) -> bool:
        media_service_media_da.hset(media_id, service_id)
        return True

    def del_service_media(self, service_id: str, media_id: str) -> bool:
        media_service_media_da.hdel(media_id)
        return True

    def get_service_media(self, service_id: Union[str, None] = None) -> Union[Dict[str, str], None]:
        filter = service_id
        return media_service_media_da.hgetall()
