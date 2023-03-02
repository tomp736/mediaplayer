

from enum import IntFlag
import json


class ServiceInfo():

    def __init__(self, **kwargs) -> None:
        self.server_id = kwargs.get("server_id", "")
        self.server_roles = kwargs.get("server_roles", 0)
        self.server_proto = kwargs.get("server_proto", "")
        self.server_host = kwargs.get("server_host", "")
        self.server_port = kwargs.get("server_port", "")

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
        if self.server_proto in ["http", "https"]:
            return True
        else:
            return False

    def get_uri(self):
        if self.server_proto in ["http", "https"]:
            return f"{self.server_proto}://{self.server_host}:{self.server_port}"
        else:
            raise Exception(f"ServiceInfo Not Valid: {self.__dict__}")


class MediaInfo():

    def __init__(self, **kwargs) -> None:
        self.media_id = kwargs.get("media_id", "")
        self.server_id = kwargs.get("server_id", "")

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


class PympServerRoles(IntFlag):
    MEDIA_API = 1
    META_API = 2
    THUMB_API = 4
    MEDIA_SVC = 8
    FFMPEG_SVC = 16
    MEDIAREGISTRY_SVC = 32
