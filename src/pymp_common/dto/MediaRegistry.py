

from enum import IntFlag
import json


class ServiceInfo():

    def __init__(self) -> None:
        self.service_id = ""
        self.service_type = 0
        self.service_proto = ""
        self.service_host = ""
        self.service_port = ""

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return ServiceInfo(**json_dict)

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

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return MediaInfo(**json_dict)


class PympServiceType(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    MEDIAREGISTRY_SVC = 32
    FILEUPLOAD_SVC = 64
