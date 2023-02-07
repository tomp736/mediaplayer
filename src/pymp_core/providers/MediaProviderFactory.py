import logging
from typing import List

from pymp_core.abstractions.providers import DataProvider, MediaDataProvider, MediaMetaProvider, MediaThumbProvider
from pymp_core.app.PympConfig import pymp_env
from pymp_core.dto.MediaRegistry import PympServiceType
from pymp_core.providers import MediaRegistryProviderFactory
from pymp_core.providers.MetaRedisDataProvider import MetaRedisDataProvider
from pymp_core.providers.ThumbRedisDataProvider import ThumbRedisDataProvider
from pymp_core.providers.MediaFileDataProvider import MediaFileDataProvider
from pymp_core.providers.MediaHttpDataProvider import MediaHttpDataProvider


def get_data_providers(service_id, wants_write_access: bool = False) -> List[MediaDataProvider]:
    logging.info("GETTING MEDIA DATA PROVIDERS")
    media_providers = []

    this_service_info = pymp_env.get_this_service_info()

    # add local data provider
    if PympServiceType(this_service_info.service_type) & PympServiceType.MEDIA_SVC:
        media_file_data_provider = MediaFileDataProvider()
        if check_data_provider(wants_write_access, media_file_data_provider):
            media_providers.append(media_file_data_provider)
            
    # add data provider from media_registry
    else:
        media_registry_provider = MediaRegistryProviderFactory.get_media_registry_providers()[0]
        if media_registry_provider:
            service_info = media_registry_provider.get_service_info(service_id)
            if service_info and service_info.is_valid():
                media_provider = MediaHttpDataProvider(service_info)
                if check_data_provider(wants_write_access, media_provider):
                    media_providers.append(media_provider)

    # add hardcoded service
    env_service_info = pymp_env.get_service_info(PympServiceType.MEDIA_SVC)
    if env_service_info.is_valid() and env_service_info.service_id == service_id:
        media_http_data_provider = MediaHttpDataProvider(env_service_info)
        if check_data_provider(wants_write_access, media_http_data_provider):
            media_providers.append(media_http_data_provider)

    return media_providers

def get_thumb_providers(wants_write_access: bool = False) -> List[MediaThumbProvider]:
    logging.info("GETTING MEDIA THUMB PROVIDERS")
    thumb_providers = []

    thumb_provider = ThumbRedisDataProvider()
    if check_data_provider(wants_write_access, thumb_provider):
        thumb_providers.append(thumb_provider)

    return thumb_providers

def get_meta_providers(wants_write_access: bool = False) -> List[MediaMetaProvider]:
    logging.info("GETTING MEDIA META PROVIDERS")
    meta_providers = []

    meta_provider = MetaRedisDataProvider()
    if check_data_provider(wants_write_access, meta_provider):
        meta_providers.append(meta_provider)

    return meta_providers


def check_data_provider(wants_write_access, data_provider: DataProvider) -> bool:
    if not data_provider.is_ready():
        logging.info(f"IGNORING {data_provider}: failed ready check")
        return False

    if wants_write_access and data_provider.is_readonly():
        logging.info(
            f"IGNORING {data_provider}: failed write_access check")
        return False

    return True
