"""
Data models for AI Learning Generator

This package contains data model classes that define the structure
and validation for various entities in the application.
"""

from .quiz_models import Quiz, Question, Answer, QuizResult
from .content_models import Course, Section, LearningObjective
from .user_models import User, UserProfile, LearningProgress
from .api_models import APIRequest, APIResponse, ErrorResponse

__all__ = [
    'Quiz',
    'Question', 
    'Answer',
    'QuizResult',
    'Course',
    'Section',
    'LearningObjective',
    'User',
    'UserProfile',
    'LearningProgress',
    'APIRequest',
    'APIResponse', 
    'ErrorResponse'
]

__version__ = '1.0.0'
