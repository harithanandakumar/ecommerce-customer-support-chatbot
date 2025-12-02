"""REST API wrapper for the E-Commerce Customer Support Chatbot.

This module provides a REST API interface for integrating the chatbot
with external applications and services.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from .dialogue_system import DialogueSystem


class ChatbotAPIWrapper:
    """REST API wrapper for the chatbot."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the API wrapper.
        
        Args:
            config_path: Optional path to configuration file.
        """
        self.chatbot = DialogueSystem()
        self.logger = logging.getLogger(__name__)
        self.sessions = {}  # Store active sessions
    
    def process_message(self, user_id: str, message: str, 
                       session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user message and return a response.
        
        Args:
            user_id: Unique user identifier.
            message: User's input message.
            session_id: Optional session ID for context tracking.
            
        Returns:
            Dictionary containing response and metadata.
        """
        try:
            # Process input through chatbot
            response = self.chatbot.process_input(message)
            
            # Create response object
            result = {
                'success': True,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'response': response,
                'session_id': session_id or self._generate_session_id(user_id)
            }
            
            self.logger.info(f"Processed message from user {user_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def track_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Track order status.
        
        Args:
            user_id: User identifier.
            order_id: Order ID to track.
            
        Returns:
            Order status information.
        """
        message = f"Track my order {order_id}"
        return self.process_message(user_id, message)
    
    def cancel_order(self, user_id: str, order_id: str) -> Dict[str, Any]:
        """Request order cancellation.
        
        Args:
            user_id: User identifier.
            order_id: Order ID to cancel.
            
        Returns:
            Cancellation status.
        """
        message = f"Cancel order {order_id}"
        return self.process_message(user_id, message)
    
    def get_faq(self, user_id: str, query: str) -> Dict[str, Any]:
        """Get FAQ response.
        
        Args:
            user_id: User identifier.
            query: FAQ query.
            
        Returns:
            FAQ response.
        """
        return self.process_message(user_id, query)
    
    def reset_session(self, session_id: str) -> Dict[str, Any]:
        """Reset conversation session.
        
        Args:
            session_id: Session ID to reset.
            
        Returns:
            Status confirmation.
        """
        try:
            self.chatbot.reset_conversation()
            if session_id in self.sessions:
                del self.sessions[session_id]
            return {'success': True, 'message': 'Session reset'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on the chatbot.
        
        Returns:
            Health status.
        """
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate unique session ID.
        
        Args:
            user_id: User identifier.
            
        Returns:
            Generated session ID.
        """
        import hashlib
        session_key = f"{user_id}_{datetime.now().timestamp()}"
        return hashlib.md5(session_key.encode()).hexdigest()
