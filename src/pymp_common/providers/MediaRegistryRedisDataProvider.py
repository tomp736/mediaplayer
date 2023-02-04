
import json
import logging
from typing import Dict
from typing import Union
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.dataaccess.redis import redis_service_info
from pymp_common.dataaccess.redis import redis_media_info

from pymp_common.dto.MediaRegistry import MediaInfo, ServiceInfo


class MediaRegistryRedisDataProvider(MediaRegistryDataProvider):

    def __repr__(self) -> str:
        readonly = self.is_readonly()
        ready = self.is_readonly()
        return f"MediaRegistryRedisDataProvider({readonly},{ready})"

    def is_readonly(self) -> bool:
        try:
            return redis_service_info.is_redis_readonly_replica()
        except Exception:
            return True

    def is_ready(self) -> bool:
        try:
            return redis_service_info.redis.ping()
        except Exception:
            return False

    # SERVICEID => SERVICEINFO

    def get_service_info(self, service_id: str) -> Union[ServiceInfo, None]:
        return redis_service_info.hget(service_id)

    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        all_service_info = redis_service_info.hgetall()
        if all_service_info:
            return all_service_info
        return {}

    def set_service_info(self, service_info: ServiceInfo) -> bool:
        redis_service_info.hset(service_info)
        return True

    def del_service_info(self, service_id) -> Union[int, None]:
        return redis_service_info.hdel(service_id)

    # media_id -> MEDIAINFO

    def get_media_info(self, media_id: str) -> MediaInfo:
        service_id = redis_media_info.hget(media_id)
        media_info = MediaInfo()
        media_info.media_id = media_id
        if service_id:
            media_info.service_id = service_id
        return media_info

    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        redis_media_infos = redis_media_info.hgetall()
        media_info_dict = {}
        if redis_media_infos:
            for media_id, service_id in redis_media_infos.items():
                media_info = MediaInfo()
                media_info.media_id = media_id
                media_info.service_id = service_id
                media_info_dict[media_id] = media_info

        return media_info_dict

    def set_media_info(self, media_info: MediaInfo) -> bool:
        return redis_media_info.hset(media_info.media_id, media_info.service_id) > 0

    def del_media_info(self, media_id: str) -> bool:
        return redis_media_info.hdel(media_id) > 0
