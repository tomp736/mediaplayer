

import io
from typing import Union
from pymp_common.abstractions.providers import FfmpegDataProvider
from pymp_common.dto.MediaRegistry import ServiceInfo


class FfmpegHttpDataProvider(FfmpegDataProvider):
    
    def __init__(self, serviceinfo: ServiceInfo):
        self.status = False
        self.serviceinfo = serviceinfo
        self.readonly = True
        
    def __repr__(self) -> str:
        return "FfmpegHttpDataProvider()"

    def is_readonly(self) -> bool:
        return self.readonly

    def get_service_url(self) -> str:
        return self.serviceinfo.get_uri()

    def get_status(self) -> bool:
        return self.status

    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        raise Exception("Not Implemented")

    def get_meta(self, media_id) -> Union[str, None]:
        raise Exception("Not Implemented")
    
    def set_thumb(self, media_id, thumb: io.BytesIO):
        raise Exception("Not Implemented")
    
    def set_meta(self, media_id, meta: str):
        raise Exception("Not Implemented")
    
    def del_thumb(self, media_id):
        raise Exception("Not Implemented")

    def del_meta(self, media_id):
        raise Exception("Not Implemented")