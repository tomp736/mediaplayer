

import io
from typing import Union
from pymp_common.abstractions.providers import FfmpegProvider


class FfmpegProviderHttp(FfmpegProvider):
    
    def __init__(self) -> None:
        super().__init__()
        self.is_readonly = True
        
    def __repr__(self) -> str:
        return "FfmpegProviderHttp()"
            
    def readonly(self) -> bool:
        return self.is_readonly
    
    def get_status(self) -> bool:
        return True

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