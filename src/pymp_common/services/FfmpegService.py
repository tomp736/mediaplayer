import logging

from pymp_common.providers.MediaRegistryProviderFactory import MediaRegistryProviderFactory
from pymp_common.providers.FfmpegProviderFactory import FfmpegProviderFactory
from pymp_common.utils.RepeatTimer import RepeatTimer

class FfmpegService:  
    def __init__(self) -> None:
        self.ffmpegProvider = FfmpegProviderFactory.create_instance()
        self.mediaRegistryProvider = MediaRegistryProviderFactory.create_instance()
        
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
        return self.ffmpegProvider.gen_meta(mediaId)
    
    def process_meta(self, mediaId) -> bool:
        return self.ffmpegProvider.gen_meta(mediaId)