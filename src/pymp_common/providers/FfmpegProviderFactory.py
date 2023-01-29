import logging
from pymp_common.providers.FfmpegProviderLocal import FfmpegProviderLocal
from pymp_common.providers.FfmpegProviderRemote import FfmpegProviderRemote
from pymp_common.app.PympConfig import pymp_env, PympServer


class FfmpegProviderFactory:

    @staticmethod
    def create_instance():
        if pymp_env.getServerType() & PympServer.FFMPEG_SVC:
            logging.info("Creating FfmpegProviderLocal")
            return FfmpegProviderLocal()
        else:
            logging.info("Creating FfmpegProviderRemote")
            return FfmpegProviderRemote()
