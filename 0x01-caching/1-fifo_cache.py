#!/usr/bin/env python3
"""FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO cache system that inherits from BaseCaching
    and is a caching system
    """
    def __init__(self):
        """Initiliazes the class.
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ adds an item in cache
        args:
            key: key of item
            item: item to add
        """
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.queue.pop(0)
                del self.cache_data[discard]
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ gets an item by key
        args:
            key: key where item is stored
        """
        return self.cache_data.get(key, None)
