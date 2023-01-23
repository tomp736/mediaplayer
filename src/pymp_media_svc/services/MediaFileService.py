
import requests
from pymp_common.app.PympConfig import pymp_env

from typing import Dict
import os
import logging


class MediaFileService:

    @staticmethod
    def get_media_indexes():
        media_path_dictionary = {}
        media_size_dictionary = {}

        for path in os.listdir("/app/videos"):
            file_path = os.path.join("/app/videos", path)
            logging.info(file_path)
            if os.path.isfile(file_path):
                media_key = os.path.basename(os.readlink(file_path))
                media_size = os.stat(file_path).st_size

                logging.info(f"{media_key}={file_path}")
                media_path_dictionary[media_key] = file_path
                media_size_dictionary[media_key] = media_size

        return (media_path_dictionary, media_size_dictionary)

    @staticmethod
    def get_media_chunk(media_path: str, byte1: int, byte2=None):
        if not os.path.isfile(media_path):
            raise OSError(f"no such file: {media_path}")
        file_size = os.stat(media_path).st_size

        start, length = MediaFileService.get_chunk_info(
            file_size, byte1, byte2)
        with open(media_path, 'rb') as f:
            f.seek(start)
            chunk = f.read(length)

        return chunk, start, length, file_size

    @staticmethod
    def get_chunk_info(file_size: int, byte1: int, byte2=None):
        start = 0
        if byte1 < file_size:
            start = byte1

        length = file_size - start
        if byte2:
            length = byte2 + 1 - byte1

        if length > int(pymp_env.get("MEDIA_CHUNK_SIZE")):
            length = int(pymp_env.get("MEDIA_CHUNK_SIZE"))

        return start, length
