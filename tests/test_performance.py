"""Performance testing suite for chatbot components.

Conducts load testing and performance benchmarking for:
- Intent classification throughput
- IR-based QA latency
- Dialogue system response times
- Overall chatbot performance
"""

import time
import unittest
from unittest.mock import patch, MagicMock
from chatbot.dialogue_system import DialogueSystem
from chatbot.intent_classifier import IntentClassifier
from chatbot.ir_based_qa import IRBasedQA


class PerformanceTest(unittest.TestCase):
    """Performance benchmarking test suite."""

    def setUp(self):
        """Initialize components for testing."""
        self.classifier = IntentClassifier()
        self.qa_system = IRBasedQA()
        self.dialogue_system = DialogueSystem()

    def test_intent_classification_throughput(self):
        """Benchmark intent classification speed."""
        test_inputs = [
            "Track my order ORD001",
            "What's the shipping cost?",
            "I want to cancel item SKU123",
            "Hello!",
            "Where are my products?",
        ] * 100

        start_time = time.time()
        for user_input in test_inputs:
            intent, confidence = self.classifier.classify(user_input)
        elapsed = time.time() - start_time
        throughput = len(test_inputs) / elapsed

        print(f"Intent Classification Throughput: {throughput:.2f} requests/sec")
        print(f"Avg latency: {(elapsed/len(test_inputs))*1000:.2f}ms")

        # Should process at least 100 requests/sec
        self.assertGreater(throughput, 100)

    def test_dialogue_response_latency(self):
        """Benchmark dialogue system response generation."""
        test_inputs = [
            "Track my order ORD001",
            "What's the return policy?",
            "Can you help?",
        ] * 50

        start_time = time.time()
        for user_input in test_inputs:
            response = self.dialogue_system.process_input(user_input)
        elapsed = time.time() - start_time
        avg_latency = (elapsed / len(test_inputs)) * 1000

        print(f"Dialogue Response Time: {avg_latency:.2f}ms (avg)")
        print(f"Total time for {len(test_inputs)} requests: {elapsed:.2f}s")

        # Should respond within 200ms on average
        self.assertLess(avg_latency, 200)

    def test_concurrent_processing(self):
        """Benchmark concurrent request handling."""
        import threading

        responses = []
        errors = []

        def process_request():
            try:
                response = self.dialogue_system.process_input(
                    "What's my order status?"
                )
                responses.append(response)
            except Exception as e:
                errors.append(str(e))

        start_time = time.time()
        threads = []
        for _ in range(50):
            t = threading.Thread(target=process_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        elapsed = time.time() - start_time

        print(f"Concurrent requests (50): {elapsed:.2f}s")
        print(f"Successful: {len(responses)}, Errors: {len(errors)}")

        self.assertEqual(len(responses), 50)
        self.assertEqual(len(errors), 0)

    def test_memory_efficiency(self):
        """Check memory usage patterns."""
        import gc

        gc.collect()
        initial_size = len(gc.get_objects())

        for i in range(1000):
            self.dialogue_system.process_input(f"Request {i}")

        gc.collect()
        final_size = len(gc.get_objects())
        growth = final_size - initial_size

        print(f"Object growth after 1000 requests: {growth}")
        # Should not grow unboundedly
        self.assertLess(growth, 500)


if __name__ == "__main__":
    unittest.main()
