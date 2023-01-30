
import logging
from pymp_common.services.MediaRegistryService import MediaRegistryService
from pymp_common.services.FfmpegService import FfmpegService
from pymp_common.services.MediaService import MediaService

mediaRegistryService = MediaRegistryService()
ffmpegService = FfmpegService()
mediaService = MediaService()

def printServiceInfo():
    mediaRegistryService.printServiceInfo()
    ffmpegService.printServiceInfo()
    mediaService.printServiceInfo()