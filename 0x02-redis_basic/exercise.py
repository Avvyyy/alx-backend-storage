#!/usr/bin/env python3
"""Exercide.py"""


import redis
import uuid
from typing import Callable, Optional

class Cache:
    """A class to interact with Redis for caching."""

    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str) -> str:
        """
        Store data in Redis and return the generated key.

        Args:
            data (str): The data to be stored in Redis.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve data associated with a key from Redis.

        Args:
            key (str): The key associated with the data in Redis.
            fn (Optional[Callable]): An optional conversion function.

        Returns:
            Any: The retrieved data, optionally converted using the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return data if fn is None else fn(data)

    def get_str(self, key: str) -> str:
        """
        Retrieve data associated with a key from Redis and convert to string.

        Args:
            key (str): The key associated with the data in Redis.

        Returns:
            str: The retrieved data converted to string.
        """
        return self.get(key, fn=lambda x: x.decode())

    def get_int(self, key: str) -> int:
        """
        Retrieve data associated with a key from Redis and convert to integer.

        Args:
            key (str): The key associated with the data in Redis.

        Returns:
            int: The retrieved data converted to integer.
        """
        return self.get(key, fn=int)

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    def wrapper(self, *args, **kwargs):
        """Wrapper function to count method calls."""
        key = method.__qualname__
        self._redis.incr(f"{key}_calls")
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method."""
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store input/output history."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper

def replay(method: Callable):
    """Replay the history of calls for a method."""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}{inp.decode()} -> {out.decode()}")

