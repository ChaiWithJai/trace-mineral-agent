"""Caching layer for literature search results."""

import contextlib
import hashlib
import json
import os
import time
from datetime import timedelta
from pathlib import Path
from typing import Any


class SearchCache:
    """
    Cache for literature search results.

    Supports both in-memory and file-based backends.
    """

    def __init__(
        self,
        backend: str = "memory",
        ttl: timedelta = timedelta(hours=24),
        cache_dir: str | None = None,
    ):
        """
        Initialize the search cache.

        Args:
            backend: Cache backend ("memory" or "file")
            ttl: Time-to-live for cache entries
            cache_dir: Directory for file-based cache (default: ~/.trace_mineral_cache)
        """
        self.backend = backend
        self.ttl = ttl
        self._memory_cache: dict[str, tuple[float, Any]] = {}

        if backend == "file":
            self.cache_dir = Path(cache_dir or os.path.expanduser("~/.trace_mineral_cache"))
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.cache_dir = None

        # Stats
        self.hits = 0
        self.misses = 0

    def _make_key(self, query: str, paradigm: str, max_results: int) -> str:
        """Create a cache key from search parameters."""
        key_data = f"{query.lower().strip()}:{paradigm}:{max_results}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]

    def get(self, query: str, paradigm: str, max_results: int = 10) -> list | None:
        """
        Get cached search results.

        Args:
            query: Search query
            paradigm: Medical paradigm
            max_results: Maximum results requested

        Returns:
            Cached results if valid, None otherwise
        """
        key = self._make_key(query, paradigm, max_results)

        if self.backend == "memory":
            return self._get_memory(key)
        elif self.backend == "file":
            return self._get_file(key)
        return None

    def set(
        self,
        query: str,
        paradigm: str,
        results: list,
        max_results: int = 10,
    ) -> None:
        """
        Cache search results.

        Args:
            query: Search query
            paradigm: Medical paradigm
            results: Search results to cache
            max_results: Maximum results requested
        """
        key = self._make_key(query, paradigm, max_results)
        timestamp = time.time()

        if self.backend == "memory":
            self._set_memory(key, results, timestamp)
        elif self.backend == "file":
            self._set_file(key, results, timestamp, query, paradigm)

    def _get_memory(self, key: str) -> list | None:
        """Get from memory cache."""
        if key not in self._memory_cache:
            self.misses += 1
            return None

        timestamp, results = self._memory_cache[key]
        if time.time() - timestamp > self.ttl.total_seconds():
            # Expired
            del self._memory_cache[key]
            self.misses += 1
            return None

        self.hits += 1
        return results

    def _set_memory(self, key: str, results: list, timestamp: float) -> None:
        """Set in memory cache."""
        self._memory_cache[key] = (timestamp, results)

    def _get_file(self, key: str) -> list | None:
        """Get from file cache."""
        if self.cache_dir is None:
            return None

        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            self.misses += 1
            return None

        try:
            with open(cache_file) as f:
                data = json.load(f)

            timestamp = data.get("timestamp", 0)
            if time.time() - timestamp > self.ttl.total_seconds():
                # Expired - delete file
                cache_file.unlink()
                self.misses += 1
                return None

            self.hits += 1
            return data.get("results", [])
        except (json.JSONDecodeError, KeyError):
            self.misses += 1
            return None

    def _set_file(
        self,
        key: str,
        results: list,
        timestamp: float,
        query: str,
        paradigm: str,
    ) -> None:
        """Set in file cache."""
        if self.cache_dir is None:
            return

        cache_file = self.cache_dir / f"{key}.json"
        data = {
            "timestamp": timestamp,
            "query": query,
            "paradigm": paradigm,
            "results": results,
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
        except (OSError, TypeError):
            pass  # Fail silently on cache write errors

    def clear(self) -> None:
        """Clear all cached entries."""
        if self.backend == "memory":
            self._memory_cache.clear()
        elif self.backend == "file" and self.cache_dir:
            for cache_file in self.cache_dir.glob("*.json"):
                with contextlib.suppress(OSError):
                    cache_file.unlink()

        self.hits = 0
        self.misses = 0

    def stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0.0

        return {
            "backend": self.backend,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1%}",
            "ttl_hours": self.ttl.total_seconds() / 3600,
        }


# Global cache instance
_cache: SearchCache | None = None


def get_cache() -> SearchCache:
    """Get or create the global cache instance."""
    global _cache

    if _cache is None:
        backend = os.getenv("SEARCH_CACHE_BACKEND", "memory")
        ttl_hours = int(os.getenv("SEARCH_CACHE_TTL_HOURS", "24"))
        cache_dir = os.getenv("SEARCH_CACHE_DIR")

        _cache = SearchCache(
            backend=backend,
            ttl=timedelta(hours=ttl_hours),
            cache_dir=cache_dir,
        )

    return _cache


def cached_search(
    search_func,
    query: str,
    paradigm: str,
    max_results: int = 10,
) -> list:
    """
    Wrapper to cache search function results.

    Args:
        search_func: The actual search function to call
        query: Search query
        paradigm: Medical paradigm
        max_results: Maximum results

    Returns:
        Search results (cached or fresh)
    """
    cache = get_cache()

    # Try cache first
    cached = cache.get(query, paradigm, max_results)
    if cached is not None:
        return cached

    # Call actual search function
    results = search_func(query, max_results)

    # Cache results (only if not an error)
    if results and not (len(results) == 1 and "error" in results[0]):
        cache.set(query, paradigm, results, max_results)

    return results
