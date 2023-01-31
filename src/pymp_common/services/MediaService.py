import logging
from typing import IO
from typing import List
from typing import Union
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.abstractions.providers import MediaProvider
from pymp_common.app.PympConfig import pymp_env
from pymp_common.utils.RepeatTimer import RepeatTimer


class MediaService:
    def __init__(self, mediaRegistryProvider: MediaRegistryProvider, mediaProvider: MediaProvider) -> None:
        self.mediaRegistryProvider = mediaRegistryProvider
        self.mediaProvider = mediaProvider
        
    def __repr__(self) -> str:
        return f"MediaService({self.mediaRegistryProvider},{self.mediaProvider})"

    def get_media_chunk(self, mediaId, sByte: int = 0, eByte: int = 0, fileSize: int = 0) -> Union[MediaChunk, None]:
        return self.mediaProvider.get_media_chunk(mediaId, sByte, eByte)

    def save_media(self, name: str, stream: IO[bytes]):
        return self.mediaProvider.save_media(name, stream)

    def get_media_ids(self) -> List[str]:
        return self.mediaProvider.get_media_ids()

    def update_index(self) -> None:
        self.mediaProvider.update_index()

    def watch_media(self):
        self.registerTimer = RepeatTimer(60, self.register)
        self.registerTimer.start()

    def register(self):
        server_id = pymp_env.get("SERVER_ID")
        service_scheme = pymp_env.get("MEDIA_SVC_SCHEME")
        service_host = pymp_env.get("MEDIA_SVC_HOST")
        service_port = pymp_env.get("MEDIA_SVC_PORT")
        self.update_index()
        self.mediaRegistryProvider.register(server_id, service_scheme, service_host, service_port)
