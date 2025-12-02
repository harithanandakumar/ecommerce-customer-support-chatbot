import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.intent_classifier import IntentClassifier

class TestIntentClassifier(unittest.TestCase):
    """Test suite for IntentClassifier module."""
    
    def setUp(self):
        """Initialize classifier before each test."""
        self.classifier = IntentClassifier()
    
    def test_track_order_intent(self):
        """Test tracking order intent detection."""
        result = self.classifier.classify("Track my order ORD001")
        self.assertEqual(result['intent'], 'track_order')
    
    def test_cancel_item_intent(self):
        """Test cancel item intent detection."""
        result = self.classifier.classify("Cancel order ORD002")
        self.assertEqual(result['intent'], 'cancel_item')
    
    def test_faq_intent(self):
        """Test FAQ intent detection."""
        result = self.classifier.classify("How long does shipping take?")
        self.assertEqual(result['intent'], 'faq')
    
    def test_greeting_intent(self):
        """Test greeting intent detection."""
        result = self.classifier.classify("Hello!")
        self.assertEqual(result['intent'], 'greeting')
    
    def test_confidence_score(self):
        """Test that confidence score is returned."""
        result = self.classifier.classify("Track my order")
        self.assertIn('confidence', result)
        self.assertGreaterEqual(result['confidence'], 0)
        self.assertLessEqual(result['confidence'], 1)

if __name__ == '__main__':
    unittest.main()
