import logging
from typing import Union
from pymp_common.abstractions.providers import MediaProvider
from pymp_common.providers.MediaProviderLocal import MediaProviderLocal
from pymp_common.providers.MediaProviderRemote import MediaProviderRemote
from pymp_common.app.PympConfig import pymp_env, PympServer
from pymp_common.dataaccess.redis import media_service_da

class MediaProviderFactory:
        
    @staticmethod
    def create_instance(serviceId) -> Union[MediaProvider, None]:
        logging.info(f"Creating MediaProvider {serviceId}")

        if pymp_env.getServerType() & PympServer.MEDIA_SVC and pymp_env.get("SERVER_ID") == serviceId:
            return MediaProviderLocal()
        
        serviceinfo = media_service_da.hget(serviceId)
        if serviceinfo:
            return MediaProviderRemote(serviceinfo)
