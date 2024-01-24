#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """stores an instance of the Redis client"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores input data in redis using random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
