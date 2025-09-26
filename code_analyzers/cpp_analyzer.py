"""
DevMatch AI - C++ Code Analyzer
Advanced C++ code quality analysis with performance and memory leak detection
"""

import re
import os
from collections import defaultdict

class CppAnalyzer:
    def __init__(self):
        self.setup_cpp_patterns()
        self.setup_best_practices()
        self.setup_performance_patterns()
    
    def setup_cpp_patterns(self):
        """Setup C++ specific patterns for analysis"""
        self.cpp_patterns = {
            'memory_management': {
                'new_without_delete': r'new\s+\w+.*?(?!.*delete)',
                'malloc_without_free': r'malloc\s*\(.*?(?!.*free)',
                'memory_leaks': r'(?:new|malloc)\s*\([^)]*\)(?!.*(?:delete|free))',
                'double_delete': r'delete\s+\w+.*?delete\s+\w+',
                'use_after_free': r'delete\s+(\w+).*?\1',
                'smart_pointers': r'(?:std::)?(?:unique_ptr|shared_ptr|weak_ptr)',
                'raw_pointers': r'\w+\s*\*\s*\w+\s*=\s*new'
            },
            'performance': {
                'unnecessary_copies': r'(\w+)\s+(\w+)\s*=\s*\1\(',
                'inefficient_loops': r'for\s*\([^)]*\.size\(\)',
                'string_concatenation': r'\+\s*=\s*["\']',
                'vector_push_back_loop': r'for.*push_back',
                'unnecessary_includes': r'#include\s*<iostream>(?!.*cout|.*cin)',
                'magic_numbers': r'\b(?!0|1)\d{2,}\b(?!\s*[;,)])',
                'recursive_calls': r'(\w+)\s*\([^)]*\).*?\1\s*\('
            },
            'best_practices': {
                'const_correctness': r'const\s+\w+',
                'reference_parameters': r'\w+\s*&\s*\w+',
                'initialization_lists': r':\s*\w+\s*\(',
                'virtual_destructors': r'virtual\s+~\w+',
                'override_keyword': r'override\b',
                'nullptr_usage': r'nullptr\b',
                'auto_keyword': r'auto\s+\w+',
                'range_based_loops': r'for\s*\(\s*(?:auto|const\s+auto)\s*&?\s*\w+\s*:\s*\w+\s*\)'
            },
            'modern_cpp': {
                'cpp11_features': r'(?:auto|nullptr|override|final|constexpr|decltype)',
                'cpp14_features': r'(?:std::make_unique|auto\s+\w+\s*=\s*\[)',
                'cpp17_features': r'(?:std::optional|std::variant|if\s*constexpr)',
                'cpp20_features': r'(?:concept|requires|co_await|co_yield)',
                'lambda_expressions': r'\[[^\]]*\]\s*\([^)]*\)\s*(?:mutable\s*)?(?:->\s*\w+\s*)?{',
                'move_semantics': r'std::move\s*\(',
                'perfect_forwarding': r'std::forward\s*<'
            },
            'error_handling': {
                'exception_handling': r'try\s*{.*?}\s*catch',
                'noexcept_specifier': r'noexcept\b',
                'error_codes': r'(?:return\s+)?-?\d+\s*;.*(?:error|fail)',
                'assert_usage': r'assert\s*\(',
                'static_assert': r'static_assert\s*\('
            }
        }
    
    def setup_best_practices(self):
        """Setup C++ best practices checklist"""
        self.best_practices = {
            'memory_safety': [
                'Use smart pointers instead of raw pointers',
                'Always pair new/delete and malloc/free',
                'Avoid memory leaks by proper resource management',
                'Use RAII (Resource Acquisition Is Initialization)',
                'Prefer stack allocation over heap allocation when possible'
            ],
            'performance': [
                'Use const references for function parameters',
                'Avoid unnecessary object copies',
                'Use move semantics for expensive operations',
                'Prefer pre-increment over post-increment',
                'Use reserve() for vectors when size is known',
                'Avoid string concatenation in loops'
            ],
            'modern_cpp': [
                'Use auto for type deduction',
                'Use nullptr instead of NULL',
                'Use range-based for loops',
                'Use override keyword for virtual functions',
                'Use constexpr for compile-time constants',
                'Use lambda expressions where appropriate'
            ],
            'code_organization': [
                'Use header guards or #pragma once',
                'Separate interface from implementation',
                'Use const correctness throughout',
                'Follow consistent naming conventions',
                'Use meaningful variable and function names',
                'Keep functions small and focused'
            ]
        }
    
    def setup_performance_patterns(self):
        """Setup performance analysis patterns"""
        self.performance_issues = {
            'critical': [
                (r'while\s*\(\s*true\s*\)', 'Infinite loop detected'),
                (r'new\s+\w+\[.*?\](?!.*delete\[\])', 'Array new without delete[]'),
                (r'delete\s+\w+(?!\[\]).*new\s+\w+\[', 'delete/delete[] mismatch'),
                (r'(\w+)\s*=\s*\1', 'Self-assignment without check')
            ],
            'major': [
                (r'#include\s*<.*?>.*#include\s*<.*?>', 'Multiple includes of same header'),
                (r'for\s*\([^)]*\.size\(\)', 'Calling size() in loop condition'),
                (r'std::endl', 'Using std::endl instead of \\n'),
                (r'printf\s*\(', 'Using printf instead of iostream')
            ],
            'minor': [
                (r'\+\+\w+', 'Post-increment usage'),
                (r'std::vector<.*?>\s+\w+;.*push_back', 'Vector without reserve'),
                (r'std::string\s+\w+\s*\+=', 'String concatenation in loop'),
                (r'[^a-zA-Z_]0[xX][0-9a-fA-F]+', 'Magic hexadecimal numbers')
            ]
        }
    
    def analyze_cpp_code(self, content, filepath):
        """Main C++ code analysis function"""
        analysis_results = {
            'language': 'C++',
            'file_path': filepath,
            'lines_of_code': len(content.split('\n')),
            'memory_analysis': self.analyze_memory_management(content),
            'performance_analysis': self.analyze_performance(content),
            'modern_cpp_usage': self.analyze_modern_cpp(content),
            'best_practices_score': self.calculate_best_practices_score(content),
            'issues_found': self.find_issues(content),
            'suggestions': self.generate_suggestions(content),
            'complexity_score': self.calculate_complexity(content),
            'maintainability_score': self.calculate_maintainability(content)
        }
        
        # Calculate overall quality score
        analysis_results['quality_score'] = self.calculate_overall_score(analysis_results)
        
        return analysis_results
    
    def analyze_memory_management(self, content):
        """Analyze memory management practices"""
        memory_analysis = {
            'smart_pointers_used': len(re.findall(self.cpp_patterns['memory_management']['smart_pointers'], content)),
            'raw_pointers_found': len(re.findall(self.cpp_patterns['memory_management']['raw_pointers'], content)),
            'potential_leaks': [],
            'memory_safety_score': 0
        }
        
        # Check for potential memory leaks
        new_calls = re.findall(r'new\s+\w+', content)
        delete_calls = re.findall(r'delete\s+\w+', content)
        
        if len(new_calls) > len(delete_calls):
            memory_analysis['potential_leaks'].append(f"Found {len(new_calls)} 'new' calls but only {len(delete_calls)} 'delete' calls")
        
        # Check for malloc/free pairs
        malloc_calls = len(re.findall(r'malloc\s*\(', content))
        free_calls = len(re.findall(r'free\s*\(', content))
        
        if malloc_calls > free_calls:
            memory_analysis['potential_leaks'].append(f"Found {malloc_calls} 'malloc' calls but only {free_calls} 'free' calls")
        
        # Calculate memory safety score
        total_allocations = len(new_calls) + malloc_calls
        if total_allocations == 0:
            memory_analysis['memory_safety_score'] = 100
        else:
            smart_pointer_ratio = memory_analysis['smart_pointers_used'] / max(total_allocations, 1)
            leak_penalty = len(memory_analysis['potential_leaks']) * 20
            memory_analysis['memory_safety_score'] = max(0, 100 - leak_penalty + (smart_pointer_ratio * 30))
        
        return memory_analysis
    
    def analyze_performance(self, content):
        """Analyze performance-related code patterns"""
        performance_analysis = {
            'issues': [],
            'optimizations_found': [],
            'performance_score': 100
        }
        
        # Check for performance issues
        for severity, patterns in self.performance_issues.items():
            for pattern, description in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    performance_analysis['issues'].append({
                        'severity': severity,
                        'description': description,
                        'count': len(matches),
                        'pattern': pattern
                    })
        
        # Check for performance optimizations
        optimizations = [
            (r'const\s+\w+\s*&', 'Const reference parameters used'),
            (r'std::move\s*\(', 'Move semantics utilized'),
            (r'\.reserve\s*\(', 'Vector reserve() used'),
            (r'constexpr\s+', 'Compile-time constants used'),
            (r'inline\s+', 'Inline functions used')
        ]
        
        for pattern, description in optimizations:
            if re.search(pattern, content):
                performance_analysis['optimizations_found'].append(description)
        
        # Calculate performance score
        critical_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'critical')
        major_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'major')
        minor_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'minor')
        
        performance_analysis['performance_score'] = max(0, 100 - (critical_issues * 30) - (major_issues * 15) - (minor_issues * 5))
        
        return performance_analysis
    
    def analyze_modern_cpp(self, content):
        """Analyze usage of modern C++ features"""
        modern_cpp_analysis = {
            'cpp11_features': [],
            'cpp14_features': [],
            'cpp17_features': [],
            'cpp20_features': [],
            'modernization_score': 0
        }
        
        # Check for C++11 features
        cpp11_patterns = [
            (r'auto\s+\w+', 'Auto type deduction'),
            (r'nullptr\b', 'nullptr usage'),
            (r'override\b', 'Override specifier'),
            (r'\[[^\]]*\]\s*\([^)]*\)', 'Lambda expressions'),
            (r'constexpr\s+', 'constexpr usage'),
            (r'std::unique_ptr|std::shared_ptr', 'Smart pointers'),
            (r'for\s*\(\s*auto.*?:', 'Range-based for loops')
        ]
        
        for pattern, feature in cpp11_patterns:
            if re.search(pattern, content):
                modern_cpp_analysis['cpp11_features'].append(feature)
        
        # Check for C++14 features
        cpp14_patterns = [
            (r'std::make_unique', 'make_unique usage'),
            (r'auto\s+\w+\s*=\s*\[', 'Generic lambdas'),
            (r'constexpr\s+(?!const)', 'Relaxed constexpr')
        ]
        
        for pattern, feature in cpp14_patterns:
            if re.search(pattern, content):
                modern_cpp_analysis['cpp14_features'].append(feature)
        
        # Check for C++17 features
        cpp17_patterns = [
            (r'std::optional', 'std::optional usage'),
            (r'std::variant', 'std::variant usage'),
            (r'if\s*constexpr', 'constexpr if'),
            (r'auto\s*\[.*?\]', 'Structured bindings')
        ]
        
        for pattern, feature in cpp17_patterns:
            if re.search(pattern, content):
                modern_cpp_analysis['cpp17_features'].append(feature)
        
        # Calculate modernization score
        total_features = (len(modern_cpp_analysis['cpp11_features']) + 
                         len(modern_cpp_analysis['cpp14_features']) + 
                         len(modern_cpp_analysis['cpp17_features']) + 
                         len(modern_cpp_analysis['cpp20_features']))
        
        modern_cpp_analysis['modernization_score'] = min(100, total_features * 10)
        
        return modern_cpp_analysis
    
    def calculate_best_practices_score(self, content):
        """Calculate adherence to C++ best practices"""
        score = 100
        
        # Check for common best practices
        practices = [
            (r'const\s+\w+', 'Const correctness', 10),
            (r'#pragma\s+once|#ifndef.*#define.*#endif', 'Header guards', 15),
            (r'virtual\s+~\w+', 'Virtual destructors', 10),
            (r'explicit\s+\w+\s*\(', 'Explicit constructors', 10),
            (r'namespace\s+\w+', 'Namespace usage', 10),
            (r'//.*|/\*.*?\*/', 'Code comments', 5)
        ]
        
        for pattern, practice, points in practices:
            if not re.search(pattern, content, re.DOTALL):
                score -= points
        
        return max(0, score)
    
    def find_issues(self, content):
        """Find specific code issues"""
        issues = []
        
        # Memory-related issues
        if re.search(r'new\s+\w+(?!.*delete)', content):
            issues.append({
                'type': 'Memory Leak',
                'severity': 'High',
                'description': 'Potential memory leak: new without corresponding delete',
                'suggestion': 'Use smart pointers or ensure proper delete calls'
            })
        
        # Performance issues
        if re.search(r'for\s*\([^)]*\.size\(\)', content):
            issues.append({
                'type': 'Performance',
                'severity': 'Medium',
                'description': 'Calling size() in loop condition',
                'suggestion': 'Store size() result in a variable before the loop'
            })
        
        # Modern C++ issues
        if re.search(r'NULL\b', content) and not re.search(r'nullptr\b', content):
            issues.append({
                'type': 'Modernization',
                'severity': 'Low',
                'description': 'Using NULL instead of nullptr',
                'suggestion': 'Replace NULL with nullptr for better type safety'
            })
        
        return issues
    
    def generate_suggestions(self, content):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Memory management suggestions
        if re.search(r'new\s+\w+', content) and not re.search(r'std::(?:unique_ptr|shared_ptr)', content):
            suggestions.append("Consider using smart pointers (std::unique_ptr, std::shared_ptr) for automatic memory management")
        
        # Performance suggestions
        if re.search(r'std::endl', content):
            suggestions.append("Replace std::endl with '\\n' for better performance unless buffer flushing is needed")
        
        if re.search(r'std::vector.*push_back', content) and not re.search(r'\.reserve\s*\(', content):
            suggestions.append("Use vector.reserve() when the final size is known to avoid reallocations")
        
        # Modern C++ suggestions
        if not re.search(r'auto\s+\w+', content):
            suggestions.append("Consider using 'auto' for type deduction to improve code maintainability")
        
        if not re.search(r'constexpr\s+', content):
            suggestions.append("Use 'constexpr' for compile-time constants and functions when possible")
        
        # Code organization suggestions
        if not re.search(r'namespace\s+\w+', content):
            suggestions.append("Consider organizing code in namespaces to avoid naming conflicts")
        
        return suggestions[:8]  # Limit to top 8 suggestions
    
    def calculate_complexity(self, content):
        """Calculate cyclomatic complexity"""
        complexity_keywords = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', 
            r'\bswitch\b', r'\bcase\b', r'\bcatch\b', r'\b\?\s*.*?:', 
            r'\b&&\b', r'\b\|\|\b'
        ]
        
        complexity = 1  # Base complexity
        for keyword in complexity_keywords:
            complexity += len(re.findall(keyword, content))
        
        return min(complexity, 50)  # Cap at 50
    
    def calculate_maintainability(self, content):
        """Calculate maintainability score"""
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Factors affecting maintainability
        avg_line_length = sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1)
        comment_ratio = len([line for line in lines if line.strip().startswith('//')]) / max(len(non_empty_lines), 1)
        function_count = len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*{', content))
        
        # Calculate score
        score = 100
        if avg_line_length > 100:
            score -= 20
        if comment_ratio < 0.1:
            score -= 15
        if function_count == 0:
            score -= 25
        
        return max(0, score)
    
    def calculate_overall_score(self, analysis_results):
        """Calculate overall code quality score"""
        weights = {
            'memory_safety': 0.25,
            'performance': 0.25,
            'modern_cpp': 0.20,
            'best_practices': 0.15,
            'maintainability': 0.15
        }
        
        memory_score = analysis_results['memory_analysis']['memory_safety_score']
        performance_score = analysis_results['performance_analysis']['performance_score']
        modern_score = analysis_results['modern_cpp_usage']['modernization_score']
        practices_score = analysis_results['best_practices_score']
        maintainability_score = analysis_results['maintainability_score']
        
        overall_score = (
            memory_score * weights['memory_safety'] +
            performance_score * weights['performance'] +
            modern_score * weights['modern_cpp'] +
            practices_score * weights['best_practices'] +
            maintainability_score * weights['maintainability']
        )
        
        return round(overall_score)

# Example usage and testing
if __name__ == "__main__":
    analyzer = CppAnalyzer()
    
    # Test with sample C++ code
    sample_cpp_code = '''
    #include <iostream>
    #include <vector>
    #include <memory>
    
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
        
        auto getHistory() const -> const std::vector<int>& {
            return history;
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
    
    results = analyzer.analyze_cpp_code(sample_cpp_code, 'test.cpp')
    
    print("C++ Code Analysis Results:")
    print(f"Quality Score: {results['quality_score']}/100")
    print(f"Memory Safety Score: {results['memory_analysis']['memory_safety_score']}/100")
    print(f"Performance Score: {results['performance_analysis']['performance_score']}/100")
    print(f"Modern C++ Score: {results['modern_cpp_usage']['modernization_score']}/100")
    print(f"Best Practices Score: {results['best_practices_score']}/100")
    print(f"Maintainability Score: {results['maintainability_score']}/100")
    
    print("\nSuggestions:")
    for suggestion in results['suggestions']:
        print(f"- {suggestion}")