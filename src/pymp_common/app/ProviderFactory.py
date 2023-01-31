import logging
from typing import Union
from pymp_common.abstractions.providers import MediaProvider
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.providers.MediaProviderLocal import MediaProviderLocal
from pymp_common.providers.MediaProviderRemote import MediaProviderRemote
from pymp_common.providers.MediaRegistryProviderLocal import MediaRegistryProviderLocal
from pymp_common.providers.MediaRegistryProviderRemote import MediaRegistryProviderRemote
from pymp_common.providers.FfmpegProviderLocal import FfmpegProviderLocal
from pymp_common.providers.FfmpegProviderRemote import FfmpegProviderRemote

from pymp_common.app.PympConfig import pymp_env
from pymp_common.app.PympConfig import PympServer


def get_media_registry_provider() -> MediaRegistryProvider:
    if pymp_env.get_servertype() & PympServer.MEDIAREGISTRY_SVC:
        logging.info("Creating MediaRegistryProviderLocal")
        return MediaRegistryProviderLocal()
    else:
        logging.info(f"Creating MediaRegistryProviderRemote")
        return MediaRegistryProviderRemote()


def get_media_provider(serviceId) -> MediaProvider:
    if pymp_env.get_servertype() & PympServer.MEDIA_SVC and pymp_env.get("SERVER_ID") == serviceId:
        return MediaProviderLocal()
    return MediaProviderRemote(serviceId)


def get_ffmpeg_provider():
    if pymp_env.get_servertype() & PympServer.FFMPEG_SVC:
        logging.info("Creating FfmpegProviderLocal")
        return FfmpegProviderLocal()
    else:
        logging.info("Creating FfmpegProviderRemote")
        return FfmpegProviderRemote()
