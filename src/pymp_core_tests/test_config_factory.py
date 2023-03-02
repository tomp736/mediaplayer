

# from unittest.mock import MagicMock
# from pymp_core.app.config import PympServerRoles, ServerConfig
# from pymp_core.app.config_factory import ConfigFactory


# def test_load_environment_configs():
#     json_config_reader = MagicMock()
#     mock_runtime_config_provider = MagicMock()
#     mock_environment_config_reader = MagicMock()

#     mock_server_config = ServerConfig(server_id="1", server_roles=PympServerRoles.NONE, server_host="localhost", server_proto="http", server_port=8080)
#     mock_environment_config_reader.load_config.return_value = mock_server_config

#     config_factory = ConfigFactory(json_config_reader, mock_environment_config_reader, mock_runtime_config_provider)

#     mock_runtime_config_provider.load_config.assert_called_once_with(**mock_server_config.__dict__)