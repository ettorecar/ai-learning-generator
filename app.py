"""
AI-Powered E-Learning Generator - Main Application

This Flask application serves as the backend API for generating
educational content and quizzes using OpenAI's GPT models.
"""

import sys
import os
import logging
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import openai
from dotenv import load_dotenv
from config import get_config

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Setup CORS
CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})

# Configure OpenAI
openai.api_key = config.OPENAI_API_KEY

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuizGenerator:
    """Handles quiz and course content generation using OpenAI API"""
    
    def __init__(self):
        self.model = config.DEFAULT_MODEL
        self.max_tokens = config.MAX_TOKENS
        self.temperature = config.TEMPERATURE
    
    def generate_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate course content and quiz based on parameters"""
        try:
            topic = params.get('topic', '')
            random_topic = params.get('random_topic', 'false')
            num_questions = params.get('num_of_questions', '1')
            num_replies = params.get('num_of_replies', '2')
            language = params.get('language', 'english')
            
            # Validate parameters
            self._validate_parameters(params)
            
            # Generate image URL
            image_url = self._generate_image(topic, random_topic == 'true')
            
            # Build prompt for content generation
            prompt = self._build_prompt(topic, random_topic, num_questions, num_replies, language)
            
            logger.info(f"Generating content for topic: {topic}, language: {language}")
            
            # For development/testing, return mock data
            if config.DEBUG and os.environ.get('USE_MOCK_DATA', 'false').lower() == 'true':
                return self._get_mock_response(image_url)
            
            # Generate content using OpenAI
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse and return response
            content = response.choices[0].text.strip()
            return self._parse_response(content, image_url)
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
    
    def _validate_parameters(self, params: Dict[str, Any]) -> None:
        """Validate input parameters"""
        num_questions = int(params.get('num_of_questions', 0))
        num_replies = int(params.get('num_of_replies', 0))
        
        if num_questions < 1 or num_questions > config.MAX_QUESTIONS:
            raise ValueError(f"Number of questions must be between 1 and {config.MAX_QUESTIONS}")
        
        if num_replies < 2 or num_replies > config.MAX_ANSWERS:
            raise ValueError(f"Number of replies must be between 2 and {config.MAX_ANSWERS}")
        
        language = params.get('language', '')
        if language not in config.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
    
    def _generate_image(self, topic: str, is_random: bool) -> str:
        """Generate or return image URL"""
        try:
            if not is_random and topic:
                prompt = f"An educational illustration representing: {topic}"
                response = openai.Image.create(
                    prompt=prompt,
                    n=config.IMAGE_COUNT,
                    size=config.IMAGE_SIZE,
                )
                return response["data"][0]["url"]
            else:
                return "images/about_img.jpg"  # Default image
        except Exception as e:
            logger.warning(f"Failed to generate image: {str(e)}")
            return "images/about_img.jpg"  # Fallback to default
    
    def _build_prompt(self, topic: str, random_topic: str, num_questions: str, 
                     num_replies: str, language: str) -> str:
        """Build the prompt for OpenAI"""
        if random_topic == 'true':
            topic = "a random educational topic chosen by ChatGPT"
        
        questions_text = "one question" if num_questions == '1' else f"{num_questions} questions, each"
        
        prompt = f"""Generate a quiz with {questions_text} having {num_replies} different possible answers 
        (numbered with alphabet letters), with only one correct answer (indicate only the letter 
        without replicating the answer content), while the others are incorrect but plausible. 
        Also indicate which is the correct answer. Before the quiz, print a summary of the topic 
        in about 500 words in {language}.

        All results, including topic, summary, questions and answers must be formatted in JSON. 
        The topic to use for questions is: {topic}

        All output should be in language: {language}

        The JSON formatting must follow this example:
        {{
            "topic": "example",
            "sintesi": "Example summary.",
            "questionario": [
                {{
                    "domanda": "Example question?",
                    "risposte": {{
                        "A": "Answer A.",
                        "B": "Answer B."
                    }},
                    "risposta_corretta": "A"
                }}
            ]
        }}"""
        
        return prompt
    
    def _parse_response(self, content: str, image_url: str) -> Dict[str, Any]:
        """Parse OpenAI response and add image URL"""
        try:
            # Try to parse as JSON
            import json
            response_data = json.loads(content)
            response_data["imageUrl"] = image_url
            return response_data
        except json.JSONDecodeError:
            # If parsing fails, return a structured error response
            logger.error("Failed to parse OpenAI response as JSON")
            return {
                "topic": "Error",
                "sintesi": "Failed to generate content. Please try again.",
                "questionario": [],
                "imageUrl": image_url
            }
    
    def _get_mock_response(self, image_url: str) -> Dict[str, Any]:
        """Return mock response for testing"""
        return {
            "topic": "Artificial Intelligence",
            "sintesi": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. AI encompasses various subfields including machine learning, natural language processing, computer vision, and robotics. Modern AI applications range from virtual assistants and recommendation systems to autonomous vehicles and medical diagnosis tools.",
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
            "imageUrl": image_url
        }

# Initialize quiz generator
quiz_generator = QuizGenerator()

@app.route('/')
def root() -> str:
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return jsonify({
        "message": "AI-Powered E-Learning Generator API",
        "version": config.API_VERSION,
        "status": "active"
    })

@app.route("/health")
def health_check() -> Response:
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ai-learning-generator",
        "version": config.API_VERSION
    })

@app.route(f"{config.API_BASE_PATH}/middleware_chatgpt", methods=["GET"])
def request_get() -> Response:
    """Handle GET requests (not allowed)"""
    logger.warning("GET request attempted on POST-only endpoint")
    return jsonify({"error": "GET method not allowed"}), 405

@app.route(f"{config.API_BASE_PATH}/middleware_chatgpt", methods=["POST"])
def request_post() -> Response:
    """Handle POST requests for content generation"""
    try:
        logger.info("POST request received for content generation")
        
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No data provided"}), 400
        
        # Generate content
        result = quiz_generator.generate_content(request_data)
        
        logger.info("Content generated successfully")
        return jsonify(result)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error) -> Response:
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error) -> Response:
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info(f"Starting AI-Learning Generator on {config.HOST}:{config.PORT}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    if not config.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable not set!")
        sys.exit(1)
    
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
