import functools
from typing import Any, Callable
import hashlib
import pickle
import os
import numpy as np

class Cache:
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Check for no_cache keyword argument
            no_cache = kwargs.pop('no_cache', False)
            
            # Create cache key from function name and arguments
            key = self._create_cache_key(func.__name__, args, kwargs)
            cache_path = os.path.join(self.cache_dir, f"{key}.pkl")

            # Check cache if not forced to recompute
            if not no_cache and os.path.exists(cache_path):
                try:
                    with open(cache_path, 'rb') as f:
                        return pickle.load(f)
                except Exception:
                    # If cache read fails, recompute
                    pass

            # Compute result
            result = func(*args, **kwargs)

            # Cache result
            try:
                with open(cache_path, 'wb') as f:
                    pickle.dump(result, f)
            except Exception as e:
                print(f"Warning: Could not cache result: {e}")
                
            return result
            
        return wrapper