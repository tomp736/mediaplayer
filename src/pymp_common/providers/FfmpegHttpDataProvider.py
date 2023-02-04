

import io
from typing import Union
from pymp_common.abstractions.providers import FfmpegDataProvider
from pymp_common.decorators.prom import prom_count

from pymp_common.dto.MediaRegistry import ServiceInfo


class FfmpegHttpDataProvider(FfmpegDataProvider):
    
    def __init__(self, serviceinfo: ServiceInfo):
        self.serviceinfo = serviceinfo
        
    def __repr__(self) -> str:
        return "FfmpegHttpDataProvider()"

    def is_readonly(self) -> bool:
        return True

    def is_ready(self) -> bool:
        return True

    @prom_count
    def get_thumb(self, media_uri) -> Union[io.BytesIO, None]:
        raise Exception("Not Implemented")

    @prom_count
    def get_meta(self, media_uri) -> Union[str, None]:
        raise Exception("Not Implemented")