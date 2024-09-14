#!/usr/bin/env python3
"""LFU caching"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU cache system that inherits from BaseCaching"""
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """Adds an item in cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.update_frequency(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self.discard_item()
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key"""
        if key is None or key not in self.cache_data:
            return None

        self.update_frequency(key)
        return self.cache_data[key]

    def update_frequency(self, key):
        """Updates the frequency of an item in cache"""
        frequency, value = self.cache_data[key]
        frequency += 1
        self.cache_data[key] = (frequency, value)

    def discard_item(self):
        """Discards the least frequently used item in cache"""
        min_frequency = float('inf')
        lfu_keys = []
        for key, (frequency, _) in self.cache_data.items():
            if frequency < min_frequency:
                min_frequency = frequency
                lfu_keys = [key]
            elif frequency == min_frequency:
                lfu_keys.append(key)

        if len(lfu_keys) > 1:
            lru_key = min(lfu_keys, key=lambda k: self.cache_data[k][1])
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}\n")
        else:
            del self.cache_data[lfu_keys[0]]
            print(f"DISCARD: {lfu_keys[0]}\n")
