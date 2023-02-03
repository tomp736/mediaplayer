import logging
from typing import List
from typing import Union
import io
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.abstractions.providers import MediaDataProvider
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dto.MediaRegistry import PympServiceType
from pymp_common.utils.RepeatTimer import RepeatTimer
from pymp_common.app.ProviderFactory import get_media_providers, get_media_registry_providers, get_meta_providers, get_thumb_providers


class MediaService:

    def __init__(self) -> None:
        self.register_timer = RepeatTimer(60, self.register)

    def __repr__(self) -> str:
        return "MediaService()"

    def get_media_provider(self, media_id) -> Union[MediaDataProvider, None]:
        # check if local
        local_service_id = pymp_env.get_this_service_info().service_id
        for media_provider in get_media_providers(local_service_id):
            logging.info(media_provider)
            if(media_id in media_provider.get_media_ids()):
                return media_provider
            
        media_registry_providers = get_media_registry_providers()
        media_registry_provider = media_registry_providers[0]
        media_info = media_registry_provider.get_media_info(media_id)
        if media_info:
            for media_provider in get_media_providers(media_info.service_id):
                logging.info(media_provider)
                if(media_id in media_provider.get_media_ids()):
                    return media_provider            
            
        return None

    def get_media_chunk(self, media_id, start_byte: int = 0, end_byte: int = 0) -> Union[MediaChunk, None]:
        media_provider = self.get_media_provider(media_id)
        if media_provider:
            return media_provider.get_media_chunk(media_id, start_byte, end_byte)
        return None

    def get_media_thumb(self, media_id) -> Union[io.BytesIO, None]:
        return get_thumb_providers()[0].get_thumb(media_id)

    def get_media_meta(self, media_id) -> Union[str, None]:
        return get_meta_providers()[0].get_meta(media_id)
    
    # TODO
    # def save_media(self, name: str, stream: IO[bytes]):
    #     media_provider = self.get_media_provider(media_id)
    #     if media_provider:
    #         return media_provider.save_media(name, stream)

    def get_media_ids(self) -> List[str]:
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.MEDIA_SVC:
            media_provider = get_media_providers(service_info.service_id)[0]
            return media_provider.get_media_ids()
        return []

    def watch_media(self):
        self.register_timer.start()

    def update_index(self) -> None:
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.MEDIA_SVC:
            media_provider = get_media_providers(service_info.service_id)[0]
            media_provider.update_index()

    def register(self):
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.MEDIA_SVC:            
            self.update_index()
            media_registry_providers = get_media_registry_providers()
            media_registry_provider = media_registry_providers[0]
            logging.info(media_registry_provider.__repr__())
            media_registry_provider.set_service_info(service_info)
