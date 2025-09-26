"""
DevMatch AI - Code Quality Checker
Multi-language code analysis with custom analyzers for each language
"""

import os
import re
import ast
import json
import subprocess
from datetime import datetime
from collections import defaultdict, Counter

class CodeQualityChecker:
    def __init__(self):
        self.setup_analyzers()
        self.load_best_practices()
        self.setup_language_specific_analyzers()
    
    def setup_analyzers(self):
        """Initialize language-specific analyzers"""
        self.analyzers = {
            'py': self.analyze_python,
            'cpp': self.analyze_cpp,
            'c': self.analyze_cpp,
            'h': self.analyze_cpp,
            'hpp': self.analyze_cpp,
            'java': self.analyze_java,
            'go': self.analyze_go,
            'js': self.analyze_javascript,
            'ts': self.analyze_javascript,
            'html': self.analyze_html,
            'css': self.analyze_css
        }
    
    def setup_language_specific_analyzers(self):
        """Setup advanced language-specific analyzers"""
        try:
            from .cpp_analyzer import CppAnalyzer
            self.cpp_analyzer = CppAnalyzer()
        except ImportError:
            self.cpp_analyzer = None
            
        try:
            from .java_analyzer import JavaAnalyzer
            self.java_analyzer = JavaAnalyzer()
        except ImportError:
            self.java_analyzer = None
            
        try:
            from .go_analyzer import GoAnalyzer
            self.go_analyzer = GoAnalyzer()
        except ImportError:
            self.go_analyzer = None
    
    def load_best_practices(self):
        """Load best practices for each language"""
        self.best_practices = {
            'python': {
                'naming_convention': r'^[a-z_][a-z0-9_]*$',
                'class_naming': r'^[A-Z][a-zA-Z0-9]*$',
                'constant_naming': r'^[A-Z_][A-Z0-9_]*$',
                'max_line_length': 79,
                'max_function_length': 50,
                'max_complexity': 10
            },
            'cpp': {
                'naming_convention': r'^[a-z_][a-z0-9_]*$',
                'class_naming': r'^[A-Z][a-zA-Z0-9]*$',
                'max_line_length': 100,
                'max_function_length': 60,
                'max_complexity': 15
            },
            'java': {
                'naming_convention': r'^[a-z][a-zA-Z0-9]*$',
                'class_naming': r'^[A-Z][a-zA-Z0-9]*$',
                'constant_naming': r'^[A-Z_][A-Z0-9_]*$',
                'max_line_length': 120,
                'max_function_length': 50,
                'max_complexity': 10
            },
            'go': {
                'naming_convention': r'^[a-z][a-zA-Z0-9]*$',
                'max_line_length': 100,
                'max_function_length': 50,
                'max_complexity': 10
            },
            'javascript': {
                'naming_convention': r'^[a-z][a-zA-Z0-9]*$',
                'class_naming': r'^[A-Z][a-zA-Z0-9]*$',
                'constant_naming': r'^[A-Z_][A-Z0-9_]*$',
                'max_line_length': 100,
                'max_function_length': 40,
                'max_complexity': 10
            }
        }
    
    def analyze_file(self, filepath):
        """Main analysis function for any code file"""
        try:
            file_ext = os.path.splitext(filepath)[1][1:].lower()
            
            if file_ext not in self.analyzers:
                return self.get_error_result(f"Unsupported file type: {file_ext}")
            
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Basic metrics
            basic_metrics = self.calculate_basic_metrics(content)
            
            # Language-specific analysis
            analyzer = self.analyzers[file_ext]
            specific_analysis = analyzer(content, filepath)
            
            # Combine results
            results = {
                'filename': os.path.basename(filepath),
                'language': self.get_language_name(file_ext),
                'file_size': len(content),
                'analysis_date': datetime.now().isoformat(),
                **basic_metrics,
                **specific_analysis
            }
            
            # Calculate overall quality score
            results['quality_score'] = self.calculate_quality_score(results)
            
            return results
            
        except Exception as e:
            return self.get_error_result(f"Analysis failed: {str(e)}")
    
    def get_language_name(self, ext):
        """Get full language name from extension"""
        language_map = {
            'py': 'Python',
            'cpp': 'C++',
            'c': 'C',
            'h': 'C/C++',
            'hpp': 'C++',
            'java': 'Java',
            'go': 'Go',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'html': 'HTML',
            'css': 'CSS'
        }
        return language_map.get(ext, ext.upper())
    
    def calculate_basic_metrics(self, content):
        """Calculate basic code metrics"""
        lines = content.split('\n')
        
        # Line counts
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = self.count_comment_lines(lines)
        code_lines = total_lines - blank_lines - comment_lines
        
        # Character and word counts
        total_chars = len(content)
        total_words = len(content.split())
        
        # Average line length
        non_empty_lines = [line for line in lines if line.strip()]
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'blank_lines': blank_lines,
            'comment_lines': comment_lines,
            'total_chars': total_chars,
            'total_words': total_words,
            'avg_line_length': round(avg_line_length, 2),
            'comment_ratio': round((comment_lines / total_lines) * 100, 2) if total_lines > 0 else 0
        }
    
    def count_comment_lines(self, lines):
        """Count comment lines (basic implementation)"""
        comment_count = 0
        in_block_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Single line comments
            if (stripped.startswith('//') or 
                stripped.startswith('#') or 
                stripped.startswith('<!--')):
                comment_count += 1
            
            # Block comments (basic detection)
            elif '/*' in stripped or '"""' in stripped or "'''" in stripped:
                comment_count += 1
                if '*/' not in stripped and '"""' not in stripped[3:] and "'''" not in stripped[3:]:
                    in_block_comment = True
            
            elif in_block_comment:
                comment_count += 1
                if '*/' in stripped or '"""' in stripped or "'''" in stripped:
                    in_block_comment = False
        
        return comment_count
    
    def analyze_python(self, content, filepath):
        """Analyze Python code"""
        issues = []
        best_practices = []
        
        try:
            # Parse AST for deeper analysis
            tree = ast.parse(content)
            
            # Analyze AST
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
            
            # Function analysis
            for func in functions:
                func_lines = func.end_lineno - func.lineno if hasattr(func, 'end_lineno') else 0
                if func_lines > self.best_practices['python']['max_function_length']:
                    issues.append(f"Function '{func.name}' is too long ({func_lines} lines)")
                
                # Check naming convention
                if not re.match(self.best_practices['python']['naming_convention'], func.name):
                    issues.append(f"Function '{func.name}' doesn't follow naming convention")
                else:
                    best_practices.append(f"Good naming convention for function '{func.name}'")
            
            # Class analysis
            for cls in classes:
                if not re.match(self.best_practices['python']['class_naming'], cls.name):
                    issues.append(f"Class '{cls.name}' doesn't follow naming convention")
                else:
                    best_practices.append(f"Good naming convention for class '{cls.name}'")
            
            # Import analysis
            if len(imports) > 20:
                issues.append("Too many imports - consider organizing them")
            elif imports:
                best_practices.append("Imports are present and organized")
            
            # Check for common Python patterns
            content_lower = content.lower()
            
            # Check for list comprehensions
            if '[' in content and 'for' in content and 'in' in content:
                best_practices.append("Uses list comprehensions - good Python practice")
            
            # Check for context managers
            if 'with open' in content:
                best_practices.append("Uses context managers for file handling")
            
            # Check for exception handling
            if 'try:' in content and 'except' in content:
                best_practices.append("Includes proper exception handling")
            
            # Check for docstrings
            if '"""' in content or "'''" in content:
                best_practices.append("Includes docstrings for documentation")
            
        except SyntaxError as e:
            issues.append(f"Syntax error: {str(e)}")
        except Exception as e:
            issues.append(f"Analysis error: {str(e)}")
        
        # Line length check
        lines = content.split('\n')
        long_lines = [i+1 for i, line in enumerate(lines) 
                     if len(line) > self.best_practices['python']['max_line_length']]
        if long_lines:
            issues.append(f"Lines too long: {long_lines[:5]}")  # Show first 5
        
        return {
            'functions_count': len(functions) if 'functions' in locals() else 0,
            'classes_count': len(classes) if 'classes' in locals() else 0,
            'imports_count': len(imports) if 'imports' in locals() else 0,
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': self.calculate_complexity_score(content, 'python'),
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_cpp(self, content, filepath):
        """Analyze C++ code using advanced analyzer"""
        # Use advanced C++ analyzer if available
        if self.cpp_analyzer:
            try:
                return self.cpp_analyzer.analyze_cpp_code(content, filepath)
            except Exception as e:
                print(f"Advanced C++ analysis failed: {e}, falling back to basic analysis")
        
        # Fallback to basic analysis
        issues = []
        best_practices = []
        
        # Basic C++ analysis
        lines = content.split('\n')
        
        # Check for includes
        includes = [line for line in lines if line.strip().startswith('#include')]
        if includes:
            best_practices.append(f"Proper use of includes ({len(includes)} found)")
        
        # Check for memory management
        if 'new' in content and 'delete' not in content:
            issues.append("Memory allocation found without corresponding deallocation")
        elif 'new' in content and 'delete' in content:
            best_practices.append("Proper memory management with new/delete")
        
        # Check for smart pointers
        smart_pointers = ['unique_ptr', 'shared_ptr', 'weak_ptr']
        if any(ptr in content for ptr in smart_pointers):
            best_practices.append("Uses modern C++ smart pointers")
        
        # Check for const correctness
        if 'const' in content:
            best_practices.append("Uses const for immutable data")
        
        # Check for namespace usage
        if 'namespace' in content:
            best_practices.append("Proper namespace usage")
        
        # Check for RAII pattern
        if 'class' in content and ('~' in content or 'destructor' in content.lower()):
            best_practices.append("Implements RAII pattern with destructors")
        
        # Function analysis
        function_pattern = r'\w+\s+\w+\s*\([^)]*\)\s*{'
        functions = re.findall(function_pattern, content)
        
        # Class analysis
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        # Check naming conventions
        for class_name in classes:
            if not re.match(self.best_practices['cpp']['class_naming'], class_name):
                issues.append(f"Class '{class_name}' doesn't follow naming convention")
        
        # Line length check
        long_lines = [i+1 for i, line in enumerate(lines) 
                     if len(line) > self.best_practices['cpp']['max_line_length']]
        if long_lines:
            issues.append(f"Lines too long: {long_lines[:5]}")
        
        return {
            'functions_count': len(functions),
            'classes_count': len(classes),
            'includes_count': len(includes),
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': self.calculate_complexity_score(content, 'cpp'),
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_java(self, content, filepath):
        """Analyze Java code using advanced analyzer"""
        # Use advanced Java analyzer if available
        if self.java_analyzer:
            try:
                return self.java_analyzer.analyze_java_code(content, filepath)
            except Exception as e:
                print(f"Advanced Java analysis failed: {e}, falling back to basic analysis")
        
        # Fallback to basic analysis
        issues = []
        best_practices = []
        
        lines = content.split('\n')
        
        # Package declaration
        if 'package' in content:
            best_practices.append("Proper package declaration")
        
        # Import statements
        imports = [line for line in lines if line.strip().startswith('import')]
        if imports:
            best_practices.append(f"Organized imports ({len(imports)} found)")
        
        # Class analysis
        class_pattern = r'(?:public\s+)?class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        # Method analysis
        method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)*\w+\s*\([^)]*\)\s*{'
        methods = re.findall(method_pattern, content)
        
        # Check for proper encapsulation
        if 'private' in content:
            best_practices.append("Uses proper encapsulation with private members")
        
        # Check for interfaces
        if 'interface' in content:
            best_practices.append("Implements interfaces for abstraction")
        
        # Check for exception handling
        if 'try' in content and 'catch' in content:
            best_practices.append("Includes proper exception handling")
        
        # Check for generics
        if '<' in content and '>' in content:
            best_practices.append("Uses generics for type safety")
        
        # Check naming conventions
        for class_name in classes:
            if not re.match(self.best_practices['java']['class_naming'], class_name):
                issues.append(f"Class '{class_name}' doesn't follow naming convention")
        
        # Check for common anti-patterns
        if 'System.out.println' in content:
            issues.append("Uses System.out.println - consider using logging framework")
        
        # Line length check
        long_lines = [i+1 for i, line in enumerate(lines) 
                     if len(line) > self.best_practices['java']['max_line_length']]
        if long_lines:
            issues.append(f"Lines too long: {long_lines[:5]}")
        
        return {
            'classes_count': len(classes),
            'methods_count': len(methods),
            'imports_count': len(imports),
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': self.calculate_complexity_score(content, 'java'),
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_go(self, content, filepath):
        """Analyze Go code using advanced analyzer"""
        # Use advanced Go analyzer if available
        if self.go_analyzer:
            try:
                return self.go_analyzer.analyze_go_code(content, filepath)
            except Exception as e:
                print(f"Advanced Go analysis failed: {e}, falling back to basic analysis")
        
        # Fallback to basic analysis
        issues = []
        best_practices = []
        
        lines = content.split('\n')
        
        # Package declaration
        if content.strip().startswith('package'):
            best_practices.append("Proper package declaration")
        else:
            issues.append("Missing package declaration")
        
        # Import analysis
        import_pattern = r'import\s*(?:\(([^)]+)\)|"([^"]+)")'
        imports = re.findall(import_pattern, content)
        
        # Function analysis
        func_pattern = r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\([^)]*\)(?:\s*[^{]*)?{'
        functions = re.findall(func_pattern, content)
        
        # Struct analysis
        struct_pattern = r'type\s+(\w+)\s+struct'
        structs = re.findall(struct_pattern, content)
        
        # Check for error handling
        if 'if err != nil' in content:
            best_practices.append("Proper Go error handling pattern")
        elif 'error' in content:
            issues.append("Error handling could be improved")
        
        # Check for goroutines
        if 'go ' in content:
            best_practices.append("Uses goroutines for concurrency")
        
        # Check for channels
        if 'chan' in content:
            best_practices.append("Uses channels for communication")
        
        # Check for defer statements
        if 'defer' in content:
            best_practices.append("Uses defer for cleanup")
        
        # Check for interfaces
        if 'interface' in content:
            best_practices.append("Defines interfaces for abstraction")
        
        # Naming convention checks
        for func_name in functions:
            if func_name[0].isupper() and len(func_name) > 1:
                best_practices.append(f"Function '{func_name}' is properly exported")
        
        return {
            'functions_count': len(functions),
            'structs_count': len(structs),
            'imports_count': len(imports),
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': self.calculate_complexity_score(content, 'go'),
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_javascript(self, content, filepath):
        """Analyze JavaScript/TypeScript code"""
        issues = []
        best_practices = []
        
        # Check for modern JavaScript features
        modern_features = {
            'const': 'Uses const for immutable variables',
            'let': 'Uses let for block-scoped variables',
            '=>': 'Uses arrow functions',
            'async': 'Uses async/await for asynchronous code',
            'await': 'Proper async/await usage',
            '...': 'Uses spread/rest operators',
            'class': 'Uses ES6 classes',
            'import': 'Uses ES6 modules',
            'export': 'Proper module exports'
        }
        
        for feature, description in modern_features.items():
            if feature in content:
                best_practices.append(description)
        
        # Check for jQuery (might be outdated)
        if '$(' in content or 'jQuery' in content:
            issues.append("Uses jQuery - consider modern alternatives")
        
        # Check for console.log (should be removed in production)
        if 'console.log' in content:
            issues.append("Contains console.log statements - remove for production")
        
        # Check for proper error handling
        if 'try' in content and 'catch' in content:
            best_practices.append("Includes proper error handling")
        
        # Function analysis
        func_patterns = [
            r'function\s+(\w+)',  # Regular functions
            r'(\w+)\s*=\s*function',  # Function expressions
            r'(\w+)\s*=\s*\([^)]*\)\s*=>',  # Arrow functions
            r'(\w+)\s*\([^)]*\)\s*{'  # Method definitions
        ]
        
        functions = []
        for pattern in func_patterns:
            functions.extend(re.findall(pattern, content))
        
        # Check for TypeScript features (if .ts file)
        if filepath.endswith('.ts'):
            if ':' in content and ('string' in content or 'number' in content or 'boolean' in content):
                best_practices.append("Uses TypeScript type annotations")
            
            if 'interface' in content:
                best_practices.append("Defines TypeScript interfaces")
        
        return {
            'functions_count': len(functions),
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': self.calculate_complexity_score(content, 'javascript'),
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_html(self, content, filepath):
        """Analyze HTML code"""
        issues = []
        best_practices = []
        
        # Check for DOCTYPE
        if '<!DOCTYPE html>' in content:
            best_practices.append("Includes proper DOCTYPE declaration")
        else:
            issues.append("Missing DOCTYPE declaration")
        
        # Check for semantic HTML
        semantic_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        found_semantic = [tag for tag in semantic_tags if f'<{tag}' in content]
        if found_semantic:
            best_practices.append(f"Uses semantic HTML tags: {', '.join(found_semantic)}")
        
        # Check for accessibility
        if 'alt=' in content:
            best_practices.append("Includes alt attributes for images")
        
        if 'aria-' in content:
            best_practices.append("Uses ARIA attributes for accessibility")
        
        # Check for meta tags
        if '<meta' in content:
            best_practices.append("Includes meta tags")
        
        # Check for external resources
        if 'href=' in content or 'src=' in content:
            best_practices.append("Links to external resources")
        
        return {
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': 'Low',
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def analyze_css(self, content, filepath):
        """Analyze CSS code"""
        issues = []
        best_practices = []
        
        # Check for CSS organization
        if '@media' in content:
            best_practices.append("Uses media queries for responsive design")
        
        # Check for CSS variables
        if '--' in content and 'var(' in content:
            best_practices.append("Uses CSS custom properties (variables)")
        
        # Check for flexbox/grid
        if 'display: flex' in content or 'display: grid' in content:
            best_practices.append("Uses modern layout methods (Flexbox/Grid)")
        
        # Check for vendor prefixes
        if '-webkit-' in content or '-moz-' in content:
            issues.append("Contains vendor prefixes - consider using autoprefixer")
        
        # Check for !important overuse
        important_count = content.count('!important')
        if important_count > 5:
            issues.append(f"Overuses !important ({important_count} times)")
        
        return {
            'issues_found': issues,
            'best_practices': best_practices,
            'complexity_score': 'Medium',
            'maintainability': self.assess_maintainability(issues, best_practices)
        }
    
    def calculate_complexity_score(self, content, language):
        """Calculate cyclomatic complexity score"""
        # Simplified complexity calculation
        complexity_keywords = {
            'python': ['if', 'elif', 'for', 'while', 'try', 'except', 'and', 'or'],
            'cpp': ['if', 'else', 'for', 'while', 'switch', 'case', '&&', '||'],
            'java': ['if', 'else', 'for', 'while', 'switch', 'case', '&&', '||'],
            'go': ['if', 'for', 'switch', 'case', '&&', '||'],
            'javascript': ['if', 'else', 'for', 'while', 'switch', 'case', '&&', '||']
        }
        
        keywords = complexity_keywords.get(language, ['if', 'for', 'while'])
        complexity = sum(content.lower().count(keyword) for keyword in keywords)
        
        if complexity <= 5:
            return 'Low'
        elif complexity <= 15:
            return 'Medium'
        else:
            return 'High'
    
    def assess_maintainability(self, issues, best_practices):
        """Assess code maintainability"""
        issue_count = len(issues)
        practice_count = len(best_practices)
        
        if practice_count >= issue_count * 2:
            return 'Excellent'
        elif practice_count >= issue_count:
            return 'Good'
        elif issue_count <= practice_count * 2:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def calculate_quality_score(self, results):
        """Calculate overall quality score"""
        score = 50  # Base score
        
        # Positive factors
        if 'best_practices' in results:
            score += min(30, len(results['best_practices']) * 3)
        
        if results.get('comment_ratio', 0) >= 10:
            score += 10
        elif results.get('comment_ratio', 0) >= 5:
            score += 5
        
        if results.get('complexity_score') == 'Low':
            score += 10
        elif results.get('complexity_score') == 'Medium':
            score += 5
        
        # Negative factors
        if 'issues_found' in results:
            score -= min(25, len(results['issues_found']) * 2)
        
        if results.get('avg_line_length', 0) > 120:
            score -= 5
        
        return max(0, min(100, score))
    
    def get_error_result(self, error_message):
        """Return error result structure"""
        return {
            'error': True,
            'message': error_message,
            'language': 'Unknown',
            'quality_score': 0,
            'issues_found': [error_message],
            'best_practices': [],
            'complexity_score': 'Unknown',
            'maintainability': 'Unknown'
        }

# Example usage and testing
if __name__ == "__main__":
    checker = CodeQualityChecker()
    
    # Test with sample Python code
    sample_python = '''
def calculate_fibonacci(n):
    """Calculate fibonacci number using recursion."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class MathUtils:
    """Utility class for mathematical operations."""
    
    @staticmethod
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

# Example usage
if __name__ == "__main__":
    try:
        result = calculate_fibonacci(10)
        print(f"Fibonacci result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    '''
    
    # Simulate file analysis
    results = checker.analyze_python(sample_python, 'test.py')
    print(json.dumps(results, indent=2))