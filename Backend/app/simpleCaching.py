from typing import Dict, Any
import threading
from datetime import datetime, timedelta
import json

class SimpleCache:
    def __init__(self, expiration_time: int = 3600):
        """
        Initializes the cache instance.

        :param expiration_time: Time in seconds for cache expiration (default 1 hour).
        """
        self.lock = threading.Lock()  # Thread-safety for concurrent access.
        # self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.expiration_time = expiration_time  # Cache expiration time in seconds.

    def add_to_cache(self, key: str, value: Any):
        """
        Adds a key-value pair to the cache with the current timestamp.

        :param key: Cache key.
        :param value: Value to be cached.
        """
        with self.lock:
            self.cache[key] = {
                "value": value,
                "timestamp": datetime.now()
            }
            print(f"Cache updated. Key: {key}")

    def get_from_cache(self, key: str) -> Any:
        """
        Retrieves a value from the cache if it exists and is not expired.

        :param key: Cache key.
        :return: Cached value if found and not expired, else None.
        """
        
        with self.lock:
            cache_item = self.cache.get(key)
            if cache_item:
                if datetime.now() - cache_item["timestamp"] > timedelta(seconds=self.expiration_time):
                    del self.cache[key]
                    print(f"Cache expired. Key: {key}")
                    return None
                print(f"Cache hit. Key: {key}")
                return cache_item["value"]
            print(f"Cache miss. Key: {key}")
            return None
        
    def clear_cache(self):
        """
        Clears the entire cache.
        """
        with self.lock:
            self.cache.clear()
            print("Cache cleared.")
            

    def remove_from_cache(self, key: str):
        """
        Removes a specific key-value pair from the cache.

        :param key: Cache key to remove.
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                print(f"Cache removed. Key: {key}")

    def cache_size(self) -> int:
        """
        Returns the current size of the cache (number of items).

        :return: Number of items in the cache.
        """
        with self.lock:
            size = len(self.cache)
            print(f"Cache size: {size}")
            return size

def print_cache(self):
        """
        For debugging purposes, print the current cache state.
        """
        print(json.dumps(self.cache, indent=4))

def ignore_milliseconds(dt: datetime) -> datetime:
    """
    Truncate the datetime object to remove the microsecond part for consistent comparison.
    You can adjust this function to round to the nearest second, if needed.
    """
    return dt.replace(microsecond=0)

# # Create a global-default cache instance, expiration is 3600(1hour)
cache = SimpleCache()