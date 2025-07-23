#!/usr/bin/env python
"""
AI Learning Generator Setup
===========================

An AI-powered educational content generation platform that creates
interactive quizzes, learning materials, and assessments using OpenAI's GPT models.

Features:
- Dynamic quiz generation from text content
- Multiple question types (multiple choice, true/false, short answer)
- Interactive web interface
- RESTful API for integration
- Comprehensive testing suite
- CLI tools for batch operations
"""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
def get_version():
    """Extract version from package __init__.py"""
    init_py = os.path.join(os.path.dirname(__file__), 'ai_learning_generator', '__init__.py')
    if os.path.exists(init_py):
        with open(init_py, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content)
            if match:
                return match.group(1)
    return '1.0.0'

# Read long description from README
def get_long_description():
    """Get long description from README file"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements from requirements.txt
def get_requirements():
    """Parse requirements from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments, empty lines, and optional dependencies
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Remove inline comments
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    requirements.append(line)
    
    return requirements

# Development dependencies
dev_requirements = [
    'pytest>=7.0.0',
    'pytest-cov>=4.0.0',
    'pytest-mock>=3.10.0',
    'black>=23.0.0',
    'flake8>=6.0.0',
    'isort>=5.12.0',
    'mypy>=1.0.0',
    'pre-commit>=3.0.0',
    'sphinx>=7.0.0',
    'sphinx-rtd-theme>=1.3.0',
]

# Production dependencies
prod_requirements = [
    'gunicorn>=21.0.0',
    'redis>=5.0.0',
    'psycopg2-binary>=2.9.0',
    'sentry-sdk>=1.30.0',
]

setup(
    # Basic package information
    name='ai-learning-generator',
    version=get_version(),
    author='AI Learning Generator Team',
    author_email='contact@ai-learning-generator.com',
    description='AI-powered educational content generation platform',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ai-learning-generator',
    
    # Package discovery
    packages=find_packages(exclude=['tests', 'tests.*']),
    
    # Include non-Python files
    include_package_data=True,
    package_data={
        'ai_learning_generator': [
            'templates/*.html',
            'static/css/*.css',
            'static/js/*.js',
            'static/images/*',
            'config/*.yaml',
            'config/*.json',
        ],
    },
    
    # Python version requirement
    python_requires='>=3.8',
    
    # Dependencies
    install_requires=get_requirements(),
    extras_require={
        'dev': dev_requirements,
        'prod': prod_requirements,
        'all': dev_requirements + prod_requirements,
    },
    
    # Console scripts
    entry_points={
        'console_scripts': [
            'ai-quiz-generator=scripts.generate_quiz:main',
            'ai-data-manager=scripts.data_manager:main',
            'ai-learning-server=app:main',
        ],
    },
    
    # Classification
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: JavaScript',
        'Framework :: Flask',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Natural Language :: Italian',
    ],
    
    # Keywords for PyPI search
    keywords=[
        'ai', 'education', 'quiz', 'learning', 'openai', 'gpt',
        'flask', 'web', 'api', 'machine-learning', 'nlp',
        'educational-technology', 'content-generation', 'assessment'
    ],
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/ai-learning-generator/issues',
        'Source': 'https://github.com/yourusername/ai-learning-generator',
        'Documentation': 'https://ai-learning-generator.readthedocs.io/',
        'Funding': 'https://github.com/sponsors/yourusername',
    },
    
    # License
    license='MIT',
    
    # Zip safety
    zip_safe=False,
)
