import logging
from pymp_common.abstractions.providers import MediaRegistryProvider
from pymp_common.providers.MediaRegistryProviderLocal import MediaRegistryProviderLocal
from pymp_common.providers.MediaRegistryProviderRemote import MediaRegistryProviderRemote
from pymp_common.app.PympConfig import pymp_env, PympServer


class MediaRegistryProviderFactory:
    
    @staticmethod
    def create_instance() -> MediaRegistryProvider:
        if pymp_env.getServerType() & PympServer.MEDIAREGISTRY_SVC:
            logging.info("Creating MediaRegistryProviderLocal")
            return MediaRegistryProviderLocal()
        else:
            logging.info(f"Creating MediaRegistryProviderRemote")
            return MediaRegistryProviderRemote()
