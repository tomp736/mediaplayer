import logging
from typing import Dict, Union
from pymp_common.abstractions.providers import MediaProvider
from pymp_common.providers.MediaProviderLocal import MediaProviderLocal
from pymp_common.providers.MediaProviderRemote import MediaProviderRemote
from pymp_common.app.PympConfig import pymp_env, PympServer
from pymp_common.dataaccess.redis import media_service_da

class MediaProviderFactory:

    @staticmethod
    def create_local_instance() -> Union[MediaProvider, None]:
        if pymp_env.getServerType() & PympServer.MEDIA_SVC:
            return MediaProviderLocal()
        return None
    
    @staticmethod
    def create_remote_instance(serviceInfo: Dict) -> MediaProvider:
        return MediaProviderRemote(serviceInfo)
        
    @staticmethod
    def create_instance(serviceId=None) -> Union[MediaProvider, None]:
        if serviceId is None or serviceId == "DEFAULT":
            logging.info(f"Creating MediaProviderLocal()")
            return MediaProviderFactory.create_local_instance()
        else:
            logging.info(f"Creating MediaProviderRemote({serviceId})")
            if serviceId:
                serviceinfo = media_service_da.hget(serviceId)
                if serviceinfo:
                    return MediaProviderFactory.create_remote_instance(serviceinfo)
