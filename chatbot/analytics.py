"""Advanced analytics and reporting module for chatbot insights."""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict


class AnalyticsEngine:
    """Analyze chatbot interactions for business insights."""

    def __init__(self):
        self.interactions = []
        self.start_time = datetime.now()

    def log_interaction(self, user_id: str, intent: str, response_time: float,
                       success: bool, session_id: str):
        """Log an interaction for analytics."""
        self.interactions.append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'intent': intent,
            'response_time': response_time,
            'success': success,
            'session_id': session_id
        })

    def get_intent_distribution(self) -> Dict[str, int]:
        """Get distribution of intents handled."""
        intents = [i['intent'] for i in self.interactions]
        return dict(Counter(intents))

    def get_success_rate(self) -> float:
        """Calculate overall success rate."""
        if not self.interactions:
            return 0.0
        successful = sum(1 for i in self.interactions if i['success'])
        return (successful / len(self.interactions)) * 100

    def get_response_time_stats(self) -> Dict[str, float]:
        """Get response time statistics."""
        if not self.interactions:
            return {}
        times = [i['response_time'] for i in self.interactions]
        return {
            'avg': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'p95': sorted(times)[int(len(times) * 0.95)]
        }

    def get_user_engagement(self) -> Dict[str, int]:
        """Get user engagement metrics."""
        unique_users = len(set(i['user_id'] for i in self.interactions))
        avg_interactions_per_user = len(self.interactions) / max(unique_users, 1)
        return {
            'unique_users': unique_users,
            'total_interactions': len(self.interactions),
            'avg_per_user': avg_interactions_per_user
        }

    def get_session_analytics(self) -> Dict[str, Any]:
        """Analyze session patterns."""
        sessions = defaultdict(list)
        for i in self.interactions:
            sessions[i['session_id']].append(i)
        
        return {
            'total_sessions': len(sessions),
            'avg_interactions_per_session': len(self.interactions) / len(sessions),
            'longest_session': max(len(s) for s in sessions.values())
        }

    def generate_report(self) -> str:
        """Generate comprehensive analytics report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'uptime_minutes': (datetime.now() - self.start_time).total_seconds() / 60,
            'intent_distribution': self.get_intent_distribution(),
            'success_rate': self.get_success_rate(),
            'response_times': self.get_response_time_stats(),
            'user_engagement': self.get_user_engagement(),
            'session_analytics': self.get_session_analytics()
        }
        return json.dumps(report, indent=2)
