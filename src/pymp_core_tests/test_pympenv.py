import logging
import os
import unittest
from pymp_core.app import config

class PympEnvTest(unittest.TestCase):
    
    def test_default_config(self):
        self.assertEqual(config.FLASK_RUN_HOST, '0.0.0.0')
        self.assertEqual(config.FLASK_RUN_PORT, '80')
        self.assertEqual(config.REDIS_HOST, '')
        self.assertEqual(config.REDIS_PORT, '2379')
        self.assertEqual(config.MEDIA_SVC_MEDIAPATH, '/app/media')
        self.assertEqual(config.MEDIA_SVC_INDEXPATH, '/app/index')
        self.assertEqual(config.CORS_HEADER, '*')
        self.assertEqual(config.MEDIA_CHUNK_SIZE, 2 ** 22)
        self.assertEqual(config.THUMB_CHUNK_SIZE, 2 ** 10)