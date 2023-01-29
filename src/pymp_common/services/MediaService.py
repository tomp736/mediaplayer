import logging
from typing import IO, List, Union
from pymp_common.abstractions.providers import MediaChunk

from pymp_common.providers.MediaRegistryProviderFactory import MediaRegistryProviderFactory
from pymp_common.providers.MediaProviderFactory import MediaProviderFactory
from pymp_common.utils.RepeatTimer import RepeatTimer
from pymp_common.app.PympConfig import pymp_env

class MediaService:
    def __init__(self) -> None:
        self.mediaRegistryProvider = MediaRegistryProviderFactory.create_instance()
    
    def get_media_chunk(self, mediaId, sByte: int=0, eByte:int=0, fileSize:int=0) -> Union[MediaChunk, None]:
        serviceId = self.mediaRegistryProvider.getMediaService(mediaId)
        mediaProvider = MediaProviderFactory.create_instance(serviceId)
        if mediaProvider:
            return mediaProvider.get_media_chunk(mediaId, sByte, eByte)
        return None
    
    def saveMedia(self, serviceId:str, name:str, stream: IO[bytes]) -> Union[MediaChunk, None]:
        mediaProvider = MediaProviderFactory.create_instance(serviceId)
        if mediaProvider:
            return mediaProvider.save_media(name, stream)
        return None

    def getMediaIds(self, serviceId:str) -> Union[List[str], None]:
        mediaProvider = MediaProviderFactory.create_instance(serviceId)
        if mediaProvider:
            return mediaProvider.get_mediaIds()
        return None

    def updateIndex(self, serviceId:str) -> None:
        mediaProvider = MediaProviderFactory.create_instance(serviceId)
        if mediaProvider:
            return mediaProvider.update_index()
        return None
    
    def watchMedia(self):  
        self.mediaRegistryProvider = MediaRegistryProviderFactory.create_instance()  
        self.mediaProvider = MediaProviderFactory.create_instance()      
        self.registerTimer = RepeatTimer(60, self.register_media_service)
        self.registerTimer.start()  
    
    def register_media_service(self):
        id = pymp_env.get("SERVER_ID")
        scheme = pymp_env.get("MEDIA_SVC_SCHEME")
        host = pymp_env.get("MEDIA_SVC_HOST")
        port = pymp_env.get("MEDIA_SVC_PORT")
        
        logging.info(f" --- MEDIASERVICE --- Registered {id} - {scheme} - {host} - {port}")
        if self.mediaProvider:
            self.mediaProvider.update_index()
        self.mediaRegistryProvider.register(id, scheme, host, port)