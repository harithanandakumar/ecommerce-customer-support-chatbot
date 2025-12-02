# E-Commerce Customer Support Chatbot

Rule-based NLP e-commerce customer support chatbot with intent classification, IR-based QA, and response generation.

## Features

- Intent Classification using pattern matching
- TF-IDF based IR for FAQ retrieval
- Dialogue system for multi-turn conversations
- Order tracking and cancellation
- Contextual response generation

## Project Structure

- `chatbot/intent_classifier.py` - Rule-based intent detection
- `chatbot/ir_based_qa.py` - Information retrieval QA
- `chatbot/dialogue_system.py` - Main dialogue orchestration
- `chatbot/response_generator.py` - Response generation
- `chatbot/order_tracker.py` - Order management
- `data/intents.json` - Intent patterns
- `data/faq.json` - FAQ database
- `data/sample_orders.json` - Sample order data
- `main.py` - CLI interface

## Installation

```bash
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot
cd ecommerce-customer-support-chatbot
pip install -r requirements.txt
```

## Usage

```python
from chatbot.dialogue_system import DialogueSystem

chatbot = DialogueSystem()
response = chatbot.process_input("Track my order ORD001")
print(response)
```

## Supported Intents

1. **track_order** - Track order status
2. **cancel_item** - Cancel orders
3. **faq** - FAQ queries
4. **greeting** - General greetings
