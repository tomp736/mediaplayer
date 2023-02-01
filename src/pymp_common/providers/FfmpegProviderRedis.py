

from typing import Union
import io
from pymp_common.abstractions.providers import FfmpegProvider

from pymp_common.dataaccess.redis import media_thumb_da
from pymp_common.dataaccess.redis import media_meta_da


class FfmpegProviderRedis(FfmpegProvider):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return f"FfmpegProviderRedis()"

    def status(self):
        # TODO
        return True

    def get_thumb(self, mediaId, serviceId) -> Union[io.BytesIO, None]:
        thumb = media_thumb_da.get(mediaId)
        if thumb:
            return io.BytesIO(thumb)
        return None

    def set_thumb(self, mediaId, serviceId, thumb: io.BytesIO):
        if media_thumb_da.redis.readwrite:
            media_thumb_da.set(mediaId, thumb.getvalue())

    def get_meta(self, mediaId, serviceId) -> Union[str, None]:
        meta = media_meta_da.get(mediaId)
        if meta:
            return meta.decode()
        return None

    def set_meta(self, mediaId, serviceId, meta: str):
        if media_thumb_da.redis.readwrite:
            media_meta_da.set(mediaId, meta)
