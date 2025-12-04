# Complete Guide to Run E-Commerce Chatbot Successfully

## Quick Start (5 Minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot
```

### Step 2: Create Python Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Chatbot CLI
```bash
python main.py
```

### Step 5: Interact with the Chatbot
Example commands to try:
```
You: Hello
Bo: Hello! How can I help you today?

You: Track my order ORD001
Bot: Your order ORD001 is pending. Expected delivery: 2025-12-10

You: What is your return policy?
Bot: We offer 30-day returns for most items...

You: quit
Bot: Thank you for using our support chatbot. Goodbye!
```

---

## Detailed Setup Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- 500MB disk space
- 2GB RAM minimum

### Installation Methods

#### Method 1: CLI Interface (Recommended for Testing)
```bash
# Navigate to project directory
cd ecommerce-customer-support-chatbot

# Install dependencies
pip install -r requirements.txt

# Run interactive chatbot
python main.py
```

#### Method 2: REST API Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python -m chatbot.api_wrapper

# Server starts at http://localhost:5000
```

#### Method 3: Docker Container
```bash
# Build Docker image
docker build -t ecommerce-chatbot .

# Run container
docker run -p 5000:5000 ecommerce-chatbot

# Access at http://localhost:5000
```

---

## Directory Structure

```
ecommerce-customer-support-chatbot/
├── chatbot/                       # Main chatbot modules
│   ├── __init__.py
│   ├── dialogue_system.py         # Main orchestration
│   ├── intent_classifier.py       # Intent detection
│   ├── ir_based_qa.py            # FAQ retrieval
│   ├── response_generator.py      # Response generation
│   ├── order_tracker.py          # Order management
│   ├── api_wrapper.py            # REST API
│   ├── health_check.py           # System monitoring
│   ├── monitoring.py             # Performance metrics
│   └── logger.py                 # Logging system
├── data/                          # Configuration data
│   ├── intents.json              # Intent definitions
│   ├── faq.json                  # FAQ database
│   └── sample_orders.json        # Sample orders
├── tests/                         # Test suite
│   ├── test_intent_classifier.py
│   ├── test_performance.py
│   └── test_integration.py
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── config.json                   # Configuration file
├── README.md                     # Project overview
└── RUN_CHATBOT_GUIDE.md         # This file
```

---

## Dependencies

```
nltk==3.8.1                  # Natural Language Toolkit
numpy==1.24.0                # Numerical computing
scikit-learn==1.2.0          # Machine learning
flask==2.3.0                 # Web framework (API)
python-dotenv==0.21.0        # Environment variables
```

---

## Configuration

### 1. Environment Variables (.env)
Create `.env` file in root directory:
```
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=INFO
PORT=5000
```

### 2. Configuration File (config.json)
Edit `config.json` for custom settings:
```json
{
  "intents_file": "data/intents.json",
  "faq_file": "data/faq.json",
  "orders_file": "data/sample_orders.json",
  "log_level": "INFO",
  "max_history": 100
}
```

---

## Running Tests

### Unit Tests
```bash
python -m pytest tests/test_intent_classifier.py -v
```

### Integration Tests
```bash
python -m pytest tests/test_integration.py -v
```

### Performance Tests
```bash
python -m pytest tests/test_performance.py -v
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

---

## API Usage Examples

### 1. Chat Endpoint
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Track order ORD001"}'
```

### 2. Health Check
```bash
curl http://localhost:5000/api/health
```

### 3. Get Conversation History
```bash
curl http://localhost:5000/api/session/history
```

### 4. Track Order
```bash
curl -X POST http://localhost:5000/api/track_order \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORD001"}'
```

### 5. Cancel Order
```bash
curl -X POST http://localhost:5000/api/cancel_order \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORD002"}'
```

---

## Using Python Script

### Basic Usage
```python
from chatbot.dialogue_system import DialogueSystem

# Initialize chatbot
chatbot = DialogueSystem()

# Process user input
response = chatbot.process_input("Track my order ORD001")
print(response)

# Get conversation history
history = chatbot.get_conversation_history()
print(history)

# Set user context
chatbot.set_context('user_id', 'USER_123')
chatbot.set_context('customer_name', 'John')
```

### Advanced Usage
```python
from chatbot.dialogue_system import DialogueSystem
from chatbot.intent_classifier import IntentClassifier
from chatbot.ir_based_qa import IRBasedQA

# Initialize components
chatbot = DialogueSystem()
classifier = IntentClassifier()
qa = IRBasedQA()

# Classify intent
intent, confidence = classifier.classify("Show me my orders")
print(f"Intent: {intent}, Confidence: {confidence}")

# Retrieve FAQ
results = qa.retrieve("How do I return an item?", top_k=3)
for result in results:
    print(f"Q: {result['question']}")
    print(f"A: {result['answer']}")
```

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'chatbot'"
**Solution:**
```bash
# Ensure you're in the project root directory
cd ecommerce-customer-support-chatbot

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in development mode
pip install -e .
```

### Issue 2: "FileNotFoundError: data/intents.json"
**Solution:**
```bash
# Verify all data files exist
ls data/

# Files should include: intents.json, faq.json, sample_orders.json
```

### Issue 3: "Port 5000 already in use"
**Solution:**
```bash
# Run on different port
python -m chatbot.api_wrapper --port 8000

# Or kill process using port 5000
# On macOS/Linux
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
```

### Issue 4: "Import errors when running tests"
**Solution:**
```bash
# Install test dependencies
pip install pytest pytest-mock

# Run tests from project root
python -m pytest tests/
```

---

## Performance Optimization

### Enable Caching
Edit `config.json`:
```json
{
  "cache_enabled": true,
  "cache_ttl": 3600
}
```

### Adjust Logging Level
```bash
export LOG_LEVEL=WARNING  # Reduces logging overhead
```

### Run with Production Settings
```bash
export FLASK_ENV=production
python -m chatbot.api_wrapper
```

---

## Sample Test Conversations

### Test 1: Order Tracking
```
User: Hi
Bot: Hello! How can I help you today?

User: Can you track my order?
Bot: Sure! I can help you track your order. Please provide your order ID.

User: My order ID is ORD001
Bot: Your order ORD001 is pending. Expected delivery: 2025-12-10
```

### Test 2: Order Cancellation
```
User: I need to cancel an order
Bot: I can help you cancel your order. Please provide your order ID.

User: Cancel order ORD002
Bot: Order ORD002 has been cancelled successfully.
```

### Test 3: FAQ Query
```
User: What is your return policy?
Bot: We offer 30-day returns for most items in original condition...

User: How long does shipping take?
Bot: Standard shipping takes 5-7 business days...
```

---

## Support & Documentation

For more information, refer to:
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture
- `API_SPEC.md` - API specification
- `DEPLOYMENT.md` - Production deployment
- `CHATBOT_COMPLETION_SUMMARY.md` - Feature summary

---

## Success Checklist

Before deploying to production, verify:
- [ ] All dependencies installed (`pip list | grep nltk`)
- [ ] Virtual environment activated
- [ ] CLI chatbot working (`python main.py`)
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] API server running (`python -m chatbot.api_wrapper`)
- [ ] Health check endpoint responding
- [ ] Sample conversations working
- [ ] Configuration file present and valid
- [ ] Logs generating in expected location
- [ ] Docker build successful (if using Docker)

---

## Next Steps

1. **Start with CLI**: Test the chatbot locally using `python main.py`
2. **Run Tests**: Verify everything works with `pytest tests/`
3. **Try API**: Run API server and test endpoints
4. **Customize**: Modify `data/intents.json` and `data/faq.json`
5. **Deploy**: Use Docker for production deployment

---

## Contact & Support

For issues or questions:
- Check `TROUBLESHOOTING.md`
- Review existing GitHub issues
- Refer to documentation files

Happy chatting!
