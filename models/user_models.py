"""
User-related data models

This module defines data models for users, user profiles,
and learning progress tracking.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    """Enumeration for user roles"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    GUEST = "guest"

class SkillLevel(Enum):
    """Enumeration for skill levels"""
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class UserPreferences:
    """User preferences for learning experience"""
    language: str = "english"
    difficulty_preference: str = "intermediate"
    content_format: str = "mixed"  # text, video, interactive, mixed
    learning_pace: str = "normal"  # slow, normal, fast
    notification_enabled: bool = True
    theme: str = "light"  # light, dark, auto
    font_size: str = "medium"  # small, medium, large
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert preferences to dictionary"""
        return {
            'language': self.language,
            'difficulty_preference': self.difficulty_preference,
            'content_format': self.content_format,
            'learning_pace': self.learning_pace,
            'notification_enabled': self.notification_enabled,
            'theme': self.theme,
            'font_size': self.font_size
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create UserPreferences from dictionary"""
        return cls(
            language=data.get('language', 'english'),
            difficulty_preference=data.get('difficulty_preference', 'intermediate'),
            content_format=data.get('content_format', 'mixed'),
            learning_pace=data.get('learning_pace', 'normal'),
            notification_enabled=data.get('notification_enabled', True),
            theme=data.get('theme', 'light'),
            font_size=data.get('font_size', 'medium')
        )

@dataclass
class LearningGoal:
    """Represents a user's learning goal"""
    title: str
    description: str
    target_completion_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high
    category: Optional[str] = None
    progress: float = 0.0  # 0-100 percentage
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate learning goal after initialization"""
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Goal title must be a non-empty string")
        
        if self.progress < 0 or self.progress > 100:
            raise ValueError("Progress must be between 0 and 100")
        
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    
    def update_progress(self, progress: float) -> None:
        """Update goal progress"""
        self.progress = max(0, min(100, progress))
        if self.progress >= 100:
            self.is_completed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary"""
        return {
            'title': self.title,
            'description': self.description,
            'target_completion_date': self.target_completion_date.isoformat() if self.target_completion_date else None,
            'priority': self.priority,
            'category': self.category,
            'progress': self.progress,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningGoal':
        """Create LearningGoal from dictionary"""
        target_date = data.get('target_completion_date')
        if isinstance(target_date, str):
            target_date = datetime.fromisoformat(target_date)
        
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            title=data['title'],
            description=data['description'],
            target_completion_date=target_date,
            priority=data.get('priority', 'medium'),
            category=data.get('category'),
            progress=data.get('progress', 0.0),
            is_completed=data.get('is_completed', False),
            created_at=created_at or datetime.now()
        )

@dataclass
class UserProfile:
    """Extended user profile information"""
    bio: Optional[str] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    interests: List[str] = field(default_factory=list)
    skills: Dict[str, SkillLevel] = field(default_factory=dict)
    learning_goals: List[LearningGoal] = field(default_factory=list)
    preferences: UserPreferences = field(default_factory=UserPreferences)
    avatar_url: Optional[str] = None
    timezone: str = "UTC"
    
    def add_skill(self, skill_name: str, level: Union[SkillLevel, str]) -> None:
        """Add or update a skill"""
        if isinstance(level, str):
            level = SkillLevel(level)
        
        self.skills[skill_name] = level
    
    def add_learning_goal(self, goal: Union[LearningGoal, Dict[str, Any]]) -> None:
        """Add a learning goal"""
        if isinstance(goal, dict):
            goal = LearningGoal.from_dict(goal)
        
        self.learning_goals.append(goal)
    
    def get_completed_goals(self) -> List[LearningGoal]:
        """Get completed learning goals"""
        return [goal for goal in self.learning_goals if goal.is_completed]
    
    def get_active_goals(self) -> List[LearningGoal]:
        """Get active (non-completed) learning goals"""
        return [goal for goal in self.learning_goals if not goal.is_completed]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary"""
        return {
            'bio': self.bio,
            'occupation': self.occupation,
            'education_level': self.education_level,
            'interests': self.interests,
            'skills': {skill: level.value for skill, level in self.skills.items()},
            'learning_goals': [goal.to_dict() for goal in self.learning_goals],
            'preferences': self.preferences.to_dict(),
            'avatar_url': self.avatar_url,
            'timezone': self.timezone
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create UserProfile from dictionary"""
        skills = {}
        for skill, level in data.get('skills', {}).items():
            skills[skill] = SkillLevel(level)
        
        goals = [LearningGoal.from_dict(goal_data) 
                for goal_data in data.get('learning_goals', [])]
        
        preferences = UserPreferences.from_dict(data.get('preferences', {}))
        
        return cls(
            bio=data.get('bio'),
            occupation=data.get('occupation'),
            education_level=data.get('education_level'),
            interests=data.get('interests', []),
            skills=skills,
            learning_goals=goals,
            preferences=preferences,
            avatar_url=data.get('avatar_url'),
            timezone=data.get('timezone', 'UTC')
        )

@dataclass
class User:
    """Represents a user of the learning system"""
    user_id: str
    username: str
    email: str
    role: UserRole = UserRole.STUDENT
    profile: UserProfile = field(default_factory=UserProfile)
    is_active: bool = True
    email_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate user data after initialization"""
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("User ID must be a non-empty string")
        
        if not self.username or not isinstance(self.username, str):
            raise ValueError("Username must be a non-empty string")
        
        if not self.email or not isinstance(self.email, str):
            raise ValueError("Email must be a non-empty string")
        
        if not isinstance(self.role, UserRole):
            if isinstance(self.role, str):
                try:
                    self.role = UserRole(self.role)
                except ValueError:
                    raise ValueError(f"Invalid user role: {self.role}")
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()
    
    def update_profile(self, profile_data: Dict[str, Any]) -> None:
        """Update user profile"""
        # Update profile fields
        for key, value in profile_data.items():
            if hasattr(self.profile, key):
                setattr(self.profile, key, value)
        
        self.updated_at = datetime.now()
    
    def add_interest(self, interest: str) -> None:
        """Add an interest to user profile"""
        if interest and interest not in self.profile.interests:
            self.profile.interests.append(interest)
            self.updated_at = datetime.now()
    
    def remove_interest(self, interest: str) -> bool:
        """Remove an interest from user profile"""
        if interest in self.profile.interests:
            self.profile.interests.remove(interest)
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_skill_level(self, skill: str) -> Optional[SkillLevel]:
        """Get user's skill level for a specific skill"""
        return self.profile.skills.get(skill)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        # Simple role-based permissions
        admin_permissions = ["manage_users", "manage_content", "view_analytics"]
        instructor_permissions = ["create_content", "manage_quizzes", "view_student_progress"]
        student_permissions = ["take_quizzes", "view_content", "track_progress"]
        
        if self.role == UserRole.ADMIN:
            return permission in admin_permissions + instructor_permissions + student_permissions
        elif self.role == UserRole.INSTRUCTOR:
            return permission in instructor_permissions + student_permissions
        elif self.role == UserRole.STUDENT:
            return permission in student_permissions
        
        return False
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary"""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role.value,
            'profile': self.profile.to_dict(),
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
        
        if include_sensitive:
            data['email'] = self.email
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User from dictionary"""
        profile = UserProfile.from_dict(data.get('profile', {}))
        
        last_login = data.get('last_login')
        if isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login)
        
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = data.get('updated_at')
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            role=UserRole(data.get('role', 'student')),
            profile=profile,
            is_active=data.get('is_active', True),
            email_verified=data.get('email_verified', False),
            last_login=last_login,
            created_at=created_at or datetime.now(),
            updated_at=updated_at or datetime.now(),
            metadata=data.get('metadata', {})
        )

@dataclass
class ActivityLog:
    """Log of user activities"""
    user_id: str
    activity_type: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert activity log to dictionary"""
        return {
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActivityLog':
        """Create ActivityLog from dictionary"""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            user_id=data['user_id'],
            activity_type=data['activity_type'],
            description=data['description'],
            timestamp=timestamp or datetime.now(),
            metadata=data.get('metadata', {})
        )

@dataclass
class LearningProgress:
    """Tracks user's learning progress"""
    user_id: str
    content_id: str
    content_type: str  # quiz, course, section
    status: str = "not_started"  # not_started, in_progress, completed
    progress_percentage: float = 0.0
    time_spent: int = 0  # in seconds
    attempts: int = 0
    best_score: Optional[float] = None
    last_accessed: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate progress data after initialization"""
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            raise ValueError("Progress percentage must be between 0 and 100")
        
        valid_statuses = ["not_started", "in_progress", "completed"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    
    def start_learning(self) -> None:
        """Mark learning as started"""
        if self.status == "not_started":
            self.status = "in_progress"
            self.last_accessed = datetime.now()
    
    def update_progress(self, percentage: float, time_spent_delta: int = 0) -> None:
        """Update learning progress"""
        self.progress_percentage = max(0, min(100, percentage))
        self.time_spent += time_spent_delta
        self.last_accessed = datetime.now()
        
        if self.progress_percentage >= 100 and self.status != "completed":
            self.complete_learning()
    
    def complete_learning(self, score: Optional[float] = None) -> None:
        """Mark learning as completed"""
        self.status = "completed"
        self.progress_percentage = 100.0
        self.completed_at = datetime.now()
        self.last_accessed = datetime.now()
        
        if score is not None:
            if self.best_score is None or score > self.best_score:
                self.best_score = score
    
    def add_attempt(self, score: Optional[float] = None) -> None:
        """Record a new attempt"""
        self.attempts += 1
        self.last_accessed = datetime.now()
        
        if score is not None:
            if self.best_score is None or score > self.best_score:
                self.best_score = score
    
    def reset_progress(self) -> None:
        """Reset learning progress"""
        self.status = "not_started"
        self.progress_percentage = 0.0
        self.time_spent = 0
        self.attempts = 0
        self.best_score = None
        self.completed_at = None
        self.notes = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert progress to dictionary"""
        return {
            'user_id': self.user_id,
            'content_id': self.content_id,
            'content_type': self.content_type,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'time_spent': self.time_spent,
            'attempts': self.attempts,
            'best_score': self.best_score,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningProgress':
        """Create LearningProgress from dictionary"""
        last_accessed = data.get('last_accessed')
        if isinstance(last_accessed, str):
            last_accessed = datetime.fromisoformat(last_accessed)
        
        completed_at = data.get('completed_at')
        if isinstance(completed_at, str):
            completed_at = datetime.fromisoformat(completed_at)
        
        return cls(
            user_id=data['user_id'],
            content_id=data['content_id'],
            content_type=data['content_type'],
            status=data.get('status', 'not_started'),
            progress_percentage=data.get('progress_percentage', 0.0),
            time_spent=data.get('time_spent', 0),
            attempts=data.get('attempts', 0),
            best_score=data.get('best_score'),
            last_accessed=last_accessed,
            completed_at=completed_at,
            notes=data.get('notes'),
            metadata=data.get('metadata', {})
        )
