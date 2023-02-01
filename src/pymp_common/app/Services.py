
import logging
from pymp_common.app import ProviderFactory
from pymp_common.app.PympConfig import pymp_env

media_registry_providers = ProviderFactory.get_media_registry_providers()
ffmpeg_providers = ProviderFactory.get_ffmpeg_providers()
media_providers = ProviderFactory.get_media_providers(pymp_env.get_server_id())