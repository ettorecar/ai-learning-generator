"""
Unit tests for configuration module (config.py)

This module tests all configuration settings, environment variable handling,
and validation of configuration parameters.
"""

import unittest
import os
import sys
from unittest.mock import patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config, get_config

class TestConfiguration(unittest.TestCase):
    """Test cases for configuration settings"""
    
    def test_default_configuration(self):
        """Test default configuration values"""
        config = Config()
        
        # Test basic configuration
        self.assertIsNotNone(config.SECRET_KEY)
        self.assertIsInstance(config.DEBUG, bool)
        self.assertIsInstance(config.HOST, str)
        self.assertIsInstance(config.PORT, int)
        
        # Test API configuration
        self.assertEqual(config.API_VERSION, 'v1.0')
        self.assertTrue(config.API_BASE_PATH.startswith('/api/'))
        
        # Test AI model configuration
        self.assertIsInstance(config.DEFAULT_MODEL, str)
        self.assertGreater(config.MAX_TOKENS, 0)
        self.assertGreaterEqual(config.TEMPERATURE, 0)
        self.assertLessEqual(config.TEMPERATURE, 2)
    
    def test_environment_variables(self):
        """Test environment variable configuration"""
        test_env = {
            'SECRET_KEY': 'test-secret-key',
            'FLASK_ENV': 'development',
            'FLASK_HOST': '192.168.1.100',
            'FLASK_PORT': '5000',
            'OPENAI_API_KEY': 'test-api-key',
            'CORS_ORIGIN': 'http://localhost:3000,http://localhost:8080'
        }
        
        with patch.dict(os.environ, test_env):
            config = Config()
            
            self.assertEqual(config.SECRET_KEY, 'test-secret-key')
            self.assertTrue(config.DEBUG)  # FLASK_ENV=development
            self.assertEqual(config.HOST, '192.168.1.100')
            self.assertEqual(config.PORT, 5000)
            self.assertEqual(config.OPENAI_API_KEY, 'test-api-key')
            self.assertIn('http://localhost:3000', config.CORS_ORIGINS)
            self.assertIn('http://localhost:8080', config.CORS_ORIGINS)
    
    def test_cors_origins_parsing(self):
        """Test CORS origins string parsing"""
        test_origins = 'http://localhost:3000,https://example.com,http://192.168.1.1:8080'
        
        with patch.dict(os.environ, {'CORS_ORIGIN': test_origins}):
            config = Config()
            
            self.assertEqual(len(config.CORS_ORIGINS), 3)
            self.assertIn('http://localhost:3000', config.CORS_ORIGINS)
            self.assertIn('https://example.com', config.CORS_ORIGINS)
            self.assertIn('http://192.168.1.1:8080', config.CORS_ORIGINS)
    
    def test_application_limits(self):
        """Test application limit configurations"""
        config = Config()
        
        self.assertGreater(config.MAX_QUESTIONS, 0)
        self.assertGreater(config.MAX_ANSWERS, 0)
        self.assertGreater(config.MAX_CONTENT_LENGTH, 0)
        
        # Test reasonable limits
        self.assertLessEqual(config.MAX_QUESTIONS, 100)
        self.assertLessEqual(config.MAX_ANSWERS, 20)
    
    def test_supported_languages(self):
        """Test supported languages configuration"""
        config = Config()
        
        self.assertIsInstance(config.SUPPORTED_LANGUAGES, dict)
        self.assertGreater(len(config.SUPPORTED_LANGUAGES), 0)
        
        # Test that common languages are supported
        expected_languages = ['italian', 'english']
        for lang in expected_languages:
            self.assertIn(lang, config.SUPPORTED_LANGUAGES)
            self.assertIsInstance(config.SUPPORTED_LANGUAGES[lang], str)
    
    def test_image_configuration(self):
        """Test image generation configuration"""
        config = Config()
        
        self.assertIsInstance(config.IMAGE_SIZE, str)
        self.assertIsInstance(config.IMAGE_COUNT, int)
        self.assertGreater(config.IMAGE_COUNT, 0)
        
        # Test valid image size format
        self.assertRegex(config.IMAGE_SIZE, r'^\d+x\d+$')
    
    def test_get_config_function(self):
        """Test the get_config factory function"""
        config = get_config()
        self.assertIsInstance(config, Config)
        
        # Test with environment variable
        with patch.dict(os.environ, {'FLASK_ENV': 'production'}):
            prod_config = get_config()
            self.assertIsInstance(prod_config, Config)

class TestConfigurationValidation(unittest.TestCase):
    """Test cases for configuration validation"""
    
    def test_required_environment_variables(self):
        """Test behavior when required environment variables are missing"""
        # Test when OPENAI_API_KEY is not set
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            self.assertIsNone(config.OPENAI_API_KEY)
    
    def test_invalid_port_handling(self):
        """Test handling of invalid port numbers"""
        with patch.dict(os.environ, {'FLASK_PORT': 'invalid'}):
            try:
                config = Config()
                # Should fall back to default if conversion fails
                self.assertIsInstance(config.PORT, int)
            except ValueError:
                # Or raise appropriate error
                pass
    
    def test_boolean_environment_variables(self):
        """Test boolean environment variable handling"""
        # Test various ways to specify development environment
        dev_values = ['development', 'dev', 'debug']
        
        for value in dev_values:
            with patch.dict(os.environ, {'FLASK_ENV': value}):
                config = Config()
                if value == 'development':
                    self.assertTrue(config.DEBUG)
                else:
                    # Only 'development' should set DEBUG to True
                    self.assertFalse(config.DEBUG)
    
    def test_temperature_bounds(self):
        """Test that temperature is within valid OpenAI bounds"""
        config = Config()
        
        # OpenAI temperature should be between 0 and 2
        self.assertGreaterEqual(config.TEMPERATURE, 0)
        self.assertLessEqual(config.TEMPERATURE, 2)
    
    def test_token_limits(self):
        """Test that token limits are reasonable"""
        config = Config()
        
        # Test reasonable token limits for OpenAI models
        self.assertGreater(config.MAX_TOKENS, 100)  # Minimum for useful responses
        self.assertLess(config.MAX_TOKENS, 4097)    # Maximum for most models

if __name__ == '__main__':
    unittest.main()
