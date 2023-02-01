import io
import logging
from typing import Union
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.abstractions.providers import FfmpegProvider
from pymp_common.utils.RepeatTimer import RepeatTimer


class FfmpegService:
    def __init__(self, mediaRegistryProvider: MediaRegistryProvider, ffmpegProvider: FfmpegProvider) -> None:
        self.mediaRegistryProvider = mediaRegistryProvider
        self.ffmpegProvider = ffmpegProvider

    def __repr__(self) -> str:
        return f"FfmpegService({self.mediaRegistryProvider},{self.ffmpegProvider})"

    def watch_media(self):
        self.timer = RepeatTimer(60, self.process_media_services)
        self.timer.start()

    def process_media_services(self):
        media = self.mediaRegistryProvider.get_media_index()
        if media:
            for mediaId, serviceId in media:
                logging.info(mediaId)

                meta = self.get_meta(mediaId, serviceId)
                if meta:
                    self.set_meta(mediaId, serviceId, meta)

                thumb = self.get_thumb(mediaId, serviceId)
                if thumb:
                    self.set_thumb(mediaId, serviceId, thumb)

    def get_thumb(self, mediaId, serviceId) -> Union[io.BytesIO, None]:
        return self.ffmpegProvider.get_thumb(mediaId, serviceId)

    def set_thumb(self, mediaId, serviceId, thumb: io.BytesIO):
        self.ffmpegProvider.set_thumb(mediaId, serviceId, thumb)

    def get_meta(self, mediaId, serviceId) -> Union[str, None]:
        return self.ffmpegProvider.get_meta(mediaId, serviceId)

    def set_meta(self, mediaId, serviceId, meta: str):
        self.ffmpegProvider.set_meta(mediaId, serviceId, meta)
