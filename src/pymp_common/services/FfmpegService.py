import logging
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.abstractions.providers import FfmpegProvider
from pymp_common.utils.RepeatTimer import RepeatTimer


class FfmpegService:
    def __init__(self, mediaRegistryProvider: MediaRegistryProvider, ffmpegProvider: FfmpegProvider) -> None:
        self.ffmpegProvider = ffmpegProvider
        self.mediaRegistryProvider = mediaRegistryProvider
        
    def __repr__(self) -> str:
        return f"FfmpegService({self.mediaRegistryProvider},{self.ffmpegProvider})"

    def watch_media(self):
        self.timer = RepeatTimer(60, self.process_media_services)
        self.timer.start()

    def process_media_services(self):
        media = self.mediaRegistryProvider.get_media_index()
        if media:
            for id in media:
                logging.info(id)
                self.process_media(id)

    def process_media(self, mediaId) -> bool:
        return self.process_thumb(mediaId) & self.process_meta(mediaId)

    def process_thumb(self, mediaId) -> bool:
        return self.ffmpegProvider.gen_thumb(mediaId)

    def process_meta(self, mediaId) -> bool:
        return self.ffmpegProvider.gen_meta(mediaId)
