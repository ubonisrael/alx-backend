#!/usr/bin/env python3
"""Contains the FIFOCache class"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """Implements a Cache using LIFO"""
    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        if self.cache_data.get(key, None) is None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keys = list(self.cache_data.keys())
                print("DISCARD: {}".format(keys[0]))
                del self.cache_data[keys[0]]

        self.cache_data[key] = item

    def get(self, key):
        """Returns a cached value"""
        return self.cache_data.get(key, None)
