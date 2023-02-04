

from typing import Union
from pymp_common.abstractions.providers import MetaDataProvider

from pymp_common.dataaccess.redis import redis_media_meta


class MetaRedisDataProvider(MetaDataProvider):

    def __repr__(self) -> str:
        return "FfmpegRedisDataProvider()"
    
    def is_readonly(self) -> bool:
        try:
            return redis_media_meta.is_redis_readonly_replica()
        except Exception:
            return True

    def is_ready(self) -> bool:
        try:
            return redis_media_meta.redis.ping()
        except Exception:
            return False

    def get_meta(self, media_id) -> Union[str, None]:
        meta = redis_media_meta.get(media_id)
        if meta:
            return meta.decode()
        return None

    def set_meta(self, media_id, meta: str):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        redis_media_meta.set(media_id, meta)

    def del_meta(self, media_id):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        raise Exception("Not implemented")
