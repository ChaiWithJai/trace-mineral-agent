"""Tests for the caching layer."""

import tempfile
import time
from datetime import timedelta

from trace_mineral_agent.cache import SearchCache, cached_search, get_cache


class TestSearchCache:
    """Tests for the SearchCache class."""

    def test_memory_cache_set_and_get(self):
        """Should store and retrieve from memory cache."""
        cache = SearchCache(backend="memory", ttl=timedelta(hours=1))

        results = [{"title": "Test Paper", "authors": "Smith"}]
        cache.set("chromium insulin", "allopathy", results, max_results=10)

        retrieved = cache.get("chromium insulin", "allopathy", max_results=10)
        assert retrieved == results

    def test_memory_cache_miss(self):
        """Should return None for cache miss."""
        cache = SearchCache(backend="memory", ttl=timedelta(hours=1))

        result = cache.get("nonexistent query", "allopathy", max_results=10)
        assert result is None

    def test_memory_cache_expiration(self):
        """Should expire entries after TTL."""
        cache = SearchCache(backend="memory", ttl=timedelta(milliseconds=50))

        results = [{"title": "Test"}]
        cache.set("test query", "allopathy", results, max_results=5)

        # Should be retrievable immediately
        assert cache.get("test query", "allopathy", max_results=5) == results

        # Wait for expiration
        time.sleep(0.1)

        # Should be expired
        assert cache.get("test query", "allopathy", max_results=5) is None

    def test_file_cache_set_and_get(self):
        """Should store and retrieve from file cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = SearchCache(
                backend="file",
                ttl=timedelta(hours=1),
                cache_dir=tmpdir,
            )

            results = [{"title": "Test Paper"}]
            cache.set("zinc deficiency", "naturopathy", results, max_results=5)

            # Create new cache instance to test persistence
            cache2 = SearchCache(
                backend="file",
                ttl=timedelta(hours=1),
                cache_dir=tmpdir,
            )

            retrieved = cache2.get("zinc deficiency", "naturopathy", max_results=5)
            assert retrieved == results

    def test_file_cache_expiration(self):
        """Should expire file cache entries after TTL."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = SearchCache(
                backend="file",
                ttl=timedelta(milliseconds=50),
                cache_dir=tmpdir,
            )

            results = [{"title": "Test"}]
            cache.set("test", "tcm", results, max_results=3)

            # Wait for expiration
            time.sleep(0.1)

            assert cache.get("test", "tcm", max_results=3) is None

    def test_cache_key_uniqueness(self):
        """Different parameters should produce different cache entries."""
        cache = SearchCache(backend="memory")

        cache.set("query", "allopathy", [{"title": "A"}], max_results=5)
        cache.set("query", "ayurveda", [{"title": "B"}], max_results=5)
        cache.set("query", "allopathy", [{"title": "C"}], max_results=10)

        assert cache.get("query", "allopathy", max_results=5) == [{"title": "A"}]
        assert cache.get("query", "ayurveda", max_results=5) == [{"title": "B"}]
        assert cache.get("query", "allopathy", max_results=10) == [{"title": "C"}]

    def test_cache_stats_tracking(self):
        """Should track hits and misses."""
        cache = SearchCache(backend="memory")

        cache.set("query", "allopathy", [{"title": "Test"}], max_results=5)

        cache.get("query", "allopathy", max_results=5)  # Hit
        cache.get("query", "allopathy", max_results=5)  # Hit
        cache.get("nonexistent", "allopathy", max_results=5)  # Miss

        stats = cache.stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["hit_rate"] == "66.7%"

    def test_cache_clear(self):
        """Should clear all entries and reset stats."""
        cache = SearchCache(backend="memory")

        cache.set("query1", "allopathy", [{"title": "A"}], max_results=5)
        cache.set("query2", "tcm", [{"title": "B"}], max_results=5)

        # Verify data exists before clear
        assert cache.get("query1", "allopathy", max_results=5) is not None
        assert cache.get("query2", "tcm", max_results=5) is not None

        cache.clear()

        # Stats should be reset to 0 immediately after clear
        assert cache.hits == 0
        assert cache.misses == 0

        # Data should be cleared (gets after clear will add misses)
        assert cache.get("query1", "allopathy", max_results=5) is None
        assert cache.get("query2", "tcm", max_results=5) is None

    def test_case_insensitive_keys(self):
        """Query matching should be case-insensitive."""
        cache = SearchCache(backend="memory")

        cache.set("Chromium Insulin", "allopathy", [{"title": "Test"}], max_results=5)

        assert cache.get("chromium insulin", "allopathy", max_results=5) is not None
        assert cache.get("CHROMIUM INSULIN", "allopathy", max_results=5) is not None


class TestCachedSearch:
    """Tests for the cached_search wrapper function."""

    def test_cached_search_caches_results(self):
        """Should cache search function results."""
        call_count = 0

        def mock_search(query, max_results):
            nonlocal call_count
            call_count += 1
            return [{"title": f"Result for {query}"}]

        # Clear any existing cache
        cache = get_cache()
        cache.clear()

        # First call should invoke the search function
        result1 = cached_search(mock_search, "test query", "allopathy", 5)
        assert call_count == 1

        # Second call should use cache
        result2 = cached_search(mock_search, "test query", "allopathy", 5)
        assert call_count == 1  # Should not increment

        assert result1 == result2

    def test_cached_search_does_not_cache_errors(self):
        """Should not cache error results."""
        call_count = 0

        def mock_search_with_error(query, max_results):
            nonlocal call_count
            call_count += 1
            return [{"error": "API Error"}]

        cache = get_cache()
        cache.clear()

        cached_search(mock_search_with_error, "error query", "allopathy", 5)
        cached_search(mock_search_with_error, "error query", "allopathy", 5)

        # Should call twice since errors aren't cached
        assert call_count == 2


class TestGetCache:
    """Tests for the global cache getter."""

    def test_get_cache_returns_singleton(self):
        """Should return the same cache instance."""
        cache1 = get_cache()
        cache2 = get_cache()

        assert cache1 is cache2

    def test_get_cache_uses_env_config(self, monkeypatch):
        """Should use environment variables for configuration."""
        # Reset global cache
        import trace_mineral_agent.cache as cache_module
        cache_module._cache = None

        monkeypatch.setenv("SEARCH_CACHE_BACKEND", "memory")
        monkeypatch.setenv("SEARCH_CACHE_TTL_HOURS", "48")

        cache = get_cache()

        assert cache.backend == "memory"
        assert cache.ttl.total_seconds() == 48 * 3600
