

import json
import os
from typing import Any, Dict, List
from pymp_core.app.config import FlaskConfig, MediaConfig, PympServerRoles, RedisConfig, ServerConfig, ServiceConfig


class EnvironmentConfigReader:
    def __init__(self):
        pass

    def load_config(self, config_type):
        if config_type == ServerConfig:
            return ServerConfig(
                server_id=os.environ.get('SERVER_ID', 'DEFAULT'),
                server_roles=PympServerRoles(
                    int(os.environ.get('SERVER_ROLES', '1'))),
                server_host=os.environ.get('SERVER_HOST', 'localhost'),
                server_proto=os.environ.get('SERVER_PROTO', 'http'),
                server_port=int(os.environ.get('SERVER_PORT', 80))
            )
        elif config_type == FlaskConfig:
            return FlaskConfig(
                host=os.environ.get('FLASK_HOST', '0.0.0.0'),
                port=os.environ.get('FLASK_PORT', '80'),
                cors_headers=os.environ.get('FLASK_CORS_HEADERS', '*')
            )
        elif config_type == RedisConfig:
            return RedisConfig(
                server_host=os.environ.get('REDIS_HOST', 'localhost'),
                server_port=int(os.environ.get('REDIS_PORT', 80))
            )
        elif config_type == MediaConfig:
            return MediaConfig(
                media_path=os.environ.get('MEDIA_PATH', '/var/media'),
                index_path=os.environ.get('INDEX_PATH', '/var/index'),
                media_chunk_size=int(os.environ.get('MEDIA_CHUNK_SIZE', 1024)),
                thumb_chunk_size=int(os.environ.get('THUMB_CHUNK_SIZE', 512))
            )
        else:
            raise ValueError(f"Unsupported config type: {config_type}")


class JsonServiceConfigReader:
    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path

    def load_config(self) -> List[ServiceConfig]:
        with open(self.config_file_path, 'r', encoding='utf-8') as file_io:
            data = json.load(file_io)
        return [ServiceConfig(**config) for config in data]
