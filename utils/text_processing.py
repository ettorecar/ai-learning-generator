"""
Text processing utilities for AI Learning Generator

This module provides text processing functions for cleaning,
formatting, and manipulating educational content and quiz text.
"""

import re
import html
import unicodedata
from typing import List, Dict, Any, Optional
import markdown
from markdownify import markdownify

class TextProcessor:
    """Main text processing class for content manipulation"""
    
    def __init__(self):
        self.markdown_processor = markdown.Markdown(
            extensions=['extra', 'codehilite', 'toc']
        )
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML entities
        text = html.unescape(text)
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract key terms from text content"""
        if not text:
            return []
        
        # Simple keyword extraction using frequency analysis
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'a', 'an', 'il', 'la', 'le', 'lo', 'gli',
            'un', 'una', 'uno', 'del', 'della', 'dei', 'delle', 'che',
            'di', 'da', 'per', 'con', 'su', 'tra', 'fra', 'come', 'quando'
        }
        
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Create a simple summary of the text"""
        if not text:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return '. '.join(sentences) + '.'
        
        # Simple extractive summarization - take first and last sentences,
        # plus one from the middle
        if max_sentences >= 3:
            summary_sentences = [
                sentences[0],
                sentences[len(sentences) // 2],
                sentences[-1]
            ]
        else:
            summary_sentences = sentences[:max_sentences]
        
        return '. '.join(summary_sentences) + '.'
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown text to HTML"""
        return self.markdown_processor.convert(markdown_text)
    
    def html_to_markdown(self, html_text: str) -> str:
        """Convert HTML text to markdown"""
        return markdownify(html_text)
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common words"""
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        
        # Italian indicators
        italian_words = ['il', 'la', 'di', 'che', 'per', 'con', 'del', 'della', 'questo', 'questa']
        italian_count = sum(1 for word in italian_words if word in text_lower)
        
        # English indicators  
        english_words = ['the', 'and', 'of', 'to', 'for', 'with', 'this', 'that', 'from', 'they']
        english_count = sum(1 for word in english_words if word in text_lower)
        
        # French indicators
        french_words = ['le', 'de', 'et', 'un', 'une', 'pour', 'avec', 'dans', 'sur', 'ce']
        french_count = sum(1 for word in french_words if word in text_lower)
        
        if italian_count > english_count and italian_count > french_count:
            return "italian"
        elif french_count > english_count and french_count > italian_count:
            return "french"
        elif english_count > 0:
            return "english"
        
        return "unknown"

class ContentFormatter:
    """Formats content for different output types"""
    
    @staticmethod
    def format_quiz_question(question: Dict[str, Any]) -> str:
        """Format a quiz question for display"""
        formatted = f"**{question.get('question', '')}**\n\n"
        
        options = question.get('options', [])
        for i, option in enumerate(options):
            letter = chr(65 + i)  # A, B, C, D...
            formatted += f"{letter}. {option}\n"
        
        if question.get('explanation'):
            formatted += f"\n*Spiegazione: {question['explanation']}*\n"
        
        return formatted
    
    @staticmethod
    def format_course_content(content: Dict[str, Any]) -> str:
        """Format course content for display"""
        formatted = f"# {content.get('title', 'Untitled')}\n\n"
        
        if content.get('description'):
            formatted += f"{content['description']}\n\n"
        
        sections = content.get('sections', [])
        for section in sections:
            formatted += f"## {section.get('title', 'Untitled Section')}\n\n"
            formatted += f"{section.get('content', '')}\n\n"
        
        return formatted
    
    @staticmethod
    def format_for_api_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """Format data for API JSON response"""
        formatted_data = {
            'success': True,
            'timestamp': ContentFormatter._get_timestamp(),
            'data': data
        }
        
        return formatted_data
    
    @staticmethod
    def format_error_response(error_message: str, error_code: str = "GENERIC_ERROR") -> Dict[str, Any]:
        """Format error response for API"""
        return {
            'success': False,
            'error': {
                'code': error_code,
                'message': error_message,
                'timestamp': ContentFormatter._get_timestamp()
            }
        }
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def format_difficulty_badge(difficulty: str) -> str:
        """Format difficulty level as a badge"""
        difficulty_map = {
            'beginner': '🟢 Principiante',
            'intermediate': '🟡 Intermedio', 
            'advanced': '🔴 Avanzato',
            'expert': '🟣 Esperto'
        }
        
        return difficulty_map.get(difficulty.lower(), f"📝 {difficulty.title()}")
    
    @staticmethod
    def format_question_count(count: int) -> str:
        """Format question count with appropriate singular/plural"""
        if count == 1:
            return "1 domanda"
        else:
            return f"{count} domande"

class MarkdownProcessor:
    """Advanced markdown processing utilities"""
    
    def __init__(self):
        self.processor = TextProcessor()
    
    def extract_headings(self, markdown_text: str) -> List[Dict[str, Any]]:
        """Extract headings from markdown text"""
        headings = []
        lines = markdown_text.split('\n')
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                
                headings.append({
                    'level': level,
                    'title': title,
                    'line_number': line_num + 1
                })
        
        return headings
    
    def generate_table_of_contents(self, markdown_text: str) -> str:
        """Generate table of contents from markdown headings"""
        headings = self.extract_headings(markdown_text)
        
        if not headings:
            return ""
        
        toc = "## Indice\n\n"
        
        for heading in headings:
            indent = "  " * (heading['level'] - 1)
            anchor = heading['title'].lower().replace(' ', '-')
            anchor = re.sub(r'[^\w\-]', '', anchor)
            
            toc += f"{indent}- [{heading['title']}](#{anchor})\n"
        
        return toc + "\n"
    
    def add_code_syntax_highlighting(self, code: str, language: str = "python") -> str:
        """Add syntax highlighting markers to code"""
        return f"```{language}\n{code}\n```"
    
    def create_callout_box(self, content: str, box_type: str = "info") -> str:
        """Create a callout box in markdown"""
        box_types = {
            'info': '💡',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅',
            'tip': '💭'
        }
        
        icon = box_types.get(box_type, '📝')
        return f"> {icon} **{box_type.title()}**\n> \n> {content}\n"
