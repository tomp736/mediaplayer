import logging
from typing import List
from pymp_core.abstractions.providers import DataProvider, MediaRegistryDataProvider
from pymp_core.app.PympConfig import pymp_env
from pymp_core.dto.MediaRegistry import PympServiceType
from pymp_core.providers.MediaRegistryHttpDataProvider import MediaRegistryHttpDataProvider
from pymp_core.providers.MediaRegistryRedisDataProvider import MediaRegistryRedisDataProvider


def get_media_registry_providers(wants_write_access: bool = False) -> List[MediaRegistryHttpDataProvider]:
    logging.info("GETTING MEDIA REGISTRY PROVIDERS")
    media_registry_providers = []

    env_media_registry_service_info = pymp_env.get_service_info(
        PympServiceType.MEDIAREGISTRY_SVC)

    media_registry_redis_data_provider = MediaRegistryRedisDataProvider()
    if check_data_provider(wants_write_access, media_registry_redis_data_provider):
        media_registry_providers.append(media_registry_redis_data_provider)

    media_registry_http_data_provider = MediaRegistryHttpDataProvider(
        env_media_registry_service_info)
    if check_data_provider(wants_write_access, media_registry_http_data_provider):
        media_registry_providers.append(media_registry_http_data_provider)

    return media_registry_providers


def check_data_provider(wants_write_access, data_provider: DataProvider) -> bool:
    if not data_provider.is_ready():
        logging.info(f"IGNORING {data_provider}: failed ready check")
        return False

    if wants_write_access and data_provider.is_readonly():
        logging.info(
            f"IGNORING {data_provider}: failed write_access check")
        return False

    return True