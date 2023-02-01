import io
import json
import logging
from typing import Union

import ffmpeg
from pymp_common.utils.RepeatTimer import RepeatTimer

from pymp_common.app.ProviderFactory import get_ffmpeg_providers, get_media_registry_providers

class FfmpegService:
    def __init__(self) -> None:
        self.mediaRegistryProvider = list(get_media_registry_providers().values())[0]
        self.ffmpegProvider = list(get_ffmpeg_providers().values())[0]
        self.timer = RepeatTimer(60, self.process_media_services)

    def __repr__(self) -> str:
        return f"FfmpegService({self.mediaRegistryProvider},{self.ffmpegProvider})"

    def watch_media(self):
        self.timer.start()

    def process_media_services(self):
        service_info = self.mediaRegistryProvider.get_service_info()
        service_media = self.mediaRegistryProvider.get_service_media()
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
        return self.ffmpegProvider.get_thumb(media_id)

    def set_thumb(self, media_id, thumb: io.BytesIO):
        self.ffmpegProvider.set_thumb(media_id, thumb)

    def get_meta(self, media_id) -> Union[str, None]:
        return self.ffmpegProvider.get_meta(media_id)

    def set_meta(self, media_id, meta: str):
        self.ffmpegProvider.set_meta(media_id, meta)     
    
    def generate_thumb(self, media_source) -> Union[io.BytesIO, None]:
        width = 300
        out, error = (
            ffmpeg
            .input(media_source, ss=2)
            .filter('scale', width, -1)
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )
        logging.info(error)
        return io.BytesIO(out)

    def generate_meta(self, media_source) -> Union[str, None]:
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(media_source)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta
