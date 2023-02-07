from typing import Union
import io
from pymp_core.abstractions.providers import MediaThumbProvider


from pymp_core.dataaccess.redis import redis_media_thumb
from pymp_core.decorators import prom

class ThumbRedisDataProvider(MediaThumbProvider):
    
    def __repr__(self) -> str:
        readonly = self.is_readonly()
        ready = self.is_ready()
        return f"ThumbRedisDataProvider(ready:{ready},readonly:{readonly})"

    def is_readonly(self) -> bool:
        try:
            return redis_media_thumb.is_redis_readonly_replica()
        except Exception:
            return True

    def is_ready(self) -> bool:
        try:
            return redis_media_thumb.redis.ping()
        except Exception:
            return False
    
    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        thumb = redis_media_thumb.get(media_id)
        if thumb:
            return io.BytesIO(thumb)
        return None
    
    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def has_thumb(self, media_id) -> bool:
        return redis_media_thumb.has(media_id)

    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def set_thumb(self, media_id, thumb: io.BytesIO):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        redis_media_thumb.set(media_id, thumb.getvalue())
        
    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def del_thumb(self, media_id):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        raise Exception("Not implemented")