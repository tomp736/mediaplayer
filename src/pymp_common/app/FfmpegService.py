import io
import logging
import ffmpeg
import json

from ..app.PympMetrics import prometheus

from ..dataaccess.redis import media_source_da
from ..dataaccess.redis import media_meta_da
from ..dataaccess.redis import media_thumb_da

from pymp_common.providers.MediaProviderFactory import MediaServiceFactory

class FfmpegService:                  
    
    def process_media(self, id, force: bool = False) -> bool:
        self.process_thumb(id, force)
        self.process_meta(id, force)
        return True
    
    def process_thumb(self, media_id, force: bool = False) -> bool:
        if force or not media_thumb_da.has(media_id):
            try:
                if media_source_da.has():
                    media_source_id = media_source_da.hget(media_id)
                    media_service = MediaServiceFactory.create_instance(media_source_id)
                    media_uri = media_service.get_media_uri(media_id)
                    if media_uri:
                        media_thumb = self.generate_thumb(media_uri)
                        media_thumb_da.set(media_id, media_thumb.getvalue())
            except Exception as err:
                logging.exception(err)
                return False
        return True
    
    def process_meta(self, media_id, force: bool = False) -> bool:
        if force or not media_meta_da.has(media_id):
            try:
                if media_source_da.has():
                    media_source_id = media_source_da.hget(media_id)
                    media_service = MediaServiceFactory.create_instance(media_source_id)
                    media_uri = media_service.get_media_uri(media_id)
                    if media_uri:
                        media_meta = self.generate_meta(media_uri)
                        media_meta_da.set(media_id, media_meta)
            except Exception as err:
                logging.exception(err)
                return False
        return True

    def generate_static(self) -> io.BytesIO:
        prometheus.Count("ffmpeg_static_gen_total")
        out, _ = (
            ffmpeg
            .input('smptebars=s=640x480:d=5', f='lavfi')
            .output('pipe:', format='webm', pix_fmt='rgb24')
            .run(capture_stdout=True)
        )
        return io.BytesIO(out)

    def generate_meta(self, media_source: str) -> str:
        prometheus.Count("ffmpeg_meta_gen_total")
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(media_source)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta

    def generate_thumb(self, media_source: str) -> io.BytesIO:
        prometheus.Count("ffmpeg_thumb_gen_total")
        width = 300
        out, _ = (
            ffmpeg
            .input(media_source, ss=2)
            .filter('scale', width, -1)
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )
        return io.BytesIO(out)


ffmpeg_service = FfmpegService()
