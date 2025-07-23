"""
Quiz-related data models

This module defines data models for quiz questions, answers, 
quiz structures, and quiz results.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class DifficultyLevel(Enum):
    """Enumeration for difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class QuestionType(Enum):
    """Enumeration for question types"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"
    MATCHING = "matching"
    ORDERING = "ordering"

@dataclass
class Answer:
    """Represents a possible answer option"""
    text: str
    is_correct: bool = False
    explanation: Optional[str] = None
    order: int = 0
    
    def __post_init__(self):
        """Validate answer data after initialization"""
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Answer text must be a non-empty string")
        
        if not isinstance(self.is_correct, bool):
            raise ValueError("is_correct must be a boolean")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert answer to dictionary"""
        return {
            'text': self.text,
            'is_correct': self.is_correct,
            'explanation': self.explanation,
            'order': self.order
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Answer':
        """Create Answer from dictionary"""
        return cls(
            text=data['text'],
            is_correct=data.get('is_correct', False),
            explanation=data.get('explanation'),
            order=data.get('order', 0)
        )

@dataclass
class Question:
    """Represents a quiz question"""
    text: str
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    answers: List[Answer] = field(default_factory=list)
    explanation: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    topic: Optional[str] = None
    points: int = 1
    time_limit: Optional[int] = None  # in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate question data after initialization"""
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Question text must be a non-empty string")
        
        if not isinstance(self.question_type, QuestionType):
            if isinstance(self.question_type, str):
                try:
                    self.question_type = QuestionType(self.question_type)
                except ValueError:
                    raise ValueError(f"Invalid question type: {self.question_type}")
        
        if not isinstance(self.difficulty, DifficultyLevel):
            if isinstance(self.difficulty, str):
                try:
                    self.difficulty = DifficultyLevel(self.difficulty)
                except ValueError:
                    raise ValueError(f"Invalid difficulty level: {self.difficulty}")
        
        if self.points < 0:
            raise ValueError("Points must be non-negative")
        
        if self.time_limit is not None and self.time_limit <= 0:
            raise ValueError("Time limit must be positive")
    
    def add_answer(self, answer: Union[Answer, str], is_correct: bool = False, 
                   explanation: Optional[str] = None) -> None:
        """Add an answer to the question"""
        if isinstance(answer, str):
            answer = Answer(text=answer, is_correct=is_correct, explanation=explanation)
        
        self.answers.append(answer)
    
    def get_correct_answers(self) -> List[Answer]:
        """Get all correct answers"""
        return [answer for answer in self.answers if answer.is_correct]
    
    def get_correct_answer_indices(self) -> List[int]:
        """Get indices of correct answers"""
        return [i for i, answer in enumerate(self.answers) if answer.is_correct]
    
    def is_valid(self) -> bool:
        """Check if question is valid"""
        if not self.answers:
            return False
        
        if self.question_type == QuestionType.MULTIPLE_CHOICE:
            # Should have at least 2 options and exactly 1 correct answer
            correct_count = len(self.get_correct_answers())
            return len(self.answers) >= 2 and correct_count == 1
        
        elif self.question_type == QuestionType.TRUE_FALSE:
            # Should have exactly 2 options and 1 correct answer
            correct_count = len(self.get_correct_answers())
            return len(self.answers) == 2 and correct_count == 1
        
        elif self.question_type == QuestionType.FILL_IN_BLANK:
            # Should have at least 1 correct answer
            return len(self.get_correct_answers()) >= 1
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert question to dictionary"""
        return {
            'text': self.text,
            'question_type': self.question_type.value,
            'answers': [answer.to_dict() for answer in self.answers],
            'explanation': self.explanation,
            'difficulty': self.difficulty.value,
            'topic': self.topic,
            'points': self.points,
            'time_limit': self.time_limit,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """Create Question from dictionary"""
        answers = [Answer.from_dict(answer_data) for answer_data in data.get('answers', [])]
        
        return cls(
            text=data['text'],
            question_type=QuestionType(data.get('question_type', 'multiple_choice')),
            answers=answers,
            explanation=data.get('explanation'),
            difficulty=DifficultyLevel(data.get('difficulty', 'intermediate')),
            topic=data.get('topic'),
            points=data.get('points', 1),
            time_limit=data.get('time_limit'),
            metadata=data.get('metadata', {})
        )

@dataclass
class Quiz:
    """Represents a complete quiz"""
    title: str
    description: Optional[str] = None
    questions: List[Question] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    language: str = "english"
    topic: Optional[str] = None
    time_limit: Optional[int] = None  # in minutes
    passing_score: int = 70  # percentage
    max_attempts: Optional[int] = None
    shuffle_questions: bool = False
    shuffle_answers: bool = False
    show_results_immediately: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate quiz data after initialization"""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Quiz title must be a non-empty string")
        
        if not isinstance(self.difficulty, DifficultyLevel):
            if isinstance(self.difficulty, str):
                try:
                    self.difficulty = DifficultyLevel(self.difficulty)
                except ValueError:
                    raise ValueError(f"Invalid difficulty level: {self.difficulty}")
        
        if self.passing_score < 0 or self.passing_score > 100:
            raise ValueError("Passing score must be between 0 and 100")
        
        if self.time_limit is not None and self.time_limit <= 0:
            raise ValueError("Time limit must be positive")
        
        if self.max_attempts is not None and self.max_attempts <= 0:
            raise ValueError("Max attempts must be positive")
    
    def add_question(self, question: Union[Question, Dict[str, Any]]) -> None:
        """Add a question to the quiz"""
        if isinstance(question, dict):
            question = Question.from_dict(question)
        
        self.questions.append(question)
        self.updated_at = datetime.now()
    
    def remove_question(self, index: int) -> bool:
        """Remove a question by index"""
        if 0 <= index < len(self.questions):
            self.questions.pop(index)
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_total_points(self) -> int:
        """Calculate total points for the quiz"""
        return sum(question.points for question in self.questions)
    
    def get_question_count(self) -> int:
        """Get the number of questions"""
        return len(self.questions)
    
    def get_estimated_duration(self) -> int:
        """Estimate quiz duration in minutes"""
        if self.time_limit:
            return self.time_limit
        
        # Estimate based on question count and complexity
        base_time = len(self.questions) * 1.5  # 1.5 minutes per question
        
        # Adjust for difficulty
        if self.difficulty == DifficultyLevel.ADVANCED:
            base_time *= 1.3
        elif self.difficulty == DifficultyLevel.EXPERT:
            base_time *= 1.5
        
        return max(5, int(base_time))  # Minimum 5 minutes
    
    def is_valid(self) -> bool:
        """Check if quiz is valid"""
        if not self.questions:
            return False
        
        return all(question.is_valid() for question in self.questions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quiz to dictionary"""
        return {
            'title': self.title,
            'description': self.description,
            'questions': [question.to_dict() for question in self.questions],
            'difficulty': self.difficulty.value,
            'language': self.language,
            'topic': self.topic,
            'time_limit': self.time_limit,
            'passing_score': self.passing_score,
            'max_attempts': self.max_attempts,
            'shuffle_questions': self.shuffle_questions,
            'shuffle_answers': self.shuffle_answers,
            'show_results_immediately': self.show_results_immediately,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quiz':
        """Create Quiz from dictionary"""
        questions = [Question.from_dict(q_data) for q_data in data.get('questions', [])]
        
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = data.get('updated_at')
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        return cls(
            title=data['title'],
            description=data.get('description'),
            questions=questions,
            difficulty=DifficultyLevel(data.get('difficulty', 'intermediate')),
            language=data.get('language', 'english'),
            topic=data.get('topic'),
            time_limit=data.get('time_limit'),
            passing_score=data.get('passing_score', 70),
            max_attempts=data.get('max_attempts'),
            shuffle_questions=data.get('shuffle_questions', False),
            shuffle_answers=data.get('shuffle_answers', False),
            show_results_immediately=data.get('show_results_immediately', True),
            created_at=created_at or datetime.now(),
            updated_at=updated_at or datetime.now(),
            metadata=data.get('metadata', {})
        )

@dataclass
class QuizAttempt:
    """Represents a user's attempt at a quiz"""
    user_id: str
    quiz_id: str
    answers: Dict[int, Union[int, List[int], str]]  # question_index -> answer
    start_time: datetime
    end_time: Optional[datetime] = None
    score: Optional[float] = None
    passed: Optional[bool] = None
    time_taken: Optional[int] = None  # in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def submit_answer(self, question_index: int, answer: Union[int, List[int], str]) -> None:
        """Submit an answer for a question"""
        self.answers[question_index] = answer
    
    def complete_attempt(self, quiz: Quiz) -> None:
        """Complete the quiz attempt and calculate score"""
        self.end_time = datetime.now()
        self.time_taken = int((self.end_time - self.start_time).total_seconds())
        
        total_points = 0
        earned_points = 0
        
        for i, question in enumerate(quiz.questions):
            total_points += question.points
            
            if i in self.answers:
                user_answer = self.answers[i]
                correct_indices = question.get_correct_answer_indices()
                
                # Check if answer is correct
                if isinstance(user_answer, int):
                    if user_answer in correct_indices:
                        earned_points += question.points
                elif isinstance(user_answer, list):
                    if set(user_answer) == set(correct_indices):
                        earned_points += question.points
        
        self.score = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.score >= quiz.passing_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert attempt to dictionary"""
        return {
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'answers': self.answers,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'score': self.score,
            'passed': self.passed,
            'time_taken': self.time_taken,
            'metadata': self.metadata
        }

@dataclass
class QuizResult:
    """Aggregated results for a quiz"""
    quiz_id: str
    total_attempts: int = 0
    total_completions: int = 0
    average_score: float = 0.0
    pass_rate: float = 0.0
    average_time: float = 0.0  # in seconds
    difficulty_rating: float = 0.0  # 1-5 scale
    question_analytics: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    def update_from_attempts(self, attempts: List[QuizAttempt]) -> None:
        """Update results from list of attempts"""
        if not attempts:
            return
        
        completed_attempts = [a for a in attempts if a.end_time is not None]
        
        self.total_attempts = len(attempts)
        self.total_completions = len(completed_attempts)
        
        if completed_attempts:
            scores = [a.score for a in completed_attempts if a.score is not None]
            times = [a.time_taken for a in completed_attempts if a.time_taken is not None]
            passes = [a.passed for a in completed_attempts if a.passed is not None]
            
            self.average_score = sum(scores) / len(scores) if scores else 0
            self.average_time = sum(times) / len(times) if times else 0
            self.pass_rate = (sum(passes) / len(passes) * 100) if passes else 0
            
            # Calculate difficulty rating based on average score and time
            if self.average_score > 80:
                self.difficulty_rating = 2.0
            elif self.average_score > 60:
                self.difficulty_rating = 3.0
            elif self.average_score > 40:
                self.difficulty_rating = 4.0
            else:
                self.difficulty_rating = 5.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary"""
        return {
            'quiz_id': self.quiz_id,
            'total_attempts': self.total_attempts,
            'total_completions': self.total_completions,
            'average_score': self.average_score,
            'pass_rate': self.pass_rate,
            'average_time': self.average_time,
            'difficulty_rating': self.difficulty_rating,
            'question_analytics': self.question_analytics
        }
