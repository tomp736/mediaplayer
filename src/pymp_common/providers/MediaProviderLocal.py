import logging
import os
import uuid
from typing import IO, Dict, Union

from pymp_common.app.PympConfig import pymp_env
from pymp_common.abstractions.providers import MediaProvider, MediaChunk


class MediaProviderLocal(MediaProvider):
    def __init__(self):
        self.index = {}
        self.mediapath = "/app/media"
        self.indexpath = "/app/index"

    def get_media_uri(self, media_id: str) -> Union[str, None]:
        return os.path.join(self.indexpath, media_id)

    def get_media_list(self):
        ids = []
        for id in self.index.keys():
            ids.append(id)
        return ids

    def saveMedia(self, stream: IO[bytes]):
        fullpath = os.path.join(self.mediapath, "output_file") 
        
        with open(fullpath, "bw") as f:
            chunk_size = 4096
            while True:
                chunk = stream.read(chunk_size)
                if len(chunk) == 0:
                    return 
                f.write(chunk)

    def get_media_chunk(self, id, byte1: int, byte2=None) -> Union[MediaChunk, None]:
        if self.index.__contains__(id):
            mediafile = f"{self.indexpath}/{id}"
            if not mediafile or not os.path.isfile(mediafile):
                raise OSError(f"no such file: {mediafile}")

            file_size = os.stat(mediafile).st_size

            start, length = self.get_chunk_info(file_size, byte1, byte2)
            with open(mediafile, 'rb') as f:
                f.seek(start)
                chunk = f.read(length)
                
            MediaChunk(chunk, start, start + length - 1, file_size)
        return None

    def read_index(self) -> Dict[str, str]:
        fs_indexfiles = self.read_indexfiles()
        index = {}

        for indexfile in fs_indexfiles:
            if os.path.islink(indexfile):
                mediafile = os.path.realpath(indexfile)
                id = os.path.basename(indexfile)
                index[id] = mediafile

        return index

    def update_index(self):
        fs_indexfiles = self.read_indexfiles()
        fs_mediafiles = self.read_mediafiles()
        index = {}

        logging.info(fs_indexfiles)
        logging.info(fs_mediafiles)

        for fs_indexfile in fs_indexfiles:
            islink = os.path.islink(fs_indexfile)
            exists = os.path.exists(fs_indexfile)
            if islink and exists:
                realpath = os.path.realpath(fs_indexfile)
                index_basename = os.path.basename(fs_indexfile)
                media_basename = os.path.basename(realpath)
                index[index_basename] = media_basename

                logging.info(realpath)
                if (fs_mediafiles.__contains__(realpath)):
                    logging.info(f" -- INDEX OK -- : {realpath}")
                    fs_mediafiles.remove(realpath)
            else:
                os.remove(fs_indexfile)

        for fs_mediafile in fs_mediafiles:
            index_basename = str(uuid.uuid4())
            media_basename = os.path.basename(fs_mediafile)
            logging.info(f" -- ADDING -- {index_basename} = {media_basename}")
            os.symlink(f"../media/{media_basename}",
                       f"{self.indexpath}/{index_basename}")
            index[index_basename] = media_basename

        logging.info(index)
        self.index = index

    def read_mediafiles(self):
        file_list = []
        for filename in os.listdir(self.mediapath):
            filepath = os.path.join(self.mediapath, filename)
            if os.path.isfile(filepath):
                file_list.append(filepath)
        return file_list

    def read_indexfiles(self):
        file_list = []
        for filename in os.listdir(self.indexpath):
            filepath = os.path.join(self.indexpath, filename)
            if os.path.isfile(filepath):
                file_list.append(filepath)
        return file_list

    def get_chunk_info(self, file_size: int, byte1: int, byte2=None):
        start = 0
        if byte1 < file_size:
            start = byte1

        length = file_size - start
        if byte2:
            length = byte2 + 1 - byte1

        if length > int(pymp_env.get("MEDIA_CHUNK_SIZE")):
            length = int(pymp_env.get("MEDIA_CHUNK_SIZE"))

        return start, length
