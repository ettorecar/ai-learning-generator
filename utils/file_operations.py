"""
File operations and configuration utilities

This module provides utilities for file management, configuration loading,
and data persistence operations.
"""

import os
import json
import yaml
import csv
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import shutil
import tempfile

class FileManager:
    """Manage file operations for the application"""
    
    def __init__(self, base_directory: str = None):
        self.base_directory = Path(base_directory) if base_directory else Path.cwd()
        self.ensure_directory_exists(self.base_directory)
    
    def ensure_directory_exists(self, directory: Union[str, Path]) -> bool:
        """Ensure directory exists, create if necessary"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            return False
    
    def save_json(self, data: Dict[str, Any], filename: str, 
                  pretty_print: bool = True) -> bool:
        """Save data as JSON file"""
        try:
            filepath = self.base_directory / filename
            self.ensure_directory_exists(filepath.parent)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                if pretty_print:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON file {filename}: {e}")
            return False
    
    def load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            filepath = self.base_directory / filename
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file {filename}: {e}")
            return None
    
    def save_yaml(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as YAML file"""
        try:
            filepath = self.base_directory / filename
            self.ensure_directory_exists(filepath.parent)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"Error saving YAML file {filename}: {e}")
            return False
    
    def load_yaml(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from YAML file"""
        try:
            filepath = self.base_directory / filename
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading YAML file {filename}: {e}")
            return None
    
    def save_csv(self, data: List[Dict[str, Any]], filename: str,
                 fieldnames: Optional[List[str]] = None) -> bool:
        """Save data as CSV file"""
        try:
            if not data:
                return False
            
            filepath = self.base_directory / filename
            self.ensure_directory_exists(filepath.parent)
            
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error saving CSV file {filename}: {e}")
            return False
    
    def load_csv(self, filename: str) -> Optional[List[Dict[str, Any]]]:
        """Load data from CSV file"""
        try:
            filepath = self.base_directory / filename
            data = []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            return data
        except Exception as e:
            print(f"Error loading CSV file {filename}: {e}")
            return None
    
    def save_text(self, text: str, filename: str, encoding: str = 'utf-8') -> bool:
        """Save text to file"""
        try:
            filepath = self.base_directory / filename
            self.ensure_directory_exists(filepath.parent)
            
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error saving text file {filename}: {e}")
            return False
    
    def load_text(self, filename: str, encoding: str = 'utf-8') -> Optional[str]:
        """Load text from file"""
        try:
            filepath = self.base_directory / filename
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"Error loading text file {filename}: {e}")
            return None
    
    def save_pickle(self, data: Any, filename: str) -> bool:
        """Save data using pickle serialization"""
        try:
            filepath = self.base_directory / filename
            self.ensure_directory_exists(filepath.parent)
            
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving pickle file {filename}: {e}")
            return False
    
    def load_pickle(self, filename: str) -> Optional[Any]:
        """Load data from pickle file"""
        try:
            filepath = self.base_directory / filename
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading pickle file {filename}: {e}")
            return None
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists"""
        filepath = self.base_directory / filename
        return filepath.exists() and filepath.is_file()
    
    def directory_exists(self, dirname: str) -> bool:
        """Check if directory exists"""
        dirpath = self.base_directory / dirname
        return dirpath.exists() and dirpath.is_dir()
    
    def list_files(self, pattern: str = "*", recursive: bool = False) -> List[str]:
        """List files matching pattern"""
        try:
            if recursive:
                files = list(self.base_directory.rglob(pattern))
            else:
                files = list(self.base_directory.glob(pattern))
            
            # Return only files, not directories
            return [str(f.relative_to(self.base_directory)) for f in files if f.is_file()]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """Delete file safely"""
        try:
            filepath = self.base_directory / filename
            if filepath.exists() and filepath.is_file():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")
            return False
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file from source to destination"""
        try:
            src_path = self.base_directory / src
            dst_path = self.base_directory / dst
            
            self.ensure_directory_exists(dst_path.parent)
            shutil.copy2(src_path, dst_path)
            return True
        except Exception as e:
            print(f"Error copying file from {src} to {dst}: {e}")
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """Move file from source to destination"""
        try:
            src_path = self.base_directory / src
            dst_path = self.base_directory / dst
            
            self.ensure_directory_exists(dst_path.parent)
            shutil.move(str(src_path), str(dst_path))
            return True
        except Exception as e:
            print(f"Error moving file from {src} to {dst}: {e}")
            return False
    
    def get_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get file information"""
        try:
            filepath = self.base_directory / filename
            
            if not filepath.exists():
                return None
            
            stat = filepath.stat()
            
            return {
                'name': filepath.name,
                'path': str(filepath),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'is_file': filepath.is_file(),
                'is_directory': filepath.is_dir(),
                'extension': filepath.suffix
            }
        except Exception as e:
            print(f"Error getting file info for {filename}: {e}")
            return None
    
    def create_backup(self, filename: str, backup_dir: str = "backups") -> bool:
        """Create backup of file"""
        try:
            src_path = self.base_directory / filename
            
            if not src_path.exists():
                return False
            
            backup_path = self.base_directory / backup_dir
            self.ensure_directory_exists(backup_path)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{src_path.stem}_{timestamp}{src_path.suffix}"
            
            return self.copy_file(filename, f"{backup_dir}/{backup_filename}")
        except Exception as e:
            print(f"Error creating backup for {filename}: {e}")
            return False

class ConfigLoader:
    """Load and manage application configuration"""
    
    def __init__(self, config_directory: str = "config"):
        self.config_directory = Path(config_directory)
        self.file_manager = FileManager(config_directory)
        self._config_cache = {}
    
    def load_config(self, config_name: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """Load configuration file"""
        if use_cache and config_name in self._config_cache:
            return self._config_cache[config_name]
        
        # Try different file extensions
        for ext in ['.json', '.yaml', '.yml']:
            filename = f"{config_name}{ext}"
            
            if ext == '.json':
                config = self.file_manager.load_json(filename)
            else:
                config = self.file_manager.load_yaml(filename)
            
            if config:
                if use_cache:
                    self._config_cache[config_name] = config
                return config
        
        return None
    
    def save_config(self, config_name: str, config_data: Dict[str, Any],
                   format_type: str = 'json') -> bool:
        """Save configuration file"""
        filename = f"{config_name}.{format_type}"
        
        if format_type == 'json':
            success = self.file_manager.save_json(config_data, filename)
        elif format_type in ['yaml', 'yml']:
            success = self.file_manager.save_yaml(config_data, filename)
        else:
            return False
        
        if success and config_name in self._config_cache:
            self._config_cache[config_name] = config_data
        
        return success
    
    def get_config_value(self, config_name: str, key_path: str, default: Any = None) -> Any:
        """Get specific configuration value using dot notation"""
        config = self.load_config(config_name)
        
        if not config:
            return default
        
        keys = key_path.split('.')
        value = config
        
        try:
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config_value(self, config_name: str, key_path: str, value: Any) -> bool:
        """Set specific configuration value using dot notation"""
        config = self.load_config(config_name) or {}
        
        keys = key_path.split('.')
        current = config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        return self.save_config(config_name, config)
    
    def merge_configs(self, *config_names: str) -> Dict[str, Any]:
        """Merge multiple configuration files"""
        merged = {}
        
        for config_name in config_names:
            config = self.load_config(config_name)
            if config:
                merged = self._deep_merge(merged, config)
        
        return merged
    
    def validate_config(self, config_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration against schema"""
        config = self.load_config(config_name)
        result = {'valid': True, 'errors': []}
        
        if not config:
            result['valid'] = False
            result['errors'].append(f"Configuration {config_name} not found")
            return result
        
        # Simple validation - check required fields
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in config:
                result['valid'] = False
                result['errors'].append(f"Missing required field: {field}")
        
        # Type validation
        field_types = schema.get('types', {})
        for field, expected_type in field_types.items():
            if field in config:
                if not isinstance(config[field], expected_type):
                    result['valid'] = False
                    result['errors'].append(f"Field {field} should be of type {expected_type.__name__}")
        
        return result
    
    def list_configs(self) -> List[str]:
        """List available configuration files"""
        files = self.file_manager.list_files("*.json") + \
                self.file_manager.list_files("*.yaml") + \
                self.file_manager.list_files("*.yml")
        
        # Remove extensions and duplicates
        config_names = set()
        for file in files:
            name = Path(file).stem
            config_names.add(name)
        
        return sorted(list(config_names))
    
    def reload_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Reload configuration from file (bypass cache)"""
        if config_name in self._config_cache:
            del self._config_cache[config_name]
        
        return self.load_config(config_name, use_cache=False)
    
    def clear_cache(self) -> None:
        """Clear configuration cache"""
        self._config_cache.clear()
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result

class DataExporter:
    """Export data in various formats"""
    
    def __init__(self, file_manager: FileManager = None):
        self.file_manager = file_manager or FileManager()
    
    def export_quiz_results(self, results: List[Dict[str, Any]], 
                           format_type: str = 'csv') -> bool:
        """Export quiz results in specified format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_results_{timestamp}"
        
        if format_type == 'csv':
            return self.file_manager.save_csv(results, f"{filename}.csv")
        elif format_type == 'json':
            return self.file_manager.save_json(results, f"{filename}.json")
        else:
            return False
    
    def export_learning_analytics(self, analytics: Dict[str, Any],
                                format_type: str = 'json') -> bool:
        """Export learning analytics data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analytics_{timestamp}"
        
        if format_type == 'json':
            return self.file_manager.save_json(analytics, f"{filename}.json")
        elif format_type == 'yaml':
            return self.file_manager.save_yaml(analytics, f"{filename}.yaml")
        else:
            return False
