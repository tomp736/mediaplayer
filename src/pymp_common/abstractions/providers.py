from abc import ABC
from abc import abstractmethod
import re
from typing import IO
from typing import Dict
from typing import List
from typing import Union


class MediaChunk():
    def __init__(self, chunk, startByte=0, endByte=None, fileSize=None) -> None:
        self.chunk = chunk
        self.sByte = startByte
        self.eByte = endByte
        self.fileSize = fileSize

    def toContentRangeHeader(self) -> str:
        return 'bytes {0}-{1}/{2}'.format(self.sByte, self.eByte, self.fileSize)

    def loadContentRangeHeader(self, headerValue: str):
        sByte, eByte, fileSize = MediaChunk.parse_range_header(headerValue)
        self.sByte = sByte
        self.eByte = eByte
        self.fileSize = fileSize

    @staticmethod
    def parse_range_header(headerValue: str):
        sByte, eByte, fileSize = 0, 0, 0
        if headerValue:
            match = re.search(r'(\d+)-(\d*)\/?(\d*)', headerValue)
            if match is not None:
                groups = match.groups()
                if groups[0]:
                    sByte = int(groups[0])
                if groups[1]:
                    eByte = int(groups[1])
                if groups[2]:
                    fileSize = int(groups[2])

        return sByte, eByte, fileSize


class MediaProvider(ABC):
    @abstractmethod
    def get_status(self) -> bool:
        pass

    @abstractmethod
    def get_media_uri(self, media_id: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_mediaIds(self) -> List[str]:
        pass

    @abstractmethod
    def get_media_chunk(self, mediaId, startByte=0, endByte=None) -> Union[MediaChunk, None]:
        pass

    @abstractmethod
    def save_media(self, name: str, stream: IO[bytes]):
        pass

    @abstractmethod
    def update_index(self):
        pass


class FfmpegProvider(ABC):
    @abstractmethod
    def gen_thumb(self, mediaId) -> bool:
        pass

    @abstractmethod
    def gen_meta(self, mediaId) -> bool:
        pass

    @abstractmethod
    def get_thumb(self, mediaId) -> Union[bytes, None]:
        pass

    @abstractmethod
    def get_meta(self, mediaId) -> Union[bytes, None]:
        pass


class MediaRegistryProvider(ABC):
    @abstractmethod
    def register_(self, serviceInfo: Dict) -> bool:
        pass

    @abstractmethod
    def register(self, serviceId, scheme, host, port) -> bool:
        pass

    @abstractmethod
    def registerMedia(self, serviceId, mediaId) -> bool:
        pass

    @abstractmethod
    def remove(self, serviceId: str) -> Union[int, None]:
        pass

    @abstractmethod
    def removeMedia(self, mediaId: str) -> bool:
        pass

    @abstractmethod
    def getMediaIndex(self) -> Union[Dict[str, str], None]:
        pass

    @abstractmethod
    def getMediaServices(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def getMediaService(self, mediaId: str) -> str:
        pass
