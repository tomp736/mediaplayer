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
    config = {
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

    def __init__(self):
        self.load_configs()
        self.validate_server_configs()

    def load_configs(self):
        for envKey in self.config:
            value = os.environ.get(envKey, self.config[envKey])            
            self.config[envKey] = value
        for pympServer in PympServer:
            self.config[f"{pympServer.name}_SCHEME"] = os.environ.get(f"{pympServer.name}_SCHEME", "http")
            self.config[f"{pympServer.name}_HOST"] = os.environ.get(f"{pympServer.name}_HOST", "localhost")
            self.config[f"{pympServer.name}_PORT"] = os.environ.get(f"{pympServer.name}_PORT", "80")

    def validate_server_configs(self) -> bool:
        valid = True
        for pympServer in PympServer:
            valid &= self.get_scheme(pympServer) != ""
            valid &= self.get_host(pympServer) != ""
            valid &= self.get_port(pympServer) != ""
        return valid
        
    def get(self, key: str) -> str:
        if key in self.config:
            return str(self.config.get(key))
        else:
            raise ValueError(f"{key} is not configured in PympEnv.")
    
    def get_servertype(self):
        serverType = int(self.get("SERVER_TYPE"))
        return PympServer(serverType)

    def print_servertype(self):
        serverType = self.get_servertype()
        for pympServer in PympServer:
            if serverType & pympServer:
                logging.info(pympServer)

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


pymp_env = PympEnv()
