#!/usr/bin/env python3
"""
web.py: Module for fetching HTML content from a URL and caching the results with a decorator.
"""


import requests
from datetime import datetime, timedelta
from functools import wraps

def cache_decorator(func):
    """
    Decorator function for caching the results of a function with an expiration time.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    cache = {}

    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper function that checks the cache for the result and fetches it or updates
        the cache based on the expiration time.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            str: The HTML content of the URL.
        """
        key = f"count:{url}"
        if key in cache and cache[key]['expiration'] > datetime.now():
            cache[key]['count'] += 1
            return cache[key]['content']
        else:
            content = func(url)
            cache[key] = {'content': content, 'expiration': datetime.now() + timedelta(seconds=10), 'count': 1}
            return content

    return wrapper

@cache_decorator
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
