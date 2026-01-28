"""
Core functionality for the professional chatbot.

This module contains the main chatbot logic, conversation management,
and natural language processing capabilities.
"""

import re
import random
import json
import requests
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .config import load_config
from .utils import validate_input, sanitize_input


class ChatbotCore:
    """Core chatbot functionality."""
    
    def __init__(self):
        self.config = load_config()
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = self.config.get('max_history', 10)
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize conversation context
        self.conversation_context = {}
        
        # Initialize AI model integration
        self.ai_models = self.config.get('ai_models', {})
        self.default_model = self.config.get('default_model', 'gpt-3.5-turbo')
        self.fallback_model = self.config.get('fallback_model', 'gemini-pro')
        self.api_timeout = self.config.get('api_timeout', 30)
        self.max_retries = self.config.get('api_max_retries', 3)
        self.retry_delay = self.config.get('api_retry_delay', 2)
        
        # Available models mapping
        self.available_models = self._get_available_models()
    
    def _load_knowledge_base(self) -> Dict[str, List[str]]:
        """Load the chatbot's knowledge base."""
        return {
            'greetings': [
                'Hello! How can I assist you today?',
                'Hi there! What would you like to discuss?',
                'Greetings! How may I help you?',
                'Welcome! What brings you here today?'
            ],
            'goodbyes': [
                'Goodbye! Have a great day!',
                'Farewell! It was nice chatting with you.',
                'See you later! Take care.',
                'Until next time! Goodbye.'
            ],
            'thanks': [
                "You're welcome!",
                "I'm happy to help!",
                "No problem at all!",
                "Glad I could assist!"
            ],
            'interview_questions': {
                'technical': [
                    'Can you explain your experience with Python?',
                    'What design patterns have you worked with?',
                    'How do you approach debugging complex issues?',
                    'Describe a challenging technical problem you solved.'
                ],
                'behavioral': [
                    'Tell me about a time you worked in a team.',
                    'How do you handle tight deadlines?',
                    'Describe a situation where you had to learn something quickly.',
                    'What's your approach to problem-solving?'
                ],
                'general': [
                    'What are your strengths and weaknesses?',
                    'Where do you see yourself in 5 years?',
                    'Why are you interested in this position?',
                    'What motivates you in your work?'
                ]
            },
            'responses': {
                'default': [
                    "I see. That's interesting.",
                    "Tell me more about that.",
                    "That's a good point.",
                    "I understand what you're saying.",
                    "That makes sense."
                ],
                'positive': [
                    "That sounds great!",
                    "Excellent point!",
                    "I'm impressed!",
                    "That's very insightful.",
                    "Well said!"
                ],
                'negative': [
                    "I understand your concern.",
                    "That sounds challenging.",
                    "I see what you mean.",
                    "That must be difficult.",
                    "I appreciate you sharing that."
                ]
            },
            'ai_info': {
                'models': {
                    'gpt-3.5-turbo': 'OpenAI GPT-3.5 Turbo - Fast and cost-effective',
                    'gpt-4': 'OpenAI GPT-4 - Most advanced model',
                    'gpt-4-turbo': 'OpenAI GPT-4 Turbo - Faster GPT-4',
                    'gpt-4o': 'OpenAI GPT-4o - Omni model',
                    'gemini-pro': 'Google Gemini Pro - Google AI',
                    'gemini-ultra': 'Google Gemini Ultra - Most powerful Google model',
                    'gemini-flash': 'Google Gemini Flash - Fast and lightweight',
                    'claude-3-haiku': 'Anthropic Claude 3 Haiku - Fastest Claude',
                    'claude-3-sonnet': 'Anthropic Claude 3 Sonnet - Balanced performance',
                    'claude-3-opus': 'Anthropic Claude 3 Opus - Most powerful Claude',
                    'mixtral-8x7b': 'Mistral Mixtral 8x7B - Open-source mixture of experts',
                    'codestral': 'Mistral Codestral - Code-focused model',
                    'mistral-large': 'Mistral Large - Advanced Mistral model',
                    'command-r': 'Cohere Command R - Enterprise-grade',
                    'command-r-plus': 'Cohere Command R+ - Enhanced enterprise model'
                },
                'providers': {
                    'openai': 'OpenAI - Creator of GPT models',
                    'google': 'Google AI - Creator of Gemini models',
                    'anthropic': 'Anthropic - Creator of Claude models',
                    'mistral': 'Mistral AI - Open-source AI company',
                    'cohere': 'Cohere - Enterprise AI solutions',
                    'huggingface': 'Hugging Face - Open-source AI community'
                }
            }
        }
    
    def _get_available_models(self) -> Dict[str, Dict[str, str]]:
        """Get available AI models from configuration."""
        available = {}
        
        # OpenAI models
        if self.ai_models.get('openai', {}).get('api_key'):
            available['openai'] = {
                'gpt-3.5-turbo': self.ai_models['openai']['models']['gpt-3.5-turbo'],
                'gpt-4': self.ai_models['openai']['models']['gpt-4'],
                'gpt-4-turbo': self.ai_models['openai']['models']['gpt-4-turbo'],
                'gpt-4o': self.ai_models['openai']['models']['gpt-4o']
            }
        
        # Google models
        if self.ai_models.get('google', {}).get('api_key'):
            available['google'] = {
                'gemini-pro': self.ai_models['google']['models']['gemini-pro'],
                'gemini-ultra': self.ai_models['google']['models']['gemini-ultra'],
                'gemini-flash': self.ai_models['google']['models']['gemini-flash']
            }
        
        # Anthropic models
        if self.ai_models.get('anthropic', {}).get('api_key'):
            available['anthropic'] = {
                'claude-3-haiku': self.ai_models['anthropic']['models']['claude-3-haiku'],
                'claude-3-sonnet': self.ai_models['anthropic']['models']['claude-3-sonnet'],
                'claude-3-opus': self.ai_models['anthropic']['models']['claude-3-opus']
            }
        
        # Mistral models
        if self.ai_models.get('mistral', {}).get('api_key'):
            available['mistral'] = {
                'mixtral-8x7b': self.ai_models['mistral']['models']['mixtral-8x7b'],
                'codestral': self.ai_models['mistral']['models']['codestral'],
                'mistral-large': self.ai_models['mistral']['models']['mistral-large']
            }
        
        # Cohere models
        if self.ai_models.get('cohere', {}).get('api_key'):
            available['cohere'] = {
                'command-r': self.ai_models['cohere']['models']['command-r'],
                'command-r-plus': self.ai_models['cohere']['models']['command-r-plus']
            }
        
        return available
    
    def _call_openai_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call OpenAI API."""
        try:
            api_key = self.ai_models['openai']['api_key']
            endpoint = self.ai_models['openai']['models'][model]
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            data = {
                'model': model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=self.api_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            
            return None
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def _call_google_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call Google AI API."""
        try:
            api_key = self.ai_models['google']['api_key']
            endpoint = self.ai_models['google']['models'][model]
            
            # Convert messages to Google format
            google_messages = []
            for msg in messages:
                google_messages.append({
                    'role': 'user' if msg['role'] == 'user' else 'model',
                    'parts': [{'text': msg['content']}]
                })
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            params = {
                'key': api_key
            }
            
            data = {
                'contents': google_messages,
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 1000
                }
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                params=params,
                json=data,
                timeout=self.api_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            
            return None
            
        except Exception as e:
            print(f"Google AI error: {e}")
            return None
    
    def _call_anthropic_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call Anthropic API."""
        try:
            api_key = self.ai_models['anthropic']['api_key']
            endpoint = self.ai_models['anthropic']['models'][model]
            
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            
            data = {
                'model': model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=self.api_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'content' in result and len(result['content']) > 0:
                return result['content'][0]['text']
            
            return None
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
    
    def _call_mistral_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call Mistral API."""
        try:
            api_key = self.ai_models['mistral']['api_key']
            endpoint = self.ai_models['mistral']['models'][model]
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            data = {
                'model': model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=self.api_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            
            return None
            
        except Exception as e:
            print(f"Mistral API error: {e}")
            return None
    
    def _call_cohere_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call Cohere API."""
        try:
            api_key = self.ai_models['cohere']['api_key']
            endpoint = self.ai_models['cohere']['models'][model]
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            # Get the last user message
            user_message = ""
            for msg in reversed(messages):
                if msg['role'] == 'user':
                    user_message = msg['content']
                    break
            
            data = {
                'message': user_message,
                'model': model,
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                timeout=self.api_timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'text' in result:
                return result['text']
            
            return None
            
        except Exception as e:
            print(f"Cohere API error: {e}")
            return None
    
    def _call_ai_api(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call the appropriate AI API based on model."""
        # Determine provider from model name
        if model.startswith('gpt-'):
            return self._call_openai_api(model, messages)
        elif model.startswith('gemini-'):
            return self._call_google_api(model, messages)
        elif model.startswith('claude-'):
            return self._call_anthropic_api(model, messages)
        elif model.startswith('mixtral-') or model.startswith('codestral-') or model.startswith('mistral-'):
            return self._call_mistral_api(model, messages)
        elif model.startswith('command-'):
            return self._call_cohere_api(model, messages)
        
        return None
    
    def _call_ai_with_retry(self, model: str, messages: List[Dict[str, str]]) -> Optional[str]:
        """Call AI API with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = self._call_ai_api(model, messages)
                if response:
                    return response
                
                # If no response but no exception, wait and retry
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay)
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(self.retry_delay)
                else:
                    return None
        
        return None
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.conversation_context = {}
    
    def _add_to_history(self, user_input: str, bot_response: str):
        """Add a conversation exchange to history."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'bot': bot_response
        })
        
        # Keep history within limits
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze the sentiment of the input text."""
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'excellent', 'wonderful', 'awesome', 'fantastic', 'happy', 'joy', 'success']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'angry', 'problem', 'issue', 'difficult', 'challenge']
        
        positive_count = sum(word in text_lower for word in positive_words)
        negative_count = sum(word in text_lower for word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from the input text."""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common stop words
        stop_words = {'the', 'and', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}
        
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def _generate_response(self, user_input: str) -> str:
        """Generate an appropriate response based on user input."""
        input_lower = user_input.lower()
        keywords = self._extract_keywords(user_input)
        sentiment = self._analyze_sentiment(user_input)
        
        # Check for greetings
        if any(word in input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.knowledge_base['greetings'])
        
        # Check for thanks
        elif any(word in input_lower for word in ['thank', 'thanks', 'appreciate']):
            return random.choice(self.knowledge_base['thanks'])
        
        # Check for interview-related questions
        elif any(word in keywords for word in ['interview', 'question', 'job', 'position', 'career']):
            if any(word in keywords for word in ['technical', 'code', 'programming', 'development']):
                return random.choice(self.knowledge_base['interview_questions']['technical'])
            elif any(word in keywords for word in ['behavioral', 'team', 'work', 'situation']):
                return random.choice(self.knowledge_base['interview_questions']['behavioral'])
            else:
                return random.choice(self.knowledge_base['interview_questions']['general'])
        
        # Generate response based on sentiment
        if sentiment == 'positive':
            return random.choice(self.knowledge_base['responses']['positive'])
        elif sentiment == 'negative':
            return random.choice(self.knowledge_base['responses']['negative'])
        else:
            return random.choice(self.knowledge_base['responses']['default'])
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response."""
        # Validate and sanitize input
        if not validate_input(user_input):
            return "I'm sorry, I can't process that input."
        
        sanitized_input = sanitize_input(user_input)
        
        # Check if user wants to use AI model
        if any(word in sanitized_input.lower() for word in ['use ai', 'ai model', 'ai response', 'gpt', 'gemini', 'claude']):
            # Try to use AI model
            ai_response = self._generate_ai_response(sanitized_input)
            if ai_response:
                self._add_to_history(user_input, ai_response)
                return ai_response
        
        # Generate response using knowledge base
        response = self._generate_response(sanitized_input)
        
        # Add to conversation history
        self._add_to_history(user_input, response)
        
        return response
    
    def _generate_ai_response(self, user_input: str) -> Optional[str]:
        """Generate response using AI models."""
        # Check if any AI models are available
        if not self.available_models:
            return None
        
        # Prepare conversation context
        messages = []
        
        # Add system message
        messages.append({
            'role': 'system',
            'content': 'You are a professional interview assistant. Provide helpful, concise responses.'
        })
        
        # Add recent conversation history (last 3 exchanges)
        for exchange in self.conversation_history[-3:]:
            messages.append({'role': 'user', 'content': exchange['user']})
            messages.append({'role': 'assistant', 'content': exchange['bot']})
        
        # Add current user input
        messages.append({'role': 'user', 'content': user_input})
        
        # Try default model first
        try:
            response = self._call_ai_with_retry(self.default_model, messages)
            if response:
                return response
        except Exception as e:
            print(f"Default model {self.default_model} failed: {e}")
        
        # Try fallback model
        try:
            response = self._call_ai_with_retry(self.fallback_model, messages)
            if response:
                return response
        except Exception as e:
            print(f"Fallback model {self.fallback_model} failed: {e}")
        
        return None
    
    def get_available_models_info(self) -> Dict[str, Any]:
        """Get information about available AI models."""
        info = {
            'available_models': {},
            'total_models': 0,
            'providers': []
        }
        
        for provider, models in self.available_models.items():
            info['providers'].append(provider)
            info['available_models'][provider] = list(models.keys())
            info['total_models'] += len(models)
        
        # Add model descriptions from knowledge base
        model_descriptions = {}
        for model, description in self.knowledge_base['ai_info']['models'].items():
            if any(model in models for provider, models in self.available_models.items()):
                model_descriptions[model] = description
        
        info['model_descriptions'] = model_descriptions
        
        return info
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation."""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = []
        for i, exchange in enumerate(self.conversation_history, 1):
            summary.append(f"{i}. User: {exchange['user']}")
            summary.append(f"   Bot: {exchange['bot']}")
        
        return "\n".join(summary)