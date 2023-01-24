import os
from enum import IntFlag

class PympServer(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    
class PympEnv:

    def __init__(self):
        self.getkeys = {
            'FLASK_RUN_HOST': "0.0.0.0",
            'FLASK_RUN_PORT': "80",
            
            'REDIS_HOST': "",
            'REDIS_PORT': "80",

            'MEDIA_API_SCHEME': "http",
            'MEDIA_API_HOST': "",
            'MEDIA_API_PORT': "80",

            'THUMB_API_SCHEME': "http",
            'THUMB_API_HOST': "",
            'THUMB_API_PORT': "80",

            'META_API_SCHEME': "http",
            'META_API_HOST': "",
            'META_API_PORT': "80",

            'MEDIA_SVC_SCHEME': "http",
            'MEDIA_SVC_HOST': "",
            'MEDIA_SVC_PORT': "80",

            'FFMPEG_SVC_SCHEME': "http",
            'FFMPEG_SVC_HOST': "",
            'FFMPEG_SVC_PORT': "80",
            
            'SERVER_TYPE' : "31",
            
            'CORS_HEADER': "",
            'MEDIA_CHUNK_SIZE': 2 ** 20,
            'THUMB_CHUNK_SIZE': 2 ** 10
        }

    def get(self, key: str) -> str:
        if key in self.getkeys:
            value = os.environ.get(key)
            if not value or value == "":
                value = str(self.getkeys.get(key))
            return value

        raise ValueError(f"{key} is not valid.")
    
    def getServerType(self):
        serverType = int(self.get("SERVER_TYPE"))
        return PympServer(serverType)
    

    def getRole(self) -> str:
        scheme = self.get("MEDIA_API_SCHEME")
        host = self.get("MEDIA_API_HOST")
        port = self.get("MEDIA_API_PORT")
        return f"{scheme}://{host}:{port}"

    def media_api_base_url(self) -> str:
        scheme = self.get("MEDIA_API_SCHEME")
        host = self.get("MEDIA_API_HOST")
        port = self.get("MEDIA_API_PORT")
        return f"{scheme}://{host}:{port}"

    def thumb_api_base_url(self) -> str:
        scheme = self.get("THUMB_API_SCHEME")
        host = self.get("THUMB_API_HOST")
        port = self.get("THUMB_API_PORT")
        return f"{scheme}://{host}:{port}"

    def meta_api_base_url(self) -> str:
        scheme = self.get("META_API_SCHEME")
        host = self.get("META_API_HOST")
        port = self.get("META_API_PORT")
        return f"{scheme}://{host}:{port}"

    def media_svc_base_url(self) -> str:
        scheme = self.get("MEDIA_SVC_SCHEME")
        host = self.get("MEDIA_SVC_HOST")
        port = self.get("MEDIA_SVC_PORT")
        return f"{scheme}://{host}:{port}"

    def ffmpeg_svc_base_url(self) -> str:
        scheme = self.get("FFMPEG_SVC_SCHEME")
        host = self.get("FFMPEG_SVC_HOST")
        port = self.get("FFMPEG_SVC_PORT")
        return f"{scheme}://{host}:{port}"


pymp_env = PympEnv()
