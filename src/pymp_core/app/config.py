import os

from pymp_core.dto.MediaRegistry import PympServiceType
from pymp_core.dto.MediaRegistry import ServiceInfo

FLASK_RUN_HOST="0.0.0.0"
FLASK_RUN_PORT="80"
REDIS_HOST=""
REDIS_PORT="2379"
SERVICE_TYPE=63
SERVICE_ID="DEFAULT"
SERVICE_PROTO="http"
SERVICE_HOST="localhost"
SERVICE_PORT=80
MEDIA_SVC_MEDIAPATH="/app/media"
MEDIA_SVC_INDEXPATH="/app/index"
CORS_HEADER="*"
MEDIA_CHUNK_SIZE=2 ** 22
THUMB_CHUNK_SIZE=2 ** 10


class PympEnv:

    def __init__(self):
        self.load_configs()

    def load_configs(self):
        # load config keys from env
        for config_key, config_value in globals().items():
            globals()[config_key] = os.environ.get(config_key, config_value)

        globals()["SERVICE_ID"] = os.environ.get("SERVICE_ID", "")
        globals()["SERVICE_TYPE"] = os.environ.get("SERVICE_TYPE", "")
        globals()["SERVICE_PROTO"] = os.environ.get("SERVICE_PROTO", "")
        service_ip = os.environ.get("SERVICE_IP", "")
        if service_ip != "":
            globals()["SERVICE_HOST"] = service_ip
        else:            
            globals()["SERVICE_HOST"] = os.environ.get("SERVICE_HOST", "")
        globals()["SERVICE_PORT"] = os.environ.get("SERVICE_PORT", "")

        # load host service info
        # used for hard-coded service resolution when needed
        for pymp_service_type in PympServiceType:
            globals()[f"{pymp_service_type.name}_ID"] = os.environ.get(
                f"{pymp_service_type.name}_ID", "")
            globals()[f"{pymp_service_type.name}_TYPE"] = os.environ.get(
                f"{pymp_service_type.name}_TYPE", "")
            globals()[f"{pymp_service_type.name}_PROTO"] = os.environ.get(
                f"{pymp_service_type.name}_PROTO", "")
            globals()[f"{pymp_service_type.name}_HOST"] = os.environ.get(
                f"{pymp_service_type.name}_HOST", "")
            globals()[f"{pymp_service_type.name}_PORT"] = os.environ.get(
                f"{pymp_service_type.name}_PORT", "")

    def get(self, key: str) -> str:
        if key in globals():
            return str(globals().get(key))
        else:
            raise ValueError(f"{key} is not configured in PympEnv.")

    def set(self, key: str, value: str):
        if key in globals():
            globals()[key] = value
        else:
            raise ValueError(f"{key} is not configured in PympEnv.")

    def is_this_service_type(self, pymp_service_type: PympServiceType) -> bool:
        service_info = self.get_this_service_info()
        service_type = PympServiceType(service_info.service_type)
        is_type = bool(service_type & pymp_service_type)
        return is_type

    def get_service_info(self, pymp_service_type: PympServiceType) -> ServiceInfo:
        service_info = ServiceInfo()
        service_info.service_id = self.get(
            f"{pymp_service_type.name}_ID")
        service_info.service_type = PympServiceType(pymp_service_type.value)
        service_info.service_proto = self.get(
            f"{pymp_service_type.name}_PROTO")
        service_info.service_host = self.get(
            f"{pymp_service_type.name}_HOST")
        service_info.service_port = self.get(
            f"{pymp_service_type.name}_PORT")
        return service_info

    def set_this_service_info(self, service_info: ServiceInfo):
        globals()["SERVICE_ID"] = service_info.service_id

    def get_this_service_info(self) -> ServiceInfo:
        service_info = ServiceInfo()
        service_info.service_id = self.get("SERVICE_ID")
        service_info.service_type = PympServiceType(int(self.get("SERVICE_TYPE")))
        service_info.service_proto = self.get("SERVICE_PROTO")
        service_info.service_host = self.get("SERVICE_HOST")
        service_info.service_port = self.get("SERVICE_PORT")
        return service_info


pymp_env = PympEnv()
