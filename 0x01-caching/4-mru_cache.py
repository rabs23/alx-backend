#!/usr/bin/env python3
""" MRU Cache """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU Cache class """
    def __init__(self):
        """ Initiliazes the class """
        super().__init__()

    def put(self, key, item):
        """ Adds an item in cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            mru_key = max(self.cache_data, key=self.cache_data.get)
            del self.cache_data[mru_key]
            print("DISCARD:", mru_key)

    def get(self, key):
        """ Gets an item by key"""
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
