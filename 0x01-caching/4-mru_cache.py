#!/usr/bin/env python3
"""Contains the MRUCache class"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """Implements a Cache using MRU algorithm"""

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        if self.cache_data.get(key, None) is None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keys = list(self.cache_data.keys())
                print("DISCARD: {}".format(keys[-1]))
                del self.cache_data[keys[-1]]

        self.cache_data[key] = item

    def get(self, key):
        """Returns a cached value"""
        if self.cache_data.get(key, None) is not None:
            value = self.cache_data.get(key)
            del self.cache_data[key]
            self.cache_data[key] = value
            return value
        return None
