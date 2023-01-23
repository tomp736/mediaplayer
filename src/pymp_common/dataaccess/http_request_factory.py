from abc import ABCMeta
from typing import Mapping
from typing_extensions import TypeAlias
from enum import Enum
from requests import Request

from ..app.PympConfig import pymp_env

_HeadersMapping: TypeAlias = Mapping[str, str or bytes]


class PympApi(Enum):
    MEDIA = 1
    THUMB = 2
    META = 3
    FFMPEG = 4


class HttpRequestFactory(metaclass=ABCMeta):
    def base_url(self, api: PympApi) -> str:
        if api.value == PympApi.MEDIA.value:
            return pymp_env.media_fqdn()
        elif api.value == PympApi.THUMB.value:
            return pymp_env.thumb_fqdn()
        elif api.value == PympApi.META.value:
            return pymp_env.meta_fqdn()
        elif api.value == PympApi.FFMPEG.value:
            return pymp_env.ffmpeg_fqdn()
        return ""

    def get(self, api: PympApi, path: str, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
        return Request(
            method='GET',
            url=f"{base_url}{path}",
            headers=headers
        )

    def post(self, api: PympApi, path: str, data, headers: _HeadersMapping = {}) -> Request:
        base_url = self.base_url(api)
        return Request(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            data=data
        )


http_request_factory = HttpRequestFactory()


class MediaRequestFactory():
    def get_media(self, id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympApi.MEDIA, f"/media/{id}", mediaHeaders)

    def get_media_list(self) -> Request:
        return http_request_factory.get(PympApi.MEDIA, f"/media/list")

    def get_media_index(self) -> Request:
        return http_request_factory.get(PympApi.MEDIA, f"/media/index")


media_request_factory = MediaRequestFactory()


class ThumbRequestFactory():
    def get_thumb(self, id: str) -> Request:
        return http_request_factory.get(PympApi.THUMB, f"/thumb/{id}")


thumb_request_factory = ThumbRequestFactory()


class MetaRequestFactory():
    def get_meta(self, id: str) -> Request:
        return http_request_factory.get(PympApi.META, f"/meta/{id}")


meta_request_factory = MetaRequestFactory()


class FfmpegRequestFactory():
    def get_meta(self, id: str) -> Request:
        return http_request_factory.get(PympApi.FFMPEG, f"/meta/{id}")

    def get_thumb(self, id: str) -> Request:
        return http_request_factory.get(PympApi.FFMPEG, f"/thumb/{id}")

    def get_static(self) -> Request:
        return http_request_factory.get(PympApi.FFMPEG, f"/media/static")


ffmpeg_request_factory = FfmpegRequestFactory()
