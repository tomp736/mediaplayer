

from enum import IntFlag


class ServiceInfo():

    def __init__(self) -> None:
        self.service_id = ""
        self.service_type = 0
        self.service_proto = ""
        self.service_host = ""
        self.service_port = ""

    def is_valid(self):
        if self.service_proto in ["http", "https"]:
            return True
        else:
            return False
        
    def get_uri(self):
        if self.service_proto in ["http", "https"]:
            return f"{self.service_proto}://{self.service_host}:{self.service_port}"
        else:
            raise Exception(f"ServiceInfo Not Valid: {self.__dict__}")


class MediaInfo():

    def __init__(self) -> None:
        self.media_id = ""
        self.service_id = ""



class PympServiceType(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    MEDIAREGISTRY_SVC = 32
    FILEUPLOAD_SVC = 64