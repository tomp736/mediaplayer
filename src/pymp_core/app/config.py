from enum import IntFlag


class PympServerRoles(IntFlag):
    NONE = 1
    MEDIA_API = 2
    META_API = 4
    THUMB_API = 8
    MEDIA_SVC = 16
    FFMPEG_SVC = 32
    MEDIAREGISTRY_SVC = 64


class IConfig():
    pass


class FlaskConfig(IConfig):
    host: str
    port: int
    cors_headers: str

    def __init__(self, **kwargs) -> None:
        self.host = kwargs.get('host', '0.0.0.0')
        self.port = kwargs.get('port', 80)
        self.cors_headers = kwargs.get('cors_headers', '*')


class ServerConfig(IConfig):
    server_id: str
    server_roles: PympServerRoles
    server_host: str
    server_proto: str
    server_port: int

    def __init__(self, **kwargs) -> None:
        self.server_id = kwargs.get('server_id', 'DEFAULT')
        self.server_roles = kwargs.get('server_roles', PympServerRoles.NONE)
        self.server_host = kwargs.get('server_host', 'localhost')
        self.server_proto = kwargs.get('server_proto', 'http')
        self.server_port = kwargs.get('server_port', 80)


class ServiceConfig(IConfig):
    service_id: str
    service_roles: PympServerRoles
    service_host: str
    service_proto: str
    service_port: int

    def __init__(self, **kwargs) -> None:
        self.service_id = kwargs.get('service_id', 'DEFAULT')
        self.service_roles = kwargs.get('service_roles', PympServerRoles.NONE)
        self.service_host = kwargs.get('service_host', 'localhost')
        self.service_proto = kwargs.get('service_proto', 'http')
        self.service_port = kwargs.get('service_port', 80)

    def is_valid(self):
        if self.service_proto in ["http", "https"]:
            return True
        else:
            return False

    def get_uri(self):
        if self.service_proto in ["http", "https"]:
            return f"{self.service_proto}://{self.service_host}:{self.service_port}"
        else:
            raise Exception(f"ServiceInfo Not Valid: {self.__dict__}")


class RedisConfig(IConfig):
    server_host: str
    server_port: int

    def __init__(self, **kwargs) -> None:
        self.server_host = kwargs.get('server_host', 'localhost')
        self.server_port = kwargs.get('server_port', '2379')


class MediaConfig(IConfig):
    media_path: str
    index_path: str
    media_chunk_size: int
    thumb_chunk_size: int

    def __init__(self, **kwargs) -> None:
        self.media_path = kwargs.get('media_path', '/var/media')
        self.index_path = kwargs.get('index_path', '/var/index')
        self.media_chunk_size = kwargs.get('media_chunk_size', 2 ** 22)
        self.thumb_chunk_size = kwargs.get('thumb_chunk_size', 2 ** 10)
