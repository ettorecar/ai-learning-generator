# REST API Examples - AI Learning Generator
# Esempi di chiamate REST per tutti i servizi esposti

## Sommario
- [Quiz Generation APIs](#quiz-generation-apis)
- [Content Management APIs](#content-management-apis)
- [User Management APIs](#user-management-apis)
- [System APIs](#system-apis)
- [Authentication Examples](#authentication-examples)

---

## Quiz Generation APIs

### 1. Generate Quiz from Text
**Endpoint:** `POST /api/v1/quiz/generate`

```python
import requests
import json

# Basic quiz generation
url = "http://localhost:5000/api/v1/quiz/generate"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

data = {
    "content": """
    Machine Learning is a subset of artificial intelligence that enables computers 
    to learn and make decisions without being explicitly programmed. It uses 
    algorithms to analyze data, identify patterns, and make predictions.
    """,
    "num_questions": 5,
    "question_types": ["multiple_choice", "true_false"],
    "difficulty": "intermediate",
    "language": "en"
}

response = requests.post(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

**Expected Response:**
```json
{
  "quiz_id": "quiz_123456",
  "title": "Machine Learning Basics",
  "questions": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "question": "What is Machine Learning?",
      "options": [
        "A subset of artificial intelligence",
        "A programming language",
        "A database system",
        "A web framework"
      ],
      "correct_answer": 0,
      "explanation": "Machine Learning is indeed a subset of AI..."
    }
  ],
  "metadata": {
    "difficulty": "intermediate",
    "estimated_time": 300,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 2. Generate Quiz from URL
**Endpoint:** `POST /api/v1/quiz/generate-from-url`

```python
# Generate quiz from web content
url = "http://localhost:5000/api/v1/quiz/generate-from-url"

data = {
    "url": "https://example.com/article-about-python",
    "num_questions": 10,
    "question_types": ["multiple_choice", "short_answer"],
    "focus_topics": ["python basics", "data types", "functions"]
}

response = requests.post(url, headers=headers, json=data)
```

### 3. Get Quiz by ID
**Endpoint:** `GET /api/v1/quiz/{quiz_id}`

```python
# Retrieve specific quiz
quiz_id = "quiz_123456"
url = f"http://localhost:5000/api/v1/quiz/{quiz_id}"

response = requests.get(url, headers=headers)
quiz_data = response.json()
```

### 4. Update Quiz
**Endpoint:** `PUT /api/v1/quiz/{quiz_id}`

```python
# Update existing quiz
quiz_id = "quiz_123456"
url = f"http://localhost:5000/api/v1/quiz/{quiz_id}"

update_data = {
    "title": "Updated Machine Learning Quiz",
    "questions": [
        {
            "id": "q1",
            "question": "What is the primary goal of Machine Learning?",
            "options": ["Automation", "Pattern Recognition", "Data Storage", "Web Development"],
            "correct_answer": 1
        }
    ]
}

response = requests.put(url, headers=headers, json=update_data)
```

---

## Content Management APIs

### 5. Upload Content File
**Endpoint:** `POST /api/v1/content/upload`

```python
# Upload file for content processing
url = "http://localhost:5000/api/v1/content/upload"

files = {
    'file': ('document.pdf', open('path/to/document.pdf', 'rb'), 'application/pdf')
}
data = {
    'content_type': 'educational_material',
    'subject': 'computer_science',
    'tags': 'python,programming,basics'
}

response = requests.post(url, headers=headers, files=files, data=data)
print(f"Upload response: {response.json()}")
```

**Expected Response:**
```json
{
  "content_id": "content_789012",
  "filename": "document.pdf",
  "size": 1024000,
  "status": "processed",
  "extracted_text_preview": "Introduction to Python Programming...",
  "suggested_topics": ["variables", "functions", "loops"]
}
```

### 6. Process Text Content
**Endpoint:** `POST /api/v1/content/process`

```python
# Process and analyze text content
url = "http://localhost:5000/api/v1/content/process"

data = {
    "text": """
    Python is a high-level programming language known for its simplicity and readability.
    It supports multiple programming paradigms including procedural, object-oriented,
    and functional programming.
    """,
    "analysis_type": "comprehensive",
    "extract_keywords": True,
    "identify_concepts": True
}

response = requests.post(url, headers=headers, json=data)
analysis = response.json()
```

### 7. Get Content Analytics
**Endpoint:** `GET /api/v1/content/{content_id}/analytics`

```python
# Get detailed analytics for content
content_id = "content_789012"
url = f"http://localhost:5000/api/v1/content/{content_id}/analytics"

params = {
    "include_readability": True,
    "include_complexity": True,
    "include_topics": True
}

response = requests.get(url, headers=headers, params=params)
analytics = response.json()
```

---

## User Management APIs

### 8. Create User
**Endpoint:** `POST /api/v1/users`

```python
# Create new user
url = "http://localhost:5000/api/v1/users"

user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123",
    "profile": {
        "first_name": "John",
        "last_name": "Doe",
        "role": "student",
        "preferences": {
            "language": "en",
            "difficulty_level": "beginner"
        }
    }
}

response = requests.post(url, headers=headers, json=user_data)
user = response.json()
```

### 9. User Authentication
**Endpoint:** `POST /api/v1/auth/login`

```python
# User login
url = "http://localhost:5000/api/v1/auth/login"

credentials = {
    "email": "john@example.com",
    "password": "secure_password_123"
}

response = requests.post(url, json=credentials)
if response.status_code == 200:
    auth_data = response.json()
    token = auth_data["access_token"]
    print(f"Login successful. Token: {token}")
```

### 10. Get User Progress
**Endpoint:** `GET /api/v1/users/{user_id}/progress`

```python
# Get user learning progress
user_id = "user_456789"
url = f"http://localhost:5000/api/v1/users/{user_id}/progress"

response = requests.get(url, headers=headers)
progress = response.json()
```

---

## System APIs

### 11. Health Check
**Endpoint:** `GET /api/v1/health`

```python
# System health check
url = "http://localhost:5000/api/v1/health"

response = requests.get(url)
health_status = response.json()
print(f"System status: {health_status}")
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "openai_api": "healthy",
    "cache": "healthy"
  },
  "uptime": 86400
}
```

### 12. Get API Metrics
**Endpoint:** `GET /api/v1/metrics`

```python
# Get API usage metrics
url = "http://localhost:5000/api/v1/metrics"

response = requests.get(url, headers=headers)
metrics = response.json()
```

### 13. System Configuration
**Endpoint:** `GET /api/v1/config`

```python
# Get system configuration
url = "http://localhost:5000/api/v1/config"

response = requests.get(url, headers=headers)
config = response.json()
```

---

## Advanced Examples

### 14. Batch Quiz Generation
**Endpoint:** `POST /api/v1/quiz/batch-generate`

```python
# Generate multiple quizzes at once
url = "http://localhost:5000/api/v1/quiz/batch-generate"

batch_data = {
    "batch_id": "batch_001",
    "contents": [
        {
            "content": "Python programming basics...",
            "title": "Python Basics Quiz",
            "num_questions": 5
        },
        {
            "content": "JavaScript fundamentals...",
            "title": "JavaScript Quiz",
            "num_questions": 8
        }
    ],
    "common_settings": {
        "difficulty": "intermediate",
        "question_types": ["multiple_choice", "true_false"]
    }
}

response = requests.post(url, headers=headers, json=batch_data)
batch_result = response.json()
```

### 15. Quiz Submission and Scoring
**Endpoint:** `POST /api/v1/quiz/{quiz_id}/submit`

```python
# Submit quiz answers for scoring
quiz_id = "quiz_123456"
url = f"http://localhost:5000/api/v1/quiz/{quiz_id}/submit"

submission = {
    "user_id": "user_456789",
    "answers": {
        "q1": 0,  # Selected option index
        "q2": True,  # Boolean answer
        "q3": "Machine learning is..."  # Text answer
    },
    "time_taken": 420,  # seconds
    "submission_timestamp": "2024-01-15T10:45:00Z"
}

response = requests.post(url, headers=headers, json=submission)
score_result = response.json()
```

**Expected Response:**
```json
{
  "submission_id": "sub_999888",
  "score": 85.5,
  "total_questions": 5,
  "correct_answers": 4,
  "detailed_results": [
    {
      "question_id": "q1",
      "correct": true,
      "user_answer": 0,
      "correct_answer": 0,
      "points": 20
    }
  ],
  "feedback": "Great job! You have a solid understanding of the basics."
}
```

---

## Error Handling Examples

### 16. Handling API Errors

```python
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

def make_api_request(url, method='GET', **kwargs):
    """
    Generic function to handle API requests with proper error handling
    """
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=30, **kwargs)
        elif method.upper() == 'POST':
            response = requests.post(url, timeout=30, **kwargs)
        elif method.upper() == 'PUT':
            response = requests.put(url, timeout=30, **kwargs)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, timeout=30, **kwargs)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        return response.json()
        
    except Timeout:
        print("Request timed out")
        return {"error": "Request timeout"}
    
    except ConnectionError:
        print("Connection error")
        return {"error": "Connection failed"}
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        if response.status_code == 400:
            return {"error": "Bad request", "details": response.json()}
        elif response.status_code == 401:
            return {"error": "Unauthorized"}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded"}
        elif response.status_code == 500:
            return {"error": "Internal server error"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except RequestException as e:
        print(f"Request error: {e}")
        return {"error": "Request failed"}

# Usage example
result = make_api_request(
    "http://localhost:5000/api/v1/quiz/generate",
    method='POST',
    headers=headers,
    json=data
)
```

---

## Rate Limiting and Retry Logic

### 17. Implementing Retry Logic

```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """
    Decorator for implementing exponential backoff retry logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    
                    # Check for rate limiting
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', base_delay))
                        delay = min(retry_after + random.uniform(0, 1), max_delay)
                        print(f"Rate limited. Retrying after {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                    
                    return response
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    print(f"Attempt {attempt + 1} failed. Retrying after {delay:.2f} seconds...")
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=5)
def make_quiz_request(url, data, headers):
    return requests.post(url, headers=headers, json=data)

# Usage
response = make_quiz_request(
    "http://localhost:5000/api/v1/quiz/generate",
    data,
    headers
)
```

---

## Environment Configuration

### 18. Configuration for Different Environments

```python
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class APIConfig:
    base_url: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_environment(cls, env='development'):
        config_map = {
            'development': {
                'base_url': 'http://localhost:5000',
                'api_key': os.getenv('DEV_API_KEY', 'dev-key-123')
            },
            'staging': {
                'base_url': 'https://staging-api.example.com',
                'api_key': os.getenv('STAGING_API_KEY')
            },
            'production': {
                'base_url': 'https://api.example.com',
                'api_key': os.getenv('PROD_API_KEY')
            }
        }
        
        config = config_map.get(env, config_map['development'])
        return cls(**config)

# Usage
config = APIConfig.from_environment('development')
api_client = APIClient(config)
```

---

## Complete Client Class Example

### 19. Full API Client Implementation

```python
class AILearningAPIClient:
    """
    Complete API client for AI Learning Generator
    """
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.api_key}'
        })
    
    def generate_quiz(self, content: str, **kwargs) -> Dict[str, Any]:
        """Generate quiz from text content"""
        data = {
            'content': content,
            'num_questions': kwargs.get('num_questions', 5),
            'question_types': kwargs.get('question_types', ['multiple_choice']),
            'difficulty': kwargs.get('difficulty', 'intermediate')
        }
        
        return self._make_request('POST', '/api/v1/quiz/generate', json=data)
    
    def get_quiz(self, quiz_id: str) -> Dict[str, Any]:
        """Retrieve quiz by ID"""
        return self._make_request('GET', f'/api/v1/quiz/{quiz_id}')
    
    def submit_quiz(self, quiz_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Submit quiz answers"""
        data = {'answers': answers}
        return self._make_request('POST', f'/api/v1/quiz/{quiz_id}/submit', json=data)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Internal method for making HTTP requests"""
        url = f"{self.config.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=self.config.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Usage example
config = APIConfig.from_environment()
client = AILearningAPIClient(config)

# Generate quiz
quiz = client.generate_quiz(
    content="Python is a programming language...",
    num_questions=3,
    difficulty="beginner"
)

print(f"Generated quiz: {quiz}")
```

---

## Testing Examples

### 20. Unit Tests for API Calls

```python
import unittest
from unittest.mock import patch, Mock
import json

class TestAILearningAPI(unittest.TestCase):
    
    def setUp(self):
        self.config = APIConfig(
            base_url="http://localhost:5000",
            api_key="test-key"
        )
        self.client = AILearningAPIClient(self.config)
    
    @patch('requests.Session.request')
    def test_generate_quiz_success(self, mock_request):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "quiz_id": "test_quiz_123",
            "questions": [{"id": "q1", "question": "Test question?"}]
        }
        mock_request.return_value = mock_response
        
        # Test quiz generation
        result = self.client.generate_quiz("Test content")
        
        self.assertEqual(result["quiz_id"], "test_quiz_123")
        mock_request.assert_called_once()
    
    @patch('requests.Session.request')
    def test_api_error_handling(self, mock_request):
        # Mock error response
        mock_request.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        result = self.client.get_quiz("nonexistent_quiz")
        
        self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()
```

---

Questo file fornisce esempi completi e pratici per tutte le chiamate REST del tuo sistema AI Learning Generator. Puoi usarlo come:

1. **Documentazione di riferimento** per sviluppatori
2. **Template per test di integrazione**
3. **Base per client SDK** personalizzati
4. **Guida per frontend developers** che devono integrare le API

Ogni esempio include gestione degli errori, retry logic e best practices per l'integrazione! 🚀
