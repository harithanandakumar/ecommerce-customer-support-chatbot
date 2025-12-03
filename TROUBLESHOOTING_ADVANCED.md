# Advanced Troubleshooting Guide

Comprehensive troubleshooting guide for advanced issues in the e-commerce customer support chatbot.

## Table of Contents
1. [Performance Issues](#performance-issues)
2. [Intent Classification Problems](#intent-classification-problems)
3. [Database & Query Issues](#database--query-issues)
4. [API Integration Issues](#api-integration-issues)
5. [Memory & Resource Issues](#memory--resource-issues)
6. [Concurrency & Threading Issues](#concurrency--threading-issues)
7. [Logging & Debugging](#logging--debugging)
8. [Deployment Issues](#deployment-issues)
9. [Common Error Messages](#common-error-messages)
10. [Performance Tuning](#performance-tuning)

## Performance Issues

### Slow Response Times

**Symptoms:**
- Customer queries taking >2 seconds to process
- Chatbot timeout errors in logs
- User complaints about sluggish responses

**Investigation Steps:**
1. Check performance metrics:
```python
from chatbot.performance_tuning import performance_metrics
report = performance_metrics.report()
print(f"Avg response: {report['average_response_time_ms']:.2f}ms")
print(f"P95 response: {report['p95_response_time_ms']:.2f}ms")
```

2. Enable profiling:
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Run chatbot code
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative').print_stats(10)
```

3. Check query logs for slow queries:
```sql
SELECT query_text, execution_time_ms 
FROM query_logs 
WHERE execution_time_ms > 500 
ORDER BY execution_time_ms DESC 
LIMIT 10;
```

**Solutions:**
- Enable caching for frequently accessed data
- Add database indexes on frequently queried columns
- Optimize intent classification with text truncation (500 chars max)
- Use connection pooling instead of creating new connections
- Batch API calls to reduce round-trip overhead

### High Memory Usage

**Symptoms:**
- Memory utilization >80% of allocated heap
- Out of Memory (OOM) killer events
- Process crashes after running for hours

**Investigation:**
```python
import tracemalloc
import gc

tracemalloc.start()
# Run code section
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.1f} MB; Peak: {peak / 1024 / 1024:.1f} MB")

# Find memory leaks
gc.collect()
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

**Solutions:**
- Reduce LRU cache size: `global_cache = LRUCache(max_size=1000)` (was 5000)
- Limit chat history retention to 90 days
- Clear old sessions periodically
- Monitor and profile heap usage regularly
- Use generators instead of lists for large datasets

## Intent Classification Problems

### Low Intent Classification Accuracy

**Symptoms:**
- Intent accuracy <85% on test set
- Frequent misclassifications of order tracking queries
- False positives on cancellation intent

**Debug Classification:**
```python
from chatbot.intent_classifier import IntentClassifier

classifier = IntentClassifier()
test_queries = [
    "I want to track my order",
    "Can I cancel my order?",
    "Where is my package?"
]

for query in test_queries:
    intent = classifier.classify(query)
    confidence = classifier.get_confidence(query)
    print(f"Query: {query}")
    print(f"Intent: {intent}, Confidence: {confidence:.2%}")
```

**Solutions:**
- Add more training examples for edge cases
- Improve text preprocessing (better tokenization)
- Increase confidence thresholds to 0.75+
- Use ensemble methods combining multiple classifiers
- Implement active learning to identify misclassified examples
- Update training data quarterly

## Database & Query Issues

### Slow Database Queries

**Symptoms:**
- Query execution times >500ms
- N+1 query problems
- Lock timeouts on concurrent updates

**Analyze Query Performance:**
```sql
-- Identify slow queries
EXPLAIN ANALYZE 
SELECT * FROM orders 
WHERE customer_id = ? 
AND created_at > NOW() - INTERVAL 30 DAY;

-- Check index usage
SELECT * FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

**Solutions:**
- Add composite indexes on frequently filtered columns
- Use EXPLAIN ANALYZE to identify sequential scans
- Implement query result caching with TTL
- Denormalize data for read-heavy operations
- Use connection pooling with proper timeout settings

### Database Connection Pool Issues

**Symptoms:**
- "Connection pool exhausted" errors
- "Timeout waiting for connection" messages
- Hanging requests

**Debug Pool Status:**
```python
from chatbot.performance_tuning import connection_pool

stats = connection_pool.get_pool_stats()
print(f"Available: {stats['available']}")
print(f"Active: {stats['active']}")
print(f"Pool size: {stats['pool_size']}")
```

**Solutions:**
- Increase pool size: `ConnectionPool(pool_size=30)` (from 20)
- Lower connection acquisition timeout
- Implement connection validation and reconnection logic
- Monitor connection pool metrics continuously
- Use read replicas for scaling read operations

## API Integration Issues

### External API Failures

**Symptoms:**
- "API timeout" errors
- Intermittent order lookup failures
- 503 Service Unavailable responses

**Implement Retry Logic:**
```python
import time
from typing import Optional, Any

def call_api_with_retry(
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Optional[Any]:
    """Call API with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"API call failed after {max_retries} attempts: {e}")
                raise
            wait_time = backoff_factor ** attempt
            logger.warning(f"API call failed, retrying in {wait_time}s: {e}")
            time.sleep(wait_time)
    return None
```

**Solutions:**
- Implement circuit breaker pattern for failing APIs
- Use exponential backoff for retries
- Cache API responses with reasonable TTL
- Monitor API response times and latency
- Implement fallback responses for critical operations

## Memory & Resource Issues

### Cache Misses

**Symptoms:**
- Cache hit rate <50%
- Repeated identical queries to database
- High CPU usage from repeated computations

**Analyze Cache Performance:**
```python
from chatbot.performance_tuning import global_cache

metrics = global_cache.metrics
print(f"Cache hits: {metrics.cache_hits}")
print(f"Cache misses: {metrics.cache_misses}")
print(f"Hit rate: {metrics.get_cache_hit_rate():.2%}")
```

**Solutions:**
- Increase cache size if memory available
- Increase TTL for stable data (from 1h to 4h)
- Pre-populate cache with common queries at startup
- Implement cache warming strategy
- Use bloom filters to avoid checking missing keys

## Concurrency & Threading Issues

### Race Conditions

**Symptoms:**
- Inconsistent order states
- Duplicate order cancellations
- Lost updates in concurrent scenarios

**Add Locking:**
```python
import threading
from typing import Dict

order_locks: Dict[str, threading.Lock] = {}

def update_order_safe(order_id: str, status: str) -> bool:
    """Update order with lock to prevent race conditions."""
    if order_id not in order_locks:
        order_locks[order_id] = threading.Lock()
    
    with order_locks[order_id]:
        current_status = get_order_status(order_id)
        if is_valid_transition(current_status, status):
            set_order_status(order_id, status)
            return True
        return False
```

**Solutions:**
- Use database-level locking (SELECT FOR UPDATE)
- Implement optimistic locking with version numbers
- Use distributed locks for microservices
- Add database constraints to prevent invalid states

## Logging & Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.debug(f"Processing query: {query}")
logger.debug(f"Intent: {intent}, Confidence: {confidence}")
```

### Use Structured Logging

```python
import json
from datetime import datetime

def log_event(event_type: str, **kwargs):
    """Log structured event for analysis."""
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        **kwargs
    }
    logger.info(json.dumps(event))

log_event('order_lookup', order_id='12345', status='found', response_time_ms=245)
```

## Deployment Issues

### Container Memory Issues

**Set Resource Limits:**
```yaml
# Docker Compose
services:
  chatbot:
    image: chatbot:latest
    resources:
      limits:
        memory: 512M
      reservations:
        memory: 256M
```

**Monitor During Deployment:**
```bash
# Watch memory usage
docker stats chatbot --no-stream

# Check process memory
ps aux | grep python
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| ConnectionRefusedError | Database not running | Start database service |
| TimeoutError | API call took >30s | Increase timeout, check API health |
| MemoryError | Heap exhausted | Reduce cache size, enable garbage collection |
| KeyError in classify | Invalid intent key | Update intent training data |
| JSONDecodeError | Invalid API response | Add response validation, check API schema |
| DatabaseLocked | Concurrent write conflicts | Use transaction isolation levels |

## Performance Tuning

### Recommended Settings for Production

```python
# Performance tuning configuration
CACHE_SIZE = 2000  # LRU cache entries
CACHE_TTL = 3600   # Time-to-live in seconds
DB_POOL_SIZE = 25  # Connection pool size
DB_POOL_TIMEOUT = 10  # Connection acquisition timeout
API_TIMEOUT = 5    # API call timeout
API_RETRIES = 3    # API retry attempts
BATCH_SIZE = 50    # Query batch size
MEMORY_THRESHOLD = 80  # Alert at 80% memory usage
```

### Monitoring Checklist

- [ ] Response time SLA < 1000ms (p95)
- [ ] Cache hit rate > 70%
- [ ] Memory usage < 70% of allocated
- [ ] Database query time < 200ms (p95)
- [ ] API call success rate > 99.5%
- [ ] Error rate < 1%
- [ ] Connection pool exhaustion never
- [ ] Intent classification accuracy > 95%

---

For additional help, check logs at `chatbot_debug.log` or contact the development team.
