from typing import Dict, Union
import redis

from ..app.PympConfig import pymp_env


class RedisDataAccess():
    def __init__(self, decode_responses):
        host = pymp_env.get("REDIS_HOST")
        port = pymp_env.get("REDIS_PORT")
        self.redis = redis.Redis(host=host, port=int(
            port), db=0, decode_responses=decode_responses)


class RedisMediaPathDataAccess():
    def __init__(self):
        self.key = "media_path"
        self.redis = RedisDataAccess(True).redis

    def has(self) -> Union[bool, None]:
        return self.redis.exists(f"{self.key}") > 0

    def hhas(self, id: str) -> Union[bool, None]:
        return self.redis.hexists(f"{self.key}", id)

    def hset(self, id: str, value: str):
        return self.redis.hset(f"{self.key}", id, value)

    def hget(self, id: str) -> Union[str, None]:
        return self.redis.hget(f"{self.key}", id)

    def hdel(self, id: str):
        return self.redis.hdel(f"{self.key}", id)

    def hgetall(self) -> Union[Dict[str, str], None]:
        return self.redis.hgetall(f"{self.key}")


media_path_da = RedisMediaPathDataAccess()


class RedisMediaLengthDataAccess():
    def __init__(self):
        self.key = "media_length"
        self.redis = RedisDataAccess(True).redis

    def has(self) -> Union[bool, None]:
        return self.redis.exists(f"{self.key}") > 0

    def hhas(self, id: str) -> Union[bool, None]:
        return self.redis.hexists(f"{self.key}", id)

    def hset(self, id: str, value: int):
        return self.redis.hset(f"{self.key}", id, value)

    def hget(self, id: str) -> Union[str, None]:
        return self.redis.hget(f"{self.key}", id)

    def hdel(self, id: str):
        return self.redis.hdel(f"{self.key}", id)

    def hgetall(self) -> Union[Dict[str, str], None]:
        return self.redis.hgetall(f"{self.key}")


media_length_da = RedisMediaLengthDataAccess()


class RedisMediaMetaDataAccess():
    def __init__(self):
        self.key = "media_meta"
        self.redis = RedisDataAccess(False).redis

    def has(self, id: str) -> bool:
        return self.redis.exists(f"{self.key}_{id}") > 0

    def set(self, id: str, value: str):
        return self.redis.set(f"{self.key}_{id}", value)

    def get(self, id: str) -> Union[bytes, None]:
        return self.redis.get(f"{self.key}_{id}")


media_meta_da = RedisMediaMetaDataAccess()


class RedisMediaThumbDataAccess():
    def __init__(self):
        self.key = "media_thumb"
        self.redis = RedisDataAccess(False).redis

    def has(self, id: str) -> bool:
        return self.redis.exists(f"{self.key}_{id}") > 0

    def set(self, id: str, value: bytes):
        return self.redis.set(f"{self.key}_{id}", value)

    def get(self, id: str) -> Union[bytes, None]:
        return self.redis.get(f"{self.key}_{id}")


media_thumb_da = RedisMediaThumbDataAccess()


class RedisMediaAccess():
    def __init__(self):
        self.key = "media"
        self.redis = RedisDataAccess(False).redis

    def has(self, id: str) -> bool:
        return self.redis.exists(f"{self.key}_{id}") > 0

    def set(self, id: str, value: bytes):
        return self.redis.set(f"{self.key}_{id}", value)

    def get(self, id: str) -> Union[bytes, None]:
        return self.redis.get(f"{self.key}_{id}")


media_da = RedisMediaAccess()
