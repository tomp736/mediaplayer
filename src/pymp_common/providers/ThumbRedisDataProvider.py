from typing import Union
import io
from pymp_common.abstractions.providers import ThumbDataProvider

from pymp_common.dataaccess.redis import media_thumb_da

class ThumbRedisDataProvider(ThumbDataProvider):
    
    def __repr__(self) -> str:
        return "FfmpegRedisDataProvider()"

    def is_readonly(self) -> bool:
        try:
            return media_thumb_da.is_redis_readonly_replica()
        except Exception:
            return True

    def is_ready(self) -> bool:
        try:
            return media_thumb_da.redis.ping()
        except Exception:
            return False
    
    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        thumb = media_thumb_da.get(media_id)
        if thumb:
            return io.BytesIO(thumb)
        return None

    def set_thumb(self, media_id, thumb: io.BytesIO):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        media_thumb_da.set(media_id, thumb.getvalue())
        
    def del_thumb(self, media_id):
        if self.is_readonly():
            raise Exception("Not configured for writing")
        raise Exception("Not implemented")