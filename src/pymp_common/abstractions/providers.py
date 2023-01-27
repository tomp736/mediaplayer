from abc import ABC, abstractmethod
import logging
import os
from typing import Dict, Union, List

import requests
from pymp_common.app.MediaDirectoryService import local_media
from pymp_common.app.PympConfig import PympServer, pymp_env
from pymp_common.dataaccess.http_request_factory import media_request_factory
from ..dataaccess.redis import media_service_da
from ..dataaccess.redis import media_source_da

class MediaProvider(ABC):
    @abstractmethod
    def get_media_list(self):
        pass

    @abstractmethod
    def get_media_chunk(self, id, startByte = 0, endByte = None):
        pass
    
class RemoteMediaProvider(MediaProvider):
    def __init__(self, media_service_id):        
        self.session = requests.Session() 
        self.media_service_id = media_service_id
        self.media_service_url = self.get_media_svc_url(media_service_id)
           
    def get_media_svc_url(self, media_service_id:str) -> Union[str ,None]:
        serviceinfo = media_service_da.hget(media_service_id)
        if serviceinfo:
            media_svc_scheme = serviceinfo["scheme"]
            media_svc_host = serviceinfo["host"]
            media_svc_port = serviceinfo["port"]
            return f"{media_svc_scheme}://{media_svc_host}:{media_svc_port}"         
        return None       
    
    def get_media_list(self) -> List[str]:     
        media_ids = []   
        if not self.media_service_url is None:
            apiRequest = media_request_factory._get_media_list_(self.media_service_url)
            apiResponse = self.session.send(apiRequest.prepare())
            media_ids = apiResponse.json()
        return media_ids

    def get_media_chunk(self, id, startByte = 0, endByte = None) -> Union[bytes ,None]:
        if not self.media_service_url is None:
            apiRequest = media_request_factory._get_media_(self.media_service_url, id, startByte, endByte)
            apiResponse = self.session.send(apiRequest.prepare())
            return apiResponse.content
        return None
    
class LocalMediaProvider(MediaProvider):
    def __init__(self):
        self.index = {}
        self.mediapath = "/app/media"
        self.indexpath = "/app/index"
    
    def get_media_list(self):
        ids=[]
        for id in self.index.keys():
            ids.append(id)
        return ids        

    def get_media_chunk(self, id, byte1: int, byte2=None):
        if self.index.__contains__(id):
            mediafile = f"{self.indexpath}/{id}"
            if not mediafile or not os.path.isfile(mediafile):
                raise OSError(f"no such file: {mediafile}")
                
            file_size = os.stat(mediafile).st_size

            start, length = self.get_chunk_info(
                file_size, byte1, byte2)
            with open(mediafile, 'rb') as f:
                f.seek(start)
                chunk = f.read(length)

            return chunk, start, length, file_size
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
                if(fs_mediafiles.__contains__(realpath)):
                    logging.info(f" -- INDEX OK -- : {realpath}")
                    fs_mediafiles.remove(realpath)
            else:
                os.remove(fs_indexfile)
                    
        for fs_mediafile in fs_mediafiles:
            index_basename = str(uuid.uuid4())
            media_basename = os.path.basename(fs_mediafile)
            logging.info(f" -- ADDING -- {index_basename} = {media_basename}") 
            os.symlink(f"../media/{media_basename}", f"{self.indexpath}/{index_basename}")
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
    
class MediaServiceFactory:
    
    @staticmethod
    def create_instance(media_service_id = None):
        if pymp_env.getServerType() & PympServer.MEDIA_SVC and media_service_id is None:
            return LocalMediaProvider()
        else:
            return RemoteMediaProvider(media_service_id)