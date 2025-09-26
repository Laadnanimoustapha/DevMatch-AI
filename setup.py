#!/usr/bin/env python3
"""
DevMatch AI - Setup Script
Installs dependencies and initializes the application
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🧠💼 DevMatch AI - Setup & Installation")
    print("=" * 60)
    print("Setting up your offline resume & code analyzer platform...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Python dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def download_nlp_models():
    """Download required NLP models"""
    print("\n🧠 Downloading NLP models...")
    
    try:
        # Download NLTK data
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK models downloaded")
        
        # Try to download spaCy model
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("✅ spaCy English model downloaded")
        except subprocess.CalledProcessError:
            print("⚠️  Warning: Could not download spaCy model. Basic NLP features will be used.")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Warning: Error downloading NLP models: {e}")
        print("The application will work with basic NLP features.")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'uploads',
        'output_reports',
        'frontend/static/css',
        'frontend/static/js',
        'frontend/templates',
        'resume_scanner',
        'code_analyzers',
        'job_matcher',
        'portfolio_analyzer'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def initialize_database():
    """Initialize SQLite database"""
    print("\n🗄️  Initializing database...")
    
    try:
        conn = sqlite3.connect('devmatch.db')
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                filename TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                job_data TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def create_init_files():
    """Create __init__.py files for Python modules"""
    print("\n🐍 Creating Python module files...")
    
    modules = [
        'resume_scanner',
        'code_analyzers', 
        'job_matcher',
        'portfolio_analyzer'
    ]
    
    for module in modules:
        init_file = Path(module) / '__init__.py'
        if not init_file.exists():
            init_file.write_text('"""DevMatch AI Module"""')
    
    print("✅ Python modules initialized")

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        from resume_scanner.resume_analyzer import ResumeAnalyzer
        from code_analyzers.code_quality_checker import CodeQualityChecker
        from job_matcher.job_recommender import JobRecommender
        from portfolio_analyzer.portfolio_checker import PortfolioAnalyzer
        
        # Test basic functionality
        analyzer = ResumeAnalyzer()
        checker = CodeQualityChecker()
        recommender = JobRecommender()
        portfolio_analyzer = PortfolioAnalyzer()
        
        print("✅ All modules imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def print_success_message():
    """Print success message with next steps"""
    print("\n" + "=" * 60)
    print("🎉 DevMatch AI Setup Complete!")
    print("=" * 60)
    print()
    print("🚀 To start the application:")
    print("   python app.py")
    print()
    print("🌐 Then open your browser to:")
    print("   http://localhost:8080")
    print()
    print("📊 Features available:")
    print("   • Resume Analysis with ML recommendations")
    print("   • Multi-language code quality checking")
    print("   • Intelligent job matching")
    print("   • Portfolio UI/UX analysis")
    print("   • Export reports and suggestions")
    print()
    print("🔒 Privacy: All processing happens locally!")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create module files
    create_init_files()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Download NLP models
    download_nlp_models()
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Setup failed during database initialization")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Setup completed with warnings. Some features may not work properly.")
    
    # Print success message
    print_success_message()

if __name__ == "__main__":
    main()