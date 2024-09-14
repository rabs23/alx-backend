#!/usr/bin/env python3
"""LIFO caching"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO cache system that inherits from BaseCaching"""

    def __init__(self):
        """Initiliazes the class"""
        super().__init__()

    def put(self, key, item):
        """Adds an item in cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_item_key = list(self.cache_data.keys())[-1]
            del self.cache_data[last_item_key]
            print("DISCARD:", last_item_key)

        self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
