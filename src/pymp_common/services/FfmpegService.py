import io
import json
import logging
from typing import Union

import ffmpeg
from pymp_common.utils.RepeatTimer import RepeatTimer

from pymp_common.app.ProviderFactory import get_ffmpeg_providers, get_media_registry_providers

class FfmpegService:
    def __init__(self) -> None:
        self.MediaRegistryDataProvider = list(get_media_registry_providers().values())[0]
        self.FfmpegDataProvider = list(get_ffmpeg_providers().values())[0]
        self.timer = RepeatTimer(60, self.process_media_services)

    def __repr__(self) -> str:
        return f"FfmpegService({self.MediaRegistryDataProvider},{self.FfmpegDataProvider})"

    def watch_media(self):
        self.timer.start()

    def process_media_services(self):
        service_info = self.MediaRegistryDataProvider.get_service_info()
        service_media = self.MediaRegistryDataProvider.get_service_media()
        if service_media and service_info:
            for media_id, service_id in service_media.items():
                media_service_info = service_info.get(service_id)
                if media_service_info:
                    service_id = media_service_info["id"]
                    service_proto = media_service_info["proto"]
                    service_host = media_service_info["host"]
                    service_port = media_service_info["port"]

                meta = self.generate_meta(media_id, service_id)
                if meta:
                    self.set_meta(media_id, service_id, meta)

                thumb = self.generate_thumb(media_id, service_id)
                if thumb:
                    self.set_thumb(media_id, service_id, thumb)

    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        return self.FfmpegDataProvider.get_thumb(media_id)

    def set_thumb(self, media_id, thumb: io.BytesIO):
        self.FfmpegDataProvider.set_thumb(media_id, thumb)

    def get_meta(self, media_id) -> Union[str, None]:
        return self.FfmpegDataProvider.get_meta(media_id)

    def set_meta(self, media_id, meta: str):
        self.FfmpegDataProvider.set_meta(media_id, meta)     
    
    def generate_thumb(self, media_source) -> Union[io.BytesIO, None]:
        

    def generate_meta(self, media_source) -> Union[str, None]:
