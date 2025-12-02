"""International language support module for the e-commerce chatbot.

Supports multiple languages for customer interactions:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Portuguese (pt)
- Mandarin Chinese (zh)
"""

from typing import Dict, Optional
import json
from pathlib import Path


class LanguageManager:
  """Manages language-specific responses and text for the chatbot."""

  SUPPORTED_LANGUAGES = {'en', 'es', 'fr', 'de', 'pt', 'zh'}
  DEFAULT_LANGUAGE = 'en'

  def __init__(self, language: str = 'en'):
    """Initialize language manager with specified language.
    
    Args:
        language: Language code (en, es, fr, de, pt, zh)
    
    Raises:
        ValueError: If language not supported
    """
    if language not in self.SUPPORTED_LANGUAGES:
      raise ValueError(f"Language {language} not supported")
    self.current_language = language
    self.translations: Dict[str, Dict[str, str]] = {}
    self._load_translations()

  def _load_translations(self) -> None:
    """Load translation dictionaries."""
    self.translations = {
      'order_tracking': {
        'en': 'Track your order',
        'es': 'Rastrear tu pedido',
        'fr': 'Suivre votre commande',
        'de': 'Bestellung verfolgen',
        'pt': 'Rastrear seu pedido',
        'zh': '跟踪您的订单'
      },
      'cancel_order': {
        'en': 'Cancel your order',
        'es': 'Cancelar tu pedido',
        'fr': 'Annuler votre commande',
        'de': 'Bestellung stornieren',
        'pt': 'Cancelar seu pedido',
        'zh': '取消订单'
      },
      'check_status': {
        'en': 'Your order status is:',
        'es': 'El estado de tu pedido es:',
        'fr': 'Votre statut de commande est:',
        'de': 'Ihr Bestellstatus ist:',
        'pt': 'Seu status de pedido é:',
        'zh': '您的订单状态是:'
      },
      'support_help': {
        'en': 'How can I help you today?',
        'es': '¿Cómo puedo ayudarte hoy?',
        'fr': 'Comment puis-je vous aider aujourd\'hui?',
        'de': 'Wie kann ich dir heute helfen?',
        'pt': 'Como posso ajudá-lo hoje?',
        'zh': '我今天能如何帮助您?'
      },
      'language_changed': {
        'en': 'Language changed to English',
        'es': 'Idioma cambiado a Español',
        'fr': 'Langue changée en Français',
        'de': 'Sprache zu Deutsch gewechselt',
        'pt': 'Idioma alterado para Português',
        'zh': '语言已更改为中文'
      }
    }

  def set_language(self, language: str) -> bool:
    """Change active language.
    
    Args:
        language: Language code
    
    Returns:
        True if successful, False otherwise
    """
    if language in self.SUPPORTED_LANGUAGES:
      self.current_language = language
      return True
    return False

  def get_text(self, key: str) -> str:
    """Get translated text for given key.
    
    Args:
        key: Translation key
    
    Returns:
        Translated text in current language
    """
    if key in self.translations:
      return self.translations[key].get(
        self.current_language,
        self.translations[key].get(self.DEFAULT_LANGUAGE, key)
      )
    return key

  def translate_response(self, response: str) -> str:
    """Translate chatbot response to current language.
    
    Args:
        response: Response text
    
    Returns:
        Translated response
    """
    # Check if response contains known keys
    for key in self.translations:
      if key in response.lower():
        translated = self.get_text(key)
        response = response.replace(key, translated)
    return response

  def get_supported_languages(self) -> Dict[str, str]:
    """Get list of supported languages.
    
    Returns:
        Dict mapping language codes to language names
    """
    return {
      'en': 'English',
      'es': 'Spanish',
      'fr': 'French',
      'de': 'German',
      'pt': 'Portuguese',
      'zh': 'Mandarin Chinese'
    }

  def get_current_language(self) -> str:
    """Get currently active language code."""
    return self.current_language

  def export_translations(self) -> str:
    """Export translations as JSON string.
    
    Returns:
        JSON formatted translations
    """
    return json.dumps(self.translations, ensure_ascii=False, indent=2)


class LocalizationFormatter:
  """Formats text based on locale rules."""

  @staticmethod
  def format_price(amount: float, language: str = 'en') -> str:
    """Format price according to locale.
    
    Args:
        amount: Price amount
        language: Language code
    
    Returns:
        Formatted price string
    """
    if language in {'es', 'fr', 'de', 'pt'}:
      return f"EUR {amount:.2f}"
    elif language == 'zh':
      return f"¥{amount:.2f}"
    else:
      return f"${amount:.2f}"

  @staticmethod
  def format_date(date_str: str, language: str = 'en') -> str:
    """Format date according to locale.
    
    Args:
        date_str: Date string (YYYY-MM-DD)
        language: Language code
    
    Returns:
        Formatted date string
    """
    if language == 'en':
      return date_str  # MM/DD/YYYY
    elif language in {'es', 'fr', 'de', 'pt', 'zh'}:
      return date_str  # DD/MM/YYYY
    return date_str

  @staticmethod
  def format_phone(phone: str, language: str = 'en') -> str:
    """Format phone number according to locale.
    
    Args:
        phone: Phone number
        language: Language code
    
    Returns:
        Formatted phone number
    """
    # Removes formatting, applies locale-specific format
    digits = ''.join(filter(str.isdigit, phone))
    
    if language == 'en':
      if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif language in {'es', 'de', 'pt'}:
      if len(digits) >= 9:
        return f"+{digits[:2]} {digits[2:5]} {digits[5:]}"
    
    return phone


def initialize_language_manager(language: Optional[str] = None) -> LanguageManager:
  """Factory function to create language manager.
  
  Args:
      language: Language code, defaults to system default
  
  Returns:
      Initialized LanguageManager instance
  """
  try:
    return LanguageManager(language or LanguageManager.DEFAULT_LANGUAGE)
  except ValueError as e:
    print(f"Error initializing language manager: {e}")
    return LanguageManager(LanguageManager.DEFAULT_LANGUAGE)
