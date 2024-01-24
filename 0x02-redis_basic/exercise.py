#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called"""
    @wraps(method)
    def inc_count(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return inc_count


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs for a particular func"""
    @wraps(method)
    def store_hist(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return store_hist


def replay(method: Callable) -> None:
    """display the history of calls of a particular function"""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for input_value, output_value in zip(inputs, outputs):
        input_str = input_value.decode("utf-8")
        output_str = output_value.decode("utf-8")
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")


class Cache:
    """stores an instance of the Redis client"""
    def __init__(self):
        """Initializing a cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
