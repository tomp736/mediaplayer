import requests
from typing import Union, List

from pymp_common.dataaccess.http_request_factory import media_request_factory
from pymp_common.dataaccess.redis import media_service_da
from pymp_common.abstractions.providers import MediaProvider, MediaChunk


class MediaProviderRemote(MediaProvider):
    def __init__(self, media_service_id):
        self.session = requests.Session()
        self.media_service_id = media_service_id
        serviceinfo = media_service_da.hget(self.media_service_id)
        if serviceinfo:
            media_svc_scheme = serviceinfo["scheme"]
            media_svc_host = serviceinfo["host"]
            media_svc_port = serviceinfo["port"]
            self.media_service_url = f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"

    def get_media_uri(self, media_id: str) -> Union[str, None]:
        if not self.media_service_url == None:
            apiRequest = media_request_factory._get_media_(
                self.media_service_url, media_id, 0, None)
            return apiRequest.url
        return None

    def get_media_list(self) -> List[str]:
        media_ids = []
        if not self.media_service_url is None:
            apiRequest = media_request_factory._get_media_list_(
                self.media_service_url)
            apiResponse = self.session.send(apiRequest.prepare())
            media_ids = apiResponse.json()
        return media_ids

    def get_media_chunk(self, id, startByte=0, endByte=None) -> Union[MediaChunk, None]:
        if not self.media_service_url is None:
            apiRequest = media_request_factory._get_media_(
                self.media_service_url, id, startByte, endByte)
            apiResponse = self.session.send(apiRequest.prepare())
            MediaChunk(apiResponse.content, startByte, endByte, 0)
        return None
