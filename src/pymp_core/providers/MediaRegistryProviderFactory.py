import logging
from typing import List
from pymp_core.abstractions.providers import DataProvider, MediaRegistryDataProvider
from pymp_core.app.config import PympServerRoles
from pymp_core.app.config_factory import ConfigFactory
from pymp_core.providers.MediaRegistryHttpDataProvider import MediaRegistryHttpDataProvider
from pymp_core.providers.MediaRegistryRedisDataProvider import MediaRegistryRedisDataProvider


def get_media_registry_providers(wants_write_access: bool = False) -> List[MediaRegistryHttpDataProvider]:
    logging.info("GETTING MEDIA REGISTRY PROVIDERS")
    media_registry_providers = []

    # configure self
    media_registry_redis_data_provider = MediaRegistryRedisDataProvider()
    if media_registry_redis_data_provider.check_data_provider(wants_write_access):
        media_registry_providers.append(media_registry_redis_data_provider)

    # configure hardcoded services
    service_configs = ConfigFactory().create_service_configs()
    for service_config in service_configs:
        if service_config.service_roles & PympServerRoles.FFMPEG_SVC: 
            media_registry_http_data_provider = MediaRegistryHttpDataProvider(service_config)
            if media_registry_http_data_provider.check_data_provider(wants_write_access):
                media_registry_providers.append(media_registry_http_data_provider)

    return media_registry_providers
