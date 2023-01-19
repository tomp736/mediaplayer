
from pymp_common.services.ConfigService import ConfigService
from pymp_common.services.RedisServices import MediaPathService, MediaSizeService

from typing import Dict
import os
import logging

class MediaFileService:
    
    @staticmethod
    def get_media_indexes():
        media_path_dictionary = {}
        media_size_dictionary = {}
              
        for path in os.listdir("/app/videos"):
            file_path=os.path.join("/app/videos", path)
            logging.info(file_path)
            if os.path.isfile(file_path):    
                media_key = os.path.basename(os.readlink(file_path))
                media_size = os.stat(file_path).st_size
                
                logging.info(f"{media_key}={file_path}")
                media_path_dictionary[media_key] = file_path
                media_size_dictionary[media_key] = media_size              
                
        return (media_path_dictionary, media_size_dictionary)
    
    @staticmethod    
    def index_media():          
        media_path_dictionary, media_size_dictionary = MediaFileService.get_media_indexes() 
               
        media_path_c = MediaPathService.get_redis()
        MediaPathService.set_media_path_index(media_path_c, media_path_dictionary)     
        
        media_size_c = MediaSizeService.get_redis()
        MediaSizeService.set_media_size_index(media_size_c, media_size_dictionary)

    @staticmethod
    def get_media_chunk(media_path:str, id:str, sByte:int, eByte):
        start, length, file_size = MediaFileService.get_chunk_info(media_path, sByte, eByte)
        with open(media_path, 'rb') as f:
            f.seek(start)
            chunk = f.read(length)
        
        return chunk, start, length, file_size

    @staticmethod
    def get_chunk_info(file_path, byte1:int, byte2=None):
        if not os.path.isfile(file_path):
            raise OSError(f"no such file: {file_path}")

        file_size = os.stat(file_path).st_size
        start = 0
        if byte1 < file_size:
            start = byte1

        length = file_size - start
        if byte2:
            length = byte2 + 1 - byte1

        if length > ConfigService.chunk_size:
            length = ConfigService.chunk_size
            
        return start, length, file_size