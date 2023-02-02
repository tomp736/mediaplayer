import logging
from typing import Dict
from pymp_common.abstractions.providers import MediaRegistryDataProvider

from pymp_common.app.Services import media_registry_providers
from pymp_common.app.Services import ffmpeg_providers
from pymp_common.app.Services import media_providers
from pymp_common.utils.RepeatTimer import RepeatTimer


class MediaRegistryService():
    def __init__(self) -> None:
        self.media_registry_providers = media_registry_providers
        self.ffmpeg_providers = ffmpeg_providers
        self.media_providers = media_providers

    def __repr__(self) -> str:
        return f"MediaRegistryService({self.MediaRegistryDataProvider})"

    def register(self, service_id, proto, host, port):
        return self.MediaRegistryDataProvider.register(service_id, proto, host, port)

    def register_(self, serviceInfo: Dict[str, str]):
        return self.MediaRegistryDataProvider.register_(serviceInfo)

    def get_media_services(self) -> Dict[str, str]:
        return self.MediaRegistryDataProvider.get_media_services()

    def get_media_service(self, media_id) -> str:
        return self.MediaRegistryDataProvider.get_media_service(media_id)

    def get_media_index(self):
        return self.MediaRegistryDataProvider.get_media_index()

    def watch_services(self):
        self.timer = RepeatTimer(60, self.update_media_services)
        self.timer.start()

    def update_media_services(self):
        mediaServices = self.MediaRegistryDataProvider.get_media_services()
        if not mediaServices:
            return

        for mediaServiceId in mediaServices:
            media_svc_media_ids = self.check_media_service(mediaServiceId)
            self.check_media_sources(mediaServiceId, media_svc_media_ids)

    def check_media_service(self, service_id):
        logging.info(f"CHECKING SERVICE FOR {service_id}")
        media_svc_media_ids = []
        try:
            MediaDataProvider = ProviderFactory.get_media_provider(service_id)
            if MediaDataProvider:
                status = MediaDataProvider.get_status()
                if status:
                    media_svc_media_ids = MediaDataProvider.get_media_ids()
                    logging.info(
                        f"MediaDataProvider {service_id} passes status check.")
                else:
                    logging.info(
                        f"MediaDataProvider {service_id} fails status check.")
                    self.MediaRegistryDataProvider.remove(service_id)
            else:
                logging.info(f"MediaDataProvider {service_id} is None.")
        except Exception as ex:
            logging.info(ex)
            self.MediaRegistryDataProvider.remove(service_id)
        return media_svc_media_ids

    def check_media_sources(self, service_id, mediaIds):
        logging.info(f"CHECKING SOURCES FOR {service_id}")
        logging.info(f"{service_id} REPORTED {mediaIds}")

        registry_media = self.MediaRegistryDataProvider.get_media_index()
        if registry_media is None:
            return

        redis_svc_media_ids = []
        for registry_mediaId in registry_media:
            if registry_media[registry_mediaId] == service_id:
                redis_svc_media_ids.append(registry_mediaId)

        for registryMediaID in redis_svc_media_ids:
            # delete from redis if media_svc no longer has the media
            if not mediaIds.__contains__(registryMediaID):
                logging.info(f"DELETING: {registryMediaID}")
                self.MediaRegistryDataProvider.remove_media(registryMediaID)
                continue

            # if media source for media  has changed, update redis
            if not registry_media[registryMediaID] == service_id:
                logging.info(f"UPDATING: {registryMediaID}")
                self.MediaRegistryDataProvider.register_media(
                    registryMediaID, service_id)
                continue

        # Update all
        for media_id in mediaIds:
            logging.info(f"ADDING: {media_id}")
            self.MediaRegistryDataProvider.register_media(media_id, service_id)
