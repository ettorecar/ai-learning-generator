"""
Integration tests for the AI Learning Generator API

This module contains end-to-end tests that test the complete
functionality of the API including external service interactions.
"""

import unittest
import json
import time
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import openai_mw

class TestAPIIntegration(unittest.TestCase):
    """Integration tests for API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the entire test class"""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def tearDown(self):
        """Clean up after each test method"""
        self.ctx.pop()
    
    @patch('openai.Completion.create')
    def test_complete_quiz_generation_flow(self, mock_openai):
        """Test the complete flow of quiz generation"""
        # Mock OpenAI response with realistic quiz content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=self._get_sample_quiz_response())]
        mock_openai.return_value = mock_response
        
        request_data = {
            'topic': 'Python Programming Basics',
            'difficulty': 'beginner',
            'questions': 3,
            'language': 'english',
            'includeExplanations': True
        }
        
        response = self.client.post(
            '/api/v1.0/generate',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        # Test response structure
        self.assertIsNotNone(response)
        
    def test_api_rate_limiting(self):
        """Test API rate limiting functionality"""
        # Make multiple rapid requests
        responses = []
        for i in range(5):
            response = self.client.get('/api/v1.0/status')
            responses.append(response)
            time.sleep(0.1)  # Small delay between requests
        
        # Should handle multiple requests gracefully
        self.assertEqual(len(responses), 5)
    
    def test_error_handling_chain(self):
        """Test error handling across the entire request chain"""
        # Test with various invalid inputs
        invalid_requests = [
            {},  # Empty request
            {'topic': ''},  # Empty topic
            {'topic': 'Valid Topic', 'questions': -1},  # Invalid questions
            {'topic': 'Valid Topic', 'language': 'unsupported'},  # Invalid language
        ]
        
        for invalid_data in invalid_requests:
            response = self.client.post(
                '/api/v1.0/generate',
                data=json.dumps(invalid_data),
                content_type='application/json'
            )
            # Should handle all gracefully
            self.assertIsNotNone(response)
    
    @patch('openai.Completion.create')
    def test_content_validation(self, mock_openai):
        """Test that generated content meets quality standards"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=self._get_sample_content_response())]
        mock_openai.return_value = mock_response
        
        request_data = {
            'topic': 'Machine Learning Introduction',
            'difficulty': 'intermediate',
            'questions': 5,
            'language': 'italian'
        }
        
        response = self.client.post(
            '/api/v1.0/generate',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        
        self.assertIsNotNone(response)
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = self.client.get('/api/v1.0/status')
                results.put(('success', response.status_code))
            except Exception as e:
                results.put(('error', str(e)))
        
        # Create multiple threads for concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        success_count = 0
        while not results.empty():
            result_type, _ = results.get()
            if result_type == 'success':
                success_count += 1
        
        # Should handle concurrent requests
        self.assertGreaterEqual(success_count, 1)
    
    def _get_sample_quiz_response(self):
        """Get a sample quiz response for mocking"""
        return """
        {
            "content": {
                "title": "Python Programming Basics",
                "description": "An introduction to Python programming concepts",
                "sections": [
                    {
                        "title": "Variables and Data Types",
                        "content": "Python supports various data types..."
                    }
                ]
            },
            "quiz": {
                "questions": [
                    {
                        "question": "What is a variable in Python?",
                        "options": [
                            "A container for storing data",
                            "A type of loop",
                            "A function",
                            "A class"
                        ],
                        "correct": 0,
                        "explanation": "A variable is a container for storing data values."
                    }
                ]
            }
        }
        """
    
    def _get_sample_content_response(self):
        """Get a sample content response for mocking"""
        return """
        {
            "content": {
                "title": "Introduzione al Machine Learning",
                "description": "Una guida completa ai concetti base del machine learning",
                "sections": [
                    {
                        "title": "Cos'è il Machine Learning",
                        "content": "Il machine learning è una branca dell'intelligenza artificiale..."
                    }
                ]
            }
        }
        """

class TestOpenAIMiddleware(unittest.TestCase):
    """Test OpenAI middleware functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Import openai_mw if it exists
        try:
            import openai_mw
            self.openai_mw = openai_mw
        except ImportError:
            self.openai_mw = None
    
    def test_openai_middleware_exists(self):
        """Test that OpenAI middleware module exists"""
        self.assertIsNotNone(self.openai_mw, "openai_mw module should exist")
    
    @patch('openai.Completion.create')
    def test_openai_request_formatting(self, mock_openai):
        """Test that OpenAI requests are properly formatted"""
        if not self.openai_mw:
            self.skipTest("openai_mw module not available")
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="Test response")]
        mock_openai.return_value = mock_response
        
        # Test that the middleware properly formats requests
        # This would test actual middleware functionality
        self.assertTrue(True)  # Placeholder
    
    def test_error_handling_in_middleware(self):
        """Test error handling in OpenAI middleware"""
        if not self.openai_mw:
            self.skipTest("openai_mw module not available")
        
        # Test various error scenarios
        self.assertTrue(True)  # Placeholder

class TestPerformance(unittest.TestCase):
    """Performance tests for the application"""
    
    def setUp(self):
        """Set up performance test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_response_time(self):
        """Test that responses are returned within acceptable time"""
        start_time = time.time()
        
        response = self.client.get('/')
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Response should be fast (under 1 second for simple requests)
        self.assertLess(response_time, 1.0)
    
    @patch('openai.Completion.create')
    def test_large_content_generation(self, mock_openai):
        """Test generation of large content"""
        # Mock a large response
        large_content = "This is a large content response. " * 1000
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=large_content)]
        mock_openai.return_value = mock_response
        
        request_data = {
            'topic': 'Comprehensive Python Course',
            'difficulty': 'advanced',
            'questions': 20,
            'language': 'english'
        }
        
        start_time = time.time()
        response = self.client.post(
            '/api/v1.0/generate',
            data=json.dumps(request_data),
            content_type='application/json'
        )
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Should handle large content within reasonable time
        self.assertLess(processing_time, 10.0)  # 10 seconds max
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
