"""
OpenAI Middleware for AI Learning Generator

This module provides middleware functionality for handling OpenAI API requests,
response processing, and error handling. It serves as a wrapper around the
OpenAI API to provide additional functionality and reliability.

Legacy Implementation Note:
This file contains the original implementation. For production use,
please use app.py instead which has improved error handling and features.
"""

import sys
import json
import logging
from typing import Dict, Any, Optional, List
from flask_cors import CORS
import openai
import os
from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv
import time
from functools import wraps
import hashlib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

if not openai.api_key:
    logger.error("OPENAI_API_KEY environment variable not set!")
    print("Error: OPENAI_API_KEY environment variable not set!")
    print("Please create a .env file with your OpenAI API key.")
    sys.exit(1)

# Flask app configuration
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Rate limiting and caching
REQUEST_CACHE = {}
RATE_LIMIT_CACHE = {}
MAX_REQUESTS_PER_MINUTE = 60

class OpenAIMiddleware:
    """Middleware class for OpenAI API interactions"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or openai.api_key
        self.request_count = 0
        self.error_count = 0
        
    def rate_limit_decorator(self, func):
        """Decorator for rate limiting API requests"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr if request else 'localhost'
            current_time = int(time.time() / 60)  # Current minute
            
            key = f"{client_ip}_{current_time}"
            
            if key in RATE_LIMIT_CACHE:
                if RATE_LIMIT_CACHE[key] >= MAX_REQUESTS_PER_MINUTE:
                    return self.create_error_response(
                        "Rate limit exceeded", 
                        429,
                        "Too many requests. Please try again later."
                    )
                RATE_LIMIT_CACHE[key] += 1
            else:
                RATE_LIMIT_CACHE[key] = 1
                # Clean old entries
                keys_to_remove = [k for k in RATE_LIMIT_CACHE.keys() 
                                if int(k.split('_')[1]) < current_time - 5]
                for old_key in keys_to_remove:
                    del RATE_LIMIT_CACHE[old_key]
            
            return func(*args, **kwargs)
        return wrapper
    
    def cache_response(self, prompt_hash: str, response: Dict[str, Any]) -> None:
        """Cache API response for reuse"""
        REQUEST_CACHE[prompt_hash] = {
            'response': response,
            'timestamp': time.time(),
            'usage_count': 1
        }
        
        # Clean old cache entries (older than 1 hour)
        current_time = time.time()
        keys_to_remove = [k for k, v in REQUEST_CACHE.items() 
                         if current_time - v['timestamp'] > 3600]
        for old_key in keys_to_remove:
            del REQUEST_CACHE[old_key]
    
    def get_cached_response(self, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached response if available"""
        if prompt_hash in REQUEST_CACHE:
            cached = REQUEST_CACHE[prompt_hash]
            # Check if cache is still valid (1 hour)
            if time.time() - cached['timestamp'] < 3600:
                cached['usage_count'] += 1
                return cached['response']
            else:
                del REQUEST_CACHE[prompt_hash]
        return None
    
    def generate_prompt_hash(self, prompt: str) -> str:
        """Generate hash for prompt caching"""
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]
    
    def create_error_response(self, error: str, status_code: int = 500, 
                            details: str = None) -> Response:
        """Create standardized error response"""
        error_response = {
            'success': False,
            'error': {
                'message': error,
                'code': status_code,
                'details': details,
                'timestamp': time.time()
            }
        }
        
        response = jsonify(error_response)
        response.status_code = status_code
        return response
    
    def validate_request_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate incoming request data"""
        required_fields = ['topic', 'questions', 'language']
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate data types and ranges
        if not isinstance(data['topic'], str) or len(data['topic'].strip()) == 0:
            return False, "Topic must be a non-empty string"
        
        try:
            questions = int(data['questions'])
            if questions < 1 or questions > 50:
                return False, "Number of questions must be between 1 and 50"
        except (ValueError, TypeError):
            return False, "Questions must be a valid number"
        
        valid_languages = ['italian', 'english', 'french', 'spanish', 'german']
        if data['language'] not in valid_languages:
            return False, f"Language must be one of: {', '.join(valid_languages)}"
        
        return True, "Valid"
    
    def build_openai_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for OpenAI API"""
        topic = data['topic']
        questions = data['questions']
        language = data['language']
        difficulty = data.get('difficulty', 'intermediate')
        
        language_map = {
            'italian': 'italiano',
            'english': 'inglese',
            'french': 'francese',
            'spanish': 'spagnolo',
            'german': 'tedesco'
        }
        
        lang_instruction = language_map.get(language, 'inglese')
        
        prompt = f"""Genera un quiz educativo sull'argomento "{topic}" con le seguenti specifiche:

- Numero di domande: {questions}
- Livello di difficoltà: {difficulty}
- Lingua: {lang_instruction}
- 4 opzioni di risposta per ogni domanda (A, B, C, D)
- Solo una risposta corretta per domanda
- Includi spiegazioni per ogni risposta corretta

Formato di output richiesto (JSON):
{{
    "topic": "{topic}",
    "sintesi": "Breve sintesi dell'argomento in circa 300 parole",
    "questionario": [
        {{
            "domanda": "Testo della domanda",
            "risposte": {{
                "A": "Prima opzione",
                "B": "Seconda opzione", 
                "C": "Terza opzione",
                "D": "Quarta opzione"
            }},
            "risposta_corretta": "A",
            "spiegazione": "Spiegazione della risposta corretta"
        }}
    ],
    "imageUrl": "https://placeholder-image-url.com/quiz-image.jpg"
}}

Genera il quiz ora:"""
        
        return prompt
    
    def call_openai_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to OpenAI"""
        try:
            self.request_count += 1
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            return {
                'success': True,
                'content': response.choices[0].text.strip(),
                'usage': response.usage._asdict() if hasattr(response, 'usage') else {}
            }
            
        except openai.error.RateLimitError:
            self.error_count += 1
            logger.error("OpenAI rate limit exceeded")
            return {
                'success': False,
                'error': 'Rate limit exceeded',
                'error_type': 'rate_limit'
            }
            
        except openai.error.AuthenticationError:
            self.error_count += 1
            logger.error("OpenAI authentication failed")
            return {
                'success': False,
                'error': 'Authentication failed',
                'error_type': 'authentication'
            }
            
        except openai.error.APIError as e:
            self.error_count += 1
            logger.error(f"OpenAI API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'api_error'
            }
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Unexpected error calling OpenAI: {e}")
            return {
                'success': False,
                'error': 'Internal server error',
                'error_type': 'internal_error'
            }
    
    def process_openai_response(self, raw_response: str) -> Dict[str, Any]:
        """Process and validate OpenAI response"""
        try:
            # Try to extract JSON from response
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return {
                    'success': False,
                    'error': 'No valid JSON found in response'
                }
            
            json_str = raw_response[json_start:json_end]
            parsed_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['topic', 'sintesi', 'questionario']
            for field in required_fields:
                if field not in parsed_data:
                    return {
                        'success': False,
                        'error': f'Missing required field in response: {field}'
                    }
            
            # Validate questionario structure
            if not isinstance(parsed_data['questionario'], list):
                return {
                    'success': False,
                    'error': 'Questionario must be a list'
                }
            
            for i, question in enumerate(parsed_data['questionario']):
                required_q_fields = ['domanda', 'risposte', 'risposta_corretta']
                for field in required_q_fields:
                    if field not in question:
                        return {
                            'success': False,
                            'error': f'Missing field {field} in question {i+1}'
                        }
            
            return {
                'success': True,
                'data': parsed_data
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {
                'success': False,
                'error': 'Invalid JSON in response'
            }
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            return {
                'success': False,
                'error': 'Error processing response'
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get middleware statistics"""
        return {
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'success_rate': ((self.request_count - self.error_count) / max(self.request_count, 1)) * 100,
            'cache_size': len(REQUEST_CACHE),
            'cache_entries': [{
                'hash': k[:8] + '...',
                'usage_count': v['usage_count'],
                'age_minutes': int((time.time() - v['timestamp']) / 60)
            } for k, v in REQUEST_CACHE.items()]
        }

# Global middleware instance
middleware = OpenAIMiddleware()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    try:
        stats = middleware.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return middleware.create_error_response("Error retrieving statistics")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    })

@app.route('/api/generate', methods=['POST'])
@middleware.rate_limit_decorator
def generate_quiz():
    """Main endpoint for quiz generation"""
    try:
        # Get request data
        if not request.is_json:
            return middleware.create_error_response(
                "Content-Type must be application/json", 400
            )
        
        data = request.get_json()
        
        # Validate request data
        is_valid, validation_message = middleware.validate_request_data(data)
        if not is_valid:
            return middleware.create_error_response(validation_message, 400)
        
        # Build prompt
        prompt = middleware.build_openai_prompt(data)
        prompt_hash = middleware.generate_prompt_hash(prompt)
        
        # Check cache first
        cached_response = middleware.get_cached_response(prompt_hash)
        if cached_response:
            logger.info(f"Returning cached response for hash: {prompt_hash[:8]}")
            return jsonify(cached_response)
        
        # Call OpenAI API
        api_response = middleware.call_openai_api(prompt)
        
        if not api_response['success']:
            return middleware.create_error_response(
                api_response['error'],
                429 if api_response.get('error_type') == 'rate_limit' else 500
            )
        
        # Process response
        processed_response = middleware.process_openai_response(api_response['content'])
        
        if not processed_response['success']:
            return middleware.create_error_response(processed_response['error'])
        
        # Prepare final response
        final_response = {
            'success': True,
            'data': processed_response['data'],
            'metadata': {
                'generated_at': time.time(),
                'prompt_hash': prompt_hash,
                'from_cache': False,
                'usage': api_response.get('usage', {})
            }
        }
        
        # Cache the response
        middleware.cache_response(prompt_hash, final_response)
        
        logger.info(f"Generated new quiz for topic: {data['topic']}")
        return jsonify(final_response)
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_quiz: {e}")
        return middleware.create_error_response("Internal server error")

# Legacy endpoint for backward compatibility
@app.route('/generate', methods=['POST'])
def legacy_generate():
    """Legacy endpoint - redirects to new API"""
    return generate_quiz()

if __name__ == '__main__':
    logger.info("Starting OpenAI Middleware server...")
    print("OpenAI Middleware - AI Learning Generator")
    print("Script: " + sys.argv[0] + " started")
    print("Server running on http://127.0.0.1:8080")
    
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )



# response = openai.ChatCompletion.create(model="gpt-4",  messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ])
# print(response)


@app.route('/')
def root():
    print('call root')
    return ('flask api root execute. Nothing to display.')



@app.route("/api/v.1.0/middleware_chatgpt", methods=["GET"])
def request_get():
    print("START get request")
    return ("get request not allowed")


@app.route("/api/v.1.0/middleware_chatgpt", methods=["POST"])
def request_post():
    print("post request")
    isFake = True


    request_data = request.get_json()
    topic = request_data['topic']
    random_topic = request_data['random_topic']
    num_of_questions = request_data['num_of_questions']
    num_of_replies = request_data['num_of_replies']
    language = request_data['language']

    if isFake: 
        return (' { "topic": "Phishing", "sintesi": "Il phishing è una tecnica di attacco informatico che mira a ottenere informazioni personali come password, numero di carte di credito e altre informazioni private.", "questionario": [ { "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" }, { "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" },{ "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" },{ "domanda": "Quale delle seguenti azioni NON rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire una password complessa nella pagina di accesso." }, "risposta_corretta": "B" } ], "imageUrl": "images/about_img.jpg" }')

    if (random_topic != "true"): 
        PROMPT = "un'immagine che rappresenta: "+ topic
        responseImage = openai.Image.create(
            prompt = PROMPT,
            n = 1,
            size = "512x512",
        )
        responseImageUrl = responseImage["data"][0]["url"]
    else:
        responseImageUrl = "images/about_img.jpg" #... about image
        topic = "un argomento a piacere scelto da ChatGPT"


    if (num_of_questions == '1'):
        num_of_questions = " una domanda"
    else:
        num_of_questions = num_of_questions + " domande, ognuna "
    

    prompt = "Genera un quiz avente " + num_of_questions + " con " + num_of_replies + " possibili diverse risposte (numerandole con le lettere dell'alfabeto), \
    di cui solo una è corretta (indica solo la lettera relativa alla risposta senza replicare il contenuto della risposta), mentre le altre sbagliate ma plausibili; \
    inoltre indicami quale è la risposta corretta. Prima del questionario stampa anche una sintesi dell'argomento in circa 500 parole in lingua " + language + " .\
    Tutto il risultato, compreso topic, sintesi, domanda e risposte deve essere formattato in json. L'argomento da utilizzare per le domande è il seguente: " + topic + "\
    ,tutto questo ouput sempre in lingua: "+ language +  '.La formattazione del json deve rispettare il seguente esempio { "topic": "esempio", "sintesi": "Esempio.", "questionario": [ { "domanda": "Esempio?", "risposte": { "A": "Esempio.", "B": "Esempio." }, "risposta_corretta": "A" } ] }\
    . Infine accoda sempre allo stesso json anche un attributo imageUrl:'+ responseImageUrl
    print("prompt:" + prompt)
    if(isFake == False):
        gtp_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        ) 

    text_response = str(gtp_response.choices[0].text)
    print(text_response)
    return text_response    
    
  
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)


