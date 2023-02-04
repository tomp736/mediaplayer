import io
import json
import logging
from typing import Union

import ffmpeg
from pymp_common.abstractions.providers import FfmpegDataProvider

from pymp_common.decorators.prom import prom_count


class FfmpegFileDataProvider(FfmpegDataProvider):

    def __repr__(self) -> str:
        return "FfmpegFileDataProvider()"

    def is_readonly(self) -> bool:
        return True

    def is_ready(self) -> bool:
        return True

    @prom_count
    def get_thumb(self, media_uri) -> Union[io.BytesIO, None]:
        width = 300
        out, error = (
            ffmpeg
            .input(media_uri, ss=2)
            .filter('scale', width, -1)
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )
        logging.info(error)
        return io.BytesIO(out)

    @prom_count
    def get_meta(self, media_uri) -> Union[str, None]:
        return json.dumps(ffmpeg.probe(media_uri)['streams'][0])
