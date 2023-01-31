

import io
import json
from typing import Union
from pymp_common.abstractions.providers import FfmpegProvider
import ffmpeg
import logging

from pymp_common.app import ProviderFactory
from pymp_common.dataaccess.redis import media_meta_da
from pymp_common.dataaccess.redis import media_thumb_da


class FfmpegProviderLocal(FfmpegProvider):
    def __init__(self) -> None:
        self.mediaRegistryProvider = ProviderFactory.get_media_registry_provider()
        
    def __repr__(self) -> str:
        return f"FfmpegProviderLocal()"

    def loginfo(self, message):
        logging.info(f"{self.__repr__()}{message}")

    def gen_thumb(self, mediaId) -> bool:
        # TODO BETTER PLACE FOR THIS CHECK
        logging.info("CHECK THUMB")
        if media_thumb_da.has(mediaId):
            return True
        logging.info("GENERATING THUMB")

        mediaServiceId = self.mediaRegistryProvider.get_media_service(mediaId)
        mediaProvider = ProviderFactory.get_media_provider(mediaServiceId)
        if mediaProvider:
            mediaUri = mediaProvider.get_media_uri(mediaId)
            if mediaUri:
                media_thumb = self.generate_thumb(mediaUri)
                media_thumb_da.set(mediaId, media_thumb.getvalue())
                return True
        return False

    def gen_meta(self, mediaId) -> bool:
        # TODO BETTER PLACE FOR THIS CHECK
        logging.info("CHECK META")
        if media_meta_da.has(mediaId):
            return True
        logging.info("GENERATING META")
        mediaServiceId = self.mediaRegistryProvider.get_media_service(mediaId)
        mediaProvider = ProviderFactory.get_media_provider(mediaServiceId)
        if mediaProvider:
            mediaUri = mediaProvider.get_media_uri(mediaId)
            if mediaUri:
                media_meta = self.generate_meta(mediaUri)
                media_meta_da.set(mediaId, media_meta)
                return True
        return False

    def get_thumb(self, mediaId) -> Union[bytes, None]:
        return media_thumb_da.get(mediaId)

    def get_meta(self, mediaId) -> Union[bytes, None]:
        return media_meta_da.get(mediaId)

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
