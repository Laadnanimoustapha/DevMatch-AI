"""
DevMatch AI - Go Code Analyzer
Advanced Go code analysis focusing on concurrency, structure, error handling, and Go idioms
"""

import re
import os
from collections import defaultdict

class GoAnalyzer:
    def __init__(self):
        self.setup_go_patterns()
        self.setup_concurrency_patterns()
        self.setup_best_practices()
        self.setup_performance_patterns()
    
    def setup_go_patterns(self):
        """Setup Go-specific patterns for analysis"""
        self.go_patterns = {
            'package_structure': {
                'package_declaration': r'package\s+(\w+)',
                'import_statements': r'import\s+(?:\(([^)]+)\)|"([^"]+)")',
                'function_declaration': r'func\s+(?:\(\s*\w+\s+\*?\w+\s*\)\s+)?(\w+)\s*\([^)]*\)(?:\s*\([^)]*\))?\s*(?:\w+\s*)?{',
                'method_declaration': r'func\s+\(\s*(\w+)\s+\*?(\w+)\s*\)\s+(\w+)\s*\([^)]*\)(?:\s*\([^)]*\))?\s*(?:\w+\s*)?{',
                'struct_declaration': r'type\s+(\w+)\s+struct\s*{',
                'interface_declaration': r'type\s+(\w+)\s+interface\s*{',
                'constant_declaration': r'const\s+(?:\(([^)]+)\)|(\w+))',
                'variable_declaration': r'var\s+(?:\(([^)]+)\)|(\w+))'
            },
            'concurrency': {
                'goroutines': r'go\s+\w+\s*\(',
                'channels': r'(?:make\s*\(\s*chan\s+\w+|<-\s*\w+|\w+\s*<-)',
                'channel_operations': r'(?:<-\s*\w+|\w+\s*<-\s*\w+)',
                'select_statements': r'select\s*{',
                'mutex_usage': r'(?:sync\.Mutex|sync\.RWMutex)',
                'waitgroup_usage': r'sync\.WaitGroup',
                'context_usage': r'context\.\w+',
                'channel_closing': r'close\s*\(\s*\w+\s*\)'
            },
            'error_handling': {
                'error_returns': r'return\s+.*?,\s*(?:err|error|nil)',
                'error_checks': r'if\s+err\s*!=\s*nil\s*{',
                'custom_errors': r'errors\.New\s*\(|fmt\.Errorf\s*\(',
                'panic_usage': r'panic\s*\(',
                'recover_usage': r'recover\s*\(\s*\)',
                'defer_statements': r'defer\s+\w+'
            },
            'memory_management': {
                'make_usage': r'make\s*\(\s*(?:map|chan|\[\])',
                'new_usage': r'new\s*\(\s*\w+\s*\)',
                'slice_operations': r'(?:append\s*\(|\[\s*:\s*\])',
                'pointer_usage': r'\*\w+|\&\w+',
                'garbage_collection': r'runtime\.GC\s*\(\s*\)'
            },
            'go_idioms': {
                'blank_identifier': r'_\s*(?:=|,)',
                'type_assertions': r'\.\s*\(\s*\w+\s*\)',
                'type_switches': r'switch\s+\w+\s*:=\s*\w+\.\s*\(type\)',
                'embedding': r'^\s*\w+\s*$',  # Anonymous field in struct
                'init_functions': r'func\s+init\s*\(\s*\)\s*{',
                'variadic_functions': r'func\s+\w+\s*\([^)]*\.\.\.\w+\s*\)',
                'multiple_assignment': r'\w+\s*,\s*\w+\s*:?=',
                'range_loops': r'for\s+(?:\w+\s*,\s*)?\w+\s*:=\s*range\s+\w+'
            }
        }
    
    def setup_concurrency_patterns(self):
        """Setup concurrency analysis patterns"""
        self.concurrency_patterns = {
            'goroutine_management': [
                (r'go\s+func\s*\(', 'Anonymous goroutine'),
                (r'go\s+\w+\s*\(', 'Named function goroutine'),
                (r'sync\.WaitGroup', 'WaitGroup usage for synchronization'),
                (r'context\.WithCancel|context\.WithTimeout', 'Context-based cancellation')
            ],
            'channel_patterns': [
                (r'make\s*\(\s*chan\s+\w+\s*,\s*\d+\s*\)', 'Buffered channel'),
                (r'make\s*\(\s*chan\s+\w+\s*\)', 'Unbuffered channel'),
                (r'<-\s*done', 'Channel-based signaling'),
                (r'select\s*{.*?default\s*:', 'Non-blocking select'),
                (r'for\s+.*?range\s+\w+\s*{', 'Channel ranging')
            ],
            'synchronization': [
                (r'sync\.Mutex', 'Mutex for mutual exclusion'),
                (r'sync\.RWMutex', 'Read-write mutex'),
                (r'sync\.Once', 'Once for one-time initialization'),
                (r'atomic\.\w+', 'Atomic operations'),
                (r'sync\.Cond', 'Condition variables')
            ]
        }
    
    def setup_best_practices(self):
        """Setup Go best practices checklist"""
        self.best_practices = {
            'code_organization': [
                'Use meaningful package names',
                'Keep packages focused and cohesive',
                'Follow Go naming conventions',
                'Use gofmt for consistent formatting',
                'Organize imports properly'
            ],
            'error_handling': [
                'Always check errors explicitly',
                'Return errors as the last return value',
                'Use custom error types when appropriate',
                'Handle errors at the appropriate level',
                'Use defer for cleanup operations'
            ],
            'concurrency': [
                'Use channels to communicate between goroutines',
                'Avoid sharing memory; communicate by sharing',
                'Use context for cancellation and timeouts',
                'Close channels when done sending',
                'Use sync.WaitGroup for goroutine synchronization'
            ],
            'performance': [
                'Use slices instead of arrays when possible',
                'Pre-allocate slices with known capacity',
                'Use string builder for string concatenation',
                'Avoid unnecessary allocations',
                'Use benchmarks to measure performance'
            ],
            'idioms': [
                'Use the blank identifier for unused values',
                'Prefer composition over inheritance',
                'Use interfaces for abstraction',
                'Keep interfaces small and focused',
                'Use embedding for code reuse'
            ]
        }
    
    def setup_performance_patterns(self):
        """Setup performance analysis patterns"""
        self.performance_issues = {
            'critical': [
                (r'for\s*{[^}]*}(?!.*break)', 'Infinite loop without break'),
                (r'runtime\.GC\s*\(\s*\)', 'Explicit garbage collection call'),
                (r'go\s+func\s*\([^)]*\)\s*{[^}]*}(?!.*sync\.WaitGroup)', 'Goroutine without synchronization'),
                (r'panic\s*\([^)]*\)(?!.*recover)', 'Panic without recover')
            ],
            'major': [
                (r'\+\s*=.*?"[^"]*"', 'String concatenation in loop'),
                (r'make\s*\(\s*\[\]\w+\s*,\s*0\s*,\s*\d+\s*\)', 'Slice with zero length but capacity'),
                (r'range\s+\w+\s*{[^}]*\w+\s*=\s*append\s*\(\s*\w+', 'Appending in range loop'),
                (r'fmt\.Sprintf\s*\([^)]*\)\s*\+', 'String formatting in concatenation')
            ],
            'minor': [
                (r'len\s*\(\s*\w+\s*\)\s*==\s*0', 'Using len() == 0 instead of direct comparison'),
                (r'new\s*\(\s*\w+\s*\)', 'Using new() instead of struct literal'),
                (r'interface\s*{\s*}', 'Empty interface usage'),
                (r'reflect\.\w+', 'Reflection usage (performance impact)')
            ]
        }
    
    def analyze_go_code(self, content, filepath):
        """Main Go code analysis function"""
        analysis_results = {
            'language': 'Go',
            'file_path': filepath,
            'lines_of_code': len(content.split('\n')),
            'package_analysis': self.analyze_package_structure(content),
            'concurrency_analysis': self.analyze_concurrency(content),
            'error_handling_analysis': self.analyze_error_handling(content),
            'performance_analysis': self.analyze_performance(content),
            'idiom_usage': self.analyze_go_idioms(content),
            'best_practices_score': self.calculate_best_practices_score(content),
            'issues_found': self.find_issues(content),
            'suggestions': self.generate_suggestions(content),
            'complexity_score': self.calculate_complexity(content),
            'maintainability_score': self.calculate_maintainability(content)
        }
        
        # Calculate overall quality score
        analysis_results['quality_score'] = self.calculate_overall_score(analysis_results)
        
        return analysis_results
    
    def analyze_package_structure(self, content):
        """Analyze package structure and organization"""
        package_analysis = {
            'package_name': '',
            'imports': [],
            'functions': [],
            'methods': [],
            'structs': [],
            'interfaces': [],
            'structure_score': 0
        }
        
        # Extract package name
        package_match = re.search(self.go_patterns['package_structure']['package_declaration'], content)
        if package_match:
            package_analysis['package_name'] = package_match.group(1)
        
        # Extract imports
        import_matches = re.findall(self.go_patterns['package_structure']['import_statements'], content, re.MULTILINE | re.DOTALL)
        for match in import_matches:
            if match[0]:  # Multiple imports
                imports = [imp.strip().strip('"') for imp in match[0].split('\n') if imp.strip()]
                package_analysis['imports'].extend(imports)
            elif match[1]:  # Single import
                package_analysis['imports'].append(match[1])
        
        # Extract functions
        functions = re.findall(self.go_patterns['package_structure']['function_declaration'], content)
        package_analysis['functions'] = functions
        
        # Extract methods
        methods = re.findall(self.go_patterns['package_structure']['method_declaration'], content)
        package_analysis['methods'] = [(method[0], method[1], method[2]) for method in methods]
        
        # Extract structs
        structs = re.findall(self.go_patterns['package_structure']['struct_declaration'], content)
        package_analysis['structs'] = structs
        
        # Extract interfaces
        interfaces = re.findall(self.go_patterns['package_structure']['interface_declaration'], content)
        package_analysis['interfaces'] = interfaces
        
        # Calculate structure score
        score = 100
        if not package_analysis['package_name']:
            score -= 30
        if len(package_analysis['functions']) == 0 and len(package_analysis['methods']) == 0:
            score -= 40
        if len(package_analysis['imports']) > 20:  # Too many imports
            score -= 20
        
        package_analysis['structure_score'] = max(0, score)
        
        return package_analysis
    
    def analyze_concurrency(self, content):
        """Analyze concurrency patterns and practices"""
        concurrency_analysis = {
            'goroutines_used': 0,
            'channels_used': 0,
            'synchronization_primitives': [],
            'concurrency_patterns': [],
            'concurrency_score': 0,
            'potential_race_conditions': []
        }
        
        # Count goroutines
        concurrency_analysis['goroutines_used'] = len(re.findall(self.go_patterns['concurrency']['goroutines'], content))
        
        # Count channels
        concurrency_analysis['channels_used'] = len(re.findall(self.go_patterns['concurrency']['channels'], content))
        
        # Find synchronization primitives
        sync_primitives = [
            ('Mutex', r'sync\.Mutex'),
            ('RWMutex', r'sync\.RWMutex'),
            ('WaitGroup', r'sync\.WaitGroup'),
            ('Once', r'sync\.Once'),
            ('Cond', r'sync\.Cond')
        ]
        
        for name, pattern in sync_primitives:
            if re.search(pattern, content):
                concurrency_analysis['synchronization_primitives'].append(name)
        
        # Analyze concurrency patterns
        for category, patterns in self.concurrency_patterns.items():
            for pattern, description in patterns:
                if re.search(pattern, content):
                    concurrency_analysis['concurrency_patterns'].append(description)
        
        # Check for potential race conditions
        if concurrency_analysis['goroutines_used'] > 0:
            # Shared variable access without synchronization
            if not any(sync in concurrency_analysis['synchronization_primitives'] for sync in ['Mutex', 'RWMutex']):
                if not re.search(r'<-|chan', content):  # No channels either
                    concurrency_analysis['potential_race_conditions'].append('Goroutines without synchronization')
        
        # Calculate concurrency score
        if concurrency_analysis['goroutines_used'] > 0:
            sync_score = len(concurrency_analysis['synchronization_primitives']) * 20
            channel_score = min(concurrency_analysis['channels_used'] * 15, 60)
            pattern_score = len(concurrency_analysis['concurrency_patterns']) * 10
            race_penalty = len(concurrency_analysis['potential_race_conditions']) * 30
            
            concurrency_analysis['concurrency_score'] = max(0, sync_score + channel_score + pattern_score - race_penalty)
        else:
            concurrency_analysis['concurrency_score'] = 100  # No concurrency, no issues
        
        return concurrency_analysis
    
    def analyze_error_handling(self, content):
        """Analyze error handling practices"""
        error_analysis = {
            'error_returns': 0,
            'error_checks': 0,
            'custom_errors': 0,
            'panic_usage': 0,
            'defer_usage': 0,
            'error_handling_score': 0,
            'error_patterns': []
        }
        
        # Count error handling patterns
        error_analysis['error_returns'] = len(re.findall(self.go_patterns['error_handling']['error_returns'], content))
        error_analysis['error_checks'] = len(re.findall(self.go_patterns['error_handling']['error_checks'], content))
        error_analysis['custom_errors'] = len(re.findall(self.go_patterns['error_handling']['custom_errors'], content))
        error_analysis['panic_usage'] = len(re.findall(self.go_patterns['error_handling']['panic_usage'], content))
        error_analysis['defer_usage'] = len(re.findall(self.go_patterns['error_handling']['defer_statements'], content))
        
        # Identify error patterns
        if error_analysis['error_checks'] > 0:
            error_analysis['error_patterns'].append('Explicit error checking')
        if error_analysis['custom_errors'] > 0:
            error_analysis['error_patterns'].append('Custom error creation')
        if error_analysis['defer_usage'] > 0:
            error_analysis['error_patterns'].append('Defer for cleanup')
        
        # Calculate error handling score
        if error_analysis['error_returns'] > 0:
            check_ratio = error_analysis['error_checks'] / error_analysis['error_returns']
            base_score = min(check_ratio * 100, 100)
            
            # Bonus for good practices
            if error_analysis['custom_errors'] > 0:
                base_score += 10
            if error_analysis['defer_usage'] > 0:
                base_score += 10
            
            # Penalty for panic usage
            if error_analysis['panic_usage'] > 0:
                base_score -= error_analysis['panic_usage'] * 15
            
            error_analysis['error_handling_score'] = max(0, min(base_score, 100))
        else:
            error_analysis['error_handling_score'] = 100  # No errors to handle
        
        return error_analysis
    
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
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    performance_analysis['issues'].append({
                        'severity': severity,
                        'description': description,
                        'count': len(matches),
                        'pattern': pattern
                    })
        
        # Check for performance optimizations
        optimizations = [
            (r'make\s*\(\s*\[\]\w+\s*,\s*0\s*,\s*\d+\s*\)', 'Pre-allocated slice capacity'),
            (r'strings\.Builder', 'String builder for concatenation'),
            (r'sync\.Pool', 'Object pooling for reuse'),
            (r'context\.WithTimeout|context\.WithDeadline', 'Context-based timeouts'),
            (r'go\s+func\s*\([^)]*\)\s*{.*?defer\s+.*?Done\(\)', 'Proper goroutine cleanup')
        ]
        
        for pattern, description in optimizations:
            if re.search(pattern, content, re.DOTALL):
                performance_analysis['optimizations_found'].append(description)
        
        # Calculate performance score
        critical_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'critical')
        major_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'major')
        minor_issues = sum(1 for issue in performance_analysis['issues'] if issue['severity'] == 'minor')
        
        performance_analysis['performance_score'] = max(0, 100 - (critical_issues * 30) - (major_issues * 15) - (minor_issues * 5))
        
        return performance_analysis
    
    def analyze_go_idioms(self, content):
        """Analyze usage of Go idioms and best practices"""
        idiom_analysis = {
            'idioms_used': [],
            'idiom_score': 0
        }
        
        # Check for Go idioms
        idioms = [
            (r'_\s*(?:=|,)', 'Blank identifier usage'),
            (r'\.\s*\(\s*\w+\s*\)', 'Type assertions'),
            (r'switch\s+\w+\s*:=\s*\w+\.\s*\(type\)', 'Type switches'),
            (r'func\s+init\s*\(\s*\)\s*{', 'Init functions'),
            (r'func\s+\w+\s*\([^)]*\.\.\.\w+\s*\)', 'Variadic functions'),
            (r'for\s+(?:\w+\s*,\s*)?\w+\s*:=\s*range\s+\w+', 'Range loops'),
            (r'if\s+\w+\s*:=\s*[^;]+;\s*\w+', 'If with initialization'),
            (r'defer\s+\w+', 'Defer statements')
        ]
        
        for pattern, description in idioms:
            if re.search(pattern, content):
                idiom_analysis['idioms_used'].append(description)
        
        # Calculate idiom score
        idiom_analysis['idiom_score'] = min(len(idiom_analysis['idioms_used']) * 15, 100)
        
        return idiom_analysis
    
    def calculate_best_practices_score(self, content):
        """Calculate adherence to Go best practices"""
        score = 100
        
        # Check naming conventions
        if re.search(r'func\s+[a-z]\w*\s*\(', content):  # Exported functions should start with uppercase
            if not re.search(r'func\s+[A-Z]\w*\s*\(', content):
                score -= 10
        
        # Check error handling
        error_returns = len(re.findall(r'return\s+.*?,\s*(?:err|error)', content))
        error_checks = len(re.findall(r'if\s+err\s*!=\s*nil', content))
        if error_returns > 0 and error_checks / error_returns < 0.8:
            score -= 20
        
        # Check for proper channel closing
        channels = len(re.findall(r'make\s*\(\s*chan\s+\w+', content))
        channel_closes = len(re.findall(r'close\s*\(\s*\w+\s*\)', content))
        if channels > 0 and channel_closes == 0:
            score -= 15
        
        # Check for context usage in long-running operations
        if re.search(r'for\s*{', content) and not re.search(r'context\.\w+', content):
            score -= 10
        
        return max(0, score)
    
    def find_issues(self, content):
        """Find specific code issues"""
        issues = []
        
        # Concurrency issues
        goroutines = len(re.findall(r'go\s+\w+\s*\(', content))
        if goroutines > 0 and not re.search(r'sync\.WaitGroup|<-.*done', content):
            issues.append({
                'type': 'Concurrency',
                'severity': 'High',
                'description': 'Goroutines without proper synchronization',
                'suggestion': 'Use sync.WaitGroup or channels for goroutine synchronization'
            })
        
        # Error handling issues
        if re.search(r'_\s*=\s*\w+\s*\([^)]*\)(?!.*err)', content):
            issues.append({
                'type': 'Error Handling',
                'severity': 'Medium',
                'description': 'Ignoring potential errors',
                'suggestion': 'Always check and handle errors explicitly'
            })
        
        # Performance issues
        if re.search(r'\+\s*=.*?"[^"]*"', content):
            issues.append({
                'type': 'Performance',
                'severity': 'Medium',
                'description': 'String concatenation in loop',
                'suggestion': 'Use strings.Builder for efficient string concatenation'
            })
        
        return issues
    
    def generate_suggestions(self, content):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Concurrency suggestions
        if re.search(r'go\s+\w+', content):
            if not re.search(r'context\.\w+', content):
                suggestions.append("Consider using context for goroutine cancellation and timeouts")
            if not re.search(r'sync\.WaitGroup', content):
                suggestions.append("Use sync.WaitGroup to wait for goroutines to complete")
        
        # Error handling suggestions
        error_returns = len(re.findall(r'return\s+.*?,\s*(?:err|error)', content))
        error_checks = len(re.findall(r'if\s+err\s*!=\s*nil', content))
        if error_returns > error_checks:
            suggestions.append("Always check errors returned by functions")
        
        # Performance suggestions
        if re.search(r'make\s*\(\s*\[\]\w+\s*,\s*0\s*\)', content):
            suggestions.append("Pre-allocate slice capacity when size is known to avoid reallocations")
        
        if re.search(r'\+.*?"[^"]*"', content):
            suggestions.append("Use strings.Builder for efficient string concatenation")
        
        # Idiom suggestions
        if not re.search(r'for\s+.*?range\s+\w+', content) and re.search(r'for\s+\w+\s*:=\s*0', content):
            suggestions.append("Consider using range loops for iterating over slices and maps")
        
        if not re.search(r'defer\s+\w+', content) and re.search(r'\.Close\(\)', content):
            suggestions.append("Use defer for cleanup operations like closing files or connections")
        
        # Code organization suggestions
        if not re.search(r'package\s+\w+', content):
            suggestions.append("Every Go file should start with a package declaration")
        
        if re.search(r'func\s+[a-z]\w*\s*\(', content) and not re.search(r'//.*', content):
            suggestions.append("Add comments to exported functions and types")
        
        return suggestions[:8]  # Limit to top 8 suggestions
    
    def calculate_complexity(self, content):
        """Calculate cyclomatic complexity"""
        complexity_keywords = [
            r'\bif\b', r'\belse\b', r'\bfor\b', r'\bswitch\b', 
            r'\bcase\b', r'\bselect\b', r'\bgo\b', r'\bdefer\b',
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
        function_count = len(re.findall(r'func\s+\w+\s*\(', content))
        
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
            'concurrency': 0.25,
            'error_handling': 0.25,
            'performance': 0.20,
            'idioms': 0.15,
            'best_practices': 0.15
        }
        
        concurrency_score = analysis_results['concurrency_analysis']['concurrency_score']
        error_score = analysis_results['error_handling_analysis']['error_handling_score']
        performance_score = analysis_results['performance_analysis']['performance_score']
        idiom_score = analysis_results['idiom_usage']['idiom_score']
        practices_score = analysis_results['best_practices_score']
        
        overall_score = (
            concurrency_score * weights['concurrency'] +
            error_score * weights['error_handling'] +
            performance_score * weights['performance'] +
            idiom_score * weights['idioms'] +
            practices_score * weights['best_practices']
        )
        
        return round(overall_score)

# Example usage and testing
if __name__ == "__main__":
    analyzer = GoAnalyzer()
    
    # Test with sample Go code
    sample_go_code = '''
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
                
                // Simulate work
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
        
        // Start workers
        for i := 1; i <= numWorkers; i++ {
            wg.Add(1)
            worker := NewWorker(i, jobs, results, &wg)
            go worker.Start(ctx)
        }
        
        // Send jobs
        for j := 1; j <= numJobs; j++ {
            jobs <- j
        }
        close(jobs)
        
        // Collect results
        go func() {
            wg.Wait()
            close(results)
        }()
        
        // Print results
        for result := range results {
            fmt.Printf("Result: %d\\n", result)
        }
    }
    '''
    
    results = analyzer.analyze_go_code(sample_go_code, 'worker.go')
    
    print("Go Code Analysis Results:")
    print(f"Quality Score: {results['quality_score']}/100")
    print(f"Concurrency Score: {results['concurrency_analysis']['concurrency_score']}/100")
    print(f"Error Handling Score: {results['error_handling_analysis']['error_handling_score']}/100")
    print(f"Performance Score: {results['performance_analysis']['performance_score']}/100")
    print(f"Go Idioms Score: {results['idiom_usage']['idiom_score']}/100")
    print(f"Best Practices Score: {results['best_practices_score']}/100")
    
    print(f"\nPackage: {results['package_analysis']['package_name']}")
    print(f"Functions: {len(results['package_analysis']['functions'])}")
    print(f"Structs: {len(results['package_analysis']['structs'])}")
    print(f"Goroutines: {results['concurrency_analysis']['goroutines_used']}")
    print(f"Channels: {results['concurrency_analysis']['channels_used']}")
    
    print("\nSuggestions:")
    for suggestion in results['suggestions']:
        print(f"- {suggestion}")