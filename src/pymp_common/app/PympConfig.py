import logging
import os
from enum import IntFlag

class PympServer(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    MEDIAREGISTRY_SVC = 32
    FILEUPLOAD_SVC = 64
    
class PympEnv:
    env = {
            'FLASK_RUN_HOST': "0.0.0.0",
            'FLASK_RUN_PORT': "80",
            
            'REDIS_HOST': "",
            'REDIS_PORT': "80",
            
            'SERVER_TYPE' : "63",
            'SERVER_ID' : "DEFAULT",
            
            'MEDIA_SVC_MEDIAPATH' : "/app/media",
            'MEDIA_SVC_INDEXPATH' : "/app/index",
            
            'CORS_HEADER': "",
            'MEDIA_CHUNK_SIZE': 2 ** 22,
            'THUMB_CHUNK_SIZE': 2 ** 10
        }
    for pympServer in PympServer:
        env[f"{pympServer.name}_SCHEME"] = "http"
        env[f"{pympServer.name}_HOST"] = ""
        env[f"{pympServer.name}_PORT"] = "80"

    def __init__(self):
        self.validate_server_config(self.get_servertype())
        

    def get(self, key: str) -> str:
        if key in self.env:
            value = os.environ.get(key)
            if not value or value == "":
                value = str(self.env.get(key))
            return value
        else:
            raise ValueError(f"{key} is not configured in PympEnv.")
    
    def get_servertype(self):
        serverType = int(self.get("SERVER_TYPE"))
        return PympServer(serverType)

    def print_servertype(self):        
        logging.info(self.get_servertype())

    def get_baseurl(self, server:PympServer) -> str:
        scheme = self.get_scheme(server)
        host = self.get_host(server)
        port = self.get_port(server)
        return f"{scheme}://{host}:{port}"

    def get_scheme(self, server:PympServer) -> str:
        return self.get(f"{server.name}_SCHEME")

    def get_host(self, server:PympServer) -> str:
        return self.get(f"{server.name}_HOST")

    def get_port(self, server:PympServer) -> str:
        return self.get(f"{server.name}_PORT")

    def validate_server_config(self, server:PympServer) -> bool:
        hasScheme = self.get_scheme(server) != ""
        hasHost = self.get_host(server) != ""
        hasPort = self.get_port(server) != ""
        return hasScheme == True & hasHost == True & hasPort == True


pymp_env = PympEnv()
