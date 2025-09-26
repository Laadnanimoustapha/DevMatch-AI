#!/usr/bin/env python3
"""
DevMatch AI - Application Test Suite
Test all core functionality to ensure everything works
"""

import os
import sys
import json
import tempfile
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from resume_scanner import ResumeAnalyzer
        print("✅ Resume Analyzer imported")
        
        from code_analyzers import CodeQualityChecker
        print("✅ Code Quality Checker imported")
        
        from job_matcher import JobRecommender
        print("✅ Job Recommender imported")
        
        from portfolio_analyzer import PortfolioAnalyzer
        print("✅ Portfolio Analyzer imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_resume_analyzer():
    """Test resume analysis functionality"""
    print("\n📝 Testing Resume Analyzer...")
    
    try:
        from resume_scanner import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        
        # Test basic skill extraction
        sample_text = "I have experience with Python, JavaScript, React, AWS, Docker, SQL, and Git."
        
        # Test the skill extraction directly
        skills = analyzer.extract_skills(sample_text)
        
        if skills and len(skills) > 0:
            print(f"✅ Resume analysis successful - found {len(skills)} skills")
            print(f"   Skills detected: {skills[:5]}")
            return True
        else:
            print("❌ Resume analysis failed - no skills found")
            return False
            
    except Exception as e:
        print(f"❌ Resume analyzer test failed: {e}")
        return False

def test_code_analyzer():
    """Test code quality analysis"""
    print("\n🧪 Testing Code Quality Checker...")
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Test with sample Python code
        sample_code = '''
def fibonacci(n):
    """Calculate fibonacci number using recursion."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    """Simple calculator class."""
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

# Example usage
if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"Result: {result}")
        '''
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(sample_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            
            if results and 'quality_score' in results:
                print(f"✅ Code analysis successful - Quality score: {results['quality_score']}")
                print(f"   Language: {results.get('language', 'Unknown')}")
                return True
            else:
                print("❌ Code analysis failed - no results")
                return False
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ Code analyzer test failed: {e}")
        return False

def test_job_recommender():
    """Test job recommendation functionality"""
    print("\n💼 Testing Job Recommender...")
    
    try:
        from job_matcher import JobRecommender
        recommender = JobRecommender()
        
        # Test with sample skills
        test_skills = ['Python', 'JavaScript', 'React', 'SQL', 'AWS']
        
        recommendations = recommender.recommend_jobs(test_skills, 'Mid-level', 3)
        
        if recommendations and len(recommendations) > 0:
            print(f"✅ Job recommendations successful - found {len(recommendations)} jobs")
            print(f"   Top match: {recommendations[0]['title']} ({recommendations[0]['match_score']}% match)")
            return True
        else:
            print("❌ Job recommendations failed - no results")
            return False
            
    except Exception as e:
        print(f"❌ Job recommender test failed: {e}")
        return False

def test_portfolio_analyzer():
    """Test portfolio analysis functionality"""
    print("\n🎨 Testing Portfolio Analyzer...")
    
    try:
        from portfolio_analyzer import PortfolioAnalyzer
        analyzer = PortfolioAnalyzer()
        
        # Test HTML analysis
        sample_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My Portfolio</title>
        </head>
        <body>
            <header>
                <nav>
                    <ul>
                        <li><a href="#home">Home</a></li>
                        <li><a href="#about">About</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <section id="home">
                    <h1>Welcome</h1>
                    <img src="profile.jpg" alt="Profile picture">
                </section>
            </main>
        </body>
        </html>
        '''
        
        html_analysis = analyzer.analyze_html_file(sample_html, 'index.html')
        
        if html_analysis and 'has_doctype' in html_analysis:
            print(f"✅ Portfolio analysis successful")
            print(f"   Semantic tags found: {len(html_analysis.get('semantic_tags', []))}")
            return True
        else:
            print("❌ Portfolio analysis failed - no results")
            return False
            
    except Exception as e:
        print(f"❌ Portfolio analyzer test failed: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️  Testing Database...")
    
    try:
        import sqlite3
        
        # Check if database exists and has tables
        if os.path.exists('devmatch.db'):
            conn = sqlite3.connect('devmatch.db')
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            conn.close()
            
            if len(tables) >= 3:  # Should have at least 3 tables
                print(f"✅ Database operational - {len(tables)} tables found")
                return True
            else:
                print(f"⚠️  Database exists but missing tables - only {len(tables)} found")
                return False
        else:
            print("❌ Database file not found")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧠💼 DevMatch AI - Application Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Resume Analyzer", test_resume_analyzer),
        ("Code Analyzer", test_code_analyzer),
        ("Job Recommender", test_job_recommender),
        ("Portfolio Analyzer", test_portfolio_analyzer),
        ("Database", test_database)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! DevMatch AI is ready to use.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:8080")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)