

from typing import Union
from pymp_core.abstractions.providers import MediaMetaProvider


from pymp_core.dataaccess.redis import redis_media_meta
from pymp_core.decorators.prom import prom_count


class MetaRedisDataProvider(MediaMetaProvider):

    def __repr__(self) -> str:
        readonly = self.is_readonly()
        ready = self.is_ready()
        return f"MetaRedisDataProvider(ready:{ready},readonly:{readonly})"
   
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

    @prom_count
    def get_meta(self, media_id) -> Union[str, None]:
        meta = redis_media_meta.get(media_id)
        if meta:
            return meta.decode()
        return None
    
    @prom_count
    def has_meta(self, media_id) -> bool:
        return redis_media_meta.has(media_id)

    @prom_count
    def set_meta(self, media_id, meta: str):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        redis_media_meta.set(media_id, meta)

    @prom_count
    def del_meta(self, media_id):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        raise Exception("Not implemented")
