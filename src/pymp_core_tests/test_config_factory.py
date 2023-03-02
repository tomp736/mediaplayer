import logging
import os
import unittest
from unittest.mock import MagicMock

from pymp_core.app.config import PympServerRoles, ServerConfig
from pymp_core.app.config_factory import ConfigFactory
from pymp_core.app.config_provider import RuntimeConfigProvider
from pymp_core.app.config_readers import EnvironmentConfigReader


class ConfigFactoryTest(unittest.TestCase):
    def setUp(self):
        os.environ['SERVER_ID'] = 'test_server'
        os.environ['SERVER_ROLES'] = '30'
        os.environ['SERVER_HOST'] = 'test_host'
        os.environ['SERVER_PROTO'] = 'http'
        os.environ['SERVER_PORT'] = '8080'        

    def tearDown(self):
        del os.environ['SERVER_ID']
        del os.environ['SERVER_ROLES']
        del os.environ['SERVER_HOST']
        del os.environ['SERVER_PROTO']
        del os.environ['SERVER_PORT']
        
    def test_create_server_config(self):
        json_config_reader = MagicMock()
        runtime_config_provider = RuntimeConfigProvider()
        environment_config_reader = EnvironmentConfigReader()
        
        config_factory = ConfigFactory(json_config_reader, environment_config_reader, runtime_config_provider)
        
        server_config = config_factory.create_server_config()
        self.assertEqual(server_config.server_roles, PympServerRoles.MEDIA_API | PympServerRoles.META_API | PympServerRoles.THUMB_API | PympServerRoles.MEDIA_SVC)
        
    def test_create_server_config_runtime(self):
        
        json_config_reader = MagicMock()
        runtime_config_provider = RuntimeConfigProvider()
        environment_config_reader = EnvironmentConfigReader()        
        config_factory = ConfigFactory(json_config_reader, environment_config_reader, runtime_config_provider)
        
        server_config = config_factory.create_server_config()
        self.assertEqual(server_config.server_roles, PympServerRoles.MEDIA_API | PympServerRoles.META_API | PympServerRoles.THUMB_API | PympServerRoles.MEDIA_SVC)
        
        runtime_config_provider.set_config(ServerConfig, "ROLES", PympServerRoles.NONE)
        
        server_config = config_factory.create_server_config()
        self.assertEqual(server_config.server_roles, PympServerRoles.NONE)