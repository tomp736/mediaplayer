import os
from enum import IntFlag

class PympServer(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    MEDIAREGISTRY_SVC = 32
    
class PympEnv:

    def __init__(self):
        self.getkeys = {
            'FLASK_RUN_HOST': "0.0.0.0",
            'FLASK_RUN_PORT': "80",
            
            'REDIS_HOST': "",
            'REDIS_PORT': "80",
            
            'SERVER_TYPE' : "63",
            'SERVER_ID' : "DEFAULT",
            
            'CORS_HEADER': "",
            'MEDIA_CHUNK_SIZE': 2 ** 22,
            'THUMB_CHUNK_SIZE': 2 ** 10
        }
        for pympServer in PympServer:
            self.getkeys[f"{pympServer.name}_SCHEME"] = "http"
            self.getkeys[f"{pympServer.name}_HOST"] = ""
            self.getkeys[f"{pympServer.name}_PORT"] = "80"

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

    def getBaseUrl(self, server:PympServer) -> str:
        scheme = self.get(f"{server.name}_SCHEME")
        host = self.get(f"{server.name}_HOST")
        port = self.get(f"{server.name}_PORT")
        return f"{scheme}://{host}:{port}"


pymp_env = PympEnv()
