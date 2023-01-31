
import logging
from pymp_common.services.MediaRegistryService import MediaRegistryService
from pymp_common.services.FfmpegService import FfmpegService
from pymp_common.services.MediaService import MediaService

mediaRegistryService = MediaRegistryService()
ffmpegService = FfmpegService()
mediaService = MediaService()

def print_serviceinfo():
    mediaRegistryService.print_serviceinfo()
    ffmpegService.print_serviceinfo()
    mediaService.print_serviceinfo()