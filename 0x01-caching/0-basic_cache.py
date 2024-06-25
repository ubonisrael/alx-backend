#!/usr/bin/env python3
"""Contains the BasicCache class"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A basic cache class"""

    def put(self, key, item):
        """Adds an item to a cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        """Gets an item from the cache if its key exists"""
        return self.cache_data.get(key, None)
