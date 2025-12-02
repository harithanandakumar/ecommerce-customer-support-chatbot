import json
from typing import Tuple, Dict

class IntentClassifier:
    """Rule-based intent classifier for e-commerce queries."""
    
    def __init__(self, intents_file='data/intents.json'):
        with open(intents_file, 'r') as f:
            self.intents = json.load(f)
        self.intent_keywords = self._build_keyword_map()
    
    def _build_keyword_map(self) -> Dict:
        keyword_map = {}
        for intent in self.intents['intents']:
            intent_name = intent['tag']
            for pattern in intent['patterns']:
                keywords = pattern.lower().split()
                for keyword in keywords:
                    if keyword not in keyword_map:
                        keyword_map[keyword] = []
                    keyword_map[keyword].append(intent_name)
        return keyword_map
    
    def classify(self, user_input: str) -> Tuple[str, float]:
        """Classify user input using pattern matching and scoring."""
        user_input_lower = user_input.lower()
        intent_scores = {}
        
        for intent in self.intents['intents']:
            intent_name = intent['tag']
            intent_scores[intent_name] = 0
            
            for pattern in intent['patterns']:
                pattern_lower = pattern.lower()
                if pattern_lower in user_input_lower:
                    intent_scores[intent_name] += 2.0
                else:
                    pattern_words = pattern_lower.split()
                    matched_words = sum(1 for word in pattern_words if word in user_input_lower)
                    intent_scores[intent_name] += matched_words * 0.5
        
        if not intent_scores or max(intent_scores.values()) == 0:
            return 'greeting', 0.3
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 10, 1.0)
        return best_intent, confidence
