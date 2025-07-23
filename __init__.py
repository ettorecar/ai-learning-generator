"""
AI Learning Generator
====================

An AI-powered educational content generation platform that creates
interactive quizzes, learning materials, and assessments using OpenAI's GPT models.

This package provides:
- Flask web application for interactive quiz generation
- RESTful API for integration with external systems
- CLI tools for batch processing and data management
- Comprehensive data models and utilities
- Testing framework and quality assurance tools

Main Components:
- app.py: Main Flask application
- models/: Data models for quizzes, users, and content
- utils/: Utility functions for text processing and validation
- tests/: Comprehensive test suite
- scripts/: CLI tools for various operations

Usage:
    >>> from ai_learning_generator import create_app
    >>> app = create_app()
    >>> app.run(debug=True)

API Usage:
    >>> from ai_learning_generator.utils.ai_helpers import QuizGenerator
    >>> generator = QuizGenerator()
    >>> quiz = generator.generate_quiz("Machine Learning basics", num_questions=5)

For more information, see the documentation at:
https://ai-learning-generator.readthedocs.io/
"""

__version__ = '1.0.0'
__author__ = 'AI Learning Generator Team'
__email__ = 'contact@ai-learning-generator.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024 AI Learning Generator Team'

# Version information
VERSION = __version__
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Package metadata
PACKAGE_NAME = 'ai-learning-generator'
PACKAGE_DESCRIPTION = 'AI-powered educational content generation platform'
PACKAGE_URL = 'https://github.com/yourusername/ai-learning-generator'

# Import main components for easy access
try:
    from .app import create_app, app
    from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
    from .openai_mw import OpenAIMiddleware
    
    # Import key models
    from .models.quiz_models import Quiz, Question, Answer
    from .models.user_models import User, UserProfile
    from .models.content_models import Course, Lesson, Content
    
    # Import utilities
    from .utils.ai_helpers import QuizGenerator, ContentAnalyzer
    from .utils.text_processing import TextProcessor
    from .utils.validation import InputValidator
    from .utils.helpers import FileManager
    
    __all__ = [
        # Core components
        'create_app', 'app', 'Config', 'OpenAIMiddleware',
        
        # Models
        'Quiz', 'Question', 'Answer', 'User', 'UserProfile',
        'Course', 'Lesson', 'Content',
        
        # Utilities
        'QuizGenerator', 'ContentAnalyzer', 'TextProcessor',
        'InputValidator', 'FileManager',
        
        # Metadata
        '__version__', 'VERSION', 'VERSION_INFO',
        'PACKAGE_NAME', 'PACKAGE_DESCRIPTION', 'PACKAGE_URL',
    ]
    
except ImportError as e:
    # Handle import errors gracefully during development
    import warnings
    warnings.warn(f"Some components could not be imported: {e}")
    
    __all__ = [
        '__version__', 'VERSION', 'VERSION_INFO',
        'PACKAGE_NAME', 'PACKAGE_DESCRIPTION', 'PACKAGE_URL',
    ]

# Configuration for different environments
ENVIRONMENTS = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'default': 'config.Config'
}

# Feature flags
FEATURES = {
    'ai_generation': True,
    'user_authentication': True,
    'rate_limiting': True,
    'caching': True,
    'api_documentation': True,
    'metrics_collection': True,
    'file_uploads': True,
    'email_notifications': False,
    'social_login': False,
    'premium_features': False,
}

# Supported languages and models
SUPPORTED_LANGUAGES = ['en', 'it', 'es', 'fr', 'de']
SUPPORTED_MODELS = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4-turbo-preview',
    'text-davinci-003',
]

# Default configuration values
DEFAULT_CONFIG = {
    'QUESTIONS_PER_QUIZ': 10,
    'MAX_CONTENT_LENGTH': 50000,
    'CACHE_TIMEOUT': 300,
    'RATE_LIMIT_PER_MINUTE': 60,
    'API_VERSION': 'v1',
    'DEFAULT_LANGUAGE': 'en',
    'DEFAULT_MODEL': 'gpt-3.5-turbo',
}

def get_version():
    """Return the package version."""
    return __version__

def get_package_info():
    """Return package information dictionary."""
    return {
        'name': PACKAGE_NAME,
        'version': __version__,
        'description': PACKAGE_DESCRIPTION,
        'author': __author__,
        'email': __email__,
        'license': __license__,
        'url': PACKAGE_URL,
        'copyright': __copyright__,
    }

def check_dependencies():
    """Check if all required dependencies are available."""
    required_packages = [
        'flask', 'openai', 'requests', 'python-dotenv',
        'flask-cors', 'pyyaml', 'pandas'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        raise ImportError(
            f"Missing required packages: {', '.join(missing_packages)}. "
            f"Install them with: pip install {' '.join(missing_packages)}"
        )
    
    return True

def create_sample_app():
    """Create a sample application for testing purposes."""
    try:
        from .app import create_app
        app = create_app('testing')
        return app
    except ImportError:
        raise ImportError("Could not create sample app. Check your installation.")

# Convenience function for quick start
def quick_start(host='localhost', port=5000, debug=True):
    """Quick start function for development."""
    try:
        check_dependencies()
        app = create_sample_app()
        print(f"Starting AI Learning Generator v{__version__}")
        print(f"Server running at http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        print(f"Error starting application: {e}")
        raise

# CLI entry point
def main():
    """Main entry point for CLI usage."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Learning Generator CLI')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', choices=list(ENVIRONMENTS.keys()), 
                       default='development', help='Configuration environment')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        # No arguments provided, show help
        parser.print_help()
        return
    
    try:
        quick_start(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
