# Deployment Guide

This document provides comprehensive deployment instructions for the E-Commerce Customer Support Chatbot.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Virtual environment (recommended)

## Quick Start (Development)

### 1. Clone the Repository

```bash
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Chatbot

```bash
python main.py
```

## Production Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t ecommerce-chatbot:latest .

# Run container
docker run -p 5000:5000 -v ./logs:/app/logs ecommerce-chatbot:latest
```

### Server Deployment (Linux/Ubuntu)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Clone and setup
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service (optional)
sudo cp chatbot.service /etc/systemd/system/
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

## Testing

### Run Unit Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=chatbot
```

### Run Code Quality Checks

```bash
pip install pylint flake8
pylint chatbot/
flake8 chatbot/ --count --show-source
```

## Configuration Management

Edit `config.json` to customize:

- Intent classifier sensitivity
- IR-based QA thresholds
- Logging levels
- Performance parameters
- Database paths

### Example Configuration

```json
{
  "app_config": {
    "log_level": "INFO"
  },
  "intent_classifier": {
    "confidence_threshold": 0.6
  },
  "logging": {
    "file_path": "logs/chatbot.log"
  }
}
```

## Monitoring and Logging

### Log Files

Logs are stored in `logs/chatbot.log` with:
- Automatic rotation at 10MB
- 5 backup files retained
- Timestamps and log levels

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-02T12:00:00.000000",
  "version": "1.0.0"
}
```

## API Usage in Production

### Process Message

```bash
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Track my order"
  }'
```

### Track Order

```bash
curl -X POST http://localhost:5000/track_order \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "order_id": "ORD001"
  }'
```

## Performance Optimization

### Caching
- Enable response caching for FAQ queries
- TTL: 300 seconds (configurable)
- Max cache size: 1000 entries

### Database
- Use connection pooling
- Index frequently accessed fields
- Implement query optimization

### Load Testing

```bash
pip install locust
locust -f loadtests.py --host=http://localhost:5000
```

## Security Best Practices

1. **Environment Variables**
   - Use `.env` for sensitive data
   - Never commit credentials

2. **Input Validation**
   - Sanitize user inputs
   - Validate message length
   - Check for injection attacks

3. **Rate Limiting**
   - Implement per-user rate limits
   - Use API keys for authentication
   - Monitor suspicious patterns

4. **HTTPS/TLS**
   - Use SSL certificates in production
   - Redirect HTTP to HTTPS
   - Implement CORS policies

## Scaling

### Horizontal Scaling

```bash
# Load balancer configuration (nginx)
upstream chatbot_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

### Vertical Scaling

- Increase memory allocation
- Use faster CPU
- Optimize database queries
- Implement caching layers (Redis)

## Troubleshooting

### Common Issues

**Issue**: Module not found
```bash
# Solution
pip install -r requirements.txt --force-reinstall
```

**Issue**: Port already in use
```bash
# Solution
kill $(lsof -t -i:5000)
```

**Issue**: Low performance
```bash
# Solutions
- Check logs for errors
- Monitor system resources
- Increase cache TTL
- Optimize database queries
```

## Maintenance

### Regular Tasks

- Review and rotate logs weekly
- Update dependencies monthly
- Run security scans quarterly
- Performance profiling monthly

### Backup and Recovery

```bash
# Backup configuration and data
tar -czf chatbot_backup.tar.gz config.json data/ logs/

# Restore from backup
tar -xzf chatbot_backup.tar.gz
```

## Support and Resources

- GitHub Issues: [Report bugs and request features](https://github.com/harithanandakumar/ecommerce-customer-support-chatbot/issues)
- Documentation: See README.md and EXAMPLES.md
- Tests: Run `pytest tests/` for comprehensive testing

## Version History

- **v1.0.0** (2025-12-02) - Initial release with core features
