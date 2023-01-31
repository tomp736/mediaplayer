import logging
from typing import IO
from typing import List
from typing import Union
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.app import ProviderFactory
from pymp_common.utils.RepeatTimer import RepeatTimer
from pymp_common.app.PympConfig import pymp_env


class MediaService:
    def __init__(self) -> None:
        self.mediaRegistryProvider = ProviderFactory.get_media_registry_provider()
        self.id = pymp_env.get("SERVER_ID")
        self.scheme = pymp_env.get("MEDIA_SVC_SCHEME")
        self.host = pymp_env.get("MEDIA_SVC_HOST")
        self.port = pymp_env.get("MEDIA_SVC_PORT")
        self.mediapath = pymp_env.get("MEDIA_SVC_MEDIAPATH")
        self.indexpath = pymp_env.get("MEDIA_SVC_INDEXPATH")

    def print_serviceinfo(self):
        logging.info("MediaService")
        logging.info(type(self.mediaRegistryProvider).__name__)

    def loginfo(self, message: str):
        logging.info(f" --- MEDIASERVICE --- {message}")

    def get_media_chunk(self, serviceId, mediaId, sByte: int = 0, eByte: int = 0, fileSize: int = 0) -> Union[MediaChunk, None]:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            return mediaProvider.get_media_chunk(mediaId, sByte, eByte)
        return None

    def save_media(self, serviceId: str, name: str, stream: IO[bytes]) -> Union[MediaChunk, None]:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            return mediaProvider.save_media(name, stream)
        return None

    def get_media_ids(self, serviceId: str) -> Union[List[str], None]:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            return mediaProvider.get_media_ids()
        return None

    def update_index(self, serviceId: str) -> None:
        mediaProvider = ProviderFactory.get_media_provider(serviceId)
        if mediaProvider:
            return mediaProvider.update_index()
        return None

    def watch_media(self):
        self.registerTimer = RepeatTimer(60, self.register_media_service)
        self.registerTimer.start()

    def register_media_service(self):
        logging.info(
            f" --- MEDIASERVICE --- Registered {self.id} - {self.scheme} - {self.host} - {self.port}")
        mediaProvider = ProviderFactory.get_media_provider(self.id)
        if mediaProvider:
            mediaProvider.update_index()
        self.mediaRegistryProvider.register(
            self.id, self.scheme, self.host, self.port)
