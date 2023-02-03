import logging
from typing import Dict
from pymp_common.dto.MediaRegistry import MediaInfo, ServiceInfo

from pymp_common.app.ProviderFactory import get_media_providers, get_media_registry_providers
from pymp_common.utils.RepeatTimer import RepeatTimer
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dto.MediaRegistry import PympServiceType


class MediaRegistryService():
    def __init__(self) -> None:
        self.timer = RepeatTimer(60, self.update_media_services)

    def __repr__(self) -> str:
        return "MediaRegistryService()"

    def register_service(self, service_info: ServiceInfo):
        media_registry_provider = get_media_registry_providers()[0]
        return media_registry_provider.set_service_info(service_info)

    def register_media(self, media_info: MediaInfo):
        media_registry_provider = get_media_registry_providers()[0]
        return media_registry_provider.set_media_info(media_info)

    def get_registered_services(self) -> Dict[str, ServiceInfo]:
        media_registry_provider = get_media_registry_providers()[0]
        return media_registry_provider.get_all_service_info()

    def get_media_index(self) -> Dict[str, MediaInfo]:
        media_registry_provider = get_media_registry_providers()[0]
        return media_registry_provider.get_all_media_info()

    def get_media_info(self, media_id) -> MediaInfo:
        media_registry_provider = get_media_registry_providers()[0]
        return media_registry_provider.get_media_info(media_id)

    def watch_services(self):
        self.timer.start()

    def update_media_services(self):
        service_info = pymp_env.get_this_service_info()
        if PympServiceType(service_info.service_type) & PympServiceType.MEDIAREGISTRY_SVC:
            media_service = self.get_registered_services()
            if not media_service:
                return

            for media_service_id in media_service:
                media_svc_media_ids = self.check_media_service(media_service_id)
                self.check_media_sources(media_service_id, media_svc_media_ids)

    def check_media_service(self, service_id):
        self.logstuff(f"CHECKING SERVICE FOR {service_id}")
        media_svc_media_ids = []
        try:
            logging.info("1")
            media_registry_provider = get_media_registry_providers()[0]
            logging.info("2")
            media_provider = get_media_providers(service_id)[0]
            logging.info("3")
            if media_provider:
                logging.info("4")
                status = media_provider.is_ready()
                logging.info("5")
                if status:
                    logging.info(media_provider)
                    media_svc_media_ids = media_provider.get_media_ids()
                    self.logstuff(
                        f"MediaDataProvider {service_id} passes status check.")
                else:
                    logging.info("7")
                    self.logstuff(
                        f"MediaDataProvider {service_id} fails status check.")
                    media_registry_provider.del_service_info(service_id)
            else:
                self.logstuff(f"MediaDataProvider {service_id} is None.")
        except Exception as ex:
            logging.info(ex)
            media_registry_provider.del_service_info(service_id)
        return media_svc_media_ids

    def check_media_sources(self, service_id, service_media_ids):
        self.logstuff(f"CHECKING SOURCES FOR {service_id}")
        self.logstuff(f"{service_id} REPORTED {service_media_ids}")

        media_registry_provider = get_media_registry_providers()[0]
        registry_media = media_registry_provider.get_all_media_info()
        if registry_media is None:
            return

        redis_svc_media_ids = []
        for registry_media_id in registry_media:
            if registry_media[registry_media_id] == service_id:
                redis_svc_media_ids.append(registry_media_id)

        for registry_media_id in redis_svc_media_ids:
            # delete from redis if media_svc no longer has the media
            if not registry_media_id in service_media_ids:
                self.logstuff(f"DELETING: {registry_media_id}")
                media_registry_provider.del_media_info(registry_media_id)
                continue

            # if media source for media  has changed, update redis
            if not registry_media[registry_media_id] == service_id:
                self.logstuff(f"UPDATING: {registry_media_id}")
                media_info = MediaInfo()
                media_info.media_id = registry_media_id
                media_info.service_id = service_id
                media_registry_provider.set_media_info(media_info)
                continue

        # Update all
        for media_id in service_media_ids:
            self.logstuff(f"ADDING: {media_id}")
            media_info = MediaInfo()
            media_info.media_id = media_id
            media_info.service_id = service_id
            media_registry_provider.set_media_info(media_info)

    def logstuff(self, message):
        logging.info(f"MEDIASERVICE: {message}")
