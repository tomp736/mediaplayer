from threading import Timer

import requests
import logging
from pymp_common.app.FfmpegService import ffmpeg_service
from pymp_common.app.MediaDirectoryService import media_directory_service
from pymp_common.app.PympConfig import pymp_env
from pymp_common.dataaccess.http_request_factory import media_registry_request_factory

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            
def ffmpeg_loop():      
    s = requests.Session()    
    registryRequest = media_registry_request_factory.media_list()
    registryResponse = s.send(registryRequest.prepare())
    media_ids = registryResponse.json()
    logging.info(media_ids)
    if media_ids:
        for id in media_ids:
            logging.info(id)
            ffmpeg_service.process_media(id)
    
def media_loop():      
    id = pymp_env.get("SERVER_ID") 
    scheme = pymp_env.get("MEDIA_SVC_SCHEME")
    host = pymp_env.get("MEDIA_SVC_HOST")
    port = pymp_env.get("MEDIA_SVC_PORT")
    
    # helloResponse = media_hello(id)
    # logging.info(helloResponse)
    # if helloResponse.status_code == 404:
    registerResponse = media_register(id, scheme, host, port)
    logging.info(registerResponse)
            
def media_register(id, scheme, host, port) -> requests.Response: 
    media_directory_service.update_index()
    registerRequest = media_registry_request_factory.register(
        id, 
        scheme, 
        host, 
        port
    )
    s = requests.Session()
    return s.send(registerRequest.prepare())
            
def media_hello(id) -> requests.Response:    
    helloRequest = media_registry_request_factory.hello(
        id
    )    
    s = requests.Session()
    return s.send(helloRequest.prepare())