#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """stores an instance of the Redis client"""
    def __init__(self):
        """Initializing a cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores input data in redis using random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, float]:
        """retrieve original data type from storage"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """parametize Cache.get with correct conversion func"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """parametize Cache.get with correct conversion func"""
        return self.get(key, fn=int)
