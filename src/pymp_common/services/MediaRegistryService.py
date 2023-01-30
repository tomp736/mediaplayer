import logging
from typing import Dict

from pymp_common.providers.MediaProviderFactory import MediaProviderFactory
from pymp_common.providers.MediaRegistryProviderFactory import MediaRegistryProviderFactory
from pymp_common.utils.RepeatTimer import RepeatTimer


class MediaRegistryService():    
    def __init__(self) -> None:
        self.mediaRegistryProvider = MediaRegistryProviderFactory.create_instance()
        
    def printServiceInfo(self):
        logging.info("MediaRegistryService")
        logging.info(type(self.mediaRegistryProvider).__name__)
        
    def loginfo(self, message:str):
        logging.info(f" --- MEDIAREGISTRYSERVICE --- {message}")
        
    def register(self, serviceId, scheme, host, port):
        self.loginfo("register")
        return self.mediaRegistryProvider.register(serviceId, scheme, host, port)
        
    def register_(self, serviceInfo: Dict[str,str]):
        self.loginfo("register")
        return self.mediaRegistryProvider.register_(serviceInfo)
        
    def getMediaServices(self) -> Dict[str, str]:
        self.loginfo("getMediaServices")
        return self.mediaRegistryProvider.getMediaServices() 
        
    def getMediaService(self, mediaId) -> str:
        self.loginfo("getMediaServices")
        return self.mediaRegistryProvider.getMediaService(mediaId)   
        
    def getMediaIndex(self):
        self.loginfo("getMediaIndex")
        return self.mediaRegistryProvider.getMediaIndex()     
        
    def watchServices(self):        
        self.timer = RepeatTimer(60, self.update_media_services)
        self.timer.start()   
            
    def update_media_services(self):
        self.loginfo("START UPDATE MEDIA SERVICES")        
        mediaServices = self.mediaRegistryProvider.getMediaServices()        
        if not mediaServices:
            return
        
        self.loginfo(f"{mediaServices}")
            
        for mediaServiceId in mediaServices:
            media_svc_media_ids = self.check_media_service(mediaServiceId)
            self.check_media_sources(mediaServiceId, media_svc_media_ids)            

    def check_media_service(self, serviceId):
        self.loginfo(f"CHECKING SERVICE FOR {serviceId}")
        media_svc_media_ids = []               
        try:
            mediaProvider = MediaProviderFactory.create_instance(serviceId)
            if mediaProvider:
                status = mediaProvider.get_status()
                if status:
                    media_svc_media_ids = mediaProvider.get_mediaIds() 
                    logging.info(f"MediaProvider {serviceId} passes status check.")                         
                else:
                    logging.info(f"MediaProvider {serviceId} fails status check.")   
                    self.mediaRegistryProvider.remove(serviceId)     
            else:
                logging.info(f"MediaProvider {serviceId} is None.")                
        except Exception as ex:
            logging.info(ex)
            self.mediaRegistryProvider.remove(serviceId)
        return media_svc_media_ids

    def check_media_sources(self, serviceId, mediaIds):
        self.loginfo(f"CHECKING SOURCES FOR {serviceId}")
        self.loginfo(f"{serviceId} REPORTED {mediaIds}")
        
        registry_media = self.mediaRegistryProvider.getMediaIndex()        
        if registry_media is None:
            return
        
        redis_svc_media_ids = []
        for registry_mediaId in registry_media:
            if registry_media[registry_mediaId] == serviceId:
                redis_svc_media_ids.append(registry_mediaId)
        
        for registryMediaID in redis_svc_media_ids:       
            # delete from redis if media_svc no longer has the media
            if not mediaIds.__contains__(registryMediaID):
                logging.info(f"DELETING: {registryMediaID}")
                self.mediaRegistryProvider.removeMedia(registryMediaID)
                continue
                        
            # if media source for media  has changed, update redis
            if not registry_media[registryMediaID] == serviceId:
                logging.info(f"UPDATING: {registryMediaID}")
                self.mediaRegistryProvider.registerMedia(registryMediaID, serviceId)
                continue
                    
        # Update all 
        for mediaId in mediaIds:           
            logging.info(f"ADDING: {mediaId}")     
            self.mediaRegistryProvider.registerMedia(mediaId, serviceId)