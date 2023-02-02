import json
from typing import Dict
from pymp_common.abstractions.providers import FfmpegDataProvider, MediaDataProvider
from pymp_common.abstractions.providers import MediaRegistryDataProvider
from pymp_common.providers.MediaFileDataProvider import MediaFileDataProvider
from pymp_common.providers.MediaHttpDataProvider import MediaHttpDataProvider
from pymp_common.providers.MediaRegistryRedisDataProvider import MediaRegistryRedisDataProvider
from pymp_common.providers.MediaRegistryHttpDataProvider import MediaRegistryHttpDataProvider
from pymp_common.providers.FfmpegHttpDataProvider import FfmpegHttpDataProvider
from pymp_common.providers.FfmpegRedisDataProvider import FfmpegRedisDataProvider


def get_media_registry_providers() -> Dict[str, MediaRegistryDataProvider]:
    media_registry_providers = {}
    
    media_registry_provider = MediaRegistryRedisDataProvider()
    if media_registry_provider.get_status():
        media_registry_providers["redis"] = media_registry_provider
    
    media_registry_provider = MediaRegistryHttpDataProvider()
    if media_registry_provider.get_status():
        media_registry_providers["http"] = media_registry_provider
        
    return media_registry_providers


def get_media_providers(service_id) -> Dict[str, MediaDataProvider]:
    media_providers = {}
    media_registry_providers = get_media_registry_providers()
    
    media_registry_provider = None
    for service_id, provider in media_registry_providers.items():
        if provider.get_status():
            media_registry_provider = provider
            break
        
    if media_registry_provider:
        service_info = media_registry_provider.get_service_info()
        if service_info:
            for service_id, service_info in service_info.items():
                media_provider = MediaFileDataProvider(service_id)
                if media_provider.get_status():
                    media_providers[service_id] = media_provider
                    continue
                
                media_provider = MediaHttpDataProvider(json.loads(service_info))
                if media_provider.get_status():
                    media_providers[service_id] = media_provider
                    
    return media_providers


def get_ffmpeg_providers() -> Dict[str, FfmpegDataProvider]:
    ffmpeg_providers = {}
    
    ffmpeg_provider = FfmpegRedisDataProvider()
    if ffmpeg_provider.get_status():
        ffmpeg_providers["redis"] = ffmpeg_provider
    
    ffmpeg_provider = FfmpegHttpDataProvider()
    if ffmpeg_provider.get_status():
        ffmpeg_providers["http"] = ffmpeg_provider
        
    return ffmpeg_providers