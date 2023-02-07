import logging
from typing import List
from pymp_core.dto.MediaRegistry import MediaInfo
from pymp_core.providers import FfmpegProviderFactory, MediaProviderFactory, MediaRegistryProviderFactory
from pymp_core.utils.RepeatTimer import RepeatTimer
from pymp_core.app.PympConfig import pymp_env
from pymp_core.dto.MediaRegistry import PympServiceType

from pymp_core.decorators import prom

class FfmpegService:
    def __init__(self) -> None:
        self.timer = RepeatTimer(60, self.process_media_services)

    def __repr__(self) -> str:
        return "FfmpegService()"

    def watch_media(self):
        self.timer.start()

    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def process_media_services(self):
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.FFMPEG_SVC:
            media_registry_provider = MediaRegistryProviderFactory.get_media_registry_providers()[
                0]
            all_media_info = media_registry_provider.get_all_media_info()
            if all_media_info:
                for media_info in all_media_info.values():
                    self.process_media_service(media_info)

    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def process_media_service(self, media_info: MediaInfo):
        self.process_media_thumb(media_info)
        self.process_media_meta(media_info)

    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def process_media_thumb(self, media_info: MediaInfo):
        thumb_provider = MediaProviderFactory.get_thumb_providers()[0]
        if not thumb_provider.has_thumb(media_info.media_id):
            media_provider = MediaProviderFactory.get_data_providers(media_info.service_id)[
                0]
            ffmpeg_provider = FfmpegProviderFactory.get_ffmpeg_providers()[0]
            thumb = ffmpeg_provider.get_thumb(
                media_provider.get_media_uri(media_info.media_id))
            if thumb:
                thumb_provider.set_thumb(media_info.media_id, thumb)

    @prom.prom_count_method_call
    @prom.prom_count_method_time
    def process_media_meta(self, media_info: MediaInfo):
        meta_provider = MediaProviderFactory.get_meta_providers()[0]
        if not meta_provider.has_meta(media_info.media_id):
            media_provider = MediaProviderFactory.get_data_providers(media_info.service_id)[
                0]
            ffmpeg_provider = FfmpegProviderFactory.get_ffmpeg_providers()[0]
            meta = ffmpeg_provider.get_meta(
                media_provider.get_media_uri(media_info.media_id))
            if meta:
                meta_provider.set_meta(media_info.media_id, meta)
