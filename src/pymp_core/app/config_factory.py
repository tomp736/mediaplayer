from typing import List, Type, TypeVar, cast

from pymp_core.app.config import FlaskConfig, MediaConfig, RedisConfig, ServerConfig, ServiceConfig
from pymp_core.app.config_builder import ConfigBuilder
from pymp_core.app.config_source import EnvironmentConfigSource, IConfigSource, JsonServiceConfigReader, RuntimeConfigSource


class ConfigFactory:
    
    _config_sources: List[IConfigSource] = []
    _config_builder: ConfigBuilder = ConfigBuilder()
    _json_config_reader: JsonServiceConfigReader = JsonServiceConfigReader("/app/service_config.json")
    
    def __init__(self, config_sources) -> None:
        self._config_sources = config_sources
        
    def get_server_config(self) -> ServerConfig:
        config = ServerConfig()
        for config_source in self._config_sources:
            config = self._config_builder.build(config_source, config)
        return config

    def get_flask_config(self) -> FlaskConfig:
        config = FlaskConfig()
        for config_source in self._config_sources:
            config = self._config_builder.build(config_source, config)
        return config

    def get_redis_config(self) -> RedisConfig:
        config = RedisConfig()
        for config_source in self._config_sources:
            config = self._config_builder.build(config_source, config)
        return config

    def get_media_config(self) -> MediaConfig:
        config = MediaConfig()
        for config_source in self._config_sources:
            config = self._config_builder.build(config_source, config)
        return config

    def get_service_configs(self) -> List[ServiceConfig]:
        return cast(List[ServiceConfig], self._json_config_reader.load_config())
    
CONFIG_FACTORY = ConfigFactory([
    EnvironmentConfigSource(),
    RuntimeConfigSource()
])
