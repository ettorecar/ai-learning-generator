"""
Helper utilities for AI Learning Generator

This module contains general-purpose helper functions used throughout
the application for various common tasks and operations.
"""

import uuid
import re
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import secrets
import string

def generate_unique_id(prefix: str = "", length: int = 8) -> str:
    """Generate a unique identifier with optional prefix"""
    unique_part = str(uuid.uuid4()).replace('-', '')[:length]
    return f"{prefix}{unique_part}" if prefix else unique_part

def generate_session_id() -> str:
    """Generate a secure session ID"""
    return secrets.token_urlsafe(32)

def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(40)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage"""
    if not filename:
        return "untitled"
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    
    # Ensure filename is not empty after sanitization
    if not filename:
        filename = "untitled"
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def format_timestamp(dt: Optional[datetime] = None, format_type: str = "iso") -> str:
    """Format timestamp in various formats"""
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    format_types = {
        "iso": lambda d: d.isoformat(),
        "human": lambda d: d.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "filename": lambda d: d.strftime("%Y%m%d_%H%M%S"),
        "date_only": lambda d: d.strftime("%Y-%m-%d"),
        "time_only": lambda d: d.strftime("%H:%M:%S")
    }
    
    formatter = format_types.get(format_type, format_types["iso"])
    return formatter(dt)

def calculate_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file"""
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    
    if algorithm not in hash_algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = hash_algorithms[algorithm]()
    
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        raise IOError(f"Cannot read file {filepath}: {e}")

def calculate_text_hash(text: str, algorithm: str = "sha256") -> str:
    """Calculate hash of text content"""
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    
    if algorithm not in hash_algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = hash_algorithms[algorithm]()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string with fallback"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(obj: Any, **kwargs) -> str:
    """Safely serialize object to JSON"""
    try:
        return json.dumps(obj, **kwargs)
    except (TypeError, ValueError):
        return json.dumps({"error": "Unable to serialize object"})

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def remove_duplicates(lst: List[Any], preserve_order: bool = True) -> List[Any]:
    """Remove duplicates from list"""
    if preserve_order:
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    else:
        return list(set(lst))

def is_valid_json(json_str: str) -> bool:
    """Check if string is valid JSON"""
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def get_file_size_human(filepath: str) -> str:
    """Get file size in human-readable format"""
    try:
        size = os.path.getsize(filepath)
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        
        return f"{size:.1f} PB"
    except OSError:
        return "Unknown"

def ensure_directory_exists(directory_path: str) -> bool:
    """Ensure directory exists, create if necessary"""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except OSError:
        return False

def clean_text_for_search(text: str) -> str:
    """Clean text for search indexing"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_numbers_from_string(text: str) -> List[float]:
    """Extract all numbers from a string"""
    if not text:
        return []
    
    # Pattern to match integers and floats
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        try:
            # Try to convert to int first, then float
            if '.' in match:
                numbers.append(float(match))
            else:
                numbers.append(int(match))
        except ValueError:
            continue
    
    return numbers

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length with suffix"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """Generate a secure random password"""
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"
    
    return ''.join(secrets.choice(chars) for _ in range(length))

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    result = {
        'valid': True,
        'score': 0,
        'requirements': {
            'length': len(password) >= 8,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
    }
    
    # Calculate score
    result['score'] = sum(result['requirements'].values())
    
    # Overall validity
    result['valid'] = result['score'] >= 4 and result['requirements']['length']
    
    return result

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"

def retry_operation(func, max_attempts: int = 3, delay: float = 1.0):
    """Retry operation with exponential backoff"""
    import time
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(delay * (2 ** attempt))

class CircularBuffer:
    """Simple circular buffer implementation"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.size = 0
    
    def append(self, item: Any) -> None:
        """Add item to buffer"""
        self.buffer[self.head] = item
        self.head = (self.head + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)
    
    def get_all(self) -> List[Any]:
        """Get all items in order"""
        if self.size < self.capacity:
            return self.buffer[:self.size]
        else:
            return self.buffer[self.head:] + self.buffer[:self.head]
    
    def is_full(self) -> bool:
        """Check if buffer is full"""
        return self.size == self.capacity
    
    def clear(self) -> None:
        """Clear the buffer"""
        self.buffer = [None] * self.capacity
        self.head = 0
        self.size = 0
