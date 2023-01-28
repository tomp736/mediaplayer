from abc import ABC, abstractmethod
from typing import Union


class MediaChunk():
    def __init__(self, chunk, startByte=0, endByte=0, fileSize=0) -> None:
        self.chunk = chunk
        self.startByte = startByte
        self.endByte = endByte
        self.fileSize = fileSize

    def toContentRangeHeader(self) -> str:
        return 'bytes {0}-{1}/{2}'.format(self.startByte, self.endByte, self.fileSize)


class MediaProvider(ABC):
    @abstractmethod
    def get_media_uri(self) -> Union[str, None]:
        pass

    @abstractmethod
    def get_media_list(self):
        pass

    @abstractmethod
    def get_media_chunk(self, id, startByte=0, endByte=None) -> Union[MediaChunk, None]:
        pass
