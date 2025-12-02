# Quick Start Guide

Get up and running with the E-Commerce Customer Support Chatbot in 5 minutes.

## 1. Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Run the Chatbot (1 minute)

```bash
python main.py
```

You'll see:
```
Chatbot initialized. Type 'exit' to quit.
> 
```

## 3. Try It Out (2 minutes)

### Order Tracking
```
> Track my order ORD001
Your order ORD001 is currently Shipped.
Expected delivery: 2025-12-10
```

### FAQ Query
```
> How long does shipping take?
Standard shipping typically takes 5-7 business days.
Expedited shipping takes 2-3 business days.
```

### Order Cancellation
```
> Cancel order ORD002
Order ORD002 has status Processing.
Eligible for cancellation: Yes
Your order has been successfully cancelled.
```

## Docker Quick Start

If you prefer Docker:

```bash
# Build image
docker build -t ecommerce-chatbot .

# Run container
docker run -it -v ./logs:/app/logs ecommerce-chatbot
```

## Key Commands

| Command | Example |
|---------|----------|
| Track order | "Track my order ORD001" |
| Cancel order | "Cancel order ORD002" |
| FAQ query | "How long does shipping take?" |
| Greeting | "Hello" or "Hi" |
| Exit | "exit" |

## Configuration

Edit `config.json` to customize:

```json
{
  "intent_classifier": {
    "confidence_threshold": 0.6
  },
  "logging": {
    "file_path": "logs/chatbot.log"
  }
}
```

## Testing

Run automated tests:

```bash
pytest tests/ -v
```

## Troubleshooting

**Issue**: Module not found
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Issue**: Port 5000 already in use
```bash
# Change port in config.json or specify in code
```

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for detailed usage
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Review [README.md](README.md) for full documentation

## Common Questions

**Q: Can I add custom intents?**
A: Yes! Edit `data/intents.json` and add your patterns.

**Q: How do I integrate with my system?**
A: Use the API wrapper in `chatbot/api_wrapper.py` or REST endpoints.

**Q: Where are logs stored?**
A: Logs are in `logs/chatbot.log` with automatic rotation.

**Q: How accurate is the chatbot?**
A: Accuracy depends on intent patterns in `data/intents.json`. Test with your data.

## Getting Help

- Check GitHub Issues for common problems
- Read the full documentation in README.md
- Review DEPLOYMENT.md for production issues
- Check CONTRIBUTING.md for development help
