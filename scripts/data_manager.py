#!/usr/bin/env python3
"""
Data Management CLI Tool

Command-line interface for managing application data including
backup, restore, migration, and cleanup operations.

Usage:
    python data_manager.py backup --output backup.json
    python data_manager.py restore --input backup.json
    python data_manager.py export --format csv --type quiz_results
    python data_manager.py cleanup --older-than 30
"""

import argparse
import json
import csv
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_operations import FileManager, DataExporter
from utils.helpers import format_timestamp, calculate_file_hash
from models.quiz_models import Quiz, QuizResult
from models.user_models import User, LearningProgress

class DataManagerCLI:
    """Command-line interface for data management"""
    
    def __init__(self):
        self.file_manager = FileManager()
        self.data_exporter = DataExporter()
    
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="Manage application data",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Create data backup')
        backup_parser.add_argument(
            '--output', '-o',
            type=str,
            default=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            help='Output backup file'
        )
        backup_parser.add_argument(
            '--include',
            nargs='+',
            choices=['quizzes', 'users', 'progress', 'analytics'],
            default=['quizzes', 'users', 'progress'],
            help='Data types to include in backup'
        )
        backup_parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress backup file'
        )
        
        # Restore command
        restore_parser = subparsers.add_parser('restore', help='Restore from backup')
        restore_parser.add_argument(
            '--input', '-i',
            type=str,
            required=True,
            help='Input backup file'
        )
        restore_parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify backup integrity before restore'
        )
        restore_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be restored without actually doing it'
        )
        
        # Export command
        export_parser = subparsers.add_parser('export', help='Export data')
        export_parser.add_argument(
            '--type', '-t',
            choices=['quiz_results', 'user_progress', 'analytics', 'quizzes'],
            required=True,
            help='Type of data to export'
        )
        export_parser.add_argument(
            '--format', '-f',
            choices=['csv', 'json', 'xlsx'],
            default='csv',
            help='Export format'
        )
        export_parser.add_argument(
            '--output', '-o',
            type=str,
            help='Output file (auto-generated if not specified)'
        )
        export_parser.add_argument(
            '--date-range',
            nargs=2,
            metavar=('START', 'END'),
            help='Date range for export (YYYY-MM-DD format)'
        )
        
        # Cleanup command
        cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old data')
        cleanup_parser.add_argument(
            '--older-than',
            type=int,
            default=90,
            help='Remove data older than N days (default: 90)'
        )
        cleanup_parser.add_argument(
            '--type',
            choices=['logs', 'temp_files', 'old_backups', 'expired_sessions'],
            nargs='+',
            default=['logs', 'temp_files'],
            help='Types of data to clean up'
        )
        cleanup_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned without actually doing it'
        )
        
        # Migrate command
        migrate_parser = subparsers.add_parser('migrate', help='Migrate data between versions')
        migrate_parser.add_argument(
            '--from-version',
            type=str,
            required=True,
            help='Source version'
        )
        migrate_parser.add_argument(
            '--to-version',
            type=str,
            required=True,
            help='Target version'
        )
        migrate_parser.add_argument(
            '--backup-first',
            action='store_true',
            help='Create backup before migration'
        )
        
        # Verify command
        verify_parser = subparsers.add_parser('verify', help='Verify data integrity')
        verify_parser.add_argument(
            '--type',
            choices=['all', 'quizzes', 'users', 'progress'],
            default='all',
            help='Type of data to verify'
        )
        verify_parser.add_argument(
            '--repair',
            action='store_true',
            help='Attempt to repair corrupted data'
        )
        
        # Common arguments
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        
        return parser.parse_args()
    
    def create_backup(self, output_path: str, include_types: List[str], 
                     compress: bool = False, verbose: bool = False) -> bool:
        """Create data backup"""
        try:
            backup_data = {
                'metadata': {
                    'version': '1.0',
                    'created_at': format_timestamp(),
                    'included_types': include_types,
                    'compressed': compress
                },
                'data': {}
            }
            
            # Collect data based on included types
            if 'quizzes' in include_types:
                if verbose:
                    print("Collecting quiz data...")
                backup_data['data']['quizzes'] = self.collect_quiz_data()
            
            if 'users' in include_types:
                if verbose:
                    print("Collecting user data...")
                backup_data['data']['users'] = self.collect_user_data()
            
            if 'progress' in include_types:
                if verbose:
                    print("Collecting progress data...")
                backup_data['data']['progress'] = self.collect_progress_data()
            
            if 'analytics' in include_types:
                if verbose:
                    print("Collecting analytics data...")
                backup_data['data']['analytics'] = self.collect_analytics_data()
            
            # Save backup
            if compress:
                import gzip
                with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)
            else:
                self.file_manager.save_json(backup_data, output_path)
            
            if verbose:
                file_size = Path(output_path).stat().st_size
                print(f"Backup created: {output_path} ({file_size} bytes)")
            
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_backup(self, input_path: str, verify: bool = False, 
                      dry_run: bool = False, verbose: bool = False) -> bool:
        """Restore from backup"""
        try:
            # Load backup file
            if input_path.endswith('.gz'):
                import gzip
                with gzip.open(input_path, 'rt', encoding='utf-8') as f:
                    backup_data = json.load(f)
            else:
                backup_data = self.file_manager.load_json(input_path)
            
            if not backup_data:
                print("Error: Could not load backup file")
                return False
            
            # Verify backup integrity if requested
            if verify:
                if not self.verify_backup_integrity(backup_data):
                    print("Error: Backup integrity check failed")
                    return False
            
            if verbose:
                metadata = backup_data.get('metadata', {})
                print(f"Backup version: {metadata.get('version', 'unknown')}")
                print(f"Created: {metadata.get('created_at', 'unknown')}")
                print(f"Included types: {metadata.get('included_types', [])}")
            
            # Restore data
            data = backup_data.get('data', {})
            
            if dry_run:
                print("Dry run - would restore:")
                for data_type, items in data.items():
                    if isinstance(items, list):
                        print(f"  {data_type}: {len(items)} items")
                    elif isinstance(items, dict):
                        print(f"  {data_type}: {len(items)} items")
                    else:
                        print(f"  {data_type}: 1 item")
                return True
            
            # Actual restore
            for data_type, items in data.items():
                if verbose:
                    print(f"Restoring {data_type}...")
                
                if data_type == 'quizzes':
                    self.restore_quiz_data(items)
                elif data_type == 'users':
                    self.restore_user_data(items)
                elif data_type == 'progress':
                    self.restore_progress_data(items)
                elif data_type == 'analytics':
                    self.restore_analytics_data(items)
            
            if verbose:
                print("Restore completed successfully")
            
            return True
            
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def export_data(self, data_type: str, format_type: str, output_path: Optional[str] = None,
                   date_range: Optional[List[str]] = None, verbose: bool = False) -> bool:
        """Export data in specified format"""
        try:
            # Generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = f"{data_type}_export_{timestamp}.{format_type}"
            
            # Collect data
            if verbose:
                print(f"Collecting {data_type} data...")
            
            if data_type == 'quiz_results':
                data = self.collect_quiz_results_for_export(date_range)
            elif data_type == 'user_progress':
                data = self.collect_user_progress_for_export(date_range)
            elif data_type == 'analytics':
                data = self.collect_analytics_for_export(date_range)
            elif data_type == 'quizzes':
                data = self.collect_quizzes_for_export()
            else:
                print(f"Unknown data type: {data_type}")
                return False
            
            # Export data
            if format_type == 'csv':
                self.file_manager.save_csv(data, output_path)
            elif format_type == 'json':
                self.file_manager.save_json(data, output_path)
            elif format_type == 'xlsx':
                # Would require openpyxl library
                print("XLSX export not implemented yet")
                return False
            
            if verbose:
                print(f"Data exported to: {output_path}")
                print(f"Records exported: {len(data)}")
            
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def cleanup_data(self, older_than_days: int, cleanup_types: List[str],
                    dry_run: bool = False, verbose: bool = False) -> bool:
        """Clean up old data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cleaned_items = 0
            
            for cleanup_type in cleanup_types:
                if verbose:
                    print(f"Cleaning up {cleanup_type}...")
                
                if cleanup_type == 'logs':
                    count = self.cleanup_log_files(cutoff_date, dry_run)
                    cleaned_items += count
                    if verbose:
                        print(f"  Cleaned {count} log files")
                
                elif cleanup_type == 'temp_files':
                    count = self.cleanup_temp_files(cutoff_date, dry_run)
                    cleaned_items += count
                    if verbose:
                        print(f"  Cleaned {count} temporary files")
                
                elif cleanup_type == 'old_backups':
                    count = self.cleanup_old_backups(cutoff_date, dry_run)
                    cleaned_items += count
                    if verbose:
                        print(f"  Cleaned {count} old backup files")
                
                elif cleanup_type == 'expired_sessions':
                    count = self.cleanup_expired_sessions(cutoff_date, dry_run)
                    cleaned_items += count
                    if verbose:
                        print(f"  Cleaned {count} expired sessions")
            
            action = "Would clean" if dry_run else "Cleaned"
            print(f"{action} {cleaned_items} items total")
            
            return True
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return False
    
    def verify_data_integrity(self, data_type: str = 'all', repair: bool = False,
                            verbose: bool = False) -> bool:
        """Verify data integrity"""
        try:
            issues_found = 0
            
            if data_type in ['all', 'quizzes']:
                if verbose:
                    print("Verifying quiz data...")
                issues = self.verify_quiz_data(repair)
                issues_found += issues
                if verbose:
                    print(f"  Found {issues} issues")
            
            if data_type in ['all', 'users']:
                if verbose:
                    print("Verifying user data...")
                issues = self.verify_user_data(repair)
                issues_found += issues
                if verbose:
                    print(f"  Found {issues} issues")
            
            if data_type in ['all', 'progress']:
                if verbose:
                    print("Verifying progress data...")
                issues = self.verify_progress_data(repair)
                issues_found += issues
                if verbose:
                    print(f"  Found {issues} issues")
            
            if issues_found == 0:
                print("✓ Data integrity check passed")
            else:
                action = "repaired" if repair else "found"
                print(f"✗ Data integrity issues {action}: {issues_found}")
            
            return issues_found == 0
            
        except Exception as e:
            print(f"Error during verification: {e}")
            return False
    
    # Helper methods for data collection
    def collect_quiz_data(self) -> List[Dict[str, Any]]:
        """Collect quiz data for backup"""
        # Mock implementation - would load from actual storage
        return [
            {
                'id': 'quiz_1',
                'title': 'Sample Quiz',
                'created_at': format_timestamp(),
                'questions': []
            }
        ]
    
    def collect_user_data(self) -> List[Dict[str, Any]]:
        """Collect user data for backup"""
        # Mock implementation
        return [
            {
                'id': 'user_1',
                'username': 'sample_user',
                'created_at': format_timestamp()
            }
        ]
    
    def collect_progress_data(self) -> List[Dict[str, Any]]:
        """Collect progress data for backup"""
        # Mock implementation
        return []
    
    def collect_analytics_data(self) -> Dict[str, Any]:
        """Collect analytics data for backup"""
        # Mock implementation
        return {
            'total_users': 0,
            'total_quizzes': 0,
            'generated_at': format_timestamp()
        }
    
    # Helper methods for verification
    def verify_backup_integrity(self, backup_data: Dict[str, Any]) -> bool:
        """Verify backup file integrity"""
        required_keys = ['metadata', 'data']
        return all(key in backup_data for key in required_keys)
    
    def verify_quiz_data(self, repair: bool = False) -> int:
        """Verify quiz data integrity"""
        # Mock implementation
        return 0
    
    def verify_user_data(self, repair: bool = False) -> int:
        """Verify user data integrity"""
        # Mock implementation
        return 0
    
    def verify_progress_data(self, repair: bool = False) -> int:
        """Verify progress data integrity"""
        # Mock implementation
        return 0
    
    # Helper methods for cleanup
    def cleanup_log_files(self, cutoff_date: datetime, dry_run: bool = False) -> int:
        """Clean up old log files"""
        # Mock implementation
        return 0
    
    def cleanup_temp_files(self, cutoff_date: datetime, dry_run: bool = False) -> int:
        """Clean up temporary files"""
        # Mock implementation
        return 0
    
    def cleanup_old_backups(self, cutoff_date: datetime, dry_run: bool = False) -> int:
        """Clean up old backup files"""
        # Mock implementation
        return 0
    
    def cleanup_expired_sessions(self, cutoff_date: datetime, dry_run: bool = False) -> int:
        """Clean up expired sessions"""
        # Mock implementation
        return 0
    
    # Helper methods for data export
    def collect_quiz_results_for_export(self, date_range: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Collect quiz results for export"""
        # Mock implementation
        return [
            {
                'quiz_id': 'quiz_1',
                'user_id': 'user_1',
                'score': 85.0,
                'completed_at': format_timestamp(),
                'time_taken': 300
            }
        ]
    
    def collect_user_progress_for_export(self, date_range: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Collect user progress for export"""
        # Mock implementation
        return []
    
    def collect_analytics_for_export(self, date_range: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Collect analytics for export"""
        # Mock implementation
        return []
    
    def collect_quizzes_for_export(self) -> List[Dict[str, Any]]:
        """Collect quizzes for export"""
        # Mock implementation
        return []
    
    # Helper methods for restore
    def restore_quiz_data(self, data: List[Dict[str, Any]]) -> None:
        """Restore quiz data"""
        # Mock implementation
        pass
    
    def restore_user_data(self, data: List[Dict[str, Any]]) -> None:
        """Restore user data"""
        # Mock implementation
        pass
    
    def restore_progress_data(self, data: List[Dict[str, Any]]) -> None:
        """Restore progress data"""
        # Mock implementation
        pass
    
    def restore_analytics_data(self, data: Dict[str, Any]) -> None:
        """Restore analytics data"""
        # Mock implementation
        pass
    
    def run(self) -> None:
        """Main execution method"""
        args = self.parse_arguments()
        
        if not args.command:
            print("Error: No command specified. Use --help for usage information.")
            sys.exit(1)
        
        try:
            if args.command == 'backup':
                success = self.create_backup(
                    args.output, args.include, args.compress, args.verbose
                )
                
            elif args.command == 'restore':
                success = self.restore_backup(
                    args.input, args.verify, args.dry_run, args.verbose
                )
                
            elif args.command == 'export':
                success = self.export_data(
                    args.type, args.format, args.output, args.date_range, args.verbose
                )
                
            elif args.command == 'cleanup':
                success = self.cleanup_data(
                    args.older_than, args.type, args.dry_run, args.verbose
                )
                
            elif args.command == 'verify':
                success = self.verify_data_integrity(
                    args.type, args.repair, args.verbose
                )
                
            elif args.command == 'migrate':
                print("Migration functionality not implemented yet")
                success = False
                
            else:
                print(f"Unknown command: {args.command}")
                success = False
            
            sys.exit(0 if success else 1)
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

def main():
    """Entry point for the CLI script"""
    cli = DataManagerCLI()
    cli.run()

if __name__ == '__main__':
    main()
