# Test Automation Guide

## Overview

Comprehensive testing and CI/CD strategy for the rule-based NLP e-commerce customer support chatbot.

## Testing Strategy

### Unit Tests

**Intent Classifier Tests**
```bash
pytest tests/test_intent_classifier.py -v
```

**Order Operations Tests**
```bash
pytest tests/test_order_operations.py -v
```

**Internationalization Tests**
```bash
pytest tests/test_i18n.py -v
```

### Integration Tests

**End-to-End Conversation Flow**
- Simulate user requests through full chatbot pipeline
- Validate intent → action → response flow
- Test order tracking workflow
- Test order cancellation workflow
- Multi-language response validation

**Database Integration**
- Order retrieval accuracy
- Transaction rollback scenarios
- Connection pooling behavior

**Cache Integration**
- Cache hit/miss validation
- TTL expiration
- Cache invalidation events

### Performance Tests

**Load Testing** (using Apache JMeter or Locust)
```bash
locust -f tests/load_test.py --host=http://localhost:5000
```

**Latency Benchmarks**
- Target: <200ms average response time
- P99: <500ms
- P95: <300ms

**Memory Profiling**
```bash
python -m memory_profiler scripts/memory_profile.py
```

### Security Tests

**Input Validation**
- SQL injection attempts
- XSS payload testing
- Malformed request handling

**Authentication Tests**
- JWT token validation
- Expired token handling
- Invalid credentials

**Data Privacy**
- PII data masking in logs
- GDPR compliance checks
- Secure data deletion

## Test Coverage Goals

- **Overall Coverage**: 85%+ code coverage
- **Critical Paths**: 100% coverage (intent classification, order operations)
- **Error Handling**: 95%+ coverage
- **Edge Cases**: 90%+ coverage

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint
      run: flake8 chatbot/ --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Run unit tests
      run: pytest tests/ -v --cov=chatbot
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
    
    - name: Integration tests
      run: pytest tests/integration/ -v
    
    - name: Performance tests
      run: pytest tests/performance/ -v

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r chatbot/ -f json -o bandit-report.json
    
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: bandit-report
        path: bandit-report.json

  docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: docker build -t chatbot:latest .
    - name: Run container tests
      run: docker run --rm chatbot:latest pytest tests/
```

## Manual Testing Checklist

### Functional Testing
- [ ] Intent classification: order tracking
- [ ] Intent classification: order cancellation
- [ ] Intent classification: general inquiry
- [ ] Order tracking with valid order ID
- [ ] Order tracking with invalid order ID
- [ ] Order cancellation: successful
- [ ] Order cancellation: outside window
- [ ] Multi-language responses
- [ ] Cache hits for repeated queries

### Non-Functional Testing
- [ ] Response time under load
- [ ] Memory usage over 1 hour
- [ ] Database connection pool
- [ ] Cache memory management
- [ ] Error logging accuracy
- [ ] Metric collection completeness

## Test Data Management

### Sample Orders
```sql
INSERT INTO orders VALUES
('ORD-001', 'pending', CURRENT_TIMESTAMP),
('ORD-002', 'shipped', CURRENT_TIMESTAMP - INTERVAL 2 DAYS),
('ORD-003', 'delivered', CURRENT_TIMESTAMP - INTERVAL 10 DAYS);
```

### Reset Database
```bash
python scripts/reset_testdb.py
```

## Continuous Monitoring

### Metrics to Track
- Test pass rate (target: 100%)
- Code coverage trend
- Performance metric trends
- Critical bug escapes

### Alert Thresholds
- Coverage drops below 80%
- Performance degrades >10%
- 3+ consecutive test failures
- Security scan findings

## Related Documentation

- [INFRASTRUCTURE_GUIDE.md](INFRASTRUCTURE_GUIDE.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [REPORTING_GUIDE.md](REPORTING_GUIDE.md)
