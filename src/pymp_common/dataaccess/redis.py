from abc import ABC
import json
from typing import Dict
from typing import Union
import redis

from pymp_common.app.PympConfig import pymp_env


class RedisDataAccess(ABC):
    def __init__(self, decode_responses):
        host = pymp_env.get("REDIS_HOST")
        port = pymp_env.get("REDIS_PORT")
        self.redis = redis.Redis(host=host, port=int(
            port), db=0, decode_responses=decode_responses)

    def is_redis_readonly_replica(self):
        info = self.redis.info()
        return info.get("role") == "slave" and info.get("master_link_status") == "up"

class RedisMediaServiceDataAccess(RedisDataAccess):
    def __init__(self):
        super().__init__(True)
        self.key = "media_service"

    def has(self) -> Union[bool, None]:
        return self.redis.exists(f"{self.key}") > 0

    def hhas(self, id: str) -> Union[bool, None]:
        return self.redis.hexists(f"{self.key}", id)

    def expire(self):
        if not self.redis.readonly:
            self.redis.expire(f"{self.key}", 180)

    def hset(self, id: str, proto: str, host: str, port: str):
        self.expire()
        data = {"proto": proto, "host": host, "port": port}
        return self.redis.hset(f"{self.key}", id, json.dumps(data))

    def hget(self, id: str) -> Union[Dict, None]:
        data = self.redis.hget(f"{self.key}", id)
        if not data is None:
            return json.loads(data)
        return None

    def hdel(self, id: str):
        return self.redis.hdel(f"{self.key}", id)

    def hgetall(self) -> Union[Dict[str, str], None]:
        return self.redis.hgetall(f"{self.key}")


media_service_info_da = RedisMediaServiceDataAccess()


class RedisMediaSourceDataAccess(RedisDataAccess):
    def __init__(self):
        super().__init__(True)
        self.key = f"media_source"

    def has(self) -> Union[bool, None]:
        return self.redis.exists(f"{self.key}") > 0

    def hhas(self, id: str) -> Union[bool, None]:
        return self.redis.hexists(f"{self.key}", id)

    def expire(self):
        if not self.redis.readonly:
            self.redis.expire(f"{self.key}", 180)

    def hset(self, id: str, value: str):
        self.expire()
        return self.redis.hset(f"{self.key}", id, value)

    def hget(self, id: str) -> Union[str, None]:
        return self.redis.hget(f"{self.key}", id)

    def hdel(self, id: str):
        return self.redis.hdel(f"{self.key}", id)

    def hgetall(self) -> Union[Dict[str, str], None]:
        return self.redis.hgetall(f"{self.key}")


media_service_media_da = RedisMediaSourceDataAccess()


class RedisMediaMetaDataAccess(RedisDataAccess):
    def __init__(self):
        super().__init__(False)
        self.key = "media_meta"

    def has(self, id: str) -> bool:
        return self.redis.exists(f"{self.key}_{id}") > 0

    def expire(self):
        if not self.redis.readonly:
            self.redis.expire(f"{self.key}", 360)

    def set(self, id: str, value: str):
        self.expire()
        return self.redis.set(f"{self.key}_{id}", value)

    def get(self, id: str) -> Union[bytes, None]:
        self.expire()
        return self.redis.get(f"{self.key}_{id}")


media_meta_da = RedisMediaMetaDataAccess()


class RedisMediaThumbDataAccess(RedisDataAccess):
    def __init__(self):
        super().__init__(False)
        self.key = "media_thumb"

    def has(self, id: str) -> bool:
        return self.redis.exists(f"{self.key}_{id}") > 0

    def expire(self):
        if not self.redis.readonly:
            self.redis.expire(f"{self.key}", 360)

    def set(self, id: str, value: bytes):
        self.expire()
        return self.redis.set(f"{self.key}_{id}", value)

    def get(self, id: str) -> Union[bytes, None]:
        self.expire()
        return self.redis.get(f"{self.key}_{id}")


media_thumb_da = RedisMediaThumbDataAccess()
