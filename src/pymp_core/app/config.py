import os

from pymp_core.dto.MediaRegistry import PympServerRoles
from pymp_core.dto.MediaRegistry import ServiceInfo

FLASK_RUN_HOST="0.0.0.0"
FLASK_RUN_PORT="80"
REDIS_HOST=""
REDIS_PORT="2379"
SERVER_ROLES=63
SERVER_ID="DEFAULT"
SERVER_PROTO="http"
SERVER_HOST="localhost"
SERVER_PORT=80
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

        globals()["SERVER_ID"] = os.environ.get("SERVER_ID", "")
        globals()["SERVER_ROLES"] = os.environ.get("SERVER_ROLES", "")
        globals()["SERVER_PROTO"] = os.environ.get("SERVER_PROTO", "")
        service_ip = os.environ.get("SERVICE_IP", "")
        if service_ip != "":
            globals()["SERVER_HOST"] = service_ip
        else:            
            globals()["SERVER_HOST"] = os.environ.get("SERVER_HOST", "")
        globals()["SERVER_PORT"] = os.environ.get("SERVER_PORT", "")

        # load host service info
        # used for hard-coded service resolution when needed
        for pymp_server_roles in PympServerRoles:
            globals()[f"{pymp_server_roles.name}_ID"] = os.environ.get(
                f"{pymp_server_roles.name}_ID", "")
            globals()[f"{pymp_server_roles.name}_TYPE"] = os.environ.get(
                f"{pymp_server_roles.name}_TYPE", "")
            globals()[f"{pymp_server_roles.name}_PROTO"] = os.environ.get(
                f"{pymp_server_roles.name}_PROTO", "")
            globals()[f"{pymp_server_roles.name}_HOST"] = os.environ.get(
                f"{pymp_server_roles.name}_HOST", "")
            globals()[f"{pymp_server_roles.name}_PORT"] = os.environ.get(
                f"{pymp_server_roles.name}_PORT", "")

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

    def is_this_server_roles(self, pymp_server_roles: PympServerRoles) -> bool:
        service_info = self.get_this_service_info()
        server_roles = PympServerRoles(service_info.server_roles)
        is_type = bool(server_roles & pymp_server_roles)
        return is_type

    def get_service_info(self, pymp_server_roles: PympServerRoles) -> ServiceInfo:
        service_info = ServiceInfo()
        service_info.server_id = self.get(
            f"{pymp_server_roles.name}_ID")
        service_info.server_roles = PympServerRoles(pymp_server_roles.value)
        service_info.server_proto = self.get(
            f"{pymp_server_roles.name}_PROTO")
        service_info.server_host = self.get(
            f"{pymp_server_roles.name}_HOST")
        service_info.server_port = self.get(
            f"{pymp_server_roles.name}_PORT")
        return service_info

    def set_this_service_info(self, service_info: ServiceInfo):
        globals()["SERVER_ID"] = service_info.server_id

    def get_this_service_info(self) -> ServiceInfo:
        service_info = ServiceInfo()
        service_info.server_id = self.get("SERVER_ID")
        service_info.server_roles = PympServerRoles(int(self.get("SERVER_ROLES")))
        service_info.server_proto = self.get("SERVER_PROTO")
        service_info.server_host = self.get("SERVER_HOST")
        service_info.server_port = self.get("SERVER_PORT")
        return service_info


pymp_env = PympEnv()
