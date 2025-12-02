"""Performance Tuning Module for E-commerce Customer Support Chatbot.

Provides optimization strategies, caching mechanisms, query optimization,
and monitoring utilities to improve chatbot response times and throughput.
"""

import time
import functools
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import OrderedDict
from datetime import datetime, timedelta
import hashlib
import json

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Track and report performance metrics for the chatbot."""
    
    def __init__(self):
        """Initialize performance metrics tracker."""
        self.request_times: List[float] = []
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.database_queries: int = 0
        self.api_calls: int = 0
        self.error_count: int = 0
        
    def record_request_time(self, elapsed: float) -> None:
        """Record request processing time in seconds."""
        self.request_times.append(elapsed)
        
    def get_average_response_time(self) -> float:
        """Get average response time in milliseconds."""
        if not self.request_times:
            return 0.0
        return (sum(self.request_times) / len(self.request_times)) * 1000
    
    def get_p95_response_time(self) -> float:
        """Get 95th percentile response time in milliseconds."""
        if not self.request_times:
            return 0.0
        sorted_times = sorted(self.request_times)
        p95_index = int(len(sorted_times) * 0.95)
        return sorted_times[p95_index] * 1000
    
    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate percentage."""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return (self.cache_hits / total) * 100
    
    def report(self) -> Dict[str, Any]:
        """Generate performance report."""
        return {
            'average_response_time_ms': self.get_average_response_time(),
            'p95_response_time_ms': self.get_p95_response_time(),
            'total_requests': len(self.request_times),
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate_percent': self.get_cache_hit_rate(),
            'database_queries': self.database_queries,
            'api_calls': self.api_calls,
            'error_count': self.error_count
        }


class LRUCache:
    """Least Recently Used (LRU) cache implementation."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items to store
            ttl_seconds: Time-to-live for cached items in seconds
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, datetime] = {}
        self.metrics = PerformanceMetrics()
        
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry has expired."""
        if key not in self.timestamps:
            return True
        age = datetime.now() - self.timestamps[key]
        return age > timedelta(seconds=self.ttl_seconds)
    
    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key from function call parameters."""
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self.cache or self._is_expired(key):
            self.metrics.cache_misses += 1
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
            return None
        
        # Move to end (mark as recently used)
        self.cache.move_to_end(key)
        self.metrics.cache_hits += 1
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache."""
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.max_size:
            # Remove least recently used item
            self.cache.popitem(last=False)
            removed_key = next(iter(self.cache))
            if removed_key in self.timestamps:
                del self.timestamps[removed_key]
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now()
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.timestamps.clear()


def cache_result(ttl_seconds: int = 3600, max_size: int = 1000):
    """Decorator for caching function results.
    
    Args:
        ttl_seconds: Cache time-to-live in seconds
        max_size: Maximum cache size
    """
    cache = LRUCache(max_size=max_size, ttl_seconds=ttl_seconds)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key
            key = cache._make_key(func.__name__, args, kwargs)
            
            # Check cache
            cached_value = cache.get(key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.put(key, result)
            logger.debug(f"Cached result for {func.__name__}")
            return result
        
        wrapper.cache = cache
        return wrapper
    
    return decorator


def timer(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"{func.__name__} took {elapsed:.3f} seconds")
        return result
    
    return wrapper


class QueryOptimizer:
    """Optimize database and API queries for performance."""
    
    @staticmethod
    def batch_order_queries(order_ids: List[str], batch_size: int = 50) -> List[List[str]]:
        """Batch order IDs for efficient database queries.
        
        Args:
            order_ids: List of order IDs to query
            batch_size: Number of IDs per batch
            
        Returns:
            List of batches
        """
        batches = []
        for i in range(0, len(order_ids), batch_size):
            batches.append(order_ids[i:i + batch_size])
        return batches
    
    @staticmethod
    def optimize_intent_classification(text: str, top_k: int = 5) -> str:
        """Optimize intent classification by limiting output size.
        
        Args:
            text: Input text to classify
            top_k: Number of top intents to return
            
        Returns:
            Optimized text for classification
        """
        # Limit text length to 500 characters for faster processing
        if len(text) > 500:
            text = text[:500]
        return text.lower().strip()
    
    @staticmethod
    def create_index_hints(query_type: str) -> Dict[str, Any]:
        """Generate database index hints for query optimization.
        
        Args:
            query_type: Type of query
            
        Returns:
            Index hints dictionary
        """
        hints = {
            'order_lookup': {
                'index': 'orders_customer_id_idx',
                'use_index': True
            },
            'customer_history': {
                'index': 'chat_history_customer_date_idx',
                'use_index': True
            },
            'fulfillment_status': {
                'index': 'fulfillment_order_id_idx',
                'use_index': True
            }
        }
        return hints.get(query_type, {})


class ConnectionPool:
    """Manage database connection pooling."""
    
    def __init__(self, pool_size: int = 10):
        """Initialize connection pool.
        
        Args:
            pool_size: Number of connections to maintain
        """
        self.pool_size = pool_size
        self.available_connections: List[Any] = []
        self.active_connections: int = 0
        self.max_connections: int = pool_size * 2
        
    def get_connection(self, timeout: float = 5.0) -> Optional[Any]:
        """Get a connection from the pool.
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            Database connection or None if unavailable
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.available_connections:
                connection = self.available_connections.pop()
                self.active_connections += 1
                return connection
            time.sleep(0.1)
        return None
    
    def release_connection(self, connection: Any) -> None:
        """Release a connection back to the pool.
        
        Args:
            connection: Database connection to return
        """
        if self.active_connections > 0:
            self.active_connections -= 1
        if len(self.available_connections) < self.pool_size:
            self.available_connections.append(connection)
    
    def get_pool_stats(self) -> Dict[str, int]:
        """Get connection pool statistics.
        
        Returns:
            Dictionary with pool statistics
        """
        return {
            'available': len(self.available_connections),
            'active': self.active_connections,
            'pool_size': self.pool_size,
            'total': len(self.available_connections) + self.active_connections
        }


class ResourceMonitor:
    """Monitor system resources and performance."""
    
    def __init__(self):
        """Initialize resource monitor."""
        self.memory_usage: List[float] = []
        self.cpu_usage: List[float] = []
        self.response_times: List[float] = []
        
    def check_memory_usage(self, threshold_mb: int = 500) -> bool:
        """Check if memory usage exceeds threshold.
        
        Args:
            threshold_mb: Memory threshold in MB
            
        Returns:
            True if threshold exceeded, False otherwise
        """
        # Placeholder for actual memory monitoring
        return False
    
    def alert_if_slow(self, response_time: float, threshold: float = 1.0) -> bool:
        """Alert if response time exceeds threshold.
        
        Args:
            response_time: Response time in seconds
            threshold: Time threshold in seconds
            
        Returns:
            True if alert triggered, False otherwise
        """
        if response_time > threshold:
            logger.warning(f"Slow response detected: {response_time:.3f}s")
            return True
        return False


# Global cache instance
global_cache = LRUCache(max_size=5000, ttl_seconds=3600)
performance_metrics = PerformanceMetrics()
query_optimizer = QueryOptimizer()
connection_pool = ConnectionPool(pool_size=20)
resource_monitor = ResourceMonitor()
