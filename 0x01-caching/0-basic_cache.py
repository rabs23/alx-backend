#!/usr/bin/env python3
"""BaseCaching module"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BaseCaching defines:
      - overwrite functions 'put' and 'get' for implement
      caching system
    """

    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item
        value for the key key.
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Return the value in self.cache_data linked to key."""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
