"""
AI-specific helper utilities for the Learning Generator

This module contains utilities specifically designed for working with
AI models, prompt engineering, and response processing.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import hashlib

class PromptBuilder:
    """Build and manage AI prompts for different content types"""
    
    def __init__(self, language: str = "english"):
        self.language = language
        self.templates = self._load_templates()
    
    def build_quiz_prompt(self, topic: str, difficulty: str, questions_count: int, 
                         include_explanations: bool = True) -> str:
        """Build prompt for quiz generation"""
        
        difficulty_descriptions = {
            "beginner": "suitable for beginners with basic knowledge",
            "intermediate": "for learners with some existing knowledge",
            "advanced": "challenging questions for experienced learners",
            "expert": "complex questions for experts in the field"
        }
        
        language_instructions = {
            "italian": "Rispondi in italiano",
            "english": "Respond in English",
            "french": "Répondez en français",
            "spanish": "Responde en español",
            "german": "Antworten Sie auf Deutsch"
        }
        
        prompt = f"""Create a comprehensive educational quiz about "{topic}".

Requirements:
- Language: {language_instructions.get(self.language, "Respond in English")}
- Difficulty level: {difficulty} ({difficulty_descriptions.get(difficulty, "appropriate level")})
- Number of questions: {questions_count}
- Include explanations: {"Yes" if include_explanations else "No"}

Format the response as a JSON object with this structure:
{{
    "quiz": {{
        "title": "Quiz title",
        "description": "Brief description",
        "questions": [
            {{
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": "Explanation of the correct answer"
            }}
        ]
    }}
}}

Guidelines:
1. Questions should be clear and unambiguous
2. Include 4 options per question (A, B, C, D)
3. Ensure only one correct answer per question
4. Vary question types (multiple choice, true/false concepts)
5. {"Include detailed explanations for learning" if include_explanations else "Keep explanations brief"}
6. Difficulty should be consistent throughout
7. Cover different aspects of the topic

Generate the quiz now:"""
        
        return prompt
    
    def build_content_prompt(self, topic: str, difficulty: str, content_type: str = "course") -> str:
        """Build prompt for educational content generation"""
        
        language_instructions = {
            "italian": "Scrivi tutto in italiano",
            "english": "Write everything in English", 
            "french": "Écrivez tout en français",
            "spanish": "Escribe todo en español",
            "german": "Schreiben Sie alles auf Deutsch"
        }
        
        content_types = {
            "course": "a comprehensive course",
            "tutorial": "a step-by-step tutorial",
            "guide": "a practical guide",
            "overview": "an informative overview"
        }
        
        prompt = f"""Create {content_types.get(content_type, "educational content")} about "{topic}".

Requirements:
- Language: {language_instructions.get(self.language, "Write in English")}
- Difficulty level: {difficulty}
- Content type: {content_type}

Format the response as a JSON object with this structure:
{{
    "content": {{
        "title": "Content title",
        "description": "Brief description of what will be covered",
        "learning_objectives": ["Objective 1", "Objective 2", "Objective 3"],
        "sections": [
            {{
                "title": "Section title",
                "content": "Detailed section content with explanations and examples",
                "key_points": ["Key point 1", "Key point 2"],
                "examples": ["Example 1", "Example 2"]
            }}
        ],
        "summary": "Summary of key takeaways",
        "next_steps": "Suggested next learning steps"
    }}
}}

Guidelines:
1. Structure content logically from basic to advanced concepts
2. Include practical examples and real-world applications
3. Use clear, educational language appropriate for the difficulty level
4. Break complex topics into digestible sections
5. Provide actionable learning objectives
6. Include relevant examples and case studies
7. End with a comprehensive summary

Generate the educational content now:"""
        
        return prompt
    
    def build_summary_prompt(self, text: str, max_sentences: int = 3) -> str:
        """Build prompt for text summarization"""
        
        language_instructions = {
            "italian": "Riassumi in italiano",
            "english": "Summarize in English",
            "french": "Résumez en français", 
            "spanish": "Resume en español",
            "german": "Fassen Sie auf Deutsch zusammen"
        }
        
        prompt = f"""{language_instructions.get(self.language, "Summarize in English")} the following text in maximum {max_sentences} sentences.

Focus on:
1. Main concepts and key points
2. Most important information
3. Clear and concise language
4. Educational value

Text to summarize:
{text}

Summary:"""
        
        return prompt
    
    def build_explanation_prompt(self, concept: str, context: str = "") -> str:
        """Build prompt for concept explanation"""
        
        language_instructions = {
            "italian": "Spiega in italiano",
            "english": "Explain in English",
            "french": "Expliquez en français",
            "spanish": "Explica en español", 
            "german": "Erklären Sie auf Deutsch"
        }
        
        context_section = f"\nContext: {context}" if context else ""
        
        prompt = f"""{language_instructions.get(self.language, "Explain in English")} the concept of "{concept}" in a clear and educational way.{context_section}

Please provide:
1. A clear definition
2. Key characteristics or components
3. Practical examples
4. Why it's important to understand
5. Common misconceptions (if any)

Make the explanation accessible and engaging for learners.

Explanation:"""
        
        return prompt
    
    def _load_templates(self) -> Dict[str, str]:
        """Load prompt templates"""
        # In a real implementation, these could be loaded from files
        return {
            "quiz_template": "Create a quiz about {topic}...",
            "content_template": "Create educational content about {topic}...",
            "summary_template": "Summarize the following text...",
        }

class ResponseParser:
    """Parse and validate AI model responses"""
    
    @staticmethod
    def parse_quiz_response(response_text: str) -> Dict[str, Any]:
        """Parse quiz response from AI model"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                # Validate structure
                if ResponseParser._validate_quiz_structure(data):
                    return {
                        'success': True,
                        'data': data,
                        'raw_response': response_text
                    }
            
            # If JSON parsing fails, try to extract text-based quiz
            return ResponseParser._parse_text_quiz(response_text)
            
        except json.JSONDecodeError:
            return ResponseParser._parse_text_quiz(response_text)
    
    @staticmethod
    def parse_content_response(response_text: str) -> Dict[str, Any]:
        """Parse content response from AI model"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                # Validate structure
                if ResponseParser._validate_content_structure(data):
                    return {
                        'success': True,
                        'data': data,
                        'raw_response': response_text
                    }
            
            # If JSON parsing fails, create structured data from text
            return ResponseParser._parse_text_content(response_text)
            
        except json.JSONDecodeError:
            return ResponseParser._parse_text_content(response_text)
    
    @staticmethod
    def extract_key_information(text: str) -> Dict[str, List[str]]:
        """Extract key information from text"""
        info = {
            'concepts': [],
            'examples': [],
            'definitions': [],
            'procedures': []
        }
        
        # Extract concepts (words in quotes or capitalized terms)
        concepts = re.findall(r'"([^"]+)"|\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        info['concepts'] = list(set([c for c in concepts if c and len(c) > 2]))
        
        # Extract examples (phrases after "example:", "for example", etc.)
        example_patterns = [
            r'(?:example|for example|such as):?\s*([^.!?]+)',
            r'(?:e\.g\.|for instance):?\s*([^.!?]+)'
        ]
        
        for pattern in example_patterns:
            examples = re.findall(pattern, text, re.IGNORECASE)
            info['examples'].extend([ex.strip() for ex in examples])
        
        # Extract definitions (phrases like "X is defined as", "X means")
        definition_patterns = [
            r'([^.!?]+)\s+(?:is|are)\s+defined\s+as\s+([^.!?]+)',
            r'([^.!?]+)\s+means\s+([^.!?]+)'
        ]
        
        for pattern in definition_patterns:
            definitions = re.findall(pattern, text, re.IGNORECASE)
            info['definitions'].extend([f"{term}: {definition}" for term, definition in definitions])
        
        return info
    
    @staticmethod
    def _validate_quiz_structure(data: Dict[str, Any]) -> bool:
        """Validate quiz data structure"""
        if 'quiz' not in data:
            return False
        
        quiz = data['quiz']
        
        if 'questions' not in quiz or not isinstance(quiz['questions'], list):
            return False
        
        for question in quiz['questions']:
            if not isinstance(question, dict):
                return False
            
            required_fields = ['question', 'options', 'correct']
            if not all(field in question for field in required_fields):
                return False
            
            if not isinstance(question['options'], list) or len(question['options']) < 2:
                return False
            
            if not isinstance(question['correct'], int) or question['correct'] >= len(question['options']):
                return False
        
        return True
    
    @staticmethod
    def _validate_content_structure(data: Dict[str, Any]) -> bool:
        """Validate content data structure"""
        if 'content' not in data:
            return False
        
        content = data['content']
        
        required_fields = ['title']
        if not all(field in content for field in required_fields):
            return False
        
        if 'sections' in content:
            if not isinstance(content['sections'], list):
                return False
            
            for section in content['sections']:
                if not isinstance(section, dict) or 'title' not in section:
                    return False
        
        return True
    
    @staticmethod
    def _parse_text_quiz(text: str) -> Dict[str, Any]:
        """Parse quiz from plain text format"""
        questions = []
        current_question = None
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for question patterns
            if re.match(r'^\d+\.?\s+', line) or line.endswith('?'):
                if current_question:
                    questions.append(current_question)
                
                current_question = {
                    'question': re.sub(r'^\d+\.?\s*', '', line),
                    'options': [],
                    'correct': 0,
                    'explanation': ''
                }
            
            # Look for option patterns
            elif re.match(r'^[A-Da-d]\)?\.\s+', line) and current_question:
                option_text = re.sub(r'^[A-Da-d]\)?\.\s*', '', line)
                current_question['options'].append(option_text)
        
        if current_question:
            questions.append(current_question)
        
        return {
            'success': len(questions) > 0,
            'data': {
                'quiz': {
                    'title': 'Generated Quiz',
                    'questions': questions
                }
            },
            'raw_response': text
        }
    
    @staticmethod
    def _parse_text_content(text: str) -> Dict[str, Any]:
        """Parse content from plain text format"""
        lines = text.split('\n')
        sections = []
        current_section = None
        title = "Generated Content"
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Look for title (first meaningful line or line with # marker)
            if line.startswith('#') or (not sections and not current_section):
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                else:
                    title = line
                continue
            
            # Look for section headers (lines that are questions or start with ##)
            if line.startswith('##') or line.endswith(':') or re.match(r'^\d+\.', line):
                if current_section:
                    sections.append(current_section)
                
                section_title = line.lstrip('#').rstrip(':').strip()
                section_title = re.sub(r'^\d+\.?\s*', '', section_title)
                
                current_section = {
                    'title': section_title,
                    'content': '',
                    'key_points': []
                }
            
            # Add content to current section
            elif current_section:
                if current_section['content']:
                    current_section['content'] += ' '
                current_section['content'] += line
        
        if current_section:
            sections.append(current_section)
        
        return {
            'success': len(sections) > 0,
            'data': {
                'content': {
                    'title': title,
                    'sections': sections
                }
            },
            'raw_response': text
        }

class AIModelManager:
    """Manage AI model interactions and configurations"""
    
    def __init__(self):
        self.request_history = []
        self.response_cache = {}
    
    def cache_response(self, prompt_hash: str, response: Dict[str, Any]) -> None:
        """Cache AI response for future use"""
        self.response_cache[prompt_hash] = {
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'usage_count': 1
        }
    
    def get_cached_response(self, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached response if available"""
        if prompt_hash in self.response_cache:
            cached = self.response_cache[prompt_hash]
            cached['usage_count'] += 1
            return cached['response']
        return None
    
    def generate_prompt_hash(self, prompt: str) -> str:
        """Generate hash for prompt caching"""
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    
    def log_request(self, prompt: str, response: Dict[str, Any], metadata: Dict[str, Any] = None) -> None:
        """Log AI request for analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt_hash': self.generate_prompt_hash(prompt),
            'prompt_length': len(prompt),
            'response_success': response.get('success', False),
            'metadata': metadata or {}
        }
        
        self.request_history.append(log_entry)
        
        # Keep only recent history to manage memory
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-500:]
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get AI usage statistics"""
        if not self.request_history:
            return {'total_requests': 0}
        
        total_requests = len(self.request_history)
        successful_requests = sum(1 for req in self.request_history if req.get('response_success'))
        
        avg_prompt_length = sum(req['prompt_length'] for req in self.request_history) / total_requests
        
        cache_hits = sum(1 for cached in self.response_cache.values() if cached['usage_count'] > 1)
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'success_rate': successful_requests / total_requests if total_requests > 0 else 0,
            'average_prompt_length': avg_prompt_length,
            'cache_hits': cache_hits,
            'cache_size': len(self.response_cache)
        }
