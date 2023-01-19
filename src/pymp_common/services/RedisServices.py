import redis
from typing import Dict
import json

class MediaPathService:
    
    @staticmethod
    def get_redis() -> redis.Redis:
        return redis.Redis(host='redis', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    
    # media_path_index
    
    @staticmethod
    def has_media_path_index(r:redis.Redis) -> bool:
        r_key=f'media_path_index'       
        return r.exists(r_key) > 0
    
    @staticmethod
    def set_media_path_index(r:redis.Redis, index:Dict[str,str]):
        r_key=f'media_path_index'       
        r.set(r_key, json.dumps(index))
        
    @staticmethod
    def get_media_path_index(r:redis.Redis) -> Dict[str,str]:
        r_key=f'media_path_index'       
        return json.loads(r.get(r_key) or "{}")
    
class MediaSizeService:
    
    @staticmethod
    def get_redis() -> redis.Redis:
        return redis.Redis(host='redis', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    
    @staticmethod
    def has_media_size_index(r:redis.Redis) -> bool:
        r_key=f'media_size_index'       
        return r.exists(r_key) > 0
    
    @staticmethod
    def set_media_size_index(r:redis.Redis, index:Dict[str,str]):
        r_key=f'media_size_index'       
        r.set(r_key, json.dumps(index))
        
    @staticmethod
    def get_media_size_index(r:redis.Redis) -> Dict[str,str]:
        r_key=f'media_size_index'       
        return json.loads(r.get(r_key) or "{}")
    
    
class MediaSourceService:    
    
    @staticmethod
    def get_redis() -> redis.Redis:
        return redis.Redis(host='redis', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    
    @staticmethod
    def has_media_source(r:redis.Redis, id:str) -> bool:
        r_key=f'media_source_{id}'       
        return r.exists(r_key) > 0
    
    @staticmethod
    def set_media_source(r:redis.Redis, id:str, source:str):
        r_key=f'media_source_{id}'
        r.set(r_key, source)
        
    @staticmethod
    def get_media_source(r:redis.Redis, id:str) -> str:      
        r_key=f'media_source_{id}'
        return r.get(r_key) or ""
    
class MediaMetaService:   
    
    @staticmethod
    def get_redis() -> redis.Redis:
        return redis.Redis(host='redis', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    
    @staticmethod
    def has_media_meta(r:redis.Redis, id:str) -> bool:
        redis_chunk_key=f'media_meta_{id}'     
        return r.exists(redis_chunk_key) > 0
    
    @staticmethod
    def set_media_meta(r:redis.Redis, id:str, meta:str):
        redis_chunk_key=f'media_meta_{id}'
        r.set(redis_chunk_key, meta)
        
    @staticmethod
    def get_media_meta(r:redis.Redis, id:str) -> str:
        redis_chunk_key=f'media_meta_{id}'        
        return r.get(redis_chunk_key) or ""
    
class MediaThumbService:   
    
    @staticmethod
    def get_redis() -> redis.Redis:
        return redis.Redis(host='redis', port=6379, db=0, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    
    @staticmethod
    def has_media_thumb(r:redis.Redis, id:str) -> bool:
        redis_chunk_key=f'media_thumb_{id}'     
        return r.exists(redis_chunk_key) > 0
    
    @staticmethod
    def set_media_thumb(r:redis.Redis, id:str, thumb:str):
        redis_chunk_key=f'media_thumb_{id}'
        r.set(redis_chunk_key, thumb)
        
    @staticmethod
    def get_media_thumb(r:redis.Redis, id:str) -> str:
        redis_chunk_key=f'media_thumb_{id}'        
        return r.get(redis_chunk_key) or ""