import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
from .intent_classifier import IntentClassifier
from .ir_based_qa import IRBasedQA
from .response_generator import ResponseGenerator
from .order_tracker import OrderTracker

class DialogueSystem:
    """Main dialogue management system orchestrating all components."""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.qa_system = IRBasedQA()
        self.response_generator = ResponseGenerator()
        self.order_tracker = OrderTracker()
        self.conversation_history = []
        self.user_context = {}
    
    def process_input(self, user_input: str) -> str:
        """Main entry point for processing user queries."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'type': 'user'
        })
        intent, confidence = self.intent_classifier.classify(user_input)
        response = self._handle_intent(intent, user_input)
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'assistant': response,
            'type': 'assistant',
            'intent': intent,
            'confidence': confidence
        })
        return response
    
    def _handle_intent(self, intent: str, user_input: str) -> str:
        """Route to appropriate handler based on detected intent."""
        if intent == 'track_order':
            return self._handle_track_order(user_input)
        elif intent == 'cancel_item':
            return self._handle_cancel_item(user_input)
        elif intent == 'greeting':
            return self.response_generator.generate(intent)
        else:
            qa_results = self.qa_system.retrieve(user_input, top_k=1)
            if qa_results:
                return qa_results[0]['answer']
            return self.response_generator.generate('default')
    
    def _handle_track_order(self, user_input: str) -> str:
        """Handle order tracking requests."""
        order_id = self._extract_order_id(user_input)
        if order_id:
            order = self.order_tracker.get_order(order_id)
            if order:
                return f"Your order {order_id} is {order['status']}. Expected delivery: {order['delivery_date']}"
        return "I couldn't find your order. Please provide your order ID."
    
    def _handle_cancel_item(self, user_input: str) -> str:
        """Handle order cancellation requests."""
        order_id = self._extract_order_id(user_input)
        if order_id:
            order = self.order_tracker.get_order(order_id)
            if order and order['status'] in ['pending', 'processing']:
                self.order_tracker.cancel_order(order_id)
                return f"Order {order_id} has been cancelled successfully."
        return "Unable to cancel this order. It may have already shipped."
    
    def _extract_order_id(self, text: str) -> str:
        """Extract order ID using regex pattern matching."""
        match = re.search(r'order\s*(?:id)?:?\s*([A-Z0-9]+)', text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def get_conversation_history(self) -> List[Dict]:
        """Retrieve complete conversation history."""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_context(self) -> Dict:
        """Get current user context."""
        return self.user_context
    
    def set_context(self, key: str, value) -> None:
        """Set user context information."""
        self.user_context[key] = value
