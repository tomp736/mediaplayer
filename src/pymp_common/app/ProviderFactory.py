
import logging
from typing import List
from pymp_common.dto.MediaRegistry import PympServiceType
from pymp_common.app.PympConfig import pymp_env

from pymp_common.abstractions.providers import FfmpegDataProvider, MediaDataProvider, MetaDataProvider, ThumbDataProvider
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.providers.MediaFileDataProvider import MediaFileDataProvider
from pymp_common.providers.MediaHttpDataProvider import MediaHttpDataProvider
from pymp_common.providers.MediaRegistryRedisDataProvider import MediaRegistryRedisDataProvider
from pymp_common.providers.MediaRegistryHttpDataProvider import MediaRegistryHttpDataProvider
from pymp_common.providers.FfmpegHttpDataProvider import FfmpegHttpDataProvider
from pymp_common.providers.FfmpegFileDataProvider import FfmpegFileDataProvider

from pymp_common.providers.MetaRedisDataProvider import MetaRedisDataProvider
from pymp_common.providers.ThumbRedisDataProvider import ThumbRedisDataProvider


def get_media_registry_providers() -> List[MediaRegistryDataProvider]:
    logging.info("GETTING MEDIA REGISTRY PROVIDERS")
    media_registry_providers = []

    env_media_registry_service_info = pymp_env.get_service_info(
        PympServiceType.MEDIAREGISTRY_SVC)

    media_registry_redis_data_provider = MediaRegistryRedisDataProvider()
    logging.info(media_registry_redis_data_provider)
    if media_registry_redis_data_provider.is_ready():
        media_registry_providers.append(media_registry_redis_data_provider)

    media_registry_http_data_provider = MediaRegistryHttpDataProvider(
        env_media_registry_service_info)
    logging.info(media_registry_http_data_provider)
    if media_registry_http_data_provider.is_ready():
        media_registry_providers.append(media_registry_http_data_provider)

    return media_registry_providers


def get_media_providers(service_id) -> List[MediaDataProvider]:
    logging.info("GETTING MEDIA PROVIDERS")
    media_providers = []

    this_service_info = pymp_env.get_this_service_info()

    # add local data provider
    if PympServiceType(this_service_info.service_type) & PympServiceType.MEDIA_SVC:
        media_file_data_provider = MediaFileDataProvider()
        logging.info(media_file_data_provider)
        if media_file_data_provider.is_ready():
            media_providers.append(media_file_data_provider)
    # add data provider from media_registry
    else:
        media_registry_providers = get_media_registry_providers()
        media_registry_provider = None
        for provider in media_registry_providers:
            logging.info(media_registry_providers)
            if provider.is_ready():
                media_registry_provider = provider
                break

        if media_registry_provider:
            service_info = media_registry_provider.get_service_info(service_id)
            if service_info and service_info.is_valid():
                media_provider = MediaHttpDataProvider(service_info)
                logging.info(media_provider)
                if media_provider.is_ready():
                    media_providers.append(media_provider)

    # add hardcoded service
    env_service_info = pymp_env.get_service_info(PympServiceType.MEDIA_SVC)
    if env_service_info.is_valid() and env_service_info.service_id == service_id:
        media_http_data_provider = MediaHttpDataProvider(env_service_info)
        logging.info(media_http_data_provider)
        if media_http_data_provider.is_ready():
            media_providers.append(media_http_data_provider)

    return media_providers


def get_thumb_providers() -> List[ThumbDataProvider]:
    logging.info("GETTING THUMB PROVIDERS")
    thumb_providers = []

    thumb_provider = ThumbRedisDataProvider()
    logging.info(thumb_provider)
    if thumb_provider.is_ready():
        thumb_providers.append(thumb_provider)

    return thumb_providers


def get_meta_providers() -> List[MetaDataProvider]:
    logging.info("GETTING META PROVIDERS")
    meta_providers = []

    meta_provider = MetaRedisDataProvider()
    logging.info(meta_provider)
    if meta_provider.is_ready():
        meta_providers.append(meta_provider)

    return meta_providers


def get_ffmpeg_providers() -> List[FfmpegDataProvider]:
    logging.info("GETTING FFMPEG PROVIDERS")
    ffmpeg_providers = []

    if pymp_env.is_this_service_type(PympServiceType.FFMPEG_SVC):
        ffmpeg_provider = FfmpegFileDataProvider()
        logging.info(ffmpeg_provider)
        if ffmpeg_provider.is_ready():
            ffmpeg_providers.append(ffmpeg_provider)

    ffmpeg_provider = FfmpegHttpDataProvider(
        pymp_env.get_service_info(PympServiceType.FFMPEG_SVC))
    logging.info(ffmpeg_provider)
    if ffmpeg_provider.is_ready():
        ffmpeg_providers.append(ffmpeg_provider)

    return ffmpeg_providers
