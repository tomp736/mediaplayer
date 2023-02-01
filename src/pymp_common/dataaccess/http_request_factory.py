from abc import ABCMeta
from typing import Mapping
from typing_extensions import TypeAlias
from requests import Request

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer
from pymp_common.dto.MediaRegistry import ServiceInfo
from pymp_common.dto.MediaRegistry import MediaInfo

_HeadersMapping: TypeAlias = Mapping[str, str or bytes]


class HttpRequestFactory(metaclass=ABCMeta):
    def base_url(self, api: PympServer) -> str:
        api_map = {
            PympServer.MEDIA_API: pymp_env.get_baseurl(PympServer.MEDIA_API),
            PympServer.META_API: pymp_env.get_baseurl(PympServer.META_API),
            PympServer.THUMB_API: pymp_env.get_baseurl(PympServer.THUMB_API),
            PympServer.MEDIA_SVC: pymp_env.get_baseurl(PympServer.MEDIA_SVC),
            PympServer.FFMPEG_SVC: pymp_env.get_baseurl(PympServer.FFMPEG_SVC),
            PympServer.MEDIAREGISTRY_SVC: pymp_env.get_baseurl(
                PympServer.MEDIAREGISTRY_SVC)
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
    def get_media(self, media_id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympServer.MEDIA_API, f"/api/media/{media_id}", mediaHeaders)

    def get_media_list(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_API, "/api/media/list")

    def get_thumb(self, media_id: str) -> Request:
        return http_request_factory.get(PympServer.THUMB_API, f"/api/thumb/{media_id}")

    def get_meta(self, media_id: str) -> Request:
        return http_request_factory.get(PympServer.META_API, f"/api/meta/{media_id}")


api_request_factory = ApiRequestFactory()


class MediaRegistryRequestFactory():

    # service info
    def list_service_info(self) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, "/registry/service")

    def set_service_info(self, service_info: ServiceInfo) -> Request:
        return http_request_factory.post(PympServer.MEDIAREGISTRY_SVC, "/registry/service", service_info)

    def get_service_info(self, service_id) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, f"/registry/service/{service_id}")

    # service media
    def get_service_media(self, service_id) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, f"/registry/service/{service_id}/media")

    # service media
    def set_service_media(self, service_id, media_id) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, f"/registry/service/{service_id}/media/{media_id}")

    # all media
    def list_media(self) -> Request:
        return http_request_factory.get(PympServer.MEDIAREGISTRY_SVC, "/registry/media/list")


media_registry_request_factory = MediaRegistryRequestFactory()


class MediaRequestFactory():
    def get_media(self, media_id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/{media_id}", mediaHeaders)

    def _get_media_(self, baseurl: str, media_id: str, rangeStart: int, rangeEnd) -> Request:
        mediaHeaders = {
            'Range': f'bytes {rangeStart}-{rangeEnd}'
        }
        return http_request_factory._get_(baseurl, f"/media/{media_id}", mediaHeaders)

    def _post_media_(self, baseurl: str, data) -> Request:
        return http_request_factory._post_media_(baseurl, f"/media", data)

    def get_media_list(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/list")

    def _get_media_list_(self, baseurl: str) -> Request:
        return http_request_factory._get_(baseurl, f"/media/list")

    def get_media_index(self) -> Request:
        return http_request_factory.get(PympServer.MEDIA_SVC, f"/media/index")


media_request_factory = MediaRequestFactory()


class FfmpegRequestFactory():
    def get_meta(self, media_id: str) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/meta/{media_id}")

    def get_thumb(self, media_id: str) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/thumb/{media_id}")

    def get_static(self) -> Request:
        return http_request_factory.get(PympServer.FFMPEG_SVC, f"/ffmpeg/media/static")


ffmpeg_request_factory = FfmpegRequestFactory()
