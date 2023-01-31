import logging

from pymp_common.app import ProviderFactory
from pymp_common.utils.RepeatTimer import RepeatTimer

class FfmpegService:  
    def __init__(self) -> None:
        self.ffmpegProvider = ProviderFactory.getFfmpegProvider()
        self.mediaRegistryProvider = ProviderFactory.getMediaRegistryProvider()  
        
    def printServiceInfo(self):
        logging.info("FfmpegService")
        logging.info(type(self.ffmpegProvider).__name__)
        logging.info(type(self.mediaRegistryProvider).__name__)
    
    def watchMedia(self):        
        self.timer = RepeatTimer(60, self.process_media_services)
        self.timer.start()                   
    
    def process_media_services(self):
        media = self.mediaRegistryProvider.getMediaIndex()
        if media:
            for id in media:
                logging.info(id)
                self.process_media(id)

    def process_media(self, mediaId) -> bool:
        return self.process_thumb(mediaId) & self.process_meta(mediaId)
    
    def process_thumb(self, mediaId) -> bool:
        return self.ffmpegProvider.gen_thumb(mediaId)
    
    def process_meta(self, mediaId) -> bool:
        return self.ffmpegProvider.gen_meta(mediaId)