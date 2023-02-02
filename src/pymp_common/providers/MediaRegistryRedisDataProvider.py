
import json
from typing import Dict
from typing import Union
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.dataaccess.redis import media_service_info_da
from pymp_common.dataaccess.redis import media_service_media_da

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer
from pymp_common.dto.MediaRegistry import MediaInfo, ServiceInfo


class MediaRegistryRedisDataProvider(MediaRegistryDataProvider):

    def __init__(self):
        if pymp_env.get_servertype() & PympServer.MEDIAREGISTRY_SVC:
            self.status = False
        else:
            self.status = True
            self.readonly = media_service_info_da.is_redis_readonly_replica()

    def __repr__(self) -> str:
        return "MediaRegistryRedisDataProvider()"

    def is_readonly(self) -> bool:
        return self.readonly
    
    def get_status(self) -> bool:
        return self.status

    # SERVICEID => SERVICEINFO

    def get_service_info(self, service_id: str) -> ServiceInfo:
        service_info = media_service_info_da.hget(service_id)
        if service_info:
            return ServiceInfo.from_dict(service_info)
        return ServiceInfo()

    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        service_infos = media_service_info_da.hgetall()
        service_dict = {}
        if service_infos:
            for service_id, service_info in service_infos.items():
                service_dict[service_id] = ServiceInfo.from_dict(json.loads(service_info))
        return service_dict
    
    def set_service_info(self, service_info: ServiceInfo) -> bool:
        media_service_info_da.hset(
            service_info.service_id,
            service_info.service_proto,
            service_info.service_host,
            service_info.service_port)
        return True

    def del_service_info(self, service_id) -> Union[int, None]:
        return media_service_info_da.hdel(service_id)

    # media_id -> MEDIAINFO

    def get_media_info(self, media_id: str) -> MediaInfo:
        media_info_str = media_service_media_da.hget(media_id)
        if media_info_str:
            return MediaInfo.from_json_str(media_info_str)
        return MediaInfo()

    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        redis_media_infos = media_service_media_da.hgetall()
        media_info_dict = {}
        if redis_media_infos:
            for media_id, service_id in redis_media_infos.items():
                media_info = MediaInfo()
                media_info.media_id = media_id
                media_info.service_id = service_id
                media_info_dict[media_id] = media_info
                
        return media_info_dict
    
    def set_media_info(self, media_info: MediaInfo) -> bool:
        return media_service_media_da.hset(media_info.media_id, media_info.service_id) > 0

    def del_service_media(self, media_id: str) -> bool:
        return media_service_media_da.hdel(media_id) > 0
