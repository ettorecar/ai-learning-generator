"""
Content-related data models

This module defines data models for educational content, courses,
sections, and learning objectives.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class ContentType(Enum):
    """Enumeration for content types"""
    COURSE = "course"
    TUTORIAL = "tutorial"
    GUIDE = "guide"
    ARTICLE = "article"
    VIDEO_SCRIPT = "video_script"
    PRESENTATION = "presentation"

class ContentFormat(Enum):
    """Enumeration for content formats"""
    MARKDOWN = "markdown"
    HTML = "html"
    PLAIN_TEXT = "plain_text"
    JSON = "json"

class DifficultyLevel(Enum):
    """Enumeration for difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class LearningObjective:
    """Represents a learning objective"""
    text: str
    level: str = "understand"  # remember, understand, apply, analyze, evaluate, create
    measurable: bool = True
    order: int = 0
    
    def __post_init__(self):
        """Validate learning objective after initialization"""
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Learning objective text must be a non-empty string")
        
        valid_levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
        if self.level not in valid_levels:
            raise ValueError(f"Learning level must be one of: {', '.join(valid_levels)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert learning objective to dictionary"""
        return {
            'text': self.text,
            'level': self.level,
            'measurable': self.measurable,
            'order': self.order
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningObjective':
        """Create LearningObjective from dictionary"""
        return cls(
            text=data['text'],
            level=data.get('level', 'understand'),
            measurable=data.get('measurable', True),
            order=data.get('order', 0)
        )

@dataclass
class ContentExample:
    """Represents an example within content"""
    title: str
    description: str
    code: Optional[str] = None
    explanation: Optional[str] = None
    language: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert example to dictionary"""
        return {
            'title': self.title,
            'description': self.description,
            'code': self.code,
            'explanation': self.explanation,
            'language': self.language
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentExample':
        """Create ContentExample from dictionary"""
        return cls(
            title=data['title'],
            description=data['description'],
            code=data.get('code'),
            explanation=data.get('explanation'),
            language=data.get('language')
        )

@dataclass
class Section:
    """Represents a section of educational content"""
    title: str
    content: str
    order: int = 0
    section_type: str = "content"  # content, introduction, summary, exercise
    key_points: List[str] = field(default_factory=list)
    examples: List[ContentExample] = field(default_factory=list)
    estimated_time: Optional[int] = None  # in minutes
    prerequisites: List[str] = field(default_factory=list)
    format: ContentFormat = ContentFormat.MARKDOWN
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate section data after initialization"""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Section title must be a non-empty string")
        
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Section content must be a non-empty string")
        
        if not isinstance(self.format, ContentFormat):
            if isinstance(self.format, str):
                try:
                    self.format = ContentFormat(self.format)
                except ValueError:
                    raise ValueError(f"Invalid content format: {self.format}")
    
    def add_key_point(self, point: str) -> None:
        """Add a key point to the section"""
        if point and point not in self.key_points:
            self.key_points.append(point)
    
    def add_example(self, example: Union[ContentExample, Dict[str, Any]]) -> None:
        """Add an example to the section"""
        if isinstance(example, dict):
            example = ContentExample.from_dict(example)
        
        self.examples.append(example)
    
    def get_word_count(self) -> int:
        """Get estimated word count for the section"""
        return len(self.content.split())
    
    def get_reading_time(self) -> int:
        """Get estimated reading time in minutes"""
        words_per_minute = 200
        word_count = self.get_word_count()
        return max(1, int(word_count / words_per_minute))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert section to dictionary"""
        return {
            'title': self.title,
            'content': self.content,
            'order': self.order,
            'section_type': self.section_type,
            'key_points': self.key_points,
            'examples': [example.to_dict() for example in self.examples],
            'estimated_time': self.estimated_time,
            'prerequisites': self.prerequisites,
            'format': self.format.value,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Section':
        """Create Section from dictionary"""
        examples = [ContentExample.from_dict(ex_data) for ex_data in data.get('examples', [])]
        
        return cls(
            title=data['title'],
            content=data['content'],
            order=data.get('order', 0),
            section_type=data.get('section_type', 'content'),
            key_points=data.get('key_points', []),
            examples=examples,
            estimated_time=data.get('estimated_time'),
            prerequisites=data.get('prerequisites', []),
            format=ContentFormat(data.get('format', 'markdown')),
            metadata=data.get('metadata', {})
        )

@dataclass
class Course:
    """Represents a complete educational course"""
    title: str
    description: str
    content_type: ContentType = ContentType.COURSE
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    language: str = "english"
    topic: str = ""
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    sections: List[Section] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    target_audience: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # in hours
    author: Optional[str] = None
    version: str = "1.0"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate course data after initialization"""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Course title must be a non-empty string")
        
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Course description must be a non-empty string")
        
        if not isinstance(self.content_type, ContentType):
            if isinstance(self.content_type, str):
                try:
                    self.content_type = ContentType(self.content_type)
                except ValueError:
                    raise ValueError(f"Invalid content type: {self.content_type}")
        
        if not isinstance(self.difficulty, DifficultyLevel):
            if isinstance(self.difficulty, str):
                try:
                    self.difficulty = DifficultyLevel(self.difficulty)
                except ValueError:
                    raise ValueError(f"Invalid difficulty level: {self.difficulty}")
    
    def add_learning_objective(self, objective: Union[LearningObjective, str, Dict[str, Any]]) -> None:
        """Add a learning objective to the course"""
        if isinstance(objective, str):
            objective = LearningObjective(text=objective)
        elif isinstance(objective, dict):
            objective = LearningObjective.from_dict(objective)
        
        self.learning_objectives.append(objective)
        self.updated_at = datetime.now()
    
    def add_section(self, section: Union[Section, Dict[str, Any]]) -> None:
        """Add a section to the course"""
        if isinstance(section, dict):
            section = Section.from_dict(section)
        
        # Set section order if not specified
        if section.order == 0:
            section.order = len(self.sections) + 1
        
        self.sections.append(section)
        self.updated_at = datetime.now()
    
    def remove_section(self, index: int) -> bool:
        """Remove a section by index"""
        if 0 <= index < len(self.sections):
            self.sections.pop(index)
            
            # Reorder remaining sections
            for i, section in enumerate(self.sections):
                section.order = i + 1
            
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_total_word_count(self) -> int:
        """Get total word count for all sections"""
        return sum(section.get_word_count() for section in self.sections)
    
    def get_estimated_reading_time(self) -> int:
        """Get estimated reading time in minutes"""
        return sum(section.get_reading_time() for section in self.sections)
    
    def get_section_count(self) -> int:
        """Get the number of sections"""
        return len(self.sections)
    
    def get_learning_objectives_by_level(self, level: str) -> List[LearningObjective]:
        """Get learning objectives filtered by Bloom's taxonomy level"""
        return [obj for obj in self.learning_objectives if obj.level == level]
    
    def calculate_completion_score(self, completed_sections: List[int]) -> float:
        """Calculate completion percentage based on completed sections"""
        if not self.sections:
            return 0.0
        
        return (len(completed_sections) / len(self.sections)) * 100
    
    def get_prerequisites_text(self) -> str:
        """Get formatted prerequisites text"""
        if not self.prerequisites:
            return "No prerequisites required"
        
        return "Prerequisites: " + ", ".join(self.prerequisites)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert course to dictionary"""
        return {
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type.value,
            'difficulty': self.difficulty.value,
            'language': self.language,
            'topic': self.topic,
            'learning_objectives': [obj.to_dict() for obj in self.learning_objectives],
            'sections': [section.to_dict() for section in self.sections],
            'prerequisites': self.prerequisites,
            'target_audience': self.target_audience,
            'estimated_duration': self.estimated_duration,
            'author': self.author,
            'version': self.version,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Course':
        """Create Course from dictionary"""
        objectives = [LearningObjective.from_dict(obj_data) 
                     for obj_data in data.get('learning_objectives', [])]
        
        sections = [Section.from_dict(sec_data) 
                   for sec_data in data.get('sections', [])]
        
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = data.get('updated_at')
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        return cls(
            title=data['title'],
            description=data['description'],
            content_type=ContentType(data.get('content_type', 'course')),
            difficulty=DifficultyLevel(data.get('difficulty', 'intermediate')),
            language=data.get('language', 'english'),
            topic=data.get('topic', ''),
            learning_objectives=objectives,
            sections=sections,
            prerequisites=data.get('prerequisites', []),
            target_audience=data.get('target_audience', []),
            estimated_duration=data.get('estimated_duration'),
            author=data.get('author'),
            version=data.get('version', '1.0'),
            tags=data.get('tags', []),
            created_at=created_at or datetime.now(),
            updated_at=updated_at or datetime.now(),
            metadata=data.get('metadata', {})
        )

@dataclass
class ContentTemplate:
    """Template for generating structured content"""
    name: str
    description: str
    content_type: ContentType
    template_sections: List[Dict[str, Any]] = field(default_factory=list)
    default_objectives: List[str] = field(default_factory=list)
    suggested_tags: List[str] = field(default_factory=list)
    
    def generate_course_structure(self, title: str, topic: str) -> Course:
        """Generate a course structure from the template"""
        course = Course(
            title=title,
            description=f"A comprehensive {self.content_type.value} about {topic}",
            content_type=self.content_type,
            topic=topic,
            tags=self.suggested_tags.copy()
        )
        
        # Add default learning objectives
        for obj_text in self.default_objectives:
            course.add_learning_objective(LearningObjective(text=obj_text))
        
        # Add template sections
        for i, section_template in enumerate(self.template_sections):
            section = Section(
                title=section_template.get('title', f'Section {i+1}'),
                content=section_template.get('content', 'Content to be generated...'),
                order=i + 1,
                section_type=section_template.get('type', 'content')
            )
            course.add_section(section)
        
        return course
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'content_type': self.content_type.value,
            'template_sections': self.template_sections,
            'default_objectives': self.default_objectives,
            'suggested_tags': self.suggested_tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentTemplate':
        """Create ContentTemplate from dictionary"""
        return cls(
            name=data['name'],
            description=data['description'],
            content_type=ContentType(data['content_type']),
            template_sections=data.get('template_sections', []),
            default_objectives=data.get('default_objectives', []),
            suggested_tags=data.get('suggested_tags', [])
        )
