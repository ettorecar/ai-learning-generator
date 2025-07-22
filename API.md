# API Documentation

This document describes the REST API endpoints for the AI-Powered E-Learning Generator.

## Base URL

```
http://localhost:8080/api/v1.0
```

## Authentication

Currently, the API doesn't require authentication. In production, consider implementing API key authentication or OAuth.

## Endpoints

### Health Check

Check if the API service is running.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-learning-generator",
  "version": "v1.0"
}
```

### Generate Course Content and Quiz

Generate educational content and quiz based on the provided parameters.

```http
POST /api/v1.0/middleware_chatgpt
```

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "topic": "Artificial Intelligence",
  "random_topic": "false",
  "num_of_questions": "3",
  "num_of_replies": "4",
  "language": "english"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | Yes* | The topic for course generation |
| `random_topic` | string | No | "true" for AI-chosen topic, "false" otherwise |
| `num_of_questions` | string | Yes | Number of quiz questions (1-50) |
| `num_of_replies` | string | Yes | Number of answer options per question (2-10) |
| `language` | string | Yes | Language for content ("italian", "english", "french", "spanish") |

*Required when `random_topic` is "false"

**Response:**
```json
{
  "topic": "Artificial Intelligence",
  "sintesi": "Artificial Intelligence (AI) is a branch of computer science...",
  "questionario": [
    {
      "domanda": "What is the primary goal of Artificial Intelligence?",
      "risposte": {
        "A": "To replace human workers completely",
        "B": "To create machines that can perform tasks requiring human intelligence",
        "C": "To make computers faster",
        "D": "To reduce electricity consumption"
      },
      "risposta_corretta": "B"
    }
  ],
  "imageUrl": "https://example.com/generated-image.jpg"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `topic` | string | The topic title |
| `sintesi` | string | Course summary/content (~500 words) |
| `questionario` | array | Array of quiz questions |
| `questionario[].domanda` | string | Question text |
| `questionario[].risposte` | object | Answer options (A, B, C, etc.) |
| `questionario[].risposta_corretta` | string | Correct answer letter |
| `imageUrl` | string | URL to topic-related image |

## Error Responses

### 400 Bad Request
```json
{
  "error": "Number of questions must be between 1 and 50"
}
```

### 405 Method Not Allowed
```json
{
  "error": "GET method not allowed"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider implementing rate limiting to prevent API abuse.

## CORS

The API supports Cross-Origin Resource Sharing (CORS). The allowed origins can be configured via environment variables.

## Example Usage

### cURL Example

```bash
curl -X POST http://localhost:8080/api/v1.0/middleware_chatgpt \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Machine Learning",
    "random_topic": "false",
    "num_of_questions": "2",
    "num_of_replies": "3",
    "language": "english"
  }'
```

### JavaScript Example

```javascript
const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        topic: 'Machine Learning',
        random_topic: 'false',
        num_of_questions: '2',
        num_of_replies: '3',
        language: 'english'
    })
};

fetch('http://localhost:8080/api/v1.0/middleware_chatgpt', requestOptions)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

### Python Example

```python
import requests
import json

url = 'http://localhost:8080/api/v1.0/middleware_chatgpt'
data = {
    'topic': 'Machine Learning',
    'random_topic': 'false',
    'num_of_questions': '2',
    'num_of_replies': '3',
    'language': 'english'
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

## Content Generation Details

### AI Models Used

- **Text Generation**: OpenAI GPT-3 (text-davinci-003)
- **Image Generation**: OpenAI DALL-E

### Content Quality

- Course summaries are approximately 500 words
- Questions are generated with plausible incorrect answers
- Content is generated in the specified language
- Images are topically relevant to the subject matter

### Limitations

- Content quality depends on OpenAI API availability and limits
- Generated content should be reviewed for accuracy
- Image generation may fail; fallback images are provided
- Maximum token limits apply to generated content

## Environment Configuration

The API behavior can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Required: Your OpenAI API key |
| `FLASK_ENV` | development | Environment mode |
| `FLASK_PORT` | 8080 | Server port |
| `CORS_ORIGIN` | http://127.0.0.1:5500 | Allowed CORS origins |
| `USE_MOCK_DATA` | false | Use mock data instead of API calls |

## Development and Testing

For development and testing purposes, you can enable mock data by setting:

```bash
export USE_MOCK_DATA=true
```

This will return sample data without making actual OpenAI API calls, useful for:
- Testing the frontend without API costs
- Development when API keys are not available
- Debugging API integration issues
