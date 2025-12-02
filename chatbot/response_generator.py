import json
import random
from typing import Dict, List

class ResponseGenerator:
    """Generate context-aware responses."""
    
    def __init__(self, intents_file='data/intents.json'):
        with open(intents_file, 'r') as f:
            self.intents = json.load(f)
        self.response_map = self._build_response_map()
    
    def _build_response_map(self) -> Dict[str, List[str]]:
        response_map = {}
        for intent in self.intents['intents']:
            response_map[intent['tag']] = intent['responses']
        return response_map
    
    def generate(self, intent: str, entities: Dict = None) -> str:
        if intent not in self.response_map:
            return "I'm sorry, I didn't understand that. Can you please rephrase?"
        responses = self.response_map[intent]
        response = random.choice(responses)
        if entities:
            for key, value in entities.items():
                response = response.replace(f"{{{key}}}", str(value))
        return response
