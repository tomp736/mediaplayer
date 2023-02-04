
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dto.MediaRegistry import PympServiceType

import logging
from typing import List
from pymp_common.abstractions.providers import DataProvider, FfmpegDataProvider
from pymp_common.providers.FfmpegFileDataProvider import FfmpegFileDataProvider
from pymp_common.providers.FfmpegHttpDataProvider import FfmpegHttpDataProvider


def get_ffmpeg_providers(wants_write_access: bool = False) -> List[FfmpegDataProvider]:
    logging.info("GETTING FFMPEG PROVIDERS")
    ffmpeg_providers = []

    if pymp_env.is_this_service_type(PympServiceType.FFMPEG_SVC):
        ffmpeg_provider = FfmpegFileDataProvider()
        if check_data_provider(wants_write_access, ffmpeg_provider):
            ffmpeg_providers.append(ffmpeg_provider)

    ffmpeg_provider = FfmpegHttpDataProvider(
        pymp_env.get_service_info(PympServiceType.FFMPEG_SVC))
    if check_data_provider(wants_write_access, ffmpeg_provider):
        ffmpeg_providers.append(ffmpeg_provider)

    return ffmpeg_providers


def check_data_provider(wants_write_access, data_provider: DataProvider) -> bool:
    if not data_provider.is_ready():
        logging.info(f"IGNORING {data_provider}: failed ready check")
        return False

    if wants_write_access and data_provider.is_readonly():
        logging.info(
            f"IGNORING {data_provider}: failed write_access check")
        return False

    return True
