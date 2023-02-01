import logging
import traceback
import requests
from typing import IO
from typing import Dict
from typing import List
from typing import Union

from pymp_common.dataaccess.http_request_factory import media_request_factory
from pymp_common.abstractions.providers import MediaProvider
from pymp_common.abstractions.providers import MediaChunk

from pymp_common.app.PympConfig import pymp_env

class MediaProviderHttp(MediaProvider):
    def __init__(self, serviceinfo: Dict[str,str]):  
        self.status = True            
        self.serviceinfo = serviceinfo
        self.service_url = self.get_service_url()

    def __repr__(self) -> str:
        return f"MediaProviderHttp({self.service_url})"

    def get_service_url(self) -> str:
        proto = self.serviceinfo["proto"]
        host = self.serviceinfo["host"]
        port = self.serviceinfo["port"]
        return f"{proto}://{host}:{port}"
    
    def get_status(self) -> bool:
        return self.status

    def get_media_uri(self, media_id: str) -> Union[str, None]:
        if self.service_url:
            media_request = media_request_factory._get_media_(
                self.service_url, media_id, 0, None)
            return media_request.url
        return None

    def get_media_ids(self) -> List[str]:
        media_ids = []
        session = requests.Session()
        media_request = media_request_factory._get_media_list_(
            self.service_url)
        media_response = session.send(media_request.prepare())
        for media_id in media_response.json():
            media_ids.append(media_id)
        return media_ids

    def get_media_chunk(self, media_id, sByte: int = 0, eByte: int = 0, fileSize: int = 0) -> Union[MediaChunk, None]:
        if not self.service_url is None:
            media_request = media_request_factory._get_media_(
                self.service_url, media_id, sByte, eByte)
            session = requests.Session()
            media_response = session.send(media_request.prepare())
            if not "content-range" in media_response.headers:
                raise Exception("MISSING CONTENT RANGE")
            if not media_response.status_code == 206:
                # TODO HANDLER
                return None

            sByte, eByte, fileSize = MediaChunk.parse_range_header(
                media_response.headers["content-range"])
            return MediaChunk(media_response.content, sByte, eByte, fileSize)

        return None

    def save_media(self, name: str, stream: IO[bytes]):
        if not self.service_url is None:
            media_request = media_request_factory._post_media_(
                self.service_url, stream)
            session = requests.Session()
            session.send(media_request.prepare())

    def update_index(self):
        pass  
