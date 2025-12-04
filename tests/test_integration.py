import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.dialogue_system import DialogueSystem
from chatbot.intent_classifier import IntentClassifier
from chatbot.ir_based_qa import IRBasedQA
from chatbot.response_generator import ResponseGenerator
from chatbot.order_tracker import OrderTracker


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete chatbot workflow."""

    def setUp(self):
        """Initialize the dialogue system before each test."""
        self.dialogue_system = DialogueSystem()

    def test_greeting_intent(self):
        """Test greeting intent recognition and response."""
        response = self.dialogue_system.process_input("Hello")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_track_order_intent(self):
        """Test order tracking with order ID extraction."""
        response = self.dialogue_system.process_input("Track my order ORD001")
        self.assertIsNotNone(response)
        self.assertIn("ORD001", response)

    def test_cancel_item_intent(self):
        """Test order cancellation workflow."""
        response = self.dialogue_system.process_input("Cancel order ORD002")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

    def test_faq_retrieval(self):
        """Test FAQ retrieval for general queries."""
        response = self.dialogue_system.process_input("What is your return policy?")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

    def test_conversation_history(self):
        """Test conversation history tracking."""
        self.dialogue_system.process_input("Hi")
        self.dialogue_system.process_input("Track order ORD001")
        
        history = self.dialogue_system.get_conversation_history()
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]['type'], 'user')
        self.assertEqual(history[1]['type'], 'assistant')

    def test_context_management(self):
        """Test user context storage and retrieval."""
        self.dialogue_system.set_context('user_id', 'USER_123')
        context = self.dialogue_system.get_context()
        self.assertEqual(context['user_id'], 'USER_123')

    def test_multi_turn_conversation(self):
        """Test multi-turn conversation handling."""
        responses = []
        queries = [
            "Hi, can you help me?",
            "I need to track my order",
            "My order ID is ORD001"
        ]
        
        for query in queries:
            response = self.dialogue_system.process_input(query)
            responses.append(response)
            self.assertIsNotNone(response)
        
        self.assertTrue(all(responses))

    def test_intent_classification_confidence(self):
        """Test intent classification with confidence scores."""
        classifier = IntentClassifier()
        intent, confidence = classifier.classify("Track my order")
        
        self.assertEqual(intent, "track_order")
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 1.0)

    def test_response_generator(self):
        """Test response generation for different intents."""
        generator = ResponseGenerator()
        greeting_response = generator.generate('greeting')
        self.assertIsNotNone(greeting_response)
        self.assertIsInstance(greeting_response, list)

    def test_order_tracker_operations(self):
        """Test order tracking operations."""
        tracker = OrderTracker()
        order = tracker.get_order('ORD001')
        self.assertIsNotNone(order)
        self.assertIn('status', order)
        self.assertIn('delivery_date', order)

    def test_faq_retrieval_system(self):
        """Test FAQ retrieval with similarity matching."""
        qa_system = IRBasedQA()
        results = qa_system.retrieve("How long does shipping take?", top_k=1)
        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)

    def test_clear_history(self):
        """Test conversation history clearing."""
        self.dialogue_system.process_input("Hello")
        self.dialogue_system.process_input("Track order")
        self.dialogue_system.clear_history()
        history = self.dialogue_system.get_conversation_history()
        self.assertEqual(len(history), 0)

    def test_dialogue_system_end_to_end(self):
        """Complete end-to-end dialogue system test."""
        queries = [
            "Hi there",
            "I have a question about my order",
            "Can you track order ORD001?",
            "What's the return policy?"
        ]
        
        for query in queries:
            response = self.dialogue_system.process_input(query)
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
        
        history = self.dialogue_system.get_conversation_history()
        self.assertEqual(len(history), len(queries) * 2)


if __name__ == '__main__':
    unittest.main()
