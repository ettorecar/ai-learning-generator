#!/usr/bin/env python3
"""
Quiz Generator CLI Tool

Command-line interface for generating quizzes using the AI Learning Generator.
This script allows batch generation of quizzes from the command line.

Usage:
    python generate_quiz.py --topic "Python Programming" --difficulty beginner --questions 5 --language italian
    python generate_quiz.py --config quiz_config.json
    python generate_quiz.py --batch topics.txt
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ai_helpers import PromptBuilder, ResponseParser
from utils.validation import InputValidator, QuizValidator
from utils.file_operations import FileManager
from models.quiz_models import Quiz, Question, Answer
from config import get_config

class QuizGeneratorCLI:
    """Command-line interface for quiz generation"""
    
    def __init__(self):
        self.config = get_config()
        self.file_manager = FileManager()
        self.prompt_builder = PromptBuilder()
        self.response_parser = ResponseParser()
        
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="Generate educational quizzes using AI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --topic "Machine Learning" --difficulty intermediate --questions 10
  %(prog)s --config config.json --output quiz.json
  %(prog)s --batch topics.txt --format markdown
            """
        )
        
        # Single quiz generation
        parser.add_argument(
            '--topic', '-t',
            type=str,
            help='Topic for the quiz'
        )
        
        parser.add_argument(
            '--difficulty', '-d',
            choices=['beginner', 'intermediate', 'advanced', 'expert'],
            default='intermediate',
            help='Difficulty level (default: intermediate)'
        )
        
        parser.add_argument(
            '--questions', '-q',
            type=int,
            default=5,
            help='Number of questions (default: 5)'
        )
        
        parser.add_argument(
            '--language', '-l',
            choices=['italian', 'english', 'french', 'spanish', 'german'],
            default='english',
            help='Language for the quiz (default: english)'
        )
        
        parser.add_argument(
            '--explanations',
            action='store_true',
            help='Include explanations for answers'
        )
        
        # Configuration file
        parser.add_argument(
            '--config', '-c',
            type=str,
            help='Configuration file (JSON) with quiz parameters'
        )
        
        # Batch processing
        parser.add_argument(
            '--batch', '-b',
            type=str,
            help='Text file with topics for batch generation'
        )
        
        # Output options
        parser.add_argument(
            '--output', '-o',
            type=str,
            help='Output file path'
        )
        
        parser.add_argument(
            '--format', '-f',
            choices=['json', 'markdown', 'txt'],
            default='json',
            help='Output format (default: json)'
        )
        
        # Validation
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate input without generating quiz'
        )
        
        # Verbose output
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        
        return parser.parse_args()
    
    def load_config_file(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def load_batch_topics(self, batch_path: str) -> List[str]:
        """Load topics from batch file"""
        try:
            with open(batch_path, 'r', encoding='utf-8') as f:
                topics = [line.strip() for line in f if line.strip()]
                
            if not topics:
                print(f"Error: No topics found in batch file '{batch_path}'")
                sys.exit(1)
                
            return topics
        except FileNotFoundError:
            print(f"Error: Batch file '{batch_path}' not found")
            sys.exit(1)
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate quiz generation parameters"""
        validation_result = InputValidator.validate_api_request(params)
        
        if not validation_result['valid']:
            print("Validation errors:")
            for error in validation_result['errors']:
                print(f"  - {error}")
            return False
        
        return True
    
    def generate_quiz_from_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quiz from parameters"""
        # Build prompt
        prompt = self.prompt_builder.build_quiz_prompt(
            topic=params['topic'],
            difficulty=params['difficulty'],
            questions_count=params['questions'],
            include_explanations=params.get('includeExplanations', False)
        )
        
        # For CLI demo, we'll create a mock response
        # In real implementation, this would call the AI API
        mock_response = self.create_mock_quiz_response(params)
        
        # Parse response
        parsed_result = self.response_parser.parse_quiz_response(mock_response)
        
        return parsed_result
    
    def create_mock_quiz_response(self, params: Dict[str, Any]) -> str:
        """Create mock quiz response for demonstration"""
        topic = params['topic']
        questions_count = params['questions']
        language = params['language']
        
        if language == 'italian':
            quiz_title = f"Quiz su {topic}"
            sample_question = f"Qual è un concetto importante in {topic}?"
            options = ["Opzione A", "Opzione B", "Opzione C", "Opzione D"]
            explanation = "Spiegazione della risposta corretta"
        else:
            quiz_title = f"Quiz on {topic}"
            sample_question = f"What is an important concept in {topic}?"
            options = ["Option A", "Option B", "Option C", "Option D"]
            explanation = "Explanation of the correct answer"
        
        questions = []
        for i in range(questions_count):
            question = {
                "question": f"{sample_question} (Question {i+1})",
                "options": options,
                "correct": 0,
                "explanation": explanation
            }
            questions.append(question)
        
        quiz_data = {
            "quiz": {
                "title": quiz_title,
                "description": f"Educational quiz about {topic}",
                "questions": questions
            }
        }
        
        return json.dumps(quiz_data, indent=2)
    
    def format_output(self, quiz_data: Dict[str, Any], format_type: str) -> str:
        """Format quiz data for output"""
        if format_type == 'json':
            return json.dumps(quiz_data, indent=2, ensure_ascii=False)
        
        elif format_type == 'markdown':
            return self.format_as_markdown(quiz_data)
        
        elif format_type == 'txt':
            return self.format_as_text(quiz_data)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def format_as_markdown(self, quiz_data: Dict[str, Any]) -> str:
        """Format quiz as Markdown"""
        if 'quiz' not in quiz_data:
            return "# Error: Invalid quiz data"
        
        quiz = quiz_data['quiz']
        markdown = f"# {quiz.get('title', 'Untitled Quiz')}\n\n"
        
        if quiz.get('description'):
            markdown += f"{quiz['description']}\n\n"
        
        for i, question in enumerate(quiz.get('questions', []), 1):
            markdown += f"## Question {i}\n\n"
            markdown += f"{question.get('question', 'No question text')}\n\n"
            
            for j, option in enumerate(question.get('options', []), 1):
                marker = "✓" if j-1 == question.get('correct', 0) else " "
                markdown += f"{j}. [{marker}] {option}\n"
            
            if question.get('explanation'):
                markdown += f"\n**Explanation:** {question['explanation']}\n"
            
            markdown += "\n---\n\n"
        
        return markdown
    
    def format_as_text(self, quiz_data: Dict[str, Any]) -> str:
        """Format quiz as plain text"""
        if 'quiz' not in quiz_data:
            return "Error: Invalid quiz data"
        
        quiz = quiz_data['quiz']
        text = f"{quiz.get('title', 'Untitled Quiz')}\n"
        text += "=" * len(quiz.get('title', 'Untitled Quiz')) + "\n\n"
        
        if quiz.get('description'):
            text += f"{quiz['description']}\n\n"
        
        for i, question in enumerate(quiz.get('questions', []), 1):
            text += f"Question {i}: {question.get('question', 'No question text')}\n\n"
            
            for j, option in enumerate(question.get('options', []), 1):
                marker = "[✓]" if j-1 == question.get('correct', 0) else "[ ]"
                text += f"  {marker} {option}\n"
            
            if question.get('explanation'):
                text += f"\nExplanation: {question['explanation']}\n"
            
            text += "\n" + "-" * 50 + "\n\n"
        
        return text
    
    def save_output(self, content: str, output_path: str) -> None:
        """Save content to file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Quiz saved to: {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
            sys.exit(1)
    
    def run(self) -> None:
        """Main execution method"""
        args = self.parse_arguments()
        
        try:
            # Handle different input modes
            if args.config:
                # Load from configuration file
                config_data = self.load_config_file(args.config)
                quiz_params = config_data
                
            elif args.batch:
                # Batch processing
                topics = self.load_batch_topics(args.batch)
                self.process_batch(topics, args)
                return
                
            else:
                # Single quiz from command line arguments
                if not args.topic:
                    print("Error: Topic is required for single quiz generation")
                    print("Use --help for usage information")
                    sys.exit(1)
                
                quiz_params = {
                    'topic': args.topic,
                    'difficulty': args.difficulty,
                    'questions': args.questions,
                    'language': args.language,
                    'includeExplanations': args.explanations
                }
            
            # Validate parameters
            if args.validate_only:
                if self.validate_parameters(quiz_params):
                    print("✓ Parameters are valid")
                else:
                    print("✗ Parameter validation failed")
                    sys.exit(1)
                return
            
            if not self.validate_parameters(quiz_params):
                sys.exit(1)
            
            # Generate quiz
            if args.verbose:
                print(f"Generating quiz for topic: {quiz_params['topic']}")
                print(f"Difficulty: {quiz_params['difficulty']}")
                print(f"Questions: {quiz_params['questions']}")
                print(f"Language: {quiz_params['language']}")
            
            result = self.generate_quiz_from_params(quiz_params)
            
            if not result['success']:
                print("Error: Failed to generate quiz")
                sys.exit(1)
            
            # Format output
            formatted_output = self.format_output(result['data'], args.format)
            
            # Save or print output
            if args.output:
                self.save_output(formatted_output, args.output)
            else:
                print(formatted_output)
            
            if args.verbose:
                print("✓ Quiz generation completed successfully")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def process_batch(self, topics: List[str], args: argparse.Namespace) -> None:
        """Process multiple topics in batch"""
        print(f"Processing {len(topics)} topics in batch...")
        
        for i, topic in enumerate(topics, 1):
            print(f"\nProcessing {i}/{len(topics)}: {topic}")
            
            quiz_params = {
                'topic': topic,
                'difficulty': args.difficulty,
                'questions': args.questions,
                'language': args.language,
                'includeExplanations': args.explanations
            }
            
            if not self.validate_parameters(quiz_params):
                print(f"Skipping '{topic}' due to validation errors")
                continue
            
            try:
                result = self.generate_quiz_from_params(quiz_params)
                
                if result['success']:
                    # Generate output filename
                    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"quiz_{safe_topic.replace(' ', '_').lower()}.{args.format}"
                    
                    if args.output:
                        output_dir = Path(args.output)
                        output_path = output_dir / filename
                    else:
                        output_path = filename
                    
                    formatted_output = self.format_output(result['data'], args.format)
                    self.save_output(formatted_output, str(output_path))
                    
                else:
                    print(f"Failed to generate quiz for '{topic}'")
                    
            except Exception as e:
                print(f"Error processing '{topic}': {e}")
                continue
        
        print(f"\nBatch processing completed!")

def main():
    """Entry point for the CLI script"""
    cli = QuizGeneratorCLI()
    cli.run()

if __name__ == '__main__':
    main()
