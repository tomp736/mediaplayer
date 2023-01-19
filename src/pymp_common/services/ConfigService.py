from typing import Dict
import os

class ConfigService:
    media_host = os.environ.get('SVC_MEDIA_HOST')
    media_port = int(os.environ.get('SVC_MEDIA_PORT', '80'))
    
    thumb_host = os.environ.get('SVC_THUMB_HOST')
    thumb_port = int(os.environ.get('SVC_THUMB_PORT', '80'))
    
    meta_host = os.environ.get('SVC_META_HOST')
    meta_port = int(os.environ.get('SVC_META_PORT', '80'))
    
    feapi_host = os.environ.get('SVC_FEAPI_HOST')
    feapi_port = int(os.environ.get('SVC_FEAPI_PORT', '80'))
    
    flask_host = os.environ.get('FLASK_RUN_HOST') 
    flask_port = int(os.environ.get('FLASK_RUN_PORT', '80'))
    
    chunk_size = int(os.environ.get('CHUNK_SIZE', 2 ** 25))