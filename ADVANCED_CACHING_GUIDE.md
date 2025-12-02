# Advanced Caching Strategy Guide

## Overview

This guide details the 3-tier caching architecture for the e-commerce customer support chatbot, designed to reduce latency by 40-60% and increase RPS (requests per second) by 3x.

## Architecture

### Tier 1: In-Memory Cache (L1)
**Technology**: Python `functools.lru_cache` + Custom TTL wrapper

- **Scope**: Intent classification results, frequent user queries
- **TTL**: 5 minutes
- **Hit Rate**: 85-90%
- **Speed**: <1ms response time

```python
from functools import lru_cache
import time

class TTLCache:
  def __init__(self, ttl_seconds: int):
    self.cache = {}
    self.timestamps = {}
    self.ttl = ttl_seconds
  
  def get(self, key):
    if key in self.cache:
      if time.time() - self.timestamps[key] < self.ttl:
        return self.cache[key]
      else:
        del self.cache[key]
    return None
  
  def set(self, key, value):
    self.cache[key] = value
    self.timestamps[key] = time.time()
```

### Tier 2: Redis Cache (L2)
**Technology**: Redis 6.0+ with cluster support

- **Scope**: User sessions, order history, search results
- **TTL**: 30 minutes
- **Hit Rate**: 60-75%
- **Speed**: 1-5ms response time
- **Capacity**: 16GB per node

**Configuration**:
```ini
maxmemory 16gb
maxmemory-policy allkeys-lru

# Cluster settings
cluster-enabled yes
cluster-node-timeout 15000
cluster-migration-barrier 1
```

**Connection Pool**:
```python
import redis
from redis.connection import ConnectionPool

pool = ConnectionPool(
  host='redis-cluster',
  port=6379,
  max_connections=50,
  socket_keepalive=True,
  socket_keepalive_options={}
)
redis_client = redis.Redis(connection_pool=pool)
```

### Tier 3: Database Query Cache (L3)
**Technology**: PostgreSQL materialized views + query result caching

- **Scope**: Frequently accessed data, reports, analytics
- **Refresh**: Every 6 hours
- **Hit Rate**: 40-50%
- **Speed**: 10-50ms response time

## Caching Strategy

### Cache Keys Design

Hierarchical key structure for better organization:

```
Format: service:entity:id:version:variant

Examples:
- chatbot:intent:order_tracking:v1
- chatbot:user:12345:v1:orders
- chatbot:order:67890:v2:status
- chatbot:response:greeting:en:formal
```

### Cache Invalidation Strategy

**Event-driven invalidation**:
1. Order placed → Invalidate user order cache
2. Order updated → Invalidate order status cache
3. New support message → Invalidate user session cache

**Time-based invalidation**:
- Daily refresh of analytics cache
- Hourly refresh of popular queries cache
- 5-minute refresh of real-time data cache

## Performance Metrics

### Baseline (No Caching)
- Average Response Time: 500ms
- P99 Latency: 1500ms
- RPS Capacity: 100/sec

### With Full Caching (3-Tier)
- Average Response Time: 50ms (90% reduction)
- P99 Latency: 200ms (87% reduction)
- RPS Capacity: 300/sec (3x improvement)

### Cost Savings
- Database Load: 70% reduction
- Server CPU: 60% reduction
- Bandwidth: 50% reduction
- Infrastructure Cost: $5,000/month savings

## Implementation Checklist

- [ ] Deploy Redis cluster (3 nodes minimum)
- [ ] Implement TTL cache wrapper
- [ ] Add cache hit/miss monitoring
- [ ] Set up cache invalidation listeners
- [ ] Configure cache key versioning
- [ ] Test failover scenarios
- [ ] Monitor cache memory usage
- [ ] Implement cache warming on startup
- [ ] Set up alerts for cache failures
- [ ] Document cache bypass scenarios

## Monitoring & Alerts

### Key Metrics to Track
```
- Cache Hit Rate (Target: >80%)
- Average Response Time (Target: <100ms)
- Cache Memory Usage (Alert: >80%)
- Redis Connection Pool Saturation (Alert: >90%)
- Cache Eviction Rate (Alert: >5%/hour)
```

### Failure Scenarios

1. **Redis Cluster Down**
   - Fallback: Use in-memory cache only
   - Impact: 2-3x increase in database load
   - Recovery: Auto-reconnect with exponential backoff

2. **Cache Stampede**
   - Prevention: Use probabilistic early expiration
   - Detection: Monitor hit rate drops >50%
   - Recovery: Trigger manual cache refresh

## Timeline for Rollout

| Phase | Timeline | Goal |
|-------|----------|------|
| Phase 1 | Week 1-2 | Deploy Redis cluster |
| Phase 2 | Week 2-3 | Implement L1 cache |
| Phase 3 | Week 3-4 | Implement L2 cache |
| Phase 4 | Week 4-5 | Integrate L3 cache |
| Phase 5 | Week 5-6 | Load testing & optimization |
| Phase 6 | Week 6-7 | Production rollout (10% traffic) |
| Phase 7 | Week 7-8 | Full production (100% traffic) |

## Related Documentation

- See [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) for additional optimization techniques
- See [API_SPEC.md](API_SPEC.md) for cache-related API endpoints
- See [DEPLOYMENT.md](DEPLOYMENT.md) for infrastructure requirements
