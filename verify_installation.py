#!/usr/bin/env python3
"""
DevMatch AI - Installation Verification Script
Checks that all components are properly installed and working
"""

import os
import sys
import importlib
import sqlite3
from pathlib import Path

def print_header():
    """Print verification header"""
    print("=" * 70)
    print("🧠💼 DevMatch AI - Installation Verification")
    print("=" * 70)
    print("🔍 Checking all components and dependencies...")
    print()

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        'flask',
        'nltk',
        'textblob',
        'sklearn',
        'PyPDF2',
        'python-docx',
        'rarfile',
        'Pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            elif package == 'python-docx':
                importlib.import_module('docx')
            elif package == 'PyPDF2':
                importlib.import_module('PyPDF2')
            elif package == 'Pillow':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"   ✅ {package} - Installed")
        except ImportError:
            print(f"   ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("   🎉 All packages installed!")
        return True

def check_project_structure():
    """Check if all required files and folders exist"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'app.py',
        'setup.py',
        'requirements.txt',
        'COMPLETE_USER_GUIDE.md',
        'PROJECT_STRUCTURE.md'
    ]
    
    required_folders = [
        'frontend',
        'resume_scanner',
        'code_analyzers',
        'job_matcher',
        'portfolio_analyzer',
        'uploads',
        'output_reports'
    ]
    
    missing_files = []
    missing_folders = []
    
    # Check files
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - Found")
        else:
            print(f"   ❌ {file} - Missing")
            missing_files.append(file)
    
    # Check folders
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"   ✅ {folder}/ - Found")
        else:
            print(f"   ❌ {folder}/ - Missing")
            missing_folders.append(folder)
    
    if missing_files or missing_folders:
        print(f"\n⚠️  Missing components found!")
        if missing_files:
            print(f"   Missing files: {', '.join(missing_files)}")
        if missing_folders:
            print(f"   Missing folders: {', '.join(missing_folders)}")
        return False
    else:
        print("   🎉 All files and folders present!")
        return True

def check_modules():
    """Check if all custom modules can be imported"""
    print("\n🧩 Checking custom modules...")
    
    modules_to_check = [
        ('resume_scanner', 'resume_analyzer'),
        ('code_analyzers', 'code_quality_checker'),
        ('code_analyzers', 'cpp_analyzer'),
        ('code_analyzers', 'java_analyzer'),
        ('code_analyzers', 'go_analyzer'),
        ('job_matcher', 'job_recommender'),
        ('portfolio_analyzer', 'portfolio_checker')
    ]
    
    failed_imports = []
    
    for package, module in modules_to_check:
        try:
            mod = importlib.import_module(f'{package}.{module}')
            print(f"   ✅ {package}.{module} - OK")
        except ImportError as e:
            print(f"   ❌ {package}.{module} - Failed: {e}")
            failed_imports.append(f"{package}.{module}")
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("   🎉 All modules import successfully!")
        return True

def check_database():
    """Check database connectivity"""
    print("\n🗄️ Checking database...")
    
    try:
        # Try to connect to database
        conn = sqlite3.connect('devmatch.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✅ Database connected - {len(tables)} tables found")
            for table in tables:
                print(f"      • {table[0]}")
        else:
            print("   ⚠️  Database connected but no tables found")
            print("      Run: python setup.py")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        print("      Run: python setup.py")
        return False

def check_nltk_data():
    """Check NLTK data availability"""
    print("\n📚 Checking NLTK data...")
    
    try:
        import nltk
        
        required_data = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
        missing_data = []
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
                print(f"   ✅ {data} - Available")
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{data}')
                    print(f"   ✅ {data} - Available")
                except LookupError:
                    print(f"   ❌ {data} - Missing")
                    missing_data.append(data)
        
        if missing_data:
            print(f"\n⚠️  Missing NLTK data: {', '.join(missing_data)}")
            print("   Run: python -c \"import nltk; nltk.download('all')\"")
            return False
        else:
            print("   🎉 All NLTK data available!")
            return True
            
    except ImportError:
        print("   ❌ NLTK not installed")
        return False

def test_basic_functionality():
    """Test basic functionality of each component"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test resume analyzer
        from resume_scanner.resume_analyzer import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        print("   ✅ Resume analyzer - OK")
        
        # Test code analyzer
        from code_analyzers.code_quality_checker import CodeQualityChecker
        checker = CodeQualityChecker()
        print("   ✅ Code analyzer - OK")
        
        # Test job matcher
        from job_matcher.job_recommender import JobRecommender
        recommender = JobRecommender()
        print("   ✅ Job matcher - OK")
        
        # Test portfolio analyzer
        from portfolio_analyzer.portfolio_checker import PortfolioAnalyzer
        portfolio = PortfolioAnalyzer()
        print("   ✅ Portfolio analyzer - OK")
        
        print("   🎉 All components functional!")
        return True
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False

def check_web_interface():
    """Check if web interface files are present"""
    print("\n🌐 Checking web interface...")
    
    web_files = [
        'frontend/templates/dashboard.html',
        'frontend/static/css/dashboard.css',
        'frontend/static/js/dashboard.js'
    ]
    
    missing_web_files = []
    
    for file in web_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - Found")
        else:
            print(f"   ❌ {file} - Missing")
            missing_web_files.append(file)
    
    if missing_web_files:
        print(f"\n⚠️  Missing web files: {', '.join(missing_web_files)}")
        return False
    else:
        print("   🎉 Web interface complete!")
        return True

def run_verification():
    """Run complete verification"""
    print_header()
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Project Structure", check_project_structure),
        ("Custom Modules", check_modules),
        ("Database", check_database),
        ("NLTK Data", check_nltk_data),
        ("Basic Functionality", test_basic_functionality),
        ("Web Interface", check_web_interface)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   ❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Verification Results Summary")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 DevMatch AI is fully installed and ready to use!")
        print("\n🚀 Next steps:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:8080")
        print("   3. Start analyzing your resume and code!")
        print("\n📖 For detailed instructions, see: COMPLETE_USER_GUIDE.md")
    else:
        print("\n⚠️  Some components need attention before using DevMatch AI.")
        print("\n🔧 Recommended fixes:")
        
        for check_name, result in results:
            if not result:
                if "Packages" in check_name:
                    print("   • Run: pip install -r requirements.txt")
                elif "NLTK" in check_name:
                    print("   • Run: python -c \"import nltk; nltk.download('all')\"")
                elif "Database" in check_name:
                    print("   • Run: python setup.py")
                elif "Structure" in check_name:
                    print("   • Ensure all files are properly extracted")
    
    return passed == total

if __name__ == "__main__":
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = run_verification()
    exit(0 if success else 1)