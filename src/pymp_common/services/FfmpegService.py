from pymp_common.dto.MediaRegistry import MediaInfo
from pymp_common.utils.RepeatTimer import RepeatTimer
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dto.MediaRegistry import PympServiceType

from pymp_common.app.ProviderFactory import get_ffmpeg_providers, get_media_registry_providers, get_media_providers, get_meta_providers, get_thumb_providers


class FfmpegService:
    def __init__(self) -> None:
        self.timer = RepeatTimer(60, self.process_media_services)

    def __repr__(self) -> str:
        return "FfmpegService()"

    def watch_media(self):
        self.timer.start()

    def process_media_services(self):
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.FFMPEG_SVC:
            media_registry_provider = get_media_registry_providers()[0]
            all_media_info = media_registry_provider.get_all_media_info()
            if all_media_info:
                for media_info in all_media_info.values():
                    self.process_media_service(media_info)

    def process_media_service(self, media_info: MediaInfo):
        self.process_media_thumb(media_info)
        self.process_media_meta(media_info)

    def process_media_thumb(self, media_info: MediaInfo):
        media_provider = get_media_providers(media_info.service_id)[0]
        ffmpeg_provider = get_ffmpeg_providers()[0]
        thumb_provider = get_thumb_providers()[0]
        thumb = ffmpeg_provider.get_thumb(
            media_provider.get_media_uri(media_info.media_id))
        if thumb:
            thumb_provider.set_thumb(media_info.media_id, thumb)

    def process_media_meta(self, media_info: MediaInfo):
        media_provider = get_media_providers(media_info.service_id)[0]
        ffmpeg_provider = get_ffmpeg_providers()[0]
        meta_provider = get_meta_providers()[0]
        meta = ffmpeg_provider.get_meta(
            media_provider.get_media_uri(media_info.media_id))
        if meta:
            meta_provider.set_meta(media_info.media_id, meta)
