# Developer Guide

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis 6.0+
- Git

### Local Setup

```bash
# Clone repository
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
python scripts/migrate_database.py

# Start development server
python app.py
```

## Code Standards

### Python Style Guide

Follows PEP 8 with the following guidelines:

**Type Hints** (Required)
```python
def classify_intent(text: str) -> Dict[str, Any]:
    """Classify user intent from text."""
    pass
```

**Docstrings** (Required for all public functions)
```python
def process_order_tracking(order_id: str) -> Optional[Order]:
    """Process order tracking request.
    
    Args:
        order_id: The order identifier
    
    Returns:
        Order object if found, None otherwise
    
    Raises:
        ValueError: If order_id format is invalid
    """
    pass
```

**Naming Conventions**
- Classes: PascalCase (IntentClassifier)
- Functions/variables: snake_case (classify_intent)
- Constants: UPPER_SNAKE_CASE (MAX_RETRIES)
- Private: _leading_underscore (_internal_cache)

### Code Review Checklist

- [ ] Type hints on all parameters and returns
- [ ] Docstrings on all public functions
- [ ] No hardcoded values (use env vars)
- [ ] Error handling with appropriate exceptions
- [ ] Unit tests written for new code
- [ ] Code coverage >80%
- [ ] No console print statements (use logger)
- [ ] Performance impact assessed
- [ ] Security review completed

## Testing Requirements

### Unit Tests
```bash
pytest tests/unit/ -v --cov=chatbot
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Performance Tests
```bash
pytest tests/performance/ -v
```

**Minimum Coverage**: 85% of new code

## Git Workflow

### Branch Naming
- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Hotfix: `hotfix/description`
- Documentation: `docs/description`

### Commit Messages
```
[TYPE] Brief description (50 chars max)

Detailed explanation if needed (72 chars per line)

Fixes #issue_number (if applicable)
```

**Types**: feat, fix, docs, style, refactor, test, chore

### Pull Request Process

1. Create feature branch from `main`
2. Make focused commits
3. Push to origin
4. Create PR with:
   - Clear title
   - Detailed description
   - Link to related issues
   - Screenshots for UI changes
5. Address review comments
6. Merge when approved

## Architecture Overview

### Module Structure
```
chatbot/
├── __init__.py
├── intent_classifier.py     # Intent detection
├── ir_based_qa.py          # Information retrieval QA
├── response_generator.py    # Response generation
├── order_tracker.py         # Order tracking logic
├── order_canceller.py       # Order cancellation logic
├── dialogue_system.py       # Dialogue management
├── i18n.py                  # Internationalization
├── monitoring.py            # Health and monitoring
└── metrics.py              # Performance metrics
```

### Core Concepts

**Intent Classification**: Rule-based pattern matching
- Input: User text
- Output: Intent label + confidence
- Rules: Defined in `data/intents.json`

**Information Retrieval QA**: TF-IDF based search
- Input: User query
- Output: Most relevant response
- Corpus: FAQs in knowledge base

**Response Generation**: Template-based with personalization
- Input: Intent + context
- Output: Natural language response
- Enhancement: Internationalization support

## Performance Considerations

**Latency Targets**
- Intent classification: <50ms
- IR-based QA: <100ms
- Response generation: <50ms
- Total: <200ms

**Optimization Tips**
- Use caching for frequent queries (TTL: 5 min)
- Batch database operations when possible
- Profile before optimizing
- Use Redis for session state

## Security Best Practices

**Input Validation**
```python
if not validate_order_id(order_id):
    raise ValueError(f"Invalid order ID: {order_id}")
```

**Database Security**
- Use parameterized queries
- No hardcoded credentials
- Use connection pooling
- Enable SSL/TLS

**API Security**
- Validate JWT tokens
- Rate limiting
- HTTPS only
- CORS configuration

## Logging Standards

```python
import logging

logger = logging.getLogger(__name__)

# Usage
logger.info("User initiated order tracking")
logger.warning("Cache miss for order %s", order_id)
logger.error("Failed to retrieve order", exc_info=True)
```

**Log Levels**
- DEBUG: Development information
- INFO: Important events
- WARNING: Unusual situations
- ERROR: Error conditions
- CRITICAL: System failures

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure code passes linting
5. Submit pull request

## Support

- Documentation: See README.md
- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@company.com

## Related Documentation

- [INFRASTRUCTURE_GUIDE.md](INFRASTRUCTURE_GUIDE.md) - Deployment info
- [TEST_AUTOMATION.md](TEST_AUTOMATION.md) - Testing strategy
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
