from typing import List, Type, cast

from pymp_core.app.config import FlaskConfig, MediaConfig, RedisConfig, ServerConfig, ServiceConfig
from pymp_core.app.config_provider import RuntimeConfigProvider
from pymp_core.app.config_readers import EnvironmentConfigReader, JsonServiceConfigReader


class ConfigFactory:
    def __init__(self,
                 json_config_reader: JsonServiceConfigReader,
                 environment_config_reader: EnvironmentConfigReader,
                 runtime_config_provider: RuntimeConfigProvider) -> None:

        self.json_config_reader = json_config_reader
        self.environment_config_reader = environment_config_reader
        self.runtime_config_provider = runtime_config_provider

        self.runtime_config_provider.load_config(
            **self.environment_config_reader.load_config(ServerConfig).__dict__)
        self.runtime_config_provider.load_config(
            **self.environment_config_reader.load_config(FlaskConfig).__dict__)
        self.runtime_config_provider.load_config(
            **self.environment_config_reader.load_config(RedisConfig).__dict__)
        self.runtime_config_provider.load_config(
            **self.environment_config_reader.load_config(MediaConfig).__dict__)

    def create_server_config(self) -> ServerConfig:
        return cast(ServerConfig, self.runtime_config_provider.get_config(ServerConfig))

    def create_flask_config(self) -> FlaskConfig:
        return cast(FlaskConfig, self.runtime_config_provider.get_config(FlaskConfig))

    def create_redis_config(self) -> RedisConfig:
        return cast(RedisConfig, self.runtime_config_provider.get_config(RedisConfig))

    def create_media_config(self) -> MediaConfig:
        return cast(MediaConfig, self.runtime_config_provider.get_config(MediaConfig))

    def create_service_configs(self) -> List[ServiceConfig]:
        return cast(List[ServiceConfig], self.json_config_reader.load_config())
    
CONFIG_FACTORY = ConfigFactory(JsonServiceConfigReader("/app/service_config.json"), EnvironmentConfigReader(), RuntimeConfigProvider())
