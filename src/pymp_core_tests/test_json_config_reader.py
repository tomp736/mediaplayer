import os
import json
from typing import List
from unittest import TestCase
from pymp_core.app.config import ServiceConfig, PympServerRoles

class JsonServiceConfigReader:
    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
    
    def load_config(self) -> List[ServiceConfig]:
        with open(self.config_file_path, 'r', encoding='utf-8') as file_io:
            data = json.load(file_io)
        return [ServiceConfig(**config) for config in data]

class TestJsonServiceConfigReader(TestCase):
    def setUp(self):
        self.config_path = 'test_config.json'
        self.config_data = [
            {
                "service_id": "service1",
                "service_roles": 6,
                "service_host": "localhost",
                "service_proto": "http",
                "service_port": 8080
            },
            {
                "service_id": "service2",
                "service_roles": 96,
                "service_host": "127.0.0.1",
                "service_proto": "https",
                "service_port": 8443
            }
        ]
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data, f)

    def tearDown(self):
        os.remove(self.config_path)

    def test_load_config(self):
        reader = JsonServiceConfigReader(self.config_path)
        configs = reader.load_config()
        self.assertEqual(len(configs), 2)
        self.assertEqual(configs[0].service_id, "service1")
        self.assertEqual(configs[0].service_roles, PympServerRoles.MEDIA_API | PympServerRoles.META_API)
        self.assertEqual(configs[0].service_host, "localhost")
        self.assertEqual(configs[0].service_proto, "http")
        self.assertEqual(configs[0].service_port, 8080)
        self.assertEqual(configs[1].service_id, "service2")
        self.assertEqual(configs[1].service_roles, PympServerRoles.FFMPEG_SVC | PympServerRoles.MEDIAREGISTRY_SVC)
        self.assertEqual(configs[1].service_host, "127.0.0.1")
        self.assertEqual(configs[1].service_proto, "https")
        self.assertEqual(configs[1].service_port, 8443)
