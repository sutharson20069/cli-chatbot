"""
Utility functions for the professional chatbot.

This module contains helper functions and utilities used throughout
the chatbot application.
"""

import re
from typing import List, Dict, Any
from datetime import datetime


def validate_input(text: str) -> bool:
    """Validate user input."""
    if not text or not text.strip():
        return False
    
    # Check for potentially harmful input
    harmful_patterns = [
        r'<script.*?>.*?</script>',  # HTML scripts
        r'\b(drop|delete|truncate|insert|update)\b.*\b(table|database)\b',  # SQL commands
        r'\b(rm|del|remove|erase|format)\b.*\b(-rf|/s)\b',  # Dangerous file commands
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True


def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove potentially harmful characters
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)  # Remove control characters
    
    return text.strip()


def format_timestamp(timestamp: str) -> str:
    """Format a timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return timestamp


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def is_valid_email(email: str) -> bool:
    """Validate an email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract entities from text (simple implementation)."""
    entities = {
        'emails': re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text),
        'urls': re.findall(r'https?://[^\s]+', text),
        'phone_numbers': re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text),
        'dates': re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    }
    return entities