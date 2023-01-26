import io
import logging
from typing import Union
import ffmpeg
import json

from ..app.PympMetrics import prometheus

from ..dataaccess.redis import media_service_da
from ..dataaccess.redis import media_source_da
from ..dataaccess.redis import media_meta_da
from ..dataaccess.redis import media_thumb_da

from pymp_common.dataaccess.http_request_factory import media_request_factory

class FfmpegService:
    
    def get_media_url(self, id:str) -> Union[str ,None]:
        # check if media_source exists in redis
        if media_source_da.has():
            # get sourceid by mediaid
            sourceid = media_source_da.hget(id)
            if sourceid and media_service_da.has():
                # get service info by sourceid
                serviceinfo = media_service_da.hget(sourceid)
                if serviceinfo:
                    media_svc_scheme = serviceinfo["scheme"]
                    media_svc_host = serviceinfo["host"]
                    media_svc_port = serviceinfo["port"]
                    return f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"         
        return None                    
    
    def process_media(self, id, force: bool = False) -> bool:
        self.process_thumb(id, force)
        self.process_meta(id, force)
        return True
    
    def process_thumb(self, id, force: bool = False) -> bool:
        if force or not media_thumb_da.has(id):
            try:
                media_svc_url = self.get_media_url(id)
                if media_svc_url is None:
                    return False
                            
                apiRequest = media_request_factory._get_media_(media_svc_url, id, 0, None)
                media_thumb = self.generate_thumb(apiRequest.url)
                media_thumb_da.set(id, media_thumb.getvalue())
            except Exception as err:
                logging.exception(err)
                return False
        return True
    
    def process_meta(self, id, force: bool = False) -> bool:
        if force or not media_meta_da.has(id):
            try:
                media_svc_url = self.get_media_url(id)
                if media_svc_url is None:
                    return False
                            
                apiRequest = media_request_factory._get_media_(media_svc_url, id, 0, None)
                media_meta = self.generate_meta(apiRequest.url)
                media_meta_da.set(id, media_meta)
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

    def generate_meta(self, file_path: str) -> str:
        prometheus.Count("ffmpeg_meta_gen_total")
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(file_path)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta

    def generate_thumb(self, file_path: str) -> io.BytesIO:
        prometheus.Count("ffmpeg_thumb_gen_total")
        width = 300
        out, _ = (
            ffmpeg
            .input(file_path, ss=2)
            .filter('scale', width, -1)
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )
        return io.BytesIO(out)


ffmpeg_service = FfmpegService()
