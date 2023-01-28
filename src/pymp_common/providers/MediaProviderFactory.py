from pymp_common.providers.MediaProviderLocal import MediaProviderLocal
from pymp_common.providers.MediaProviderRemote import MediaProviderRemote
from pymp_common.app.PympConfig import pymp_env, PympServer


class MediaServiceFactory:

    @staticmethod
    def create_instance(media_service_id=None):
        if pymp_env.getServerType() & PympServer.MEDIA_SVC and media_service_id is None:
            return MediaProviderLocal()
        else:
            return MediaProviderRemote(media_service_id)
