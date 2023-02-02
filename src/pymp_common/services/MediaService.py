import logging
from typing import IO
from typing import List
from typing import Union
from pymp_common.abstractions.providers import MediaChunk
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.abstractions.providers import MediaDataProvider
from pymp_common.app.PympConfig import pymp_env
from pymp_common.utils.RepeatTimer import RepeatTimer


class MediaService:
    def __init__(self, MediaRegistryDataProvider: MediaRegistryDataProvider, MediaDataProvider: MediaDataProvider) -> None:
        self.MediaRegistryDataProvider = MediaRegistryDataProvider
        self.MediaDataProvider = MediaDataProvider
        
    def __repr__(self) -> str:
        return f"MediaService({self.MediaRegistryDataProvider},{self.MediaDataProvider})"

    def get_media_chunk(self, media_id, sByte: int = 0, eByte: int = 0, fileSize: int = 0) -> Union[MediaChunk, None]:
        return self.MediaDataProvider.get_media_chunk(media_id, sByte, eByte)

    def save_media(self, name: str, stream: IO[bytes]):
        return self.MediaDataProvider.save_media(name, stream)

    def get_media_ids(self) -> List[str]:
        return self.MediaDataProvider.get_media_ids()

    def update_index(self) -> None:
        self.MediaDataProvider.update_index()

    def watch_media(self):
        self.registerTimer = RepeatTimer(60, self.register)
        self.registerTimer.start()

    def register(self):
        server_id = pymp_env.get("SERVER_ID")
        service_proto = pymp_env.get("MEDIA_SVC_PROTO")
        service_host = pymp_env.get("MEDIA_SVC_HOST")
        service_port = pymp_env.get("MEDIA_SVC_PORT")
        self.update_index()
        self.MediaRegistryDataProvider.register(server_id, service_proto, service_host, service_port)
