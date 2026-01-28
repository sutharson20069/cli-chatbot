"""
Core functionality for the professional chatbot.

This module contains the main chatbot logic, conversation management,
and natural language processing capabilities.
"""

import re
import random
from typing import List, Dict, Optional
from datetime import datetime
from .config import load_config


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
            }
        }
    
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
        # Generate response
        response = self._generate_response(user_input)
        
        # Add to conversation history
        self._add_to_history(user_input, response)
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation."""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = []
        for i, exchange in enumerate(self.conversation_history, 1):
            summary.append(f"{i}. User: {exchange['user']}")
            summary.append(f"   Bot: {exchange['bot']}")
        
        return "\n".join(summary)