import json
from typing import Dict
from pymp_common.abstractions.providers import FfmpegProvider, MediaProvider
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.providers.MediaProviderLocal import MediaProviderLocal
from pymp_common.providers.MediaProviderHttp import MediaProviderHttp
from pymp_common.providers.MediaRegistryProviderRedis import MediaRegistryProviderRedis
from pymp_common.providers.MediaRegistryProviderHttp import MediaRegistryProviderHttp
from pymp_common.providers.FfmpegProviderHttp import FfmpegProviderHttp
from pymp_common.providers.FfmpegProviderRedis import FfmpegProviderRedis


def get_media_registry_providers() -> Dict[str, MediaRegistryProvider]:
    media_registry_providers = {}
    
    media_registry_provider = MediaRegistryProviderRedis()
    if media_registry_provider.get_status():
        media_registry_providers["redis"] = media_registry_provider
    
    media_registry_provider = MediaRegistryProviderHttp()
    if media_registry_provider.get_status():
        media_registry_providers["http"] = media_registry_provider
        
    return media_registry_providers


def get_media_providers(service_id) -> Dict[str, MediaProvider]:
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
                media_provider = MediaProviderLocal(service_id)
                if media_provider.get_status():
                    media_providers[service_id] = media_provider
                    continue
                
                media_provider = MediaProviderHttp(json.loads(service_info))
                if media_provider.get_status():
                    media_providers[service_id] = media_provider
                    
    return media_providers


def get_ffmpeg_providers() -> Dict[str, FfmpegProvider]:
    ffmpeg_providers = {}
    
    ffmpeg_provider = FfmpegProviderRedis()
    if ffmpeg_provider.get_status():
        ffmpeg_providers["redis"] = ffmpeg_provider
    
    ffmpeg_provider = FfmpegProviderHttp()
    if ffmpeg_provider.get_status():
        ffmpeg_providers["http"] = ffmpeg_provider
        
    return ffmpeg_providers