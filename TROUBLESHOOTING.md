# Troubleshooting Guide

## Overview

This guide provides solutions for common issues encountered when running and operating the e-commerce customer support chatbot.

## Quick Diagnostics

### Health Check

To quickly diagnose the chatbot's health status:

```bash
curl http://localhost:5000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-01-15T10:30:00Z",
  "uptime_seconds": 43200,
  "database": "connected",
  "cache": "connected"
}
```

### Common Health Issues

| Status | Cause | Solution |
|--------|-------|----------|
| `unhealthy` | Service degradation | Check logs: `tail -f logs/app.log` |
| `db_error` | Database connection failed | Verify DB credentials in `.env` |
| `cache_error` | Redis connection failed | Check Redis cluster: `redis-cli ping` |

## Issue Categories

### 1. Intent Classification Issues

#### Problem: Low intent classification accuracy

**Symptoms**:
- User requests misclassified
- Wrong actions triggered
- Increased user frustration

**Root Causes**:
- Insufficient training data
- Overlapping intent patterns
- Model needs retraining

**Solutions**:

1. **Check intent patterns**:
```python
from chatbot.intent_classifier import IntentClassifier

classifier = IntentClassifier()
print(classifier.get_all_patterns())
```

2. **Retrain the model**:
```bash
python scripts/train_intent_classifier.py \
  --data data/intents.json \
  --epochs 100 \
  --output_model models/intent_classifier.pkl
```

3. **Add new patterns**:
   Edit `data/intents.json` and add missing patterns to intent definitions

#### Problem: False positives in intent matching

**Solution**:
```python
# Lower confidence threshold for strict matching
classifier.set_confidence_threshold(0.85)  # Default is 0.7
```

### 2. Order Tracking Issues

#### Problem: Order status returns "Not Found"

**Symptoms**:
- Users can't find their orders
- System returns 404 errors
- Order data appears incomplete

**Diagnostic Steps**:

1. Check if order exists in database:
```sql
SELECT * FROM orders WHERE order_id = 'ORDER_ID';
```

2. Verify order format matches expected pattern:
```python
from chatbot.utils import validate_order_id

if not validate_order_id(order_id):
    print(f"Invalid order ID format: {order_id}")
```

3. Check database connection:
```python
from chatbot.database import Database

db = Database()
if not db.is_connected():
    print("Database connection failed")
    db.reconnect()
```

**Resolution**:
- Verify order ID format (should be numeric or alphanumeric)
- Check database has latest order records
- Ensure database credentials are correct in `.env`

#### Problem: Slow order status retrieval

**Symptoms**:
- Response takes >5 seconds
- High database load
- Timeout errors

**Solutions**:

1. **Check cache hit rate**:
```bash
redis-cli INFO stats | grep hits
```

2. **Enable caching for order queries**:
```python
from chatbot.cache import CacheManager

cache = CacheManager(ttl=300)  # 5 minute TTL
order_data = cache.get_with_fallback(
    key=f"order:{order_id}",
    fallback_fn=lambda: db.get_order(order_id)
)
```

### 3. Order Cancellation Issues

#### Problem: Cancellation fails or returns error

**Symptoms**:
- Cancellation request rejected
- Error message displayed to user
- Order not cancelled in database

**Causes**:
- Order already shipped
- Cancellation window expired (>24 hours)
- Order in processing state
- Database transaction failure

**Troubleshooting**:

```python
from chatbot.order_manager import OrderManager

manager = OrderManager()

# Check if cancellation is allowed
if not manager.can_cancel_order(order_id):
    reason = manager.get_cancellation_reason(order_id)
    print(f"Cancellation not allowed: {reason}")

# Attempt cancellation with error handling
try:
    manager.cancel_order(order_id)
except CancellationError as e:
    print(f"Cancellation error: {e}")
    # Log for manual review
```

### 4. Database Connection Issues

#### Problem: "Connection refused" or "Timeout"

**Symptoms**:
- All database queries fail
- Service returns 503 errors
- Connection pool exhausted

**Solutions**:

1. **Check database status**:
```bash
psql -h localhost -U chatbot_user -d chatbot_db -c "SELECT 1"
```

2. **Verify connection pool**:
```python
from chatbot.database import Database

db = Database()
print(f"Active connections: {db.get_active_connections()}")
print(f"Pool size: {db.get_pool_size()}")
```

3. **Increase connection pool size**:
```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### 5. Redis Cache Issues

#### Problem: Redis connection failed

**Symptoms**:
- Cache misses increase
- Performance degradation
- "Connection refused" errors

**Solutions**:

1. **Check Redis server status**:
```bash
redis-cli ping
redis-cli INFO server
```

2. **Restart Redis cluster**:
```bash
# For single instance
redis-cli shutdown
redis-server /etc/redis/redis.conf

# For cluster
redis-cli -c cluster info
```

3. **Verify credentials in .env**:
```bash
echo "REDIS_HOST: $REDIS_HOST"
echo "REDIS_PORT: $REDIS_PORT"
echo "REDIS_DB: $REDIS_DB"
```

### 6. Multi-Language Support Issues

#### Problem: Text appears in wrong language

**Symptoms**:
- User sets language but still gets English
- Mixed language responses
- Translation key not found

**Solutions**:

1. **Check language manager**:
```python
from chatbot.i18n import LanguageManager

lang_mgr = LanguageManager('es')  # Spanish
print(f"Current language: {lang_mgr.get_current_language()}")
```

2. **Verify translations loaded**:
```python
translations = lang_mgr.export_translations()
if 'order_tracking' not in translations:
    print("Missing translation key")
```

3. **Test translation**:
```python
text = lang_mgr.get_text('order_tracking')
print(f"Translated: {text}")
```

## Log Files and Analysis

### Log Locations

```
logs/
├── app.log              # Main application log
├── error.log            # Error messages only
├── database.log         # Database queries and operations
├── cache.log            # Cache hit/miss events
└── security.log         # Authentication and security events
```

### Analyzing Logs

```bash
# View real-time logs
tail -f logs/app.log

# Find errors in last hour
grep ERROR logs/app.log | grep -A 2 "$(date -d '1 hour ago' '+%Y-%m-%d')"

# Count errors by type
grep ERROR logs/app.log | cut -d':' -f2 | sort | uniq -c
```

## Performance Debugging

### Slow Requests

```python
import time
from chatbot.metrics import MetricsCollector

metrics = MetricsCollector()

# Log slow requests (>500ms)
for request in metrics.get_slow_requests(threshold_ms=500):
    print(f"{request['endpoint']}: {request['duration_ms']}ms")
```

### Memory Leaks

```bash
# Check memory usage
ps aux | grep python

# Profile memory
python -m memory_profiler scripts/memory_profile.py
```

## Recovery Procedures

### Full Service Restart

```bash
# Stop all services
docker-compose down

# Clean up
rm -rf data/temp/*
redis-cli FLUSHALL

# Restart
docker-compose up -d

# Verify health
curl http://localhost:5000/health
```

### Database Recovery

```bash
# Backup current database
pg_dump chatbot_db > backup_$(date +%s).sql

# Restore from backup if needed
psql chatbot_db < backup_timestamp.sql
```

## Escalation Guide

If none of the above solutions work:

1. Collect diagnostic information:
   - Application logs (last 1 hour)
   - System metrics (CPU, memory, disk)
   - Database connection status
   - Cache cluster status

2. Contact support with:
   - Error message and stack trace
   - Steps to reproduce
   - System configuration
   - Diagnostic output

3. Recommended support: `support@company.com`

## Related Documentation

- [API_SPEC.md](API_SPEC.md) - API endpoint troubleshooting
- [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) - Performance issues
- [DEPLOYMENT.md](DEPLOYMENT.md) - Infrastructure troubleshooting
