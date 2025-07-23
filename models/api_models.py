"""
API-related data models

This module defines data models for API requests, responses,
and error handling structures.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class HTTPStatus(Enum):
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

class ErrorType(Enum):
    """Types of errors"""
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NOT_FOUND_ERROR = "not_found_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    INTERNAL_ERROR = "internal_error"
    EXTERNAL_API_ERROR = "external_api_error"
    TIMEOUT_ERROR = "timeout_error"

@dataclass
class APIRequest:
    """Represents an API request"""
    endpoint: str
    method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    request_id: str = field(default_factory=lambda: f"req_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}")
    timestamp: datetime = field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    def __post_init__(self):
        """Validate request data after initialization"""
        if not self.endpoint or not isinstance(self.endpoint, str):
            raise ValueError("Endpoint must be a non-empty string")
        
        valid_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
        if self.method.upper() not in valid_methods:
            raise ValueError(f"Method must be one of: {', '.join(valid_methods)}")
        
        self.method = self.method.upper()
    
    def add_header(self, key: str, value: str) -> None:
        """Add header to request"""
        self.headers[key] = value
    
    def add_parameter(self, key: str, value: Any) -> None:
        """Add parameter to request"""
        self.parameters[key] = value
    
    def get_content_type(self) -> str:
        """Get content type from headers"""
        return self.headers.get('Content-Type', 'application/json')
    
    def is_json_request(self) -> bool:
        """Check if request contains JSON data"""
        content_type = self.get_content_type()
        return 'application/json' in content_type
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary"""
        return {
            'endpoint': self.endpoint,
            'method': self.method,
            'headers': self.headers,
            'parameters': self.parameters,
            'body': self.body,
            'user_id': self.user_id,
            'request_id': self.request_id,
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIRequest':
        """Create APIRequest from dictionary"""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            endpoint=data['endpoint'],
            method=data.get('method', 'GET'),
            headers=data.get('headers', {}),
            parameters=data.get('parameters', {}),
            body=data.get('body'),
            user_id=data.get('user_id'),
            request_id=data.get('request_id', f"req_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"),
            timestamp=timestamp or datetime.now(),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent')
        )

@dataclass
class ValidationError:
    """Represents a validation error"""
    field: str
    message: str
    code: Optional[str] = None
    value: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert validation error to dictionary"""
        return {
            'field': self.field,
            'message': self.message,
            'code': self.code,
            'value': self.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationError':
        """Create ValidationError from dictionary"""
        return cls(
            field=data['field'],
            message=data['message'],
            code=data.get('code'),
            value=data.get('value')
        )

@dataclass
class ErrorResponse:
    """Represents an API error response"""
    error_type: ErrorType
    message: str
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    details: Optional[str] = None
    validation_errors: List[ValidationError] = field(default_factory=list)
    error_code: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None
    help_url: Optional[str] = None
    
    def __post_init__(self):
        """Validate error response after initialization"""
        if not isinstance(self.error_type, ErrorType):
            if isinstance(self.error_type, str):
                try:
                    self.error_type = ErrorType(self.error_type)
                except ValueError:
                    raise ValueError(f"Invalid error type: {self.error_type}")
        
        if not isinstance(self.status_code, HTTPStatus):
            if isinstance(self.status_code, int):
                try:
                    self.status_code = HTTPStatus(self.status_code)
                except ValueError:
                    raise ValueError(f"Invalid status code: {self.status_code}")
    
    def add_validation_error(self, field: str, message: str, code: Optional[str] = None) -> None:
        """Add a validation error"""
        error = ValidationError(field=field, message=message, code=code)
        self.validation_errors.append(error)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error response to dictionary"""
        return {
            'success': False,
            'error': {
                'type': self.error_type.value,
                'message': self.message,
                'code': self.error_code,
                'details': self.details,
                'validation_errors': [err.to_dict() for err in self.validation_errors],
                'timestamp': self.timestamp.isoformat(),
                'request_id': self.request_id,
                'help_url': self.help_url
            },
            'status_code': self.status_code.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorResponse':
        """Create ErrorResponse from dictionary"""
        error_data = data.get('error', {})
        
        validation_errors = [ValidationError.from_dict(err_data) 
                           for err_data in error_data.get('validation_errors', [])]
        
        timestamp = error_data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        return cls(
            error_type=ErrorType(error_data['type']),
            message=error_data['message'],
            status_code=HTTPStatus(data.get('status_code', 400)),
            details=error_data.get('details'),
            validation_errors=validation_errors,
            error_code=error_data.get('code'),
            timestamp=timestamp or datetime.now(),
            request_id=error_data.get('request_id'),
            help_url=error_data.get('help_url')
        )

@dataclass
class PaginationInfo:
    """Pagination information for API responses"""
    page: int = 1
    per_page: int = 20
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    next_url: Optional[str] = None
    prev_url: Optional[str] = None
    
    def __post_init__(self):
        """Calculate pagination values after initialization"""
        if self.per_page <= 0:
            raise ValueError("Items per page must be positive")
        
        if self.page <= 0:
            raise ValueError("Page number must be positive")
        
        # Calculate total pages
        self.total_pages = max(1, (self.total_items + self.per_page - 1) // self.per_page)
        
        # Calculate has_next and has_prev
        self.has_next = self.page < self.total_pages
        self.has_prev = self.page > 1
    
    def get_offset(self) -> int:
        """Get the offset for database queries"""
        return (self.page - 1) * self.per_page
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pagination info to dictionary"""
        return {
            'page': self.page,
            'per_page': self.per_page,
            'total_items': self.total_items,
            'total_pages': self.total_pages,
            'has_next': self.has_next,
            'has_prev': self.has_prev,
            'next_url': self.next_url,
            'prev_url': self.prev_url
        }

@dataclass
class APIResponse:
    """Represents an API response"""
    success: bool = True
    data: Any = None
    message: Optional[str] = None
    status_code: HTTPStatus = HTTPStatus.OK
    pagination: Optional[PaginationInfo] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    request_id: Optional[str] = None
    response_time: Optional[float] = None  # in milliseconds
    
    def __post_init__(self):
        """Validate response data after initialization"""
        if not isinstance(self.status_code, HTTPStatus):
            if isinstance(self.status_code, int):
                try:
                    self.status_code = HTTPStatus(self.status_code)
                except ValueError:
                    raise ValueError(f"Invalid status code: {self.status_code}")
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to response"""
        self.metadata[key] = value
    
    def set_pagination(self, page: int, per_page: int, total_items: int) -> None:
        """Set pagination information"""
        self.pagination = PaginationInfo(
            page=page,
            per_page=per_page,
            total_items=total_items
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        response_dict = {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'request_id': self.request_id,
            'metadata': self.metadata
        }
        
        if self.response_time is not None:
            response_dict['response_time_ms'] = self.response_time
        
        if self.pagination:
            response_dict['pagination'] = self.pagination.to_dict()
        
        return response_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIResponse':
        """Create APIResponse from dictionary"""
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        pagination = None
        if 'pagination' in data:
            pagination = PaginationInfo(**data['pagination'])
        
        return cls(
            success=data.get('success', True),
            data=data.get('data'),
            message=data.get('message'),
            status_code=HTTPStatus(data.get('status_code', 200)),
            pagination=pagination,
            metadata=data.get('metadata', {}),
            timestamp=timestamp or datetime.now(),
            request_id=data.get('request_id'),
            response_time=data.get('response_time_ms')
        )
    
    @classmethod
    def success_response(cls, data: Any = None, message: str = None, 
                        status_code: HTTPStatus = HTTPStatus.OK) -> 'APIResponse':
        """Create a successful API response"""
        return cls(
            success=True,
            data=data,
            message=message,
            status_code=status_code
        )
    
    @classmethod
    def error_response(cls, error: ErrorResponse) -> 'APIResponse':
        """Create an error API response"""
        return cls(
            success=False,
            data=error.to_dict(),
            status_code=error.status_code
        )

@dataclass
class RateLimitInfo:
    """Rate limiting information"""
    limit: int  # requests per window
    remaining: int  # remaining requests
    reset_time: datetime  # when the limit resets
    window_size: int = 3600  # window size in seconds (default: 1 hour)
    
    def is_exceeded(self) -> bool:
        """Check if rate limit is exceeded"""
        return self.remaining <= 0
    
    def time_until_reset(self) -> int:
        """Get seconds until rate limit resets"""
        delta = self.reset_time - datetime.now()
        return max(0, int(delta.total_seconds()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rate limit info to dictionary"""
        return {
            'limit': self.limit,
            'remaining': self.remaining,
            'reset_time': self.reset_time.isoformat(),
            'window_size': self.window_size,
            'time_until_reset': self.time_until_reset()
        }

@dataclass
class APIMetrics:
    """API usage metrics"""
    endpoint: str
    method: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    last_request_time: Optional[datetime] = None
    
    def record_request(self, success: bool, response_time: float) -> None:
        """Record a new API request"""
        self.total_requests += 1
        self.last_request_time = datetime.now()
        
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        # Update response time statistics
        self.min_response_time = min(self.min_response_time, response_time)
        self.max_response_time = max(self.max_response_time, response_time)
        
        # Calculate new average (running average)
        self.average_response_time = (
            (self.average_response_time * (self.total_requests - 1) + response_time) 
            / self.total_requests
        )
    
    def get_success_rate(self) -> float:
        """Get success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            'endpoint': self.endpoint,
            'method': self.method,
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': self.get_success_rate(),
            'average_response_time': self.average_response_time,
            'min_response_time': self.min_response_time if self.min_response_time != float('inf') else 0,
            'max_response_time': self.max_response_time,
            'last_request_time': self.last_request_time.isoformat() if self.last_request_time else None
        }
