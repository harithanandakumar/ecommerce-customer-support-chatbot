"""Centralized logging configuration for the chatbot."""

import logging
import logging.handlers
import os
from datetime import datetime


class ChatbotLogger:
    """Centralized logging manager for the chatbot."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_level=logging.INFO, log_file='logs/chatbot.log'):
        """Initialize the logger.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            log_file: Path to log file.
        """
        if not self._initialized:
            self.log_level = log_level
            self.log_file = log_file
            self._setup_logging()
            self._initialized = True
    
    def _setup_logging(self):
        """Configure logging handlers and formatters."""
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('chatbot')
        self.logger.setLevel(self.log_level)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler (rotated)
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(detailed_formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Error setting up file logging: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the configured logger instance.
        
        Returns:
            Logger instance.
        """
        return self.logger
    
    @staticmethod
    def get_instance():
        """Get ChatbotLogger singleton instance.
        
        Returns:
            ChatbotLogger instance.
        """
        return ChatbotLogger()


# Module-level logger initialization
logger = ChatbotLogger().get_logger()


def log_error(message: str, exc_info=False):
    """Log error message.
    
    Args:
        message: Error message.
        exc_info: Include exception info.
    """
    logger.error(message, exc_info=exc_info)


def log_warning(message: str):
    """Log warning message.
    
    Args:
        message: Warning message.
    """
    logger.warning(message)


def log_info(message: str):
    """Log info message.
    
    Args:
        message: Info message.
    """
    logger.info(message)


def log_debug(message: str):
    """Log debug message.
    
    Args:
        message: Debug message.
    """
    logger.debug(message)
