

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