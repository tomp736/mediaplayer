
import json
import logging
from typing import Dict
from typing import Union
import requests
from pymp_core.abstractions.providers import MediaRegistryDataProvider

from pymp_core.dataaccess.http_request_factory import http_request_factory
from pymp_core.decorators.prom import prom_count
from pymp_core.dto.MediaRegistry import MediaInfo, ServiceInfo


class MediaRegistryHttpDataProvider(MediaRegistryDataProvider):
    def __init__(self, serviceinfo: ServiceInfo):
        self.status = True
        self.serviceinfo = serviceinfo
        self.readonly = True

    def __repr__(self) -> str:
        readonly = self.is_readonly()
        ready = self.is_readonly()
        return f"MediaRegistryHttpDataProvider({readonly},{ready})"

    def is_readonly(self) -> bool:
        return self.readonly

    def get_service_url(self) -> str:
        return self.serviceinfo.get_uri()

    def is_ready(self) -> bool:
        return self.status

    @prom_count
    def get_service_info(self, service_id: str) -> ServiceInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/service/{service_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        response_json = registry_response.json()
        return ServiceInfo(**response_json)

    @prom_count
    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/service")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        response_json = registry_response.json()
        return {service_id: ServiceInfo(**service_info) for service_id, service_info in response_json.items()}

    @prom_count
    def set_service_info(self, service_info: ServiceInfo) -> bool:
        registry_request = http_request_factory.post_json(
            self.get_service_url(), "/registry/service", service_info.to_json())
        session = requests.Session()
        session.send(registry_request.prepare())
        return True

    @prom_count
    def del_service_info(self, service_id: str) -> int:
        raise Exception("NOT IMPLEMENETED")

    @prom_count
    def get_media_info(self, media_id: str) -> MediaInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/media/{media_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        response_json = registry_response.json()
        return MediaInfo(**response_json)

    @prom_count
    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/media")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        response_json = registry_response.json()
        return {media_id: MediaInfo(**media_info) for media_id, media_info in response_json.items()}

    @prom_count
    def set_media_info(self, media_info: MediaInfo) -> bool:
        registry_request = http_request_factory.post_json(
            self.get_service_url(), "/registry/media", media_info.to_json())
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return registry_response.json()

    @prom_count
    def del_media_info(self, media_id: str) -> bool:
        raise Exception("NOT IMPLEMENETED")
