
import logging
from pymp_common.app import ProviderFactory
from pymp_common.app.PympConfig import pymp_env
from pymp_common.services.MediaRegistryService import MediaRegistryService
from pymp_common.services.FfmpegService import FfmpegService
from pymp_common.services.MediaService import MediaService

mediaRegistryProvider = ProviderFactory.get_media_registry_provider()
ffmpegProvider = ProviderFactory.get_ffmpeg_provider()
mediaProvider = ProviderFactory.get_media_provider(pymp_env.get_server_id())

mediaRegistryService = MediaRegistryService(mediaRegistryProvider)
ffmpegService = FfmpegService(mediaRegistryProvider, ffmpegProvider)
mediaService = MediaService(mediaRegistryProvider, mediaProvider)

def print_serviceinfo():
    mediaRegistryService.__repr__()
    ffmpegService.__repr__()
    mediaService.__repr__()