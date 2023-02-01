from __future__ import annotations
import json
from typing import Dict

class ServiceInfo():
    service_id = ""
    service_proto = ""
    service_host = ""
    service_port = ""
    
    def get_uri(self):
        if self.service_proto in [ "http", "https" ]:
            return f"{self.service_proto}://{self.service_host}:{self.service_port}"
        else:
            raise Exception("Not implemented")
    @staticmethod        
    def from_dict(dobject: Dict) -> ServiceInfo:
        service_info = ServiceInfo()
        service_info.service_id = dobject["id"]
        service_info.service_proto = dobject["proto"]
        service_info.service_host = dobject["host"]
        service_info.service_port = dobject["port"]
        return service_info
    
    @staticmethod
    def from_json_str(jsonString: str) -> ServiceInfo:
        jobject = json.loads(jsonString)
        return ServiceInfo(**jobject)
    
    @staticmethod
    def from_json(jobject) -> ServiceInfo:
        return ServiceInfo(**jobject)

class MediaInfo():
    media_id = ""
    service_id = ""