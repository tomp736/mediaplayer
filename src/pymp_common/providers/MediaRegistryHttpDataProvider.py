
from typing import Dict
from typing import Union
import requests
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.dataaccess.http_request_factory import http_request_factory
from pymp_common.dto.MediaRegistry import MediaInfo, ServiceInfo


class MediaRegistryHttpDataProvider(MediaRegistryDataProvider):
    def __init__(self, serviceinfo: ServiceInfo):
        self.status = True
        self.serviceinfo = serviceinfo
        self.readonly = True

    def __repr__(self) -> str:
        return "MediaRegistryHttpDataProvider()"

    def is_readonly(self) -> bool:
        return self.readonly

    def get_service_url(self) -> str:
        return self.serviceinfo.get_uri()

    def get_status(self) -> bool:
        return self.status

    def get_service_info(self, service_id: str) -> ServiceInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/service/{service_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return ServiceInfo(**registry_response.json())

    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/service")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return registry_response.json()

    def set_service_info(self, service_info: ServiceInfo):
        registry_request = http_request_factory.post(
            self.get_service_url(), "/registry/service", service_info)
        session = requests.Session()
        session.send(registry_request.prepare())

    def del_service_info(self, service_id) -> Union[int, None]:
        raise Exception("NOT IMPLEMENETED")

    def get_media_info(self, media_id: str) -> MediaInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/media/{media_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return MediaInfo(**registry_response.json())

    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/media")
        session = requests.Session()
        session.send(registry_request.prepare())
        return registry_request.json()

    def set_media_info(self, media_info: MediaInfo) -> bool:
        registry_request = http_request_factory.post(
            self.get_service_url(), "/registry/media", media_info)
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return registry_response.json()

    def del_service_media(self, service_id: str, media_id: str) -> bool:
        raise Exception("NOT IMPLEMENETED")
