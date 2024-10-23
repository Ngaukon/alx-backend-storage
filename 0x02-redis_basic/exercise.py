#!/usr/bin/env python3
'''A module for managing data in Redis, a NoSQL data storage.
   Provides functionality for storing, retrieving, and tracking method
   calls and their histories using Redis.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Decorator to count the number of times a method is called in the Cache class.
       The call count is stored in Redis with the method's qualified name as the key.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Increments the call count for the method in Redis before invoking it.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Decorator to track the history of inputs and outputs of a method in the Cache class.
       The input arguments and output results are stored in Redis as lists.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Stores the inputs in Redis before invoking the method and
           stores the output after invocation.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)  # Key for storing method inputs
        out_key = '{}:outputs'.format(method.__qualname__)  # Key for storing method outputs
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))  # Log input arguments in Redis
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)  # Log output results in Redis
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Retrieves and displays the history of calls (inputs and outputs) for a given method.
       Fetches the input/output history from Redis and prints it in a readable format.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__  # Method's qualified name (used as the key in Redis)
    in_key = '{}:inputs'.format(fxn_name)  # Redis key for inputs
    out_key = '{}:outputs'.format(fxn_name)  # Redis key for outputs

    # Get the count of method calls from Redis
    fxn_call_count = int(redis_store.get(fxn_name) or 0)
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))

    # Get input and output history from Redis
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)

    # Print the inputs and corresponding outputs
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    '''A class that provides an interface to store and retrieve data using Redis.
       It supports tracking method call counts and recording call history.
    '''
    def __init__(self) -> None:
        '''Initializes a Redis connection and clears any existing data in the Redis store.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)  # Clear the Redis database

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in the Redis store with a randomly generated UUID as the key.
           The stored value can be of type string, bytes, int, or float.
           Returns the key under which the data is stored.
        '''
        data_key = str(uuid.uuid4())  # Generate a unique key
        self._redis.set(data_key, data)  # Store the value in Redis
        return data_key  # Return the generated key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from Redis by its key.
           Optionally applies a conversion function `fn` to the retrieved data.
           Returns the value after applying the conversion function, if provided.
        '''
        data = self._redis.get(key)  # Retrieve the data from Redis
        return fn(data) if fn is not None else data  # Apply conversion if needed

    def get_str(self, key: str) -> str:
        '''Retrieves a value from Redis and converts it to a string.
           This is a helper method that applies a string conversion to the result.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves a value from Redis and converts it to an integer.
           This is a helper method that applies an integer conversion to the result.
        '''
        return self.get(key, lambda x: int(x))
