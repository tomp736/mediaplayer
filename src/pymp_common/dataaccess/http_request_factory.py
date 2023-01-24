from abc import ABCMeta
from typing import Mapping
from typing_extensions import TypeAlias
from requests import Request

from ..app.PympConfig import pymp_env, PympServer

_HeadersMapping: TypeAlias = Mapping[str, str or bytes]


class HttpRequestFactory(metaclass=ABCMeta):
    def base_url(self, api: PympServer) -> str:
        if api.value == PympServer.MEDIA_API.value:
            return pymp_env.media_api_base_url()
        elif api.value == PympServer.META_API.value:
            return pymp_env.meta_api_base_url()
        elif api.value == PympServer.THUMB_API.value:
            return pymp_env.thumb_api_base_url()
        elif api.value == PympServer.MEDIA_SVC.value:
            return pymp_env.media_svc_base_url()
        elif api.value == PympServer.FFMPEG_SVC.value:
            return pymp_env.ffmpeg_svc_base_url()
        return ""

    def get(self, api: PympServer, path: str, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
        return Request(
            method='GET',
            url=f"{base_url}{path}",
            headers=headers
        )

    def post(self, api: PympServer, path: str, data, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
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


class MediaRequestFactory():
    def get_media(self, id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/{id}", mediaHeaders)

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
