

import json
import logging

import requests
from pymp_common.dataaccess.redis import media_service_da, media_source_da
from pymp_common.dataaccess.http_request_factory import media_request_factory
from pymp_common.utils.RepeatTimer import RepeatTimer


class MediaRegistry():
    
    def __init__(self):    
        timer = RepeatTimer(60, self.update_media_services)
        timer.start()    
    
    def get_media_svc_media_ids(self, serviceinfo):
        media_svc_media_ids = []
        
        scheme = serviceinfo["scheme"]
        host = serviceinfo["host"]
        port = serviceinfo["port"]
        media_svc_url = f"{scheme}://{host}:{port}" 
        s = requests.Session()
        mediaListRequest = media_request_factory._get_media_list_(media_svc_url)
        mediaListResponse = s.send(mediaListRequest.prepare())                    
        for media_svc_media_id in mediaListResponse.json():
            media_svc_media_ids.append(media_svc_media_id)
        return media_svc_media_ids
            
    def update_media_services(self):
        if not media_service_da.has():
            return
                
        redis_media_service_dict = media_service_da.hgetall()            
        if redis_media_service_dict is None:
            return
            
        for media_svc_id in redis_media_service_dict:
            serviceinfo = json.loads(redis_media_service_dict[media_svc_id])
            media_svc_media_ids = self.check_media_service(media_svc_id, serviceinfo)
            self.check_media_sources(media_svc_id, media_svc_media_ids)            

    def check_media_service(self, media_svc_id, serviceinfo):
        media_svc_media_ids = []               
        try:
            self.get_media_svc_media_ids(serviceinfo)
        except Exception as ex:
            logging.info(ex)
            media_service_da.hdel(media_svc_id)            
        return media_svc_media_ids

    def check_media_sources(self, media_svc_id, media_svc_media_ids):
        redis_media_source_dict = media_source_da.hgetall() 
        
        if redis_media_source_dict is None:
            return
        
        for redis_media_id in redis_media_source_dict:       
            # delete from redis if media_svc no longer has the media
            if not media_svc_media_ids.__contains__(redis_media_id):
                logging.info(f"deleting: {redis_media_id}")
                media_source_da.hdel(redis_media_id)
                continue
                        
            # if media source for media  has changed, update redis
            if not redis_media_source_dict[redis_media_id] == media_svc_id:
                logging.info(f"deleting: {redis_media_id}")
                media_source_da.hset(redis_media_id, media_svc_id)
                continue