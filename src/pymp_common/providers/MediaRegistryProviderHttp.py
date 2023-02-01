
import logging
from typing import Dict
from typing import Union
import requests
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.dataaccess.http_request_factory import media_registry_request_factory
from pymp_common.dto.MediaRegistry import ServiceInfo


class MediaRegistryProviderHttp(MediaRegistryProvider):

    def __init__(self) -> None:
        super().__init__()
        self.is_readonly = True

    def __repr__(self) -> str:
        return "MediaRegistryProviderHttp()"

    def readonly(self):
        return self.is_readonly

    def get_status(self) -> bool:
        return True

    def get_service_info(self, service_id: str) -> ServiceInfo:
        registry_request = media_registry_request_factory.get_service_info(
            service_id)
        s = requests.Session()
        registry_response = s.send(registry_request.prepare())
        return ServiceInfo(**registry_response.json())

    def set_service_info(self, service_id, service_info: ServiceInfo):
        registry_request = media_registry_request_factory.set_service_info(
            service_info)
        s = requests.Session()
        return s.send(registry_request.prepare())

    def del_service_info(self, service_id) -> Union[int, None]:
        raise Exception("NOT IMPLEMENETED")

    def set_service_media(self, service_id, media_id):
        registry_request = media_registry_request_factory.set_service_media(
            service_id,
            media_id
        )
        s = requests.Session()
        return s.send(registry_request.prepare())

    def del_service_media(self, service_id: str, media_id: str) -> bool:
        raise Exception("NOT IMPLEMENETED")

    def get_service_media(self, service_id: Union[str, None] = None) -> Union[ServiceInfo, None]:
        registry_request = media_registry_request_factory.list_media()
        s = requests.Session()
        registry_response = s.send(registry_request.prepare())
        return registry_response.json()
