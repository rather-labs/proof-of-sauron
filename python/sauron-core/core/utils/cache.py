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

    def clear_cache(self, prefix=None):
        """Clear all or specific cache files"""
        if not os.path.exists(self.cache_dir):
            return

        count = 0
        for filename in os.listdir(self.cache_dir):
            if prefix is None or filename.startswith(prefix):
                try:
                    os.remove(os.path.join(self.cache_dir, filename))
                    count += 1
                except Exception:
                    pass

        print(f"Cleared {count} cache files")

    def _create_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create unique cache key based on function name and arguments"""
        # Handle numpy arrays specially
        processed_args = []
        for arg in args:
            if isinstance(arg, np.ndarray):
                # Use array shape, mean and std for the key
                processed_args.append(f"array_{arg.shape}_{np.mean(arg):.4f}_{np.std(arg):.4f}")
            else:
                processed_args.append(str(arg))

        # Create key string
        key_data = f"{func_name}:{processed_args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def memoize(func: Callable) -> Callable:
        """Memory-based memoization decorator for faster access"""
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create key from arguments
            key = str(args) + str(sorted(kwargs.items()))

            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]

        return wrapper