#!/usr/bin/env python3
"""
DevMatch AI - Enhanced Analyzers Test Suite
Test the new C++, Java, and Go analyzers
"""

import os
import tempfile
from pathlib import Path

def test_cpp_analyzer():
    """Test the C++ analyzer"""
    print("🧪 Testing Enhanced C++ Analyzer...")
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Sample C++ code
        cpp_code = '''
        #include <iostream>
        #include <memory>
        #include <vector>
        
        class Calculator {
        private:
            std::vector<int> history;
            
        public:
            explicit Calculator() {
                history.reserve(100);
            }
            
            virtual ~Calculator() = default;
            
            int add(const int& a, const int& b) const {
                return a + b;
            }
            
            void storeResult(int result) {
                history.push_back(result);
            }
        };
        
        int main() {
            auto calc = std::make_unique<Calculator>();
            int result = calc->add(5, 3);
            calc->storeResult(result);
            
            std::cout << "Result: " << result << std::endl;
            return 0;
        }
        '''
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(cpp_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            
            if results and 'quality_score' in results:
                print(f"✅ C++ analysis successful - Quality score: {results['quality_score']}")
                if 'memory_analysis' in results:
                    print(f"   Memory safety score: {results['memory_analysis']['memory_safety_score']}")
                if 'performance_analysis' in results:
                    print(f"   Performance score: {results['performance_analysis']['performance_score']}")
                return True
            else:
                print("❌ C++ analysis failed - no advanced results")
                return False
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ C++ analyzer test failed: {e}")
        return False

def test_java_analyzer():
    """Test the Java analyzer"""
    print("\n☕ Testing Enhanced Java Analyzer...")
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Sample Java code
        java_code = '''
        package com.example.calculator;
        
        import java.util.ArrayList;
        import java.util.List;
        
        public class Calculator {
            private List<Double> history;
            private static final String VERSION = "1.0";
            
            public Calculator() {
                this.history = new ArrayList<>();
            }
            
            public double add(double a, double b) {
                double result = a + b;
                history.add(result);
                return result;
            }
            
            public List<Double> getHistory() {
                return new ArrayList<>(history);
            }
            
            @Override
            public String toString() {
                return "Calculator v" + VERSION;
            }
            
            public static void main(String[] args) {
                Calculator calc = new Calculator();
                
                try {
                    double result = calc.add(10.0, 5.0);
                    System.out.println("Result: " + result);
                } catch (Exception e) {
                    System.err.println("Error: " + e.getMessage());
                }
            }
        }
        '''
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            
            if results and 'quality_score' in results:
                print(f"✅ Java analysis successful - Quality score: {results['quality_score']}")
                if 'oop_analysis' in results:
                    print(f"   OOP score: {results['oop_analysis']['overall_oop_score']:.1f}")
                if 'class_analysis' in results:
                    print(f"   Classes found: {len(results['class_analysis']['classes_found'])}")
                return True
            else:
                print("❌ Java analysis failed - no advanced results")
                return False
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ Java analyzer test failed: {e}")
        return False

def test_go_analyzer():
    """Test the Go analyzer"""
    print("\n🐹 Testing Enhanced Go Analyzer...")
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Sample Go code
        go_code = '''
        package main
        
        import (
            "context"
            "fmt"
            "sync"
            "time"
        )
        
        type Worker struct {
            id   int
            jobs <-chan int
            results chan<- int
            wg   *sync.WaitGroup
        }
        
        func NewWorker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) *Worker {
            return &Worker{
                id:      id,
                jobs:    jobs,
                results: results,
                wg:      wg,
            }
        }
        
        func (w *Worker) Start(ctx context.Context) {
            defer w.wg.Done()
            
            for {
                select {
                case job, ok := <-w.jobs:
                    if !ok {
                        return
                    }
                    
                    result := job * 2
                    
                    select {
                    case w.results <- result:
                    case <-ctx.Done():
                        return
                    }
                    
                case <-ctx.Done():
                    return
                }
            }
        }
        
        func main() {
            const numWorkers = 3
            const numJobs = 5
            
            jobs := make(chan int, numJobs)
            results := make(chan int, numJobs)
            
            ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
            defer cancel()
            
            var wg sync.WaitGroup
            
            for i := 1; i <= numWorkers; i++ {
                wg.Add(1)
                worker := NewWorker(i, jobs, results, &wg)
                go worker.Start(ctx)
            }
            
            for j := 1; j <= numJobs; j++ {
                jobs <- j
            }
            close(jobs)
            
            go func() {
                wg.Wait()
                close(results)
            }()
            
            for result := range results {
                fmt.Printf("Result: %d\\n", result)
            }
        }
        '''
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write(go_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            
            if results and 'quality_score' in results:
                print(f"✅ Go analysis successful - Quality score: {results['quality_score']}")
                if 'concurrency_analysis' in results:
                    print(f"   Concurrency score: {results['concurrency_analysis']['concurrency_score']}")
                    print(f"   Goroutines: {results['concurrency_analysis']['goroutines_used']}")
                    print(f"   Channels: {results['concurrency_analysis']['channels_used']}")
                if 'package_analysis' in results:
                    print(f"   Package: {results['package_analysis']['package_name']}")
                return True
            else:
                print("❌ Go analysis failed - no advanced results")
                return False
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ Go analyzer test failed: {e}")
        return False

def test_basic_analyzers():
    """Test that basic analyzers still work"""
    print("\n🔧 Testing Basic Analyzers...")
    
    try:
        from code_analyzers import CodeQualityChecker
        checker = CodeQualityChecker()
        
        # Test Python
        python_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(python_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            if results and 'quality_score' in results:
                print(f"✅ Python analysis: {results['quality_score']}")
            else:
                print("❌ Python analysis failed")
                return False
        finally:
            os.unlink(temp_file)
        
        # Test JavaScript
        js_code = '''
        class Calculator {
            constructor() {
                this.history = [];
            }
            
            add(a, b) {
                const result = a + b;
                this.history.push(result);
                return result;
            }
            
            getHistory() {
                return [...this.history];
            }
        }
        
        const calc = new Calculator();
        console.log(calc.add(5, 3));
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(js_code)
            temp_file = f.name
        
        try:
            results = checker.analyze_file(temp_file)
            if results and 'quality_score' in results:
                print(f"✅ JavaScript analysis: {results['quality_score']}")
            else:
                print("❌ JavaScript analysis failed")
                return False
        finally:
            os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Basic analyzers test failed: {e}")
        return False

def run_enhanced_tests():
    """Run all enhanced analyzer tests"""
    print("🧠💼 DevMatch AI - Enhanced Analyzers Test Suite")
    print("=" * 60)
    
    tests = [
        ("C++ Analyzer", test_cpp_analyzer),
        ("Java Analyzer", test_java_analyzer),
        ("Go Analyzer", test_go_analyzer),
        ("Basic Analyzers", test_basic_analyzers)
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
    print("\n" + "=" * 60)
    print("📊 Enhanced Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 All enhanced analyzers are working perfectly!")
        print("\n🚀 DevMatch AI now supports:")
        print("   • Advanced C++ analysis (memory, performance, modern C++)")
        print("   • Advanced Java analysis (OOP principles, best practices)")
        print("   • Advanced Go analysis (concurrency, error handling, idioms)")
        print("   • Multi-language code quality assessment")
    else:
        print("⚠️  Some enhanced analyzers need attention.")
    
    return passed == total

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = run_enhanced_tests()
    exit(0 if success else 1)