
import json
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
        readonly = self.is_readonly()
        ready = self.is_readonly()
        return f"MediaRegistryHttpDataProvider({readonly},{ready})"

    def is_readonly(self) -> bool:
        return self.readonly

    def get_service_url(self) -> str:
        return self.serviceinfo.get_uri()

    def is_ready(self) -> bool:
        return self.status

    def get_service_info(self, service_id: str) -> ServiceInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/service/{service_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return ServiceInfo.from_json(registry_response.json())

    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/service")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        json_datas = registry_response.json()

        service_infos = {}
        for json_data in json_datas:
            service_info = ServiceInfo.from_json(json_data)
            service_infos[service_info.service_id] = service_info
        return service_infos

    def set_service_info(self, service_info: ServiceInfo) -> bool:
        registry_request = http_request_factory.post_json(
            self.get_service_url(), "/registry/service", service_info)
        session = requests.Session()
        session.send(registry_request.prepare())
        return True

    def del_service_info(self, service_id: str) -> int:
        raise Exception("NOT IMPLEMENETED")

    def get_media_info(self, media_id: str) -> MediaInfo:
        registry_request = http_request_factory.get(
            self.get_service_url(), f"/registry/media/{media_id}")
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        jdata = registry_response.json()

        media_info = MediaInfo()
        media_info.media_id = media_id
        media_info.service_id = jdata["service_id"]
        return media_info

    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        registry_request = http_request_factory.get(
            self.get_service_url(), "/registry/media")
        session = requests.Session()
        session.send(registry_request.prepare())
        return registry_request.json()

    def set_media_info(self, media_info: MediaInfo) -> bool:
        registry_request = http_request_factory.post_json(
            self.get_service_url(), "/registry/media", media_info)
        session = requests.Session()
        registry_response = session.send(registry_request.prepare())
        return registry_response.json()

    def del_media_info(self, media_id: str) -> bool:
        raise Exception("NOT IMPLEMENETED")
