"""
Input validation utilities for AI Learning Generator

This module provides comprehensive validation functions for user inputs,
API parameters, and data integrity checks.
"""

import re
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

class InputValidator:
    """Main input validation class"""
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'italian', 'english', 'french', 'spanish', 'german', 'portuguese'
    }
    
    # Supported difficulty levels
    SUPPORTED_DIFFICULTIES = {
        'beginner', 'intermediate', 'advanced', 'expert'
    }
    
    # Maximum limits
    MAX_TOPIC_LENGTH = 200
    MAX_QUESTIONS = 50
    MAX_ANSWERS_PER_QUESTION = 10
    MIN_QUESTIONS = 1
    MIN_ANSWERS_PER_QUESTION = 2
    
    @classmethod
    def validate_topic(cls, topic: str) -> Dict[str, Any]:
        """Validate topic parameter"""
        result = {'valid': True, 'errors': []}
        
        if not topic:
            result['valid'] = False
            result['errors'].append("Topic cannot be empty")
            return result
        
        if not isinstance(topic, str):
            result['valid'] = False
            result['errors'].append("Topic must be a string")
            return result
        
        topic = topic.strip()
        
        if len(topic) < 3:
            result['valid'] = False
            result['errors'].append("Topic must be at least 3 characters long")
        
        if len(topic) > cls.MAX_TOPIC_LENGTH:
            result['valid'] = False
            result['errors'].append(f"Topic cannot exceed {cls.MAX_TOPIC_LENGTH} characters")
        
        # Check for potentially harmful content
        if cls._contains_harmful_content(topic):
            result['valid'] = False
            result['errors'].append("Topic contains inappropriate content")
        
        result['sanitized_value'] = cls._sanitize_text(topic)
        return result
    
    @classmethod
    def validate_difficulty(cls, difficulty: str) -> Dict[str, Any]:
        """Validate difficulty parameter"""
        result = {'valid': True, 'errors': []}
        
        if not difficulty:
            result['valid'] = False
            result['errors'].append("Difficulty cannot be empty")
            return result
        
        if not isinstance(difficulty, str):
            result['valid'] = False
            result['errors'].append("Difficulty must be a string")
            return result
        
        difficulty_lower = difficulty.lower().strip()
        
        if difficulty_lower not in cls.SUPPORTED_DIFFICULTIES:
            result['valid'] = False
            result['errors'].append(
                f"Difficulty must be one of: {', '.join(cls.SUPPORTED_DIFFICULTIES)}"
            )
        
        result['sanitized_value'] = difficulty_lower
        return result
    
    @classmethod
    def validate_language(cls, language: str) -> Dict[str, Any]:
        """Validate language parameter"""
        result = {'valid': True, 'errors': []}
        
        if not language:
            result['valid'] = False
            result['errors'].append("Language cannot be empty")
            return result
        
        if not isinstance(language, str):
            result['valid'] = False
            result['errors'].append("Language must be a string")
            return result
        
        language_lower = language.lower().strip()
        
        if language_lower not in cls.SUPPORTED_LANGUAGES:
            result['valid'] = False
            result['errors'].append(
                f"Language must be one of: {', '.join(cls.SUPPORTED_LANGUAGES)}"
            )
        
        result['sanitized_value'] = language_lower
        return result
    
    @classmethod
    def validate_questions_count(cls, questions: Union[int, str]) -> Dict[str, Any]:
        """Validate number of questions parameter"""
        result = {'valid': True, 'errors': []}
        
        try:
            questions_int = int(questions)
        except (ValueError, TypeError):
            result['valid'] = False
            result['errors'].append("Questions count must be a valid number")
            return result
        
        if questions_int < cls.MIN_QUESTIONS:
            result['valid'] = False
            result['errors'].append(f"Must have at least {cls.MIN_QUESTIONS} question")
        
        if questions_int > cls.MAX_QUESTIONS:
            result['valid'] = False
            result['errors'].append(f"Cannot exceed {cls.MAX_QUESTIONS} questions")
        
        result['sanitized_value'] = questions_int
        return result
    
    @classmethod
    def validate_api_request(cls, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete API request"""
        result = {
            'valid': True,
            'errors': [],
            'sanitized_data': {}
        }
        
        # Required fields
        required_fields = ['topic', 'difficulty', 'questions', 'language']
        
        for field in required_fields:
            if field not in request_data:
                result['valid'] = False
                result['errors'].append(f"Missing required field: {field}")
        
        if not result['valid']:
            return result
        
        # Validate each field
        validations = [
            ('topic', cls.validate_topic),
            ('difficulty', cls.validate_difficulty),
            ('language', cls.validate_language),
            ('questions', cls.validate_questions_count)
        ]
        
        for field_name, validator in validations:
            field_result = validator(request_data[field_name])
            
            if not field_result['valid']:
                result['valid'] = False
                result['errors'].extend(field_result['errors'])
            else:
                result['sanitized_data'][field_name] = field_result['sanitized_value']
        
        # Validate optional fields
        if 'includeExplanations' in request_data:
            include_explanations = request_data['includeExplanations']
            if isinstance(include_explanations, bool):
                result['sanitized_data']['includeExplanations'] = include_explanations
            else:
                result['sanitized_data']['includeExplanations'] = bool(include_explanations)
        
        return result
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email address format"""
        if not email or not isinstance(email, str):
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email.strip()))
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            return False
        
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(url_pattern, url.strip()))
    
    @classmethod
    def _sanitize_text(cls, text: str) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        
        # Remove potential script tags and other dangerous content
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @classmethod
    def _contains_harmful_content(cls, text: str) -> bool:
        """Check for potentially harmful content"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Simple blacklist of harmful terms
        harmful_terms = [
            'script', 'eval', 'document.', 'window.', 'alert(',
            'prompt(', 'confirm(', 'onclick', 'onerror', 'onload'
        ]
        
        return any(term in text_lower for term in harmful_terms)

class QuizValidator:
    """Specialized validator for quiz content"""
    
    @classmethod
    def validate_quiz_structure(cls, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate quiz data structure"""
        result = {'valid': True, 'errors': []}
        
        # Check required fields
        if 'questions' not in quiz_data:
            result['valid'] = False
            result['errors'].append("Quiz must contain 'questions' field")
            return result
        
        questions = quiz_data['questions']
        
        if not isinstance(questions, list):
            result['valid'] = False
            result['errors'].append("Questions must be a list")
            return result
        
        if not questions:
            result['valid'] = False
            result['errors'].append("Quiz must contain at least one question")
            return result
        
        # Validate each question
        for i, question in enumerate(questions):
            question_result = cls.validate_question_structure(question)
            if not question_result['valid']:
                result['valid'] = False
                for error in question_result['errors']:
                    result['errors'].append(f"Question {i+1}: {error}")
        
        return result
    
    @classmethod
    def validate_question_structure(cls, question: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual question structure"""
        result = {'valid': True, 'errors': []}
        
        # Required fields for a question
        required_fields = ['question', 'options', 'correct']
        
        for field in required_fields:
            if field not in question:
                result['valid'] = False
                result['errors'].append(f"Missing required field: {field}")
        
        if not result['valid']:
            return result
        
        # Validate question text
        if not question['question'] or not isinstance(question['question'], str):
            result['valid'] = False
            result['errors'].append("Question text must be a non-empty string")
        
        # Validate options
        options = question['options']
        if not isinstance(options, list):
            result['valid'] = False
            result['errors'].append("Options must be a list")
        elif len(options) < InputValidator.MIN_ANSWERS_PER_QUESTION:
            result['valid'] = False
            result['errors'].append(f"Must have at least {InputValidator.MIN_ANSWERS_PER_QUESTION} options")
        elif len(options) > InputValidator.MAX_ANSWERS_PER_QUESTION:
            result['valid'] = False
            result['errors'].append(f"Cannot have more than {InputValidator.MAX_ANSWERS_PER_QUESTION} options")
        
        # Validate correct answer index
        correct = question['correct']
        if not isinstance(correct, int):
            result['valid'] = False
            result['errors'].append("Correct answer must be an integer")
        elif correct < 0 or correct >= len(options):
            result['valid'] = False
            result['errors'].append("Correct answer index is out of range")
        
        # Validate explanation (optional)
        if 'explanation' in question and question['explanation']:
            if not isinstance(question['explanation'], str):
                result['valid'] = False
                result['errors'].append("Explanation must be a string")
        
        return result
    
    @classmethod
    def validate_content_structure(cls, content: Dict[str, Any]) -> Dict[str, Any]:
        """Validate course content structure"""
        result = {'valid': True, 'errors': []}
        
        # Check required fields
        if 'title' not in content:
            result['valid'] = False
            result['errors'].append("Content must have a title")
        
        if 'sections' in content:
            sections = content['sections']
            if not isinstance(sections, list):
                result['valid'] = False
                result['errors'].append("Sections must be a list")
            else:
                for i, section in enumerate(sections):
                    if not isinstance(section, dict):
                        result['valid'] = False
                        result['errors'].append(f"Section {i+1} must be a dictionary")
                    elif 'title' not in section or 'content' not in section:
                        result['valid'] = False
                        result['errors'].append(f"Section {i+1} missing title or content")
        
        return result

class SecurityValidator:
    """Security-focused validation functions"""
    
    @classmethod
    def validate_api_key(cls, api_key: str) -> bool:
        """Validate API key format"""
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Basic API key format validation
        # Adjust pattern based on your API key format
        api_key_pattern = r'^[a-zA-Z0-9_-]{20,}$'
        return bool(re.match(api_key_pattern, api_key.strip()))
    
    @classmethod
    def validate_file_upload(cls, filename: str, max_size: int = 10485760) -> Dict[str, Any]:
        """Validate file upload parameters"""
        result = {'valid': True, 'errors': []}
        
        if not filename:
            result['valid'] = False
            result['errors'].append("Filename cannot be empty")
            return result
        
        # Check file extension
        allowed_extensions = {'.txt', '.md', '.json', '.csv'}
        file_ext = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            result['valid'] = False
            result['errors'].append(f"File type not allowed. Allowed: {', '.join(allowed_extensions)}")
        
        # Sanitize filename
        safe_filename = re.sub(r'[^\w\-_\.]', '', filename)
        if safe_filename != filename:
            result['errors'].append("Filename contains invalid characters")
            result['sanitized_filename'] = safe_filename
        
        return result
