# Getting Started with E-commerce Customer Support Chatbot

Quick start guide to set up and deploy the e-commerce customer support chatbot in your environment.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running Locally](#running-locally)
5. [Docker Deployment](#docker-deployment)
6. [Testing](#testing)
7. [First Query](#first-query)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## System Requirements

### Minimum Requirements
- **Python:** 3.9 or higher
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 2 GB for installation and dependencies
- **OS:** Linux, macOS, or Windows
- **Internet:** For downloading dependencies and API integration

### Optional Requirements
- **Docker:** For containerized deployment
- **PostgreSQL:** 12+ for production database
- **Redis:** For caching and session management
- **Git:** For version control

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Development Dependencies (Optional)
```bash
pip install -r requirements-dev.txt  # For testing and development
```

### 5. Verify Installation
```bash
python -c "import chatbot; print('Installation successful!')"
```

---

## Configuration

### 1. Environment Variables
Create `.env` file in project root:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db

# API Keys
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
WOOCOMMERCE_KEY=your_woocommerce_key

# Server
SERVER_PORT=5000
SERVER_HOST=0.0.0.0
DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=chatbot.log
```

### 2. Database Setup
```bash
# Create database
psql -U postgres -c "CREATE DATABASE chatbot_db;"

# Run migrations
python scripts/migrate_db.py
```

### 3. Load Sample Data
```bash
python scripts/load_sample_data.py
```

---

## Running Locally

### 1. Start Development Server
```bash
python -m chatbot.app
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### 2. Test API Endpoint
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_123", "message": "Where is my order?"}'
```

### 3. Access Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-03T11:00:00Z",
  "version": "2.1.0"
}
```

---

## Docker Deployment

### 1. Build Docker Image
```bash
docker build -t chatbot:latest .
```

### 2. Run Container
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:password@postgres:5432/chatbot \
  -e LOG_LEVEL=INFO \
  chatbot:latest
```

### 3. Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f chatbot

# Stop services
docker-compose down
```

### 4. Docker Compose Services
- **chatbot:** Main application (port 5000)
- **postgres:** Database (port 5432)
- **redis:** Cache (port 6379)

---

## Testing

### 1. Run Unit Tests
```bash
pytest tests/unit/ -v
```

### 2. Run Integration Tests
```bash
pytest tests/integration/ -v
```

### 3. Run All Tests
```bash
pytest tests/ --cov=chatbot
```

### 4. Test Coverage Report
```bash
pytest tests/ --cov=chatbot --cov-report=html
open htmlcov/index.html
```

---

## First Query

### Example 1: Track Order
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "message": "Can you track my order?"
  }'
```

Expected response:
```json
{
  "intent": "track_order",
  "confidence": 0.95,
  "response": "I'll help you track your order. What's your order ID?",
  "session_id": "sess_abc123"
}
```

### Example 2: Cancel Order
```bash
curl -X POST http://localhost:5000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "message": "I want to cancel order ORD-2025-001"
  }'
```

Expected response:
```json
{
  "intent": "cancel_order",
  "confidence": 0.92,
  "response": "I can help with that. Your order ORD-2025-001 has been cancelled.",
  "session_id": "sess_abc124"
}
```

---

## Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or run on different port
PORT=5001 python -m chatbot.app
```

### Issue: Database Connection Failed
```bash
# Check PostgreSQL is running
psql -U postgres -d chatbot_db -c "SELECT version();"

# Verify DATABASE_URL in .env
echo $DATABASE_URL
```

### Issue: Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Verify Python version
python --version  # Should be 3.9+
```

### Issue: SSL Certificate Error
```bash
# For development (not recommended for production)
export PYTHONHTTPSVERIFY=0

# Or update certificates
pip install --upgrade certifi
```

---

## Next Steps

### 1. Read Documentation
- [Architecture](ARCHITECTURE.md) - System design and components
- [API Specification](API_SPEC.md) - API endpoints and examples
- [Security Guide](SECURITY.md) - Security best practices
- [Developer Guide](DEVELOPER_GUIDE.md) - Advanced development topics

### 2. Configure Integrations
- [API Integration Guide](API_INTEGRATION_GUIDE.md) - Connect to e-commerce platforms
  - Shopify, WooCommerce, Magento, BigCommerce
  - Payment gateways, shipping providers

### 3. Deploy to Production
- [Infrastructure Guide](INFRASTRUCTURE_GUIDE.md) - Production deployment
- [Deployment](DEPLOYMENT.md) - Deployment strategies and checklist
- [Monitoring Guide](MONITORING_GUIDE.md) - Setup monitoring and alerts

### 4. Monitor and Maintain
- [Troubleshooting Guide](TROUBLESHOOTING_ADVANCED.md) - Production issues
- [Performance Tuning](chatbot/performance_tuning.py) - Optimization strategies
- [Community Guidelines](COMMUNITY_GUIDELINES.md) - Contribute improvements

### 5. Scale Your Deployment
```bash
# Using Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml chatbot

# Using Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## Quick Reference

### Key Files
- `chatbot/app.py` - Main application
- `chatbot/intent_classifier.py` - Intent classification
- `chatbot/order_tracker.py` - Order tracking module
- `chatbot/cancellation.py` - Order cancellation module
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker services

### Important Directories
- `/chatbot` - Main source code
- `/data` - Sample data and configurations
- `/tests` - Test suites
- `/scripts` - Utility scripts
- `/github/workflows` - CI/CD pipelines

### Common Commands
```bash
# Development
python -m chatbot.app

# Testing
pytest tests/

# Linting
flake8 chatbot/
black chatbot/

# Type checking
mypy chatbot/

# Production
gunicorn chatbot.app:app --workers 4 --bind 0.0.0.0:5000
```

---

## Getting Help

- **Documentation:** Check [README](README.md) for overview
- **Issues:** [GitHub Issues](https://github.com/harithanandakumar/ecommerce-customer-support-chatbot/issues)
- **Discussions:** [GitHub Discussions](https://github.com/harithanandakumar/ecommerce-customer-support-chatbot/discussions)
- **Email:** support@company.com

---

## What's Next?

Congratulations! You've successfully set up the chatbot. Now:

1. ✅ Explore the [API endpoints](API_SPEC.md)
2. ✅ Connect to your e-commerce platform via [integrations](API_INTEGRATION_GUIDE.md)
3. ✅ Read about [security](SECURITY.md) for production deployment
4. ✅ Monitor performance with [performance tuning](chatbot/performance_tuning.py)
5. ✅ Deploy to production following [deployment guide](DEPLOYMENT.md)

Happy chatbotting! 🚀
