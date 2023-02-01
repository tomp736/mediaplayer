

import io
import json
from typing import Union
from pymp_common.abstractions.providers import FfmpegProvider
import ffmpeg
import logging

from pymp_common.app import ProviderFactory

class FfmpegProviderLocal(FfmpegProvider):

    def __repr__(self) -> str:
        return f"FfmpegProviderLocal()"

    def loginfo(self, message):
        logging.info(f"{self.__repr__()}{message}")

    def get_thumb(self, mediaId, serviceId) -> Union[io.BytesIO, None]:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            mediaUri = mediaProvider.get_media_uri(mediaId)
            if mediaUri:
                return self.generate_thumb(mediaUri)
        return None

    def get_meta(self, mediaId, serviceId) -> Union[str, None]:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            mediaUri = mediaProvider.get_media_uri(mediaId)
            if mediaUri:
                return self.generate_meta(mediaUri)
        return None

    def generate_static(self) -> io.BytesIO:
        out, error = (
            ffmpeg
            .input('smptebars=s=640x480:d=5', f='lavfi')
            .output('pipe:', format='webm', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )
        logging.info(error)
        return io.BytesIO(out)

    def generate_meta(self, media_source: str) -> str:
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(media_source)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta

    def generate_thumb(self, media_source: str) -> io.BytesIO:
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
