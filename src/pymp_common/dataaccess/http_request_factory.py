from abc import ABCMeta
from typing import Mapping
from typing_extensions import TypeAlias
from requests import Request

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer

_HeadersMapping: TypeAlias = Mapping[str, str or bytes]


class HttpRequestFactory(metaclass=ABCMeta):
    def base_url(self, api: PympServer) -> str:        
        api_map = {
            PympServer.MEDIA_API: pymp_env.getBaseUrl(PympServer.MEDIA_API),
            PympServer.META_API: pymp_env.getBaseUrl(PympServer.META_API),
            PympServer.THUMB_API: pymp_env.getBaseUrl(PympServer.THUMB_API),
            PympServer.MEDIA_SVC: pymp_env.getBaseUrl(PympServer.MEDIA_SVC),
            PympServer.FFMPEG_SVC: pymp_env.getBaseUrl(PympServer.FFMPEG_SVC),
            PympServer.MEDIAREGISTRY_SVC: pymp_env.getBaseUrl(PympServer.MEDIAREGISTRY_SVC)
        }        
    
        if api.value & (api.value - 1) == 0:
            return api_map.get(api, "")
        else:
            return ""

    def get(self, api: PympServer, path: str, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
        return self._get_(base_url, path, headers)
        
    def _get_(self, base_url: str, path: str, headers: _HeadersMapping = {}) -> Request:
        return Request(
            method='GET',
            url=f"{base_url}{path}",
            headers=headers
        )

    def post(self, api: PympServer, path: str, data, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
        return self._post_(base_url, path, data, headers)
    
    def _post_(self, base_url: str, path: str, data, headers: _HeadersMapping = {}) -> Request:
        return Request(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            json=data
        )
    
    def _post_media_(self, base_url: str, path: str, data, headers: _HeadersMapping = {}) -> Request:
        return Request(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            data=data
        )


http_request_factory = HttpRequestFactory()


class ApiRequestFactory():
    def get_media(self, id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympServer.MEDIA_API, f"/api/media/{id}", mediaHeaders)

    def get_media_list(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_API, f"/api/media/list")

    def get_thumb(self, id: str) -> Request:
        return http_request_factory.get(PympServer.THUMB_API, f"/api/thumb/{id}")

    def get_meta(self, id: str) -> Request:
        return http_request_factory.get(PympServer.META_API, f"/api/meta/{id}")


api_request_factory = ApiRequestFactory()


class MediaRegistryRequestFactory():
    def list(self) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, f"/registry/list")
    
    def register(self, id: str, scheme: str, host: str, port: str) -> Request:
        return http_request_factory.post(PympServer.MEDIAREGISTRY_SVC, f"/registry/register", 
            {
                'id' : id,
                'scheme' : scheme,
                'host' : host,
                'port' : port                
            }
        )
        
    def list_media(self) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, f"/registry/media/list")
        
    def register_media(self, mediaServiceId, mediaId) -> Request:
        return http_request_factory.post(PympServer.MEDIAREGISTRY_SVC, f"/registry/media/register",
            {
                'mediaServiceId' : mediaServiceId,
                'mediaId' : mediaId
            })

media_registry_request_factory = MediaRegistryRequestFactory()


class MediaRequestFactory():        
    def get_media(self, id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/{id}", mediaHeaders)
    
    def _get_media_(self, baseurl:str, id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory._get_(baseurl, f"/media/{id}", mediaHeaders)
    
    def _post_media_(self, baseurl:str, data) -> Request:
        return http_request_factory._post_media_(baseurl, f"/media", data)

    def get_media_list(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/list")

    def _get_media_list_(self, baseurl:str) -> Request:
        return http_request_factory._get_(baseurl, f"/media/list")

    def get_media_index(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/index")


media_request_factory = MediaRequestFactory()


class FfmpegRequestFactory():
    def get_meta(self, id: str) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/meta/{id}")

    def get_thumb(self, id: str) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/thumb/{id}")

    def get_static(self) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/media/static")


ffmpeg_request_factory = FfmpegRequestFactory()
