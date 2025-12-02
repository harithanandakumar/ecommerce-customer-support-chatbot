# Example Usage and Sample Conversations

This document provides example conversations demonstrating the capabilities of the E-Commerce Customer Support Chatbot.

## Example 1: Order Tracking

```
User: Track my order ORD001
Bot: Your order ORD001 is currently Shipped. Expected delivery: 2025-12-10

User: Can you tell me more about this order?
Bot: Order ID: ORD001, Status: Shipped, Items: 2, Total: $149.99, Delivery: 2025-12-10
```

## Example 2: Order Cancellation

```
User: I want to cancel order ORD002
Bot: Order ORD002 has status Processing. Eligible for cancellation: Yes
Would you like to proceed with cancellation?

User: Yes, cancel it
Bot: Your order ORD002 has been successfully cancelled. A refund will be processed within 5-7 business days.
```

## Example 3: FAQ Query

```
User: How long does shipping take?
Bot: Standard shipping typically takes 5-7 business days.
Expedited shipping takes 2-3 business days.
Same-day delivery is available in selected areas for an additional fee.

User: What about returns?
Bot: We offer a 30-day return policy for most items.
Items must be in original condition with all tags attached.
Simpply contact our support team to initiate a return.
```

## Example 4: Multi-turn Conversation

```
User: Hello
Bot: Hello! Welcome to E-Commerce Support. How can I help you today?

User: I have a question about my recent order
Bot: I'd be happy to help! Do you want to track an order or have another question?

User: Track order ORD003
Bot: Your order ORD003 is currently Processing. 
Each step is being prepared for shipment.
You'll receive a shipping notification soon.

User: When will it ship?
Bot: Your order is expected to ship within 24 hours.
You'll receive an email confirmation with tracking information.
```

## Example 5: Greeting and General Help

```
User: Hi there!
Bot: Hi! Welcome to our support team. What can I assist you with today?

User: Do you have any tips for customers?
Bot: Here are some helpful tips:
- Track your orders regularly for updates
- Save your order confirmation for reference
- Contact us within 30 days for returns
- Use expedited shipping for urgent orders
```

## Using the Chatbot Programmatically

### Python Integration

```python
from chatbot.dialogue_system import DialogueSystem

# Initialize the chatbot
chatbot = DialogueSystem()

# Process user input
response = chatbot.process_input("Track my order ORD001")
print(response)
# Output: Your order ORD001 is currently Shipped. Expected delivery: 2025-12-10

# Multi-turn conversation
response = chatbot.process_input("What's the status?")
print(response)  # Uses conversation context

# Reset conversation
chatbot.reset_conversation()
```

## Supported Intents

1. **track_order** - Check order status
   - Examples: "Track my order", "Order status", "Where is my package?"

2. **cancel_item** - Cancel an order
   - Examples: "Cancel order", "I want to cancel", "Remove my order"

3. **faq** - Frequently asked questions
   - Examples: "How long does shipping take?", "What's your return policy?"

4. **greeting** - General greeting
   - Examples: "Hello", "Hi", "Good morning"

## Testing the Chatbot

Run the CLI interface:

```bash
python main.py
```

Then enter your queries interactively:

```
> Track my order ORD001
Your order ORD001 is currently Shipped. Expected delivery: 2025-12-10

> How long does shipping take?
Standard shipping typically takes 5-7 business days.
Expedited shipping takes 2-3 business days.

> Exit
Goodbye!
```

## Tips for Best Results

- Use clear, natural language queries
- Include order IDs when checking order status
- The chatbot works best with specific intents
- Conversation history is maintained for context
- Formatting: "Track", "Cancel", "How", "What", etc.
