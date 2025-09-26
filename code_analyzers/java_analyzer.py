"""
DevMatch AI - Java Code Analyzer
Advanced Java code analysis focusing on OOP principles, best practices, and performance
"""

import re
import os
from collections import defaultdict

class JavaAnalyzer:
    def __init__(self):
        self.setup_java_patterns()
        self.setup_oop_patterns()
        self.setup_best_practices()
        self.setup_performance_patterns()
    
    def setup_java_patterns(self):
        """Setup Java-specific patterns for analysis"""
        self.java_patterns = {
            'class_structure': {
                'class_declaration': r'(?:public\s+|private\s+|protected\s+)?class\s+(\w+)',
                'interface_declaration': r'(?:public\s+)?interface\s+(\w+)',
                'abstract_class': r'abstract\s+class\s+(\w+)',
                'enum_declaration': r'enum\s+(\w+)',
                'inner_class': r'class\s+\w+.*?{.*?class\s+(\w+)',
                'static_class': r'static\s+class\s+(\w+)'
            },
            'methods': {
                'method_declaration': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(\w+)\s+(\w+)\s*\([^)]*\)',
                'constructor': r'(?:public|private|protected)\s+(\w+)\s*\([^)]*\)\s*{',
                'getter_method': r'(?:public\s+)?(\w+)\s+get(\w+)\s*\(\s*\)',
                'setter_method': r'(?:public\s+)?void\s+set(\w+)\s*\([^)]*\)',
                'main_method': r'public\s+static\s+void\s+main\s*\(\s*String\[\]\s*\w+\s*\)',
                'override_annotation': r'@Override\s*\n\s*(?:public|private|protected)',
                'static_methods': r'(?:public|private|protected)\s+static\s+\w+\s+\w+\s*\('
            },
            'oop_principles': {
                'inheritance': r'class\s+\w+\s+extends\s+(\w+)',
                'interface_implementation': r'class\s+\w+.*?implements\s+([\w\s,]+)',
                'polymorphism': r'@Override|instanceof\s+\w+',
                'encapsulation': r'private\s+\w+\s+\w+',
                'abstraction': r'abstract\s+(?:class|method)',
                'composition': r'private\s+(\w+)\s+\w+\s*=\s*new\s+\1'
            },
            'exception_handling': {
                'try_catch': r'try\s*{.*?}\s*catch\s*\([^)]+\)\s*{',
                'finally_block': r'finally\s*{',
                'throws_declaration': r'throws\s+([\w\s,]+)',
                'custom_exceptions': r'class\s+\w+Exception\s+extends\s+\w*Exception',
                'exception_throwing': r'throw\s+new\s+\w+Exception'
            },
            'collections_and_generics': {
                'generic_usage': r'<\s*\w+(?:\s*,\s*\w+)*\s*>',
                'arraylist_usage': r'ArrayList<\w+>',
                'hashmap_usage': r'HashMap<\w+,\s*\w+>',
                'iterator_usage': r'Iterator<\w+>',
                'enhanced_for_loop': r'for\s*\(\s*\w+\s+\w+\s*:\s*\w+\s*\)',
                'stream_api': r'\.stream\(\)\.(?:map|filter|collect|reduce)'
            }
        }
    
    def setup_oop_patterns(self):
        """Setup OOP principle analysis patterns"""
        self.oop_principles = {
            'encapsulation': {
                'private_fields': r'private\s+\w+\s+\w+',
                'public_getters': r'public\s+\w+\s+get\w+\s*\(\s*\)',
                'public_setters': r'public\s+void\s+set\w+\s*\([^)]+\)',
                'field_access_control': r'(?:private|protected|public)\s+\w+\s+\w+'
            },
            'inheritance': {
                'class_extension': r'class\s+\w+\s+extends\s+\w+',
                'method_overriding': r'@Override',
                'super_calls': r'super\s*\.',
                'abstract_methods': r'abstract\s+\w+\s+\w+\s*\([^)]*\)\s*;'
            },
            'polymorphism': {
                'interface_implementation': r'implements\s+\w+',
                'method_overloading': r'(\w+)\s*\([^)]*\).*?\1\s*\([^)]*\)',
                'instanceof_usage': r'instanceof\s+\w+',
                'dynamic_binding': r'@Override.*?public'
            },
            'abstraction': {
                'abstract_classes': r'abstract\s+class\s+\w+',
                'interfaces': r'interface\s+\w+',
                'abstract_methods': r'abstract\s+\w+\s+\w+\s*\([^)]*\)',
                'interface_methods': r'(?:default\s+|static\s+)?\w+\s+\w+\s*\([^)]*\)\s*(?:{|;)'
            }
        }
    
    def setup_best_practices(self):
        """Setup Java best practices checklist"""
        self.best_practices = {
            'naming_conventions': [
                'Use camelCase for variables and methods',
                'Use PascalCase for class names',
                'Use UPPER_CASE for constants',
                'Use meaningful and descriptive names',
                'Avoid abbreviations and single-letter variables'
            ],
            'code_organization': [
                'One class per file',
                'Organize imports properly',
                'Use packages for namespace management',
                'Follow consistent indentation',
                'Keep methods small and focused'
            ],
            'object_oriented': [
                'Favor composition over inheritance',
                'Program to interfaces, not implementations',
                'Use encapsulation to hide implementation details',
                'Apply SOLID principles',
                'Use design patterns appropriately'
            ],
            'performance': [
                'Use StringBuilder for string concatenation',
                'Prefer ArrayList over Vector',
                'Use enhanced for loops when possible',
                'Close resources properly (try-with-resources)',
                'Avoid creating unnecessary objects'
            ],
            'error_handling': [
                'Use specific exception types',
                'Handle exceptions at appropriate levels',
                'Use try-with-resources for resource management',
                'Document exceptions with @throws',
                'Avoid catching generic Exception'
            ]
        }
    
    def setup_performance_patterns(self):
        """Setup performance analysis patterns"""
        self.performance_issues = {
            'critical': [
                (r'while\s*\(\s*true\s*\)(?!.*break)', 'Infinite loop without break'),
                (r'System\.gc\s*\(\s*\)', 'Explicit garbage collection call'),
                (r'\.equals\s*\(\s*"[^"]*"\s*\)', 'String literal comparison (should use "literal".equals(variable))'),
                (r'new\s+String\s*\([^)]*\)', 'Unnecessary String object creation')
            ],
            'major': [
                (r'\+\s*=.*?"[^"]*"', 'String concatenation in loop (use StringBuilder)'),
                (r'Vector<', 'Using Vector instead of ArrayList'),
                (r'Hashtable<', 'Using Hashtable instead of HashMap'),
                (r'\.size\(\)\s*==\s*0', 'Using size() == 0 instead of isEmpty()')
            ],
            'minor': [
                (r'new\s+Boolean\s*\(', 'Boxing primitive boolean'),
                (r'new\s+Integer\s*\(', 'Boxing primitive int'),
                (r'\.toString\(\)\.equals\(', 'Converting to string for comparison'),
                (r'if\s*\([^)]*!=\s*null\s*&&[^)]*\.equals\(', 'Potential NullPointerException in equals')
            ]
        }
    
    def analyze_java_code(self, content, filepath):
        """Main Java code analysis function"""
        analysis_results = {
            'language': 'Java',
            'file_path': filepath,
            'lines_of_code': len(content.split('\n')),
            'class_analysis': self.analyze_classes(content),
            'oop_analysis': self.analyze_oop_principles(content),
            'method_analysis': self.analyze_methods(content),
            'exception_handling': self.analyze_exception_handling(content),
            'performance_analysis': self.analyze_performance(content),
            'best_practices_score': self.calculate_best_practices_score(content),
            'issues_found': self.find_issues(content),
            'suggestions': self.generate_suggestions(content),
            'complexity_score': self.calculate_complexity(content),
            'maintainability_score': self.calculate_maintainability(content)
        }
        
        # Calculate overall quality score
        analysis_results['quality_score'] = self.calculate_overall_score(analysis_results)
        
        return analysis_results
    
    def analyze_classes(self, content):
        """Analyze class structure and design"""
        class_analysis = {
            'classes_found': [],
            'interfaces_found': [],
            'abstract_classes': [],
            'enums_found': [],
            'inner_classes': [],
            'class_design_score': 0
        }
        
        # Find classes
        classes = re.findall(self.java_patterns['class_structure']['class_declaration'], content)
        class_analysis['classes_found'] = classes
        
        # Find interfaces
        interfaces = re.findall(self.java_patterns['class_structure']['interface_declaration'], content)
        class_analysis['interfaces_found'] = interfaces
        
        # Find abstract classes
        abstract_classes = re.findall(self.java_patterns['class_structure']['abstract_class'], content)
        class_analysis['abstract_classes'] = abstract_classes
        
        # Find enums
        enums = re.findall(self.java_patterns['class_structure']['enum_declaration'], content)
        class_analysis['enums_found'] = enums
        
        # Calculate class design score
        score = 100
        if len(classes) > 1:  # Multiple classes in one file
            score -= 20
        if len(classes) == 0 and len(interfaces) == 0:  # No classes or interfaces
            score -= 50
        
        class_analysis['class_design_score'] = max(0, score)
        
        return class_analysis
    
    def analyze_oop_principles(self, content):
        """Analyze adherence to OOP principles"""
        oop_analysis = {
            'encapsulation_score': 0,
            'inheritance_usage': 0,
            'polymorphism_usage': 0,
            'abstraction_usage': 0,
            'overall_oop_score': 0
        }
        
        # Analyze encapsulation
        private_fields = len(re.findall(self.oop_principles['encapsulation']['private_fields'], content))
        public_getters = len(re.findall(self.oop_principles['encapsulation']['public_getters'], content))
        public_setters = len(re.findall(self.oop_principles['encapsulation']['public_setters'], content))
        
        if private_fields > 0:
            oop_analysis['encapsulation_score'] = min(100, (public_getters + public_setters) / private_fields * 50 + 50)
        
        # Analyze inheritance
        inheritance_patterns = [
            self.oop_principles['inheritance']['class_extension'],
            self.oop_principles['inheritance']['method_overriding'],
            self.oop_principles['inheritance']['super_calls']
        ]
        
        inheritance_count = sum(len(re.findall(pattern, content)) for pattern in inheritance_patterns)
        oop_analysis['inheritance_usage'] = min(100, inheritance_count * 25)
        
        # Analyze polymorphism
        polymorphism_patterns = [
            self.oop_principles['polymorphism']['interface_implementation'],
            self.oop_principles['polymorphism']['method_overloading'],
            self.oop_principles['polymorphism']['instanceof_usage']
        ]
        
        polymorphism_count = sum(len(re.findall(pattern, content)) for pattern in polymorphism_patterns)
        oop_analysis['polymorphism_usage'] = min(100, polymorphism_count * 30)
        
        # Analyze abstraction
        abstraction_patterns = [
            self.oop_principles['abstraction']['abstract_classes'],
            self.oop_principles['abstraction']['interfaces'],
            self.oop_principles['abstraction']['abstract_methods']
        ]
        
        abstraction_count = sum(len(re.findall(pattern, content)) for pattern in abstraction_patterns)
        oop_analysis['abstraction_usage'] = min(100, abstraction_count * 35)
        
        # Calculate overall OOP score
        oop_analysis['overall_oop_score'] = (
            oop_analysis['encapsulation_score'] * 0.3 +
            oop_analysis['inheritance_usage'] * 0.25 +
            oop_analysis['polymorphism_usage'] * 0.25 +
            oop_analysis['abstraction_usage'] * 0.2
        )
        
        return oop_analysis
    
    def analyze_methods(self, content):
        """Analyze method structure and design"""
        method_analysis = {
            'total_methods': 0,
            'constructors': 0,
            'getters_setters': 0,
            'static_methods': 0,
            'overridden_methods': 0,
            'method_design_score': 0
        }
        
        # Count different types of methods
        method_analysis['total_methods'] = len(re.findall(self.java_patterns['methods']['method_declaration'], content))
        method_analysis['constructors'] = len(re.findall(self.java_patterns['methods']['constructor'], content))
        method_analysis['getters_setters'] = (
            len(re.findall(self.java_patterns['methods']['getter_method'], content)) +
            len(re.findall(self.java_patterns['methods']['setter_method'], content))
        )
        method_analysis['static_methods'] = len(re.findall(self.java_patterns['methods']['static_methods'], content))
        method_analysis['overridden_methods'] = len(re.findall(self.java_patterns['methods']['override_annotation'], content))
        
        # Calculate method design score
        if method_analysis['total_methods'] > 0:
            method_analysis['method_design_score'] = min(100, 
                (method_analysis['overridden_methods'] / method_analysis['total_methods']) * 50 + 50)
        else:
            method_analysis['method_design_score'] = 0
        
        return method_analysis
    
    def analyze_exception_handling(self, content):
        """Analyze exception handling practices"""
        exception_analysis = {
            'try_catch_blocks': 0,
            'finally_blocks': 0,
            'throws_declarations': 0,
            'custom_exceptions': 0,
            'exception_handling_score': 0
        }
        
        exception_analysis['try_catch_blocks'] = len(re.findall(self.java_patterns['exception_handling']['try_catch'], content, re.DOTALL))
        exception_analysis['finally_blocks'] = len(re.findall(self.java_patterns['exception_handling']['finally_block'], content))
        exception_analysis['throws_declarations'] = len(re.findall(self.java_patterns['exception_handling']['throws_declaration'], content))
        exception_analysis['custom_exceptions'] = len(re.findall(self.java_patterns['exception_handling']['custom_exceptions'], content))
        
        # Calculate exception handling score
        total_exception_features = (exception_analysis['try_catch_blocks'] + 
                                  exception_analysis['finally_blocks'] + 
                                  exception_analysis['throws_declarations'] + 
                                  exception_analysis['custom_exceptions'])
        
        exception_analysis['exception_handling_score'] = min(100, total_exception_features * 20)
        
        return exception_analysis
    
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
            (r'StringBuilder', 'StringBuilder usage for string concatenation'),
            (r'ArrayList<', 'ArrayList usage (preferred over Vector)'),
            (r'HashMap<', 'HashMap usage (preferred over Hashtable)'),
            (r'for\s*\(\s*\w+\s+\w+\s*:\s*\w+\s*\)', 'Enhanced for loops'),
            (r'try\s*\([^)]+\)\s*{', 'Try-with-resources usage'),
            (r'\.isEmpty\(\)', 'isEmpty() usage instead of size() == 0')
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
    
    def calculate_best_practices_score(self, content):
        """Calculate adherence to Java best practices"""
        score = 100
        
        # Check naming conventions
        if not re.search(r'class\s+[A-Z][a-zA-Z0-9]*', content):
            score -= 10  # Class names should start with uppercase
        
        if re.search(r'[a-z][a-zA-Z0-9]*\s+[A-Z][a-zA-Z0-9]*\s*[=;]', content):
            score -= 10  # Variable names should start with lowercase
        
        # Check for proper exception handling
        if re.search(r'catch\s*\(\s*Exception\s+\w+\s*\)', content):
            score -= 15  # Catching generic Exception
        
        # Check for resource management
        if re.search(r'new\s+File(?:Input|Output)Stream', content) and not re.search(r'try\s*\([^)]+\)', content):
            score -= 20  # Not using try-with-resources
        
        # Check for proper encapsulation
        public_fields = len(re.findall(r'public\s+(?!static\s+final)\w+\s+\w+\s*[=;]', content))
        if public_fields > 0:
            score -= public_fields * 5  # Public fields (not constants)
        
        return max(0, score)
    
    def find_issues(self, content):
        """Find specific code issues"""
        issues = []
        
        # OOP-related issues
        if re.search(r'public\s+\w+\s+\w+\s*[=;]', content) and not re.search(r'public\s+static\s+final', content):
            issues.append({
                'type': 'Encapsulation',
                'severity': 'Medium',
                'description': 'Public fields found (breaks encapsulation)',
                'suggestion': 'Make fields private and provide getter/setter methods'
            })
        
        # Performance issues
        if re.search(r'\+\s*=.*?"[^"]*"', content):
            issues.append({
                'type': 'Performance',
                'severity': 'Medium',
                'description': 'String concatenation in loop',
                'suggestion': 'Use StringBuilder for efficient string concatenation'
            })
        
        # Exception handling issues
        if re.search(r'catch\s*\(\s*Exception\s+\w+\s*\)', content):
            issues.append({
                'type': 'Exception Handling',
                'severity': 'Low',
                'description': 'Catching generic Exception',
                'suggestion': 'Catch specific exception types instead of generic Exception'
            })
        
        return issues
    
    def generate_suggestions(self, content):
        """Generate improvement suggestions"""
        suggestions = []
        
        # OOP suggestions
        if not re.search(r'private\s+\w+\s+\w+', content):
            suggestions.append("Use private fields and provide public getter/setter methods for better encapsulation")
        
        if not re.search(r'@Override', content) and re.search(r'extends\s+\w+', content):
            suggestions.append("Use @Override annotation when overriding methods for better code clarity")
        
        # Performance suggestions
        if re.search(r'Vector<', content):
            suggestions.append("Consider using ArrayList instead of Vector for better performance")
        
        if re.search(r'new\s+String\s*\(', content):
            suggestions.append("Avoid unnecessary String object creation; use string literals directly")
        
        # Modern Java suggestions
        if not re.search(r'for\s*\(\s*\w+\s+\w+\s*:\s*\w+\s*\)', content) and re.search(r'for\s*\(\s*int\s+\w+\s*=', content):
            suggestions.append("Consider using enhanced for loops (for-each) for better readability")
        
        if not re.search(r'try\s*\([^)]+\)', content) and re.search(r'new\s+File(?:Input|Output)Stream', content):
            suggestions.append("Use try-with-resources for automatic resource management")
        
        # Code organization suggestions
        if not re.search(r'package\s+[\w.]+\s*;', content):
            suggestions.append("Organize code in packages for better namespace management")
        
        if not re.search(r'import\s+[\w.]+\s*;', content) and re.search(r'java\.', content):
            suggestions.append("Use import statements instead of fully qualified class names")
        
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
        method_count = len(re.findall(r'(?:public|private|protected)\s+(?:static\s+)?\w+\s+\w+\s*\(', content))
        
        # Calculate score
        score = 100
        if avg_line_length > 120:
            score -= 20
        if comment_ratio < 0.1:
            score -= 15
        if method_count == 0:
            score -= 25
        
        return max(0, score)
    
    def calculate_overall_score(self, analysis_results):
        """Calculate overall code quality score"""
        weights = {
            'oop_principles': 0.30,
            'performance': 0.25,
            'best_practices': 0.20,
            'exception_handling': 0.15,
            'maintainability': 0.10
        }
        
        oop_score = analysis_results['oop_analysis']['overall_oop_score']
        performance_score = analysis_results['performance_analysis']['performance_score']
        practices_score = analysis_results['best_practices_score']
        exception_score = analysis_results['exception_handling']['exception_handling_score']
        maintainability_score = analysis_results['maintainability_score']
        
        overall_score = (
            oop_score * weights['oop_principles'] +
            performance_score * weights['performance'] +
            practices_score * weights['best_practices'] +
            exception_score * weights['exception_handling'] +
            maintainability_score * weights['maintainability']
        )
        
        return round(overall_score)

# Example usage and testing
if __name__ == "__main__":
    analyzer = JavaAnalyzer()
    
    # Test with sample Java code
    sample_java_code = '''
    package com.example.calculator;
    
    import java.util.ArrayList;
    import java.util.List;
    
    /**
     * A simple calculator class demonstrating OOP principles
     */
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
        
        public double subtract(double a, double b) {
            double result = a - b;
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
                double result2 = calc.subtract(result1, 3.0);
                
                System.out.println("Results: " + calc.getHistory());
                System.out.println(calc.toString());
            } catch (Exception e) {
                System.err.println("Error: " + e.getMessage());
            }
        }
    }
    '''
    
    results = analyzer.analyze_java_code(sample_java_code, 'Calculator.java')
    
    print("Java Code Analysis Results:")
    print(f"Quality Score: {results['quality_score']}/100")
    print(f"OOP Score: {results['oop_analysis']['overall_oop_score']:.1f}/100")
    print(f"Performance Score: {results['performance_analysis']['performance_score']}/100")
    print(f"Best Practices Score: {results['best_practices_score']}/100")
    print(f"Exception Handling Score: {results['exception_handling']['exception_handling_score']}/100")
    print(f"Maintainability Score: {results['maintainability_score']}/100")
    
    print(f"\nClasses Found: {results['class_analysis']['classes_found']}")
    print(f"Total Methods: {results['method_analysis']['total_methods']}")
    print(f"Encapsulation Score: {results['oop_analysis']['encapsulation_score']:.1f}/100")
    
    print("\nSuggestions:")
    for suggestion in results['suggestions']:
        print(f"- {suggestion}")