#!/usr/bin/env python3
'''A module for request caching and tracking with Redis.
   This module caches the content of fetched URLs and tracks how many
   times each URL is requested. It uses Redis for storing cached data.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The Redis instance used for caching and tracking URL requests.
'''


def data_cacher(method: Callable) -> Callable:
    '''Decorator to cache the output of a function that fetches data (e.g., HTTP requests).
       It also tracks the number of times a URL is requested.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''Wraps the method to check if the result is cached. If cached, it retrieves
           the data from Redis; otherwise, it fetches the data, caches it, and tracks the request.
        '''
        # Increment the request count for the given URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result for the URL is already cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')  # Return cached result if available

        # Fetch the result if not cached, cache it, and set an expiration time of 10 seconds
        result = method(url)
        redis_store.set(f'count:{url}', 0)  # Reset the request count
        redis_store.setex(f'result:{url}', 10, result)  # Cache result with expiration of 10 seconds
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Fetches the content of a URL and caches the result.
       Tracks the number of requests to the URL and caches the response for 10 seconds.
    '''
    return requests.get(url).text  # Fetch and return the page content
