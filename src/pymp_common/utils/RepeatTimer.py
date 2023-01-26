import json
from threading import Timer

import requests
import logging
from pymp_common.dataaccess.redis import media_service_da, media_source_da
from pymp_common.app.FfmpegService import ffmpeg_service
from pymp_common.app.MediaDirectoryService import media_directory_service
from pymp_common.app.PympConfig import pymp_env

from pymp_common.dataaccess.http_request_factory import media_registry_request_factory
from pymp_common.dataaccess.http_request_factory import media_request_factory

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            
def mediaregistry_loop():      
        
    media_svc_url = None
    # check if media_service_da exists
    if media_service_da.has():
        # get all media_services
        redis_media_service_dict = media_service_da.hgetall()
        redis_media_source_dict = media_source_da.hgetall() 
        
        media_servi_source_dict = {}
        
        if redis_media_service_dict:
            for media_svc_id in redis_media_service_dict:
                serviceinfo = json.loads(redis_media_service_dict[media_svc_id])
                scheme = serviceinfo["scheme"]
                host = serviceinfo["host"]
                port = serviceinfo["port"]
                media_svc_url = f"{scheme}://{host}:{port}"                
                try:
                    s = requests.Session()
                    mediaListRequest = media_request_factory._get_media_list_(media_svc_url)
                    mediaListResponse = s.send(mediaListRequest.prepare())                    
                    for media_svc_media_id in mediaListResponse.json():
                        media_servi_source_dict[media_svc_media_id] = media_svc_id
                        media_source_da.hset(media_svc_media_id, media_svc_id)
                    logging.info(mediaListResponse.status_code)
                except Exception as ex:
                    logging.info(ex)
                    media_service_da.hdel(media_svc_id)
                                   
            if not redis_media_source_dict is None:                
                for redis_media_id in redis_media_source_dict:       
                    
                    # delete if media_service does not have redis_media_id
                    if not media_servi_source_dict.__contains__(redis_media_id):
                        logging.info(f"deleting: {redis_media_id}")
                        media_source_da.hdel(redis_media_id)
                        continue
                                     
                    media_servi_source = media_servi_source_dict[redis_media_id] 
                    redis_media_source = redis_media_source_dict[redis_media_id]
                    
                    # delete if media_source has changed
                    if not media_servi_source == redis_media_source:
                        logging.info(f"deleting: {redis_media_id}")
                        media_source_da.hdel(redis_media_id)
                        continue
            
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