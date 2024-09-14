#!/usr/bin/env python3
"""LRU caching"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU cache system that inherits from BaseCaching"""
    def __init__(self):
        """Initiliazes the class"""
        super().__init__()

    def put(self, key, item):
        """Adds an item in cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.pop(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = next(iter(self.cache_data))
            self.cache_data.pop(lru_key)
            print(f"DISCARD: {lru_key}")

        self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
