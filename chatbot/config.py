"""
Configuration management for the professional chatbot.

This module handles loading and managing configuration settings
from environment variables and configuration files.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables and defaults."""
    config = {
        # Default configuration
        'theme': os.getenv('CHATBOT_THEME', 'default'),
        'verbose': os.getenv('CHATBOT_VERBOSE', 'false').lower() == 'true',
        'max_history': int(os.getenv('CHATBOT_MAX_HISTORY', '10')),
        'language': os.getenv('CHATBOT_LANGUAGE', 'english'),
        'debug': os.getenv('CHATBOT_DEBUG', 'false').lower() == 'true',
        
        # API configurations (if needed for future extensions)
        'api_key': os.getenv('CHATBOT_API_KEY', ''),
        'api_endpoint': os.getenv('CHATBOT_API_ENDPOINT', ''),
        
        # Logging configuration
        'log_level': os.getenv('CHATBOT_LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('CHATBOT_LOG_FILE', 'chatbot.log')
    }
    
    return config


def get_env_variable(name: str, default: Any = None) -> Any:
    """Get an environment variable with optional default."""
    return os.getenv(name, default)