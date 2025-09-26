"""
DevMatch AI - Portfolio Analyzer Module
Comprehensive portfolio analysis for UI/UX and technical assessment
"""

import os
import re
import json
import zipfile
import tarfile
import rarfile
from datetime import datetime
from collections import Counter, defaultdict
import mimetypes

class PortfolioAnalyzer:
    def __init__(self):
        self.setup_analyzers()
        self.load_best_practices()
        self.load_technology_patterns()
    
    def setup_analyzers(self):
        """Initialize file type analyzers"""
        self.file_analyzers = {
            '.html': self.analyze_html_file,
            '.css': self.analyze_css_file,
            '.js': self.analyze_js_file,
            '.ts': self.analyze_ts_file,
            '.json': self.analyze_json_file,
            '.md': self.analyze_markdown_file,
            '.txt': self.analyze_text_file
        }
        
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico'}
        self.font_extensions = {'.woff', '.woff2', '.ttf', '.otf', '.eot'}
        self.video_extensions = {'.mp4', '.webm', '.avi', '.mov'}
    
    def load_best_practices(self):
        """Load UI/UX and technical best practices"""
        self.ui_best_practices = {
            'responsive_design': ['@media', 'viewport', 'flex', 'grid', 'rem', 'em', '%'],
            'accessibility': ['alt=', 'aria-', 'role=', 'tabindex', 'label', 'title='],
            'semantic_html': ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer'],
            'modern_css': ['flexbox', 'grid', 'css variables', 'transform', 'transition', 'animation'],
            'performance': ['lazy loading', 'minified', 'compressed', 'optimized images'],
            'seo': ['meta description', 'title tag', 'h1', 'structured data', 'sitemap']
        }
        
        self.technical_best_practices = {
            'code_organization': ['components', 'modules', 'utils', 'assets', 'styles'],
            'version_control': ['.git', 'package.json', 'README.md', '.gitignore'],
            'build_tools': ['webpack', 'vite', 'gulp', 'grunt', 'parcel'],
            'testing': ['test', 'spec', 'jest', 'cypress', 'mocha'],
            'documentation': ['README', 'docs', 'comments', 'jsdoc'],
            'modern_js': ['es6', 'modules', 'async/await', 'arrow functions', 'destructuring']
        }
    
    def load_technology_patterns(self):
        """Load patterns to detect technologies"""
        self.tech_patterns = {
            'React': [r'import.*react', r'from [\'"]react[\'"]', r'React\.', r'jsx', r'useState', r'useEffect'],
            'Vue.js': [r'import.*vue', r'from [\'"]vue[\'"]', r'Vue\.', r'v-if', r'v-for', r'@click'],
            'Angular': [r'import.*@angular', r'@Component', r'@Injectable', r'ngOnInit', r'*ngFor', r'*ngIf'],
            'jQuery': [r'\$\(', r'jQuery', r'\.jquery'],
            'Bootstrap': [r'bootstrap', r'btn-', r'col-', r'row', r'container'],
            'Tailwind CSS': [r'tailwind', r'bg-', r'text-', r'p-\d', r'm-\d', r'w-\d'],
            'Sass/SCSS': [r'@import', r'@mixin', r'@include', r'\$[a-zA-Z]', r'&:'],
            'TypeScript': [r'interface\s+\w+', r'type\s+\w+', r':\s*string', r':\s*number', r':\s*boolean'],
            'Node.js': [r'require\(', r'module\.exports', r'process\.', r'__dirname', r'npm'],
            'Express.js': [r'express\(\)', r'app\.get', r'app\.post', r'req\.', r'res\.'],
            'Webpack': [r'webpack', r'module\.exports', r'entry:', r'output:', r'plugins:'],
            'Vite': [r'vite', r'import\.meta', r'vite\.config'],
            'ESLint': [r'eslint', r'\.eslintrc', r'eslint-disable'],
            'Prettier': [r'prettier', r'\.prettierrc', r'prettier-ignore']
        }
    
    def analyze_portfolio(self, filepath):
        """Main portfolio analysis function"""
        try:
            # Extract portfolio files
            extracted_path = self.extract_portfolio(filepath)
            
            if not extracted_path:
                return self.get_error_result("Could not extract portfolio files")
            
            # Analyze portfolio structure and content
            analysis_results = self.perform_comprehensive_analysis(extracted_path)
            
            # Cleanup extracted files
            self.cleanup_extracted_files(extracted_path)
            
            return analysis_results
            
        except Exception as e:
            return self.get_error_result(f"Portfolio analysis failed: {str(e)}")
    
    def extract_portfolio(self, filepath):
        """Extract portfolio archive to temporary directory"""
        import tempfile
        import shutil
        
        file_ext = os.path.splitext(filepath)[1].lower()
        temp_dir = tempfile.mkdtemp(prefix='devmatch_portfolio_')
        
        try:
            if file_ext == '.zip':
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif file_ext in ['.tar', '.gz']:
                with tarfile.open(filepath, 'r:*') as tar_ref:
                    tar_ref.extractall(temp_dir)
            elif file_ext == '.rar':
                with rarfile.RarFile(filepath, 'r') as rar_ref:
                    rar_ref.extractall(temp_dir)
            else:
                # Single file - copy to temp directory
                shutil.copy2(filepath, temp_dir)
            
            return temp_dir
            
        except Exception as e:
            print(f"Extraction error: {e}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return None
    
    def perform_comprehensive_analysis(self, portfolio_path):
        """Perform comprehensive portfolio analysis"""
        # Scan all files
        file_inventory = self.scan_files(portfolio_path)
        
        # Analyze file contents
        content_analysis = self.analyze_file_contents(portfolio_path, file_inventory)
        
        # Detect technologies
        technologies = self.detect_technologies(content_analysis['all_content'])
        
        # Analyze structure
        structure_analysis = self.analyze_project_structure(file_inventory)
        
        # UI/UX Analysis
        ui_analysis = self.analyze_ui_ux(content_analysis)
        
        # Technical Analysis
        technical_analysis = self.analyze_technical_aspects(content_analysis, file_inventory)
        
        # Performance Analysis
        performance_analysis = self.analyze_performance(file_inventory, content_analysis)
        
        # Calculate scores
        scores = self.calculate_portfolio_scores(
            ui_analysis, technical_analysis, performance_analysis, structure_analysis
        )
        
        # Generate suggestions
        suggestions = self.generate_improvement_suggestions(
            ui_analysis, technical_analysis, performance_analysis, structure_analysis
        )
        
        return {
            'analysis_date': datetime.now().isoformat(),
            'file_count': len(file_inventory['all_files']),
            'total_size': file_inventory['total_size'],
            'technologies_detected': technologies,
            'project_structure': structure_analysis,
            'ui_score': scores['ui_score'],
            'ux_score': scores['ux_score'],
            'technical_score': scores['technical_score'],
            'performance_score': scores['performance_score'],
            'overall_rating': scores['overall_rating'],
            'ui_analysis': ui_analysis,
            'technical_analysis': technical_analysis,
            'performance_analysis': performance_analysis,
            'suggestions': suggestions,
            'file_breakdown': file_inventory['file_types']
        }
    
    def scan_files(self, portfolio_path):
        """Scan and categorize all files in portfolio"""
        all_files = []
        file_types = defaultdict(int)
        total_size = 0
        
        for root, dirs, files in os.walk(portfolio_path):
            # Skip hidden directories and common build/dependency directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build', '__pycache__']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                filepath = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                file_size = os.path.getsize(filepath)
                
                all_files.append({
                    'path': filepath,
                    'name': file,
                    'extension': file_ext,
                    'size': file_size,
                    'relative_path': os.path.relpath(filepath, portfolio_path)
                })
                
                file_types[file_ext] += 1
                total_size += file_size
        
        return {
            'all_files': all_files,
            'file_types': dict(file_types),
            'total_size': total_size
        }
    
    def analyze_file_contents(self, portfolio_path, file_inventory):
        """Analyze content of relevant files"""
        content_analysis = {
            'html_content': [],
            'css_content': [],
            'js_content': [],
            'all_content': '',
            'file_analyses': {}
        }
        
        for file_info in file_inventory['all_files']:
            file_ext = file_info['extension']
            filepath = file_info['path']
            
            if file_ext in self.file_analyzers:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Store content by type
                    if file_ext == '.html':
                        content_analysis['html_content'].append(content)
                    elif file_ext == '.css':
                        content_analysis['css_content'].append(content)
                    elif file_ext in ['.js', '.ts']:
                        content_analysis['js_content'].append(content)
                    
                    # Add to all content for technology detection
                    content_analysis['all_content'] += content + '\n'
                    
                    # Analyze individual file
                    analyzer = self.file_analyzers[file_ext]
                    file_analysis = analyzer(content, filepath)
                    content_analysis['file_analyses'][file_info['relative_path']] = file_analysis
                    
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")
        
        return content_analysis
    
    def analyze_html_file(self, content, filepath):
        """Analyze HTML file"""
        analysis = {
            'has_doctype': '<!DOCTYPE html>' in content,
            'has_meta_viewport': 'viewport' in content,
            'has_title': '<title>' in content,
            'semantic_tags': [],
            'accessibility_features': [],
            'external_resources': [],
            'forms': '<form' in content,
            'images': len(re.findall(r'<img', content, re.IGNORECASE)),
            'links': len(re.findall(r'<a\s+[^>]*href', content, re.IGNORECASE))
        }
        
        # Check for semantic HTML tags
        semantic_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        for tag in semantic_tags:
            if f'<{tag}' in content.lower():
                analysis['semantic_tags'].append(tag)
        
        # Check accessibility features
        accessibility_features = ['alt=', 'aria-', 'role=', 'tabindex', 'label']
        for feature in accessibility_features:
            if feature in content.lower():
                analysis['accessibility_features'].append(feature)
        
        # Check for external resources
        css_links = re.findall(r'<link[^>]*href=["\']([^"\']*\.css)["\']', content, re.IGNORECASE)
        js_scripts = re.findall(r'<script[^>]*src=["\']([^"\']*\.js)["\']', content, re.IGNORECASE)
        analysis['external_resources'] = css_links + js_scripts
        
        return analysis
    
    def analyze_css_file(self, content, filepath):
        """Analyze CSS file"""
        analysis = {
            'uses_flexbox': 'display: flex' in content or 'display:flex' in content,
            'uses_grid': 'display: grid' in content or 'display:grid' in content,
            'has_media_queries': '@media' in content,
            'uses_variables': '--' in content and 'var(' in content,
            'uses_animations': '@keyframes' in content or 'animation:' in content,
            'uses_transforms': 'transform:' in content,
            'uses_transitions': 'transition:' in content,
            'responsive_units': bool(re.search(r'\d+(?:rem|em|%|vw|vh)', content)),
            'color_count': len(set(re.findall(r'#[0-9a-fA-F]{3,6}', content))),
            'font_families': len(set(re.findall(r'font-family:\s*([^;]+)', content, re.IGNORECASE)))
        }
        
        return analysis
    
    def analyze_js_file(self, content, filepath):
        """Analyze JavaScript file"""
        analysis = {
            'uses_es6': any(pattern in content for pattern in ['=>', 'const ', 'let ', '`', '...', 'class ']),
            'uses_async_await': 'async ' in content and 'await ' in content,
            'uses_promises': '.then(' in content or 'Promise' in content,
            'uses_modules': 'import ' in content or 'export ' in content,
            'uses_destructuring': bool(re.search(r'(?:const|let|var)\s*{[^}]+}\s*=', content)),
            'function_count': len(re.findall(r'function\s+\w+|=>\s*{|\w+\s*:\s*function', content)),
            'has_comments': '//' in content or '/*' in content,
            'uses_strict_mode': "'use strict'" in content or '"use strict"' in content,
            'dom_manipulation': any(method in content for method in ['getElementById', 'querySelector', 'addEventListener']),
            'ajax_requests': any(method in content for method in ['fetch(', 'XMLHttpRequest', 'axios', '$.ajax'])
        }
        
        return analysis
    
    def analyze_ts_file(self, content, filepath):
        """Analyze TypeScript file"""
        js_analysis = self.analyze_js_file(content, filepath)
        
        ts_specific = {
            'has_interfaces': 'interface ' in content,
            'has_types': bool(re.search(r'type\s+\w+\s*=', content)),
            'uses_generics': bool(re.search(r'<[A-Z]\w*>', content)),
            'has_type_annotations': bool(re.search(r':\s*(?:string|number|boolean|object)', content)),
            'uses_enums': 'enum ' in content
        }
        
        return {**js_analysis, **ts_specific}
    
    def analyze_json_file(self, content, filepath):
        """Analyze JSON file"""
        try:
            data = json.loads(content)
            return {
                'valid_json': True,
                'is_package_json': 'package.json' in filepath,
                'has_dependencies': 'dependencies' in data if isinstance(data, dict) else False,
                'has_scripts': 'scripts' in data if isinstance(data, dict) else False
            }
        except json.JSONDecodeError:
            return {'valid_json': False}
    
    def analyze_markdown_file(self, content, filepath):
        """Analyze Markdown file"""
        return {
            'is_readme': 'readme' in filepath.lower(),
            'has_headers': bool(re.search(r'^#+\s', content, re.MULTILINE)),
            'has_links': '[' in content and '](' in content,
            'has_images': '![' in content,
            'has_code_blocks': '```' in content,
            'word_count': len(content.split())
        }
    
    def analyze_text_file(self, content, filepath):
        """Analyze text file"""
        return {
            'line_count': len(content.split('\n')),
            'word_count': len(content.split()),
            'char_count': len(content)
        }
    
    def detect_technologies(self, content):
        """Detect technologies used in the portfolio"""
        detected_technologies = []
        
        for tech, patterns in self.tech_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_technologies.append(tech)
                    break
        
        return list(set(detected_technologies))
    
    def analyze_project_structure(self, file_inventory):
        """Analyze project structure and organization"""
        structure = {
            'has_readme': False,
            'has_package_json': False,
            'has_gitignore': False,
            'folder_structure': defaultdict(int),
            'organization_score': 0
        }
        
        for file_info in file_inventory['all_files']:
            filename = file_info['name'].lower()
            relative_path = file_info['relative_path']
            
            # Check for important files
            if 'readme' in filename:
                structure['has_readme'] = True
            elif filename == 'package.json':
                structure['has_package_json'] = True
            elif filename == '.gitignore':
                structure['has_gitignore'] = True
            
            # Analyze folder structure
            folder = os.path.dirname(relative_path)
            if folder:
                structure['folder_structure'][folder] += 1
        
        # Calculate organization score
        organization_factors = [
            structure['has_readme'],
            structure['has_package_json'],
            len(structure['folder_structure']) > 1,  # Multiple folders
            any('src' in folder or 'assets' in folder for folder in structure['folder_structure']),
            any('css' in folder or 'styles' in folder for folder in structure['folder_structure'])
        ]
        
        structure['organization_score'] = sum(organization_factors) * 20
        
        return structure
    
    def analyze_ui_ux(self, content_analysis):
        """Analyze UI/UX aspects"""
        ui_analysis = {
            'responsive_design': False,
            'accessibility_score': 0,
            'semantic_html_score': 0,
            'modern_css_usage': 0,
            'color_scheme_consistency': 0,
            'typography_quality': 0
        }
        
        # Analyze HTML content
        for html_content in content_analysis['html_content']:
            html_analysis = self.analyze_html_file(html_content, '')
            
            # Semantic HTML
            ui_analysis['semantic_html_score'] += len(html_analysis['semantic_tags']) * 10
            
            # Accessibility
            ui_analysis['accessibility_score'] += len(html_analysis['accessibility_features']) * 15
        
        # Analyze CSS content
        modern_css_features = 0
        for css_content in content_analysis['css_content']:
            css_analysis = self.analyze_css_file(css_content, '')
            
            # Responsive design
            if css_analysis['has_media_queries']:
                ui_analysis['responsive_design'] = True
            
            # Modern CSS features
            modern_features = [
                css_analysis['uses_flexbox'],
                css_analysis['uses_grid'],
                css_analysis['uses_variables'],
                css_analysis['uses_animations'],
                css_analysis['responsive_units']
            ]
            modern_css_features += sum(modern_features)
        
        ui_analysis['modern_css_usage'] = min(100, modern_css_features * 20)
        ui_analysis['accessibility_score'] = min(100, ui_analysis['accessibility_score'])
        ui_analysis['semantic_html_score'] = min(100, ui_analysis['semantic_html_score'])
        
        return ui_analysis
    
    def analyze_technical_aspects(self, content_analysis, file_inventory):
        """Analyze technical implementation"""
        technical_analysis = {
            'code_quality_score': 0,
            'modern_js_usage': 0,
            'build_tools_present': False,
            'testing_present': False,
            'documentation_quality': 0,
            'version_control_setup': False
        }
        
        # Check for build tools and configuration files
        config_files = ['webpack.config.js', 'vite.config.js', 'package.json', 'tsconfig.json']
        for file_info in file_inventory['all_files']:
            if file_info['name'] in config_files:
                technical_analysis['build_tools_present'] = True
            if 'test' in file_info['name'] or 'spec' in file_info['name']:
                technical_analysis['testing_present'] = True
            if file_info['name'].lower() in ['readme.md', '.gitignore']:
                technical_analysis['version_control_setup'] = True
        
        # Analyze JavaScript quality
        js_quality_factors = 0
        js_file_count = 0
        
        for js_content in content_analysis['js_content']:
            js_analysis = self.analyze_js_file(js_content, '')
            js_file_count += 1
            
            quality_factors = [
                js_analysis['uses_es6'],
                js_analysis['uses_modules'],
                js_analysis['has_comments'],
                js_analysis['uses_async_await'] or js_analysis['uses_promises']
            ]
            js_quality_factors += sum(quality_factors)
        
        if js_file_count > 0:
            technical_analysis['modern_js_usage'] = (js_quality_factors / (js_file_count * 4)) * 100
        
        # Documentation quality
        readme_files = [f for f in file_inventory['all_files'] if 'readme' in f['name'].lower()]
        if readme_files:
            technical_analysis['documentation_quality'] = 80
        
        return technical_analysis
    
    def analyze_performance(self, file_inventory, content_analysis):
        """Analyze performance aspects"""
        performance_analysis = {
            'image_optimization': 0,
            'file_size_efficiency': 0,
            'loading_optimization': 0,
            'caching_strategy': 0
        }
        
        # Analyze image files
        image_files = [f for f in file_inventory['all_files'] if f['extension'] in self.image_extensions]
        if image_files:
            # Check for modern image formats
            modern_formats = [f for f in image_files if f['extension'] in ['.webp', '.svg']]
            performance_analysis['image_optimization'] = (len(modern_formats) / len(image_files)) * 100
        
        # File size analysis
        large_files = [f for f in file_inventory['all_files'] if f['size'] > 1024 * 1024]  # > 1MB
        if len(file_inventory['all_files']) > 0:
            performance_analysis['file_size_efficiency'] = max(0, 100 - (len(large_files) / len(file_inventory['all_files'])) * 100)
        
        # Check for performance optimizations in code
        all_content = content_analysis['all_content'].lower()
        performance_keywords = ['lazy', 'defer', 'async', 'preload', 'prefetch', 'minified']
        found_optimizations = sum(1 for keyword in performance_keywords if keyword in all_content)
        performance_analysis['loading_optimization'] = min(100, found_optimizations * 20)
        
        return performance_analysis
    
    def calculate_portfolio_scores(self, ui_analysis, technical_analysis, performance_analysis, structure_analysis):
        """Calculate overall portfolio scores"""
        # UI Score (0-100)
        ui_score = (
            (ui_analysis['semantic_html_score'] * 0.3) +
            (ui_analysis['modern_css_usage'] * 0.3) +
            (ui_analysis['accessibility_score'] * 0.2) +
            (50 if ui_analysis['responsive_design'] else 0) * 0.2
        )
        
        # UX Score (0-100)
        ux_score = (
            (ui_analysis['accessibility_score'] * 0.4) +
            (50 if ui_analysis['responsive_design'] else 0) * 0.3 +
            (structure_analysis['organization_score'] * 0.3)
        )
        
        # Technical Score (0-100)
        technical_score = (
            (technical_analysis['modern_js_usage'] * 0.3) +
            (50 if technical_analysis['build_tools_present'] else 0) * 0.2 +
            (30 if technical_analysis['testing_present'] else 0) * 0.2 +
            (technical_analysis['documentation_quality'] * 0.3)
        )
        
        # Performance Score (0-100)
        performance_score = (
            (performance_analysis['image_optimization'] * 0.3) +
            (performance_analysis['file_size_efficiency'] * 0.3) +
            (performance_analysis['loading_optimization'] * 0.4)
        )
        
        # Overall Rating
        overall_score = (ui_score + ux_score + technical_score + performance_score) / 4
        
        if overall_score >= 85:
            overall_rating = 'Excellent'
        elif overall_score >= 70:
            overall_rating = 'Good'
        elif overall_score >= 55:
            overall_rating = 'Fair'
        else:
            overall_rating = 'Needs Improvement'
        
        return {
            'ui_score': round(ui_score),
            'ux_score': round(ux_score),
            'technical_score': round(technical_score),
            'performance_score': round(performance_score),
            'overall_rating': overall_rating
        }
    
    def generate_improvement_suggestions(self, ui_analysis, technical_analysis, performance_analysis, structure_analysis):
        """Generate specific improvement suggestions"""
        suggestions = []
        
        # UI/UX Suggestions
        if not ui_analysis['responsive_design']:
            suggestions.append("Add responsive design with CSS media queries for mobile compatibility")
        
        if ui_analysis['accessibility_score'] < 50:
            suggestions.append("Improve accessibility by adding alt attributes, ARIA labels, and semantic HTML")
        
        if ui_analysis['semantic_html_score'] < 50:
            suggestions.append("Use more semantic HTML5 elements (header, nav, main, section, article, footer)")
        
        if ui_analysis['modern_css_usage'] < 70:
            suggestions.append("Adopt modern CSS features like Flexbox, Grid, and CSS custom properties")
        
        # Technical Suggestions
        if not technical_analysis['build_tools_present']:
            suggestions.append("Consider using build tools like Webpack, Vite, or Parcel for better development workflow")
        
        if technical_analysis['modern_js_usage'] < 70:
            suggestions.append("Use modern JavaScript features like ES6+ syntax, modules, and async/await")
        
        if not technical_analysis['testing_present']:
            suggestions.append("Add unit tests to ensure code reliability and maintainability")
        
        if technical_analysis['documentation_quality'] < 50:
            suggestions.append("Create comprehensive README.md with project description, setup instructions, and usage examples")
        
        # Performance Suggestions
        if performance_analysis['image_optimization'] < 70:
            suggestions.append("Optimize images by using modern formats (WebP, SVG) and appropriate compression")
        
        if performance_analysis['loading_optimization'] < 50:
            suggestions.append("Implement lazy loading, code splitting, and resource preloading for better performance")
        
        # Structure Suggestions
        if structure_analysis['organization_score'] < 60:
            suggestions.append("Organize code into logical folders (src/, assets/, components/, styles/)")
        
        if not structure_analysis['has_readme']:
            suggestions.append("Add a README.md file with project overview and setup instructions")
        
        # General Suggestions
        suggestions.append("Consider adding a live demo link or screenshots to showcase your work")
        suggestions.append("Include comments in your code to explain complex logic and design decisions")
        
        return suggestions[:8]  # Limit to top 8 suggestions
    
    def cleanup_extracted_files(self, extracted_path):
        """Clean up extracted files"""
        import shutil
        try:
            if os.path.exists(extracted_path):
                shutil.rmtree(extracted_path)
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def get_error_result(self, error_message):
        """Return error result structure"""
        return {
            'error': True,
            'message': error_message,
            'ui_score': 0,
            'ux_score': 0,
            'technical_score': 0,
            'performance_score': 0,
            'overall_rating': 'Unknown',
            'suggestions': ['Please upload a valid portfolio archive'],
            'technologies_detected': []
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = PortfolioAnalyzer()
    
    # Test with sample HTML content
    sample_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Portfolio</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#projects">Projects</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="home">
                <h1>Welcome to My Portfolio</h1>
                <img src="profile.jpg" alt="Profile picture">
            </section>
        </main>
        <footer>
            <p>&copy; 2024 My Portfolio</p>
        </footer>
    </body>
    </html>
    '''
    
    # Test HTML analysis
    html_analysis = analyzer.analyze_html_file(sample_html, 'index.html')
    print("HTML Analysis:")
    print(json.dumps(html_analysis, indent=2))