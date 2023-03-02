from abc import ABC
from abc import abstractmethod

import io

from typing import IO
from typing import Dict
from typing import List
from typing import Union

from pymp_core.dto.Media import MediaChunk
from pymp_core.dto.MediaRegistry import MediaInfo
from pymp_core.dto.MediaRegistry import ServiceInfo


class DataProvider(ABC):

    @abstractmethod
    def is_readonly(self) -> bool:
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        pass


class MediaDataProvider(DataProvider):

    @abstractmethod
    def get_media_uri(self, media_id: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_media_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_media_chunk(
        self,
        media_id,
        start_byte=0,
        end_byte=None
    ) -> Union[MediaChunk, None]:
        pass

    @abstractmethod
    def save_media(self, name: str, stream: IO[bytes]):
        pass

    @abstractmethod
    def update_index(self):
        pass


class FfmpegDataProvider(DataProvider):

    @abstractmethod
    def get_thumb(self, media_uri) -> Union[io.BytesIO, None]:
        pass

    @abstractmethod
    def get_meta(self, media_uri) -> Union[str, None]:
        pass


class MediaThumbProvider(DataProvider):

    @abstractmethod
    def get_thumb(self, media_id) -> Union[io.BytesIO, None]:
        pass

    @abstractmethod
    def set_thumb(self, media_id, thumb: io.BytesIO):
        pass
    
    @abstractmethod
    def has_thumb(self, media_id) -> bool:
        pass

    @abstractmethod
    def del_thumb(self, media_id):
        pass


class MediaMetaProvider(DataProvider):

    @abstractmethod
    def get_meta(self, media_id) -> Union[str, None]:
        pass

    @abstractmethod
    def set_meta(self, media_id, meta: str):
        pass
    
    @abstractmethod
    def has_meta(self, media_id) -> bool:
        pass

    @abstractmethod
    def del_meta(self, media_id):
        pass


class MediaRegistryDataProvider(DataProvider):

    # server_id => ServiceInfo
    @abstractmethod
    def get_service_info(self, server_id: str) -> ServiceInfo:
        pass

    @abstractmethod
    def get_all_service_info(self) -> Dict[str, ServiceInfo]:
        pass

    @abstractmethod
    def set_service_info(self, service_info: ServiceInfo) -> bool:
        pass

    @abstractmethod
    def del_service_info(self, server_id: str) -> int:
        pass

    # media_id -> MediaInfo
    @abstractmethod
    def get_media_info(self, media_id: str) -> MediaInfo:
        pass

    @abstractmethod
    def get_all_media_info(self) -> Dict[str, MediaInfo]:
        pass

    @abstractmethod
    def set_media_info(self, media_info: MediaInfo) -> bool:
        pass

    @abstractmethod
    def del_media_info(self, media_id: str) -> bool:
        pass
