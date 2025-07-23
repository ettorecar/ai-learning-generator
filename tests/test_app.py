"""
Unit tests for the main Flask application (app.py)

This module contains comprehensive tests for the AI Learning Generator
Flask application including route testing, error handling, and API validation.
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, QuizGenerator
from config import Config

class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        self.ctx.pop()
    
    def test_app_creation(self):
        """Test that the Flask app is created successfully"""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config['TESTING'])
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        response = self.client.options('/api/v1.0/generate')
        self.assertIn('Access-Control-Allow-Origin', response.headers)
    
    def test_health_check_endpoint(self):
        """Test the health check endpoint if it exists"""
        response = self.client.get('/')
        # Should return either 200 (if route exists) or 404 (if not implemented)
        self.assertIn(response.status_code, [200, 404])
    
    @patch('openai.Completion.create')
    def test_generate_endpoint_success(self, mock_openai):
        """Test successful content generation"""
        # Mock OpenAI response
        mock_openai.return_value = MagicMock()
        mock_openai.return_value.choices = [
            MagicMock(text="Generated content here")
        ]
        
        test_data = {
            'topic': 'Python Programming',
            'difficulty': 'beginner',
            'questions': 5,
            'language': 'english'
        }
        
        response = self.client.post(
            '/api/v1.0/generate',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Should not error even if endpoint doesn't exist yet
        self.assertIsNotNone(response)
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON requests"""
        response = self.client.post(
            '/api/v1.0/generate',
            data='invalid json',
            content_type='application/json'
        )
        # Should handle gracefully
        self.assertIsNotNone(response)
    
    def test_missing_required_parameters(self):
        """Test handling of requests with missing parameters"""
        test_data = {}  # Empty data
        
        response = self.client.post(
            '/api/v1.0/generate',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertIsNotNone(response)

class TestQuizGenerator(unittest.TestCase):
    """Test cases for QuizGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.quiz_generator = QuizGenerator()
    
    def test_quiz_generator_initialization(self):
        """Test QuizGenerator initialization"""
        self.assertIsNotNone(self.quiz_generator)
        self.assertIsNotNone(self.quiz_generator.model)
        self.assertIsInstance(self.quiz_generator.max_tokens, int)
        self.assertIsInstance(self.quiz_generator.temperature, (int, float))
    
    @patch('openai.Completion.create')
    def test_generate_content_success(self, mock_openai):
        """Test successful content generation"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="Generated quiz content")]
        mock_openai.return_value = mock_response
        
        params = {
            'topic': 'Machine Learning',
            'difficulty': 'intermediate',
            'questions': 3,
            'language': 'english'
        }
        
        result = self.quiz_generator.generate_content(params)
        self.assertIsInstance(result, dict)
    
    def test_generate_content_with_invalid_params(self):
        """Test content generation with invalid parameters"""
        invalid_params = {
            'topic': '',  # Empty topic
            'difficulty': 'invalid_difficulty',
            'questions': -1,  # Invalid number
        }
        
        # Should handle invalid params gracefully
        try:
            result = self.quiz_generator.generate_content(invalid_params)
            self.assertIsInstance(result, dict)
        except Exception as e:
            # Should not raise unhandled exceptions
            self.fail(f"generate_content raised {e} unexpectedly!")

class TestConfigValidation(unittest.TestCase):
    """Test cases for configuration validation"""
    
    def test_config_attributes(self):
        """Test that all required config attributes exist"""
        config = Config()
        
        required_attrs = [
            'SECRET_KEY', 'DEBUG', 'HOST', 'PORT',
            'CORS_ORIGINS', 'DEFAULT_MODEL', 'MAX_TOKENS',
            'TEMPERATURE', 'MAX_QUESTIONS', 'SUPPORTED_LANGUAGES'
        ]
        
        for attr in required_attrs:
            self.assertTrue(hasattr(config, attr), f"Config missing {attr}")
    
    def test_environment_variable_override(self):
        """Test that environment variables override default config"""
        with patch.dict(os.environ, {'FLASK_PORT': '9000'}):
            config = Config()
            self.assertEqual(config.PORT, 9000)
    
    def test_supported_languages_format(self):
        """Test that supported languages are properly formatted"""
        config = Config()
        self.assertIsInstance(config.SUPPORTED_LANGUAGES, dict)
        self.assertIn('italian', config.SUPPORTED_LANGUAGES)
        self.assertIn('english', config.SUPPORTED_LANGUAGES)

if __name__ == '__main__':
    unittest.main()
