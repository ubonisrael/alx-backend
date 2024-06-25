#!/usr/bin/env python3
"""Contains the LFUCache class"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """Implements a Cache using LFU algorithm"""
    def __init__(self):
        """Initializes a stack"""
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """Adds an item to the cache"""
        if key is None or item is None:
            return

        if self.cache_data.get(key, None) is None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # lfk - least frequent key
                lfk = None
                for x in self.stack:
                    if lfk is None or lfk[1] > x['freq']:
                        lfk = (x['key'], x['freq'])
                print("DISCARD: {}".format(lfk[0]))
                del self.cache_data[lfk[0]]
                # remove key from stack
                count = 0
                for x in self.stack:
                    if lfk[0] == x['key']:
                        break
                    count += 1
                del self.stack[count]

        self.cache_data[key] = item
        for x in self.stack:
            if x['key'] == key:
                x['freq'] += 1
                return
        self.stack.append({'key': key, 'freq': 1})

    def get(self, key):
        """Returns a cached value"""
        if self.cache_data.get(key, None) is not None:
            value = self.cache_data.get(key)
            count = 0
            for item in self.stack:
                if key == item['key']:
                    freq = item['freq']
                    break
                count += 1
            del self.stack[count]
            del self.cache_data[key]
            self.cache_data[key] = value
            self.stack.append({'key': key, 'freq': freq + 1})
            return value
        return None
