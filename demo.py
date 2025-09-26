#!/usr/bin/env python3
"""
DevMatch AI - Complete Platform Demo
Showcase all features: Resume Analysis, Code Quality, Job Matching, Portfolio Analysis
"""

import os
import tempfile
import json
from pathlib import Path

def demo_banner():
    """Display demo banner"""
    print("=" * 80)
    print("🧠💼 DevMatch AI - Complete Platform Demo")
    print("=" * 80)
    print("🚀 An Offline, Cross-Language Resume & Code Analyzer Platform")
    print()
    print("Features demonstrated:")
    print("📝 Resume Analysis with NLP and ML recommendations")
    print("🧪 Multi-language Code Quality Analysis (Python, C++, Java, Go, JS)")
    print("💼 Intelligent Job Matching based on detected skills")
    print("🎨 Portfolio UI/UX Analysis")
    print("📊 Comprehensive reporting and suggestions")
    print("=" * 80)
    print()

def demo_resume_analysis():
    """Demo resume analysis functionality"""
    print("📝 DEMO: Resume Analysis")
    print("-" * 40)
    
    try:
        from resume_scanner import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        
        # Sample resume content
        sample_resume = """
        John Smith
        Senior Software Developer
        Email: john.smith@email.com
        Phone: (555) 123-4567
        
        PROFESSIONAL SUMMARY
        Experienced software developer with 5+ years in full-stack development.
        Expertise in Python, JavaScript, React, Node.js, and cloud technologies.
        
        TECHNICAL SKILLS
        • Programming Languages: Python, JavaScript, TypeScript, Java, Go
        • Frontend: React, Vue.js, HTML5, CSS3, Bootstrap
        • Backend: Node.js, Django, Flask, Express.js
        • Databases: PostgreSQL, MongoDB, Redis
        • Cloud: AWS, Docker, Kubernetes
        • Tools: Git, Jenkins, JIRA
        
        PROFESSIONAL EXPERIENCE
        
        Senior Software Developer | TechCorp Inc. | 2020 - Present
        • Led development of microservices architecture serving 1M+ users
        • Implemented CI/CD pipelines reducing deployment time by 60%
        • Mentored 3 junior developers and conducted code reviews
        • Technologies: Python, React, AWS, Docker, PostgreSQL
        
        Software Developer | StartupXYZ | 2018 - 2020
        • Developed responsive web applications using React and Node.js
        • Optimized database queries improving performance by 40%
        • Collaborated with cross-functional teams in Agile environment
        • Technologies: JavaScript, React, Node.js, MongoDB
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology | 2014 - 2018
        
        CERTIFICATIONS
        • AWS Certified Solutions Architect
        • Certified Kubernetes Administrator
        """
        
        print("Analyzing sample resume...")
        results = analyzer.analyze_content(sample_resume)
        
        print(f"✅ Analysis Complete!")
        print(f"📊 Overall Score: {results['score']}/100")
        print(f"🤖 ATS Score: {results['ats_score']}/100")
        print(f"💼 Experience Level: {results['experience_level']}")
        print(f"📅 Years of Experience: {results['years_experience']}")
        print(f"🔧 Skills Found: {len(results['skills_found'])}")
        print(f"   Top Skills: {', '.join(results['skills_found'][:8])}")
        print(f"📈 Missing Keywords: {len(results['missing_keywords'])}")
        print(f"💡 Suggestions: {len(results['suggestions'])}")
        
        print("\n🎯 Top Improvement Suggestions:")
        for i, suggestion in enumerate(results['suggestions'][:3], 1):
            print(f"   {i}. {suggestion}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resume analysis demo failed: {e}")
        return False

def demo_code_analysis():
    """Demo code analysis for multiple languages"""
    print("\n🧪 DEMO: Multi-Language Code Analysis")
    print("-" * 40)
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Demo different languages
        languages = {
            'Python': {
                'extension': '.py',
                'code': '''
def fibonacci(n):
    """Calculate fibonacci number using memoization."""
    memo = {}
    
    def fib_helper(n):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fib_helper(n-1) + fib_helper(n-2)
        return memo[n]
    
    return fib_helper(n)

class Calculator:
    """A simple calculator with history."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers and store in history."""
        result = a + b
        self.history.append(('add', a, b, result))
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history.copy()

if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(10, 5)
    print(f"Result: {result}")
    print(f"Fibonacci(10): {fibonacci(10)}")
                '''
            },
            'C++': {
                'extension': '.cpp',
                'code': '''
#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>

class Calculator {
private:
    std::vector<double> history;
    
public:
    explicit Calculator() {
        history.reserve(100);
    }
    
    virtual ~Calculator() = default;
    
    double add(const double& a, const double& b) {
        double result = a + b;
        history.push_back(result);
        return result;
    }
    
    const std::vector<double>& getHistory() const {
        return history;
    }
    
    void clearHistory() {
        history.clear();
    }
};

int main() {
    auto calc = std::make_unique<Calculator>();
    
    double result = calc->add(10.5, 5.3);
    std::cout << "Result: " << result << std::endl;
    
    return 0;
}
                '''
            },
            'Java': {
                'extension': '.java',
                'code': '''
package com.devmatch.calculator;

import java.util.ArrayList;
import java.util.List;

public class Calculator {
    private List<Double> history;
    private static final String VERSION = "2.0";
    
    public Calculator() {
        this.history = new ArrayList<>();
    }
    
    public double add(double a, double b) {
        double result = a + b;
        history.add(result);
        return result;
    }
    
    public double multiply(double a, double b) {
        double result = a * b;
        history.add(result);
        return result;
    }
    
    public List<Double> getHistory() {
        return new ArrayList<>(history);
    }
    
    public void clearHistory() {
        history.clear();
    }
    
    @Override
    public String toString() {
        return "Calculator v" + VERSION + " with " + history.size() + " operations";
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        try {
            double result1 = calc.add(10.0, 5.0);
            double result2 = calc.multiply(result1, 2.0);
            
            System.out.println("Results: " + calc.getHistory());
            System.out.println(calc.toString());
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
                '''
            },
            'Go': {
                'extension': '.go',
                'code': '''
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type Calculator struct {
    history []float64
    mutex   sync.RWMutex
}

func NewCalculator() *Calculator {
    return &Calculator{
        history: make([]float64, 0, 100),
    }
}

func (c *Calculator) Add(a, b float64) float64 {
    result := a + b
    
    c.mutex.Lock()
    c.history = append(c.history, result)
    c.mutex.Unlock()
    
    return result
}

func (c *Calculator) GetHistory() []float64 {
    c.mutex.RLock()
    defer c.mutex.RUnlock()
    
    history := make([]float64, len(c.history))
    copy(history, c.history)
    return history
}

func (c *Calculator) ProcessAsync(ctx context.Context, operations <-chan [2]float64, results chan<- float64) {
    defer close(results)
    
    for {
        select {
        case op, ok := <-operations:
            if !ok {
                return
            }
            result := c.Add(op[0], op[1])
            
            select {
            case results <- result:
            case <-ctx.Done():
                return
            }
            
        case <-ctx.Done():
            return
        }
    }
}

func main() {
    calc := NewCalculator()
    
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    operations := make(chan [2]float64, 5)
    results := make(chan float64, 5)
    
    go calc.ProcessAsync(ctx, operations, results)
    
    // Send operations
    operations <- [2]float64{10.5, 5.3}
    operations <- [2]float64{20.0, 3.7}
    close(operations)
    
    // Collect results
    for result := range results {
        fmt.Printf("Result: %.2f\\n", result)
    }
    
    fmt.Printf("History: %v\\n", calc.GetHistory())
}
                '''
            }
        }
        
        for lang_name, lang_data in languages.items():
            print(f"\n🔍 Analyzing {lang_name} code...")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix=lang_data['extension'], delete=False) as f:
                f.write(lang_data['code'])
                temp_file = f.name
            
            try:
                results = checker.analyze_file(temp_file)
                
                print(f"✅ {lang_name} Analysis:")
                print(f"   Quality Score: {results['quality_score']}/100")
                print(f"   Language: {results['language']}")
                print(f"   Lines of Code: {results.get('lines_of_code', 'N/A')}")
                
                # Language-specific metrics
                if lang_name == 'C++' and 'memory_analysis' in results:
                    print(f"   Memory Safety: {results['memory_analysis']['memory_safety_score']}/100")
                elif lang_name == 'Java' and 'oop_analysis' in results:
                    print(f"   OOP Score: {results['oop_analysis']['overall_oop_score']:.1f}/100")
                elif lang_name == 'Go' and 'concurrency_analysis' in results:
                    print(f"   Concurrency Score: {results['concurrency_analysis']['concurrency_score']}/100")
                
                if 'suggestions' in results and results['suggestions']:
                    print(f"   Top Suggestion: {results['suggestions'][0]}")
                
            finally:
                os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Code analysis demo failed: {e}")
        return False

def demo_job_matching():
    """Demo job matching functionality"""
    print("\n💼 DEMO: Intelligent Job Matching")
    print("-" * 40)
    
    try:
        from job_matcher import JobRecommender
        recommender = JobRecommender()
        
        # Sample skills from resume analysis
        detected_skills = [
            'Python', 'JavaScript', 'React', 'Node.js', 'AWS', 
            'Docker', 'PostgreSQL', 'MongoDB', 'Git', 'Django'
        ]
        
        print(f"🔧 Detected Skills: {', '.join(detected_skills)}")
        print("🔍 Finding matching job opportunities...")
        
        # Get job recommendations
        recommendations = recommender.recommend_jobs(detected_skills, 'Senior', 5)
        
        print(f"✅ Found {len(recommendations)} matching opportunities:")
        
        for i, job in enumerate(recommendations, 1):
            print(f"\n   {i}. {job['title']} at {job['company']}")
            print(f"      Match Score: {job['match_score']}%")
            print(f"      Salary: {job['salary_range']}")
            print(f"      Location: {job['location']}")
            print(f"      Required Skills: {', '.join(job['required_skills'][:5])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Job matching demo failed: {e}")
        return False

def demo_portfolio_analysis():
    """Demo portfolio analysis functionality"""
    print("\n🎨 DEMO: Portfolio UI/UX Analysis")
    print("-" * 40)
    
    try:
        from portfolio_analyzer import PortfolioAnalyzer
        analyzer = PortfolioAnalyzer()
        
        # Sample HTML portfolio
        sample_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>John Smith - Portfolio</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <header>
                <nav>
                    <ul>
                        <li><a href="#home">Home</a></li>
                        <li><a href="#about">About</a></li>
                        <li><a href="#projects">Projects</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </nav>
            </header>
            
            <main>
                <section id="home">
                    <h1>Welcome to My Portfolio</h1>
                    <img src="profile.jpg" alt="John Smith - Software Developer">
                    <p>I'm a passionate full-stack developer with expertise in modern web technologies.</p>
                </section>
                
                <section id="projects">
                    <h2>My Projects</h2>
                    <article class="project">
                        <h3>E-commerce Platform</h3>
                        <p>Built with React, Node.js, and PostgreSQL</p>
                    </article>
                    <article class="project">
                        <h3>Task Management App</h3>
                        <p>Developed using Vue.js and Firebase</p>
                    </article>
                </section>
            </main>
            
            <footer>
                <p>&copy; 2024 John Smith. All rights reserved.</p>
            </footer>
        </body>
        </html>
        '''
        
        print("🔍 Analyzing portfolio HTML structure...")
        results = analyzer.analyze_html_file(sample_html, 'portfolio.html')
        
        print("✅ Portfolio Analysis:")
        print(f"   Has DOCTYPE: {results['has_doctype']}")
        print(f"   Mobile Responsive: {results['has_meta_viewport']}")
        print(f"   Semantic HTML Tags: {len(results['semantic_tags'])}")
        print(f"   Accessibility Features: {len(results['accessibility_features'])}")
        print(f"   Images with Alt Text: {results['images']} images found")
        print(f"   Navigation Links: {results['links']} links found")
        
        if results['semantic_tags']:
            print(f"   Semantic Tags Used: {', '.join(results['semantic_tags'])}")
        
        if results['accessibility_features']:
            print(f"   Accessibility Features: {', '.join(results['accessibility_features'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio analysis demo failed: {e}")
        return False

def demo_summary():
    """Display demo summary and next steps"""
    print("\n" + "=" * 80)
    print("🎉 DevMatch AI Demo Complete!")
    print("=" * 80)
    print()
    print("✅ Successfully demonstrated:")
    print("   📝 Resume Analysis with NLP and skill extraction")
    print("   🧪 Multi-language Code Quality Analysis (Python, C++, Java, Go)")
    print("   💼 Intelligent Job Matching based on detected skills")
    print("   🎨 Portfolio UI/UX Analysis with accessibility checks")
    print()
    print("🚀 Ready for Production:")
    print("   • All core features working offline")
    print("   • Advanced language-specific analyzers")
    print("   • ML-powered recommendations")
    print("   • Comprehensive reporting system")
    print()
    print("💰 Monetization Ready:")
    print("   🆓 DevMatch Lite: Resume scanner only")
    print("   💎 DevMatch Pro: Full analyzer + job matcher + export")
    print()
    print("🌐 To start the web interface:")
    print("   python app.py")
    print("   Then open: http://localhost:8080")
    print()
    print("=" * 80)

def run_complete_demo():
    """Run the complete DevMatch AI demo"""
    demo_banner()
    
    demos = [
        ("Resume Analysis", demo_resume_analysis),
        ("Code Analysis", demo_code_analysis),
        ("Job Matching", demo_job_matching),
        ("Portfolio Analysis", demo_portfolio_analysis)
    ]
    
    success_count = 0
    
    for demo_name, demo_func in demos:
        try:
            if demo_func():
                success_count += 1
            else:
                print(f"⚠️  {demo_name} demo had issues")
        except Exception as e:
            print(f"❌ {demo_name} demo failed: {e}")
    
    print(f"\n📊 Demo Results: {success_count}/{len(demos)} features demonstrated successfully")
    
    if success_count == len(demos):
        demo_summary()
    else:
        print("⚠️  Some features need attention before production")
    
    return success_count == len(demos)

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = run_complete_demo()
    exit(0 if success else 1)