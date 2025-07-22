"""
AI-Powered E-Learning Generator Configuration

This module contains configuration settings for the application.
Move sensitive settings to environment variables for production.
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Server Configuration
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 8080))
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGIN', 'http://127.0.0.1:5500').split(',')
    
    # API Configuration
    API_VERSION = 'v1.0'
    API_BASE_PATH = f'/api/{API_VERSION}'
    
    # AI Model Configuration
    DEFAULT_MODEL = 'text-davinci-003'
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7
    
    # Image Generation Configuration
    IMAGE_SIZE = '512x512'
    IMAGE_COUNT = 1
    
    # Application Limits
    MAX_QUESTIONS = 50
    MAX_ANSWERS = 10
    MAX_CONTENT_LENGTH = 10000
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'italian': 'Italian',
        'english': 'English',
        'french': 'French',
        'spanish': 'Spanish'
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration mapping
config_map: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    env = env or os.environ.get('FLASK_ENV', 'default')
    return config_map.get(env, DevelopmentConfig)
