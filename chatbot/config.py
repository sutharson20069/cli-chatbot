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
        
        # AI Model configurations
        'ai_models': {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'models': {
                    'gpt-3.5-turbo': os.getenv('OPENAI_GPT35_ENDPOINT', 'https://api.openai.com/v1/chat/completions'),
                    'gpt-4': os.getenv('OPENAI_GPT4_ENDPOINT', 'https://api.openai.com/v1/chat/completions'),
                    'gpt-4-turbo': os.getenv('OPENAI_GPT4_TURBO_ENDPOINT', 'https://api.openai.com/v1/chat/completions'),
                    'gpt-4o': os.getenv('OPENAI_GPT4O_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
                }
            },
            'google': {
                'api_key': os.getenv('GOOGLE_AI_API_KEY', ''),
                'models': {
                    'gemini-pro': os.getenv('GOOGLE_GEMINI_PRO_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'),
                    'gemini-ultra': os.getenv('GOOGLE_GEMINI_ULTRA_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-ultra:generateContent'),
                    'gemini-flash': os.getenv('GOOGLE_GEMINI_FLASH_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash:generateContent')
                }
            },
            'anthropic': {
                'api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                'models': {
                    'claude-3-haiku': os.getenv('ANTHROPIC_CLAUDE3_HAIKU_ENDPOINT', 'https://api.anthropic.com/v1/messages'),
                    'claude-3-sonnet': os.getenv('ANTHROPIC_CLAUDE3_SONNET_ENDPOINT', 'https://api.anthropic.com/v1/messages'),
                    'claude-3-opus': os.getenv('ANTHROPIC_CLAUDE3_Opus_ENDPOINT', 'https://api.anthropic.com/v1/messages')
                }
            },
            'mistral': {
                'api_key': os.getenv('MISTRAL_API_KEY', ''),
                'models': {
                    'mixtral-8x7b': os.getenv('MISTRAL_MIXTRAL_ENDPOINT', 'https://api.mistral.ai/v1/chat/completions'),
                    'codestral': os.getenv('MISTRAL_CODESTRAL_ENDPOINT', 'https://api.mistral.ai/v1/chat/completions'),
                    'mistral-large': os.getenv('MISTRAL_LARGE_ENDPOINT', 'https://api.mistral.ai/v1/chat/completions')
                }
            },
            'cohere': {
                'api_key': os.getenv('COHERE_API_KEY', ''),
                'models': {
                    'command-r': os.getenv('COHERE_COMMAND_R_ENDPOINT', 'https://api.cohere.ai/v1/chat'),
                    'command-r-plus': os.getenv('COHERE_COMMAND_R_PLUS_ENDPOINT', 'https://api.cohere.ai/v1/chat')
                }
            },
            'huggingface': {
                'api_key': os.getenv('HUGGINGFACE_API_KEY', ''),
                'endpoint': os.getenv('HUGGINGFACE_API_ENDPOINT', 'https://api-inference.huggingface.co/models/')
            }
        },
        
        # Default model selection
        'default_model': os.getenv('DEFAULT_AI_MODEL', 'gpt-3.5-turbo'),
        'fallback_model': os.getenv('FALLBACK_AI_MODEL', 'gemini-pro'),
        
        # API settings
        'api_timeout': int(os.getenv('API_TIMEOUT', '30')),
        'api_max_retries': int(os.getenv('API_MAX_RETRIES', '3')),
        'api_retry_delay': int(os.getenv('API_RETRY_DELAY', '2')),
        
        # Logging configuration
        'log_level': os.getenv('CHATBOT_LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('CHATBOT_LOG_FILE', 'chatbot.log')
    }
    
    return config


def get_env_variable(name: str, default: Any = None) -> Any:
    """Get an environment variable with optional default."""
    return os.getenv(name, default)