

from typing import Any, Dict

from pymp_core.app.config import FlaskConfig, MediaConfig, PympServerRoles, RedisConfig, ServerConfig


class RuntimeConfigProvider:
    
    config: Dict[str, Any] = {}
    
    def __init__(self):
    
    def load_config(self, **kwargs):
        for key, value in kwargs.items():
            self.config[key] = value

    def get_config(self, config_type):
        if config_type == ServerConfig:
            return ServerConfig(
                server_id=self.config.get('SERVER_ID', 'DEFAULT'),
                server_roles=PympServerRoles(int(self.config.get('SERVER_ROLES', '1'))),
                server_host=self.config.get('SERVER_HOST', 'localhost'),
                server_proto=self.config.get('SERVER_PROTO', 'http'),
                server_port=int(self.config.get('SERVER_PORT', 80))
            )
        elif config_type == FlaskConfig:
            return FlaskConfig(
                host=self.config.get('FLASK_HOST', '0.0.0.0'),
                port=self.config.get('FLASK_PORT', '80'),
                cors_headers=self.config.get('FLASK_CORS_HEADERS', '*')
            )
        elif config_type == RedisConfig:
            return RedisConfig(
                server_host=self.config.get('REDIS_HOST', 'localhost'),
                server_port=int(self.config.get('REDIS_PORT', 80))
            )
        elif config_type == MediaConfig:
            return MediaConfig(
                media_path=self.config.get('MEDIA_PATH', '/var/media'),
                index_path=self.config.get('INDEX_PATH', '/var/index'),
                media_chunk_size=int(self.config.get('MEDIA_CHUNK_SIZE', 1024)),
                thumb_chunk_size=int(self.config.get('THUMB_CHUNK_SIZE', 512))
            )     
        else:
            raise ValueError(f"Unsupported config type: {config_type}")
        
    def set_config(self, config_type, config_key, config_value):
        if config_type == ServerConfig:
            self.config[f"SERVER_{config_key}"] = config_value
        else:
            raise ValueError(f"Unsupported config type: {config_type}")