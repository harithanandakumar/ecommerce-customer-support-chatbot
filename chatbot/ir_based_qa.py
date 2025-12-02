import json
import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IRBasedQA:
    """TF-IDF based IR system for FAQ retrieval."""
    
    def __init__(self, faq_file='data/faq.json'):
        with open(faq_file, 'r') as f:
            self.faq_data = json.load(f)
        self._build_index()
    
    def _build_index(self):
        self.questions = [qa['question'] for qa in self.faq_data['faqs']]
        self.answers = [qa['answer'] for qa in self.faq_data['faqs']]
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2), max_features=1000)
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.question_vectors)[0]
            top_indices = np.argsort(similarities)[::-1][:top_k]
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:
                    results.append({'question': self.questions[idx], 'answer': self.answers[idx], 'score': float(similarities[idx])})
            return results
        except:
            return []
