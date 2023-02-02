

import io
import json
import logging
from typing import Union

import ffmpeg
from pymp_common.abstractions.providers import FfmpegDataProvider
from pymp_common.app import ProviderFactory

class FfmpegFileDataProvider(FfmpegDataProvider):
    
    def __init__(self) -> None:
        super().__init__()
        self.readonly = True
        self.media_registry_data_provider = list(ProviderFactory.get_media_registry_providers().values())[0]
        
    def __repr__(self) -> str:
        return "FfmpegHttpDataProvider()"
            
    def is_readonly(self) -> bool:
        return self.readonly
    
    def get_status(self) -> bool:
        return False

    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        media_info = self.media_registry_data_provider.get_media_info(media_id)
        media_data_provider = list(ProviderFactory.get_media_providers(media_info.service_id).values())[0]        
        media_uri = media_data_provider.get_media_uri(media_id)
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
    
    def get_meta(self, media_id) -> Union[str, None]:
        media_info = self.media_registry_data_provider.get_media_info(media_id)
        media_data_provider = list(ProviderFactory.get_media_providers(media_info.service_id).values())[0]        
        media_uri = media_data_provider.get_media_uri(media_id)
        media_meta = ""
        try:
            media_meta = json.dumps(ffmpeg.probe(media_uri)['streams'][0])
        except ffmpeg.Error as e:
            logging.exception(e.stderr.decode())
        return media_meta
    
    def set_thumb(self, media_id, thumb: io.BytesIO):
        raise Exception("Not Implemented")
    
    def set_meta(self, media_id, meta: str):
        raise Exception("Not Implemented")
    
    def del_thumb(self, media_id):
        raise Exception("Not Implemented")

    def del_meta(self, media_id):
        raise Exception("Not Implemented")