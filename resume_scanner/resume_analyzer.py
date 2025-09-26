"""
DevMatch AI - Resume Analyzer Module
Advanced NLP-powered resume analysis with ML recommendations
"""

import os
import re
import json
import PyPDF2
import docx
from collections import Counter
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("spaCy not available - using basic NLP features")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ResumeAnalyzer:
    def __init__(self):
        self.setup_nltk()
        self.setup_spacy()
        self.load_skill_database()
        self.load_job_keywords()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            # Try to download NLTK data
            print("Setting up NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            print("NLTK setup completed successfully")
        except Exception as e:
            print(f"NLTK setup failed: {e}")
            print("Using basic text processing without NLTK features")
            # Fallback to basic stop words
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.lemmatizer = None
    
    def setup_spacy(self):
        """Setup spaCy NLP pipeline"""
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Warning: spaCy model not found. Using basic NLP features.")
                self.nlp = None
        else:
            print("spaCy not available. Using basic NLP features.")
            self.nlp = None
    
    def load_skill_database(self):
        """Load comprehensive skill database"""
        self.skills_db = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl',
                'shell', 'bash', 'powershell', 'sql', 'html', 'css', 'sass', 'less'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
                'express', 'node.js', 'laravel', 'rails', 'asp.net', 'bootstrap',
                'tailwind', 'jquery', 'redux', 'vuex', 'nextjs', 'nuxtjs'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'sqlite', 'oracle', 'sql server', 'cassandra', 'dynamodb',
                'firebase', 'supabase', 'neo4j', 'influxdb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'vercel',
                'netlify', 'digitalocean', 'linode', 'cloudflare'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'docker', 'kubernetes',
                'jenkins', 'travis ci', 'circle ci', 'ansible', 'terraform',
                'vagrant', 'webpack', 'vite', 'gulp', 'grunt', 'npm', 'yarn',
                'pip', 'maven', 'gradle', 'cmake'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
                'microservices', 'rest api', 'graphql', 'soap', 'mvc', 'mvvm'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical thinking', 'creativity', 'adaptability', 'time management',
                'project management', 'mentoring', 'collaboration'
            ]
        }
        
        # Flatten all skills for easy searching
        self.all_skills = []
        for category, skills in self.skills_db.items():
            self.all_skills.extend(skills)
    
    def load_job_keywords(self):
        """Load job-specific keywords for different roles"""
        self.job_keywords = {
            'frontend_developer': [
                'react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css',
                'responsive design', 'ui/ux', 'webpack', 'sass', 'bootstrap'
            ],
            'backend_developer': [
                'python', 'java', 'node.js', 'api', 'database', 'sql', 'mongodb',
                'microservices', 'rest', 'graphql', 'docker', 'kubernetes'
            ],
            'fullstack_developer': [
                'javascript', 'python', 'react', 'node.js', 'database', 'api',
                'git', 'docker', 'aws', 'mongodb', 'sql', 'html', 'css'
            ],
            'data_scientist': [
                'python', 'r', 'machine learning', 'deep learning', 'pandas',
                'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'sql', 'statistics'
            ],
            'devops_engineer': [
                'docker', 'kubernetes', 'aws', 'jenkins', 'terraform', 'ansible',
                'ci/cd', 'monitoring', 'linux', 'bash', 'python', 'git'
            ],
            'mobile_developer': [
                'react native', 'flutter', 'swift', 'kotlin', 'ios', 'android',
                'mobile', 'app store', 'firebase', 'api integration'
            ]
        }
    
    def analyze_file(self, filepath):
        """Main analysis function"""
        try:
            # Extract text from file
            text = self.extract_text(filepath)
            
            if not text:
                return self.get_error_result("Could not extract text from file")
            
            # Perform comprehensive analysis
            results = {
                'filename': os.path.basename(filepath),
                'analysis_date': datetime.now().isoformat(),
                'text_length': len(text),
                'word_count': len(text.split()),
                **self.analyze_content(text)
            }
            
            return results
            
        except Exception as e:
            return self.get_error_result(f"Analysis failed: {str(e)}")
    
    def extract_text(self, filepath):
        """Extract text from various file formats"""
        file_ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if file_ext == '.pdf':
                return self.extract_pdf_text(filepath)
            elif file_ext in ['.doc', '.docx']:
                return self.extract_docx_text(filepath)
            elif file_ext == '.txt':
                return self.extract_txt_text(filepath)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            print(f"Text extraction error: {e}")
            return ""
    
    def extract_pdf_text(self, filepath):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PDF extraction error: {e}")
        return text
    
    def extract_docx_text(self, filepath):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"DOCX extraction error: {e}")
        return text
    
    def extract_txt_text(self, filepath):
        """Extract text from TXT file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            print(f"TXT extraction error: {e}")
            return ""
    
    def analyze_content(self, text):
        """Comprehensive content analysis"""
        # Clean and preprocess text
        cleaned_text = self.clean_text(text)
        
        # Extract various information
        skills_found = self.extract_skills(cleaned_text)
        contact_info = self.extract_contact_info(text)
        experience_info = self.analyze_experience(text)
        education_info = self.extract_education(text)
        
        # Calculate scores
        ats_score = self.calculate_ats_score(text, skills_found)
        overall_score = self.calculate_overall_score(text, skills_found, experience_info)
        
        # Generate recommendations
        suggestions = self.generate_suggestions(text, skills_found, experience_info)
        missing_keywords = self.find_missing_keywords(skills_found)
        
        return {
            'score': overall_score,
            'ats_score': ats_score,
            'skills_found': skills_found,
            'missing_keywords': missing_keywords,
            'suggestions': suggestions,
            'experience_level': experience_info['level'],
            'years_experience': experience_info['years'],
            'contact_info': contact_info,
            'education': education_info,
            'keyword_density': self.calculate_keyword_density(cleaned_text),
            'readability_score': self.calculate_readability(text),
            'sections_found': self.identify_sections(text)
        }
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\-\+\#\@]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text):
        """Extract technical skills from text"""
        found_skills = []
        text_lower = text.lower()
        
        # Check for each skill in our database
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        # Also look for programming languages with common variations
        language_variations = {
            'javascript': ['js', 'javascript', 'ecmascript'],
            'typescript': ['ts', 'typescript'],
            'python': ['python', 'python3', 'py'],
            'c++': ['c++', 'cpp', 'cplusplus'],
            'c#': ['c#', 'csharp', 'c sharp'],
            'node.js': ['node', 'nodejs', 'node.js']
        }
        
        for main_lang, variations in language_variations.items():
            for variation in variations:
                pattern = r'\b' + re.escape(variation.lower()) + r'\b'
                if re.search(pattern, text_lower) and main_lang.title() not in found_skills:
                    found_skills.append(main_lang.title())
        
        return found_skills[:20]  # Limit to top 20 skills
    
    def extract_contact_info(self, text):
        """Extract contact information"""
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone pattern
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text.lower())
        if linkedin:
            contact_info['linkedin'] = linkedin[0]
        
        # GitHub pattern
        github_pattern = r'github\.com/[\w-]+'
        github = re.findall(github_pattern, text.lower())
        if github:
            contact_info['github'] = github[0]
        
        return contact_info
    
    def analyze_experience(self, text):
        """Analyze work experience"""
        text_lower = text.lower()
        
        # Look for year patterns
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        
        current_year = datetime.now().year
        experience_years = 0
        
        if years:
            min_year = min(years)
            experience_years = max(0, current_year - min_year)
        
        # Look for experience keywords
        experience_keywords = [
            'years of experience', 'years experience', 'experience',
            'worked', 'developed', 'managed', 'led', 'created',
            'implemented', 'designed', 'built', 'maintained'
        ]
        
        experience_mentions = sum(1 for keyword in experience_keywords 
                                if keyword in text_lower)
        
        # Determine experience level
        if experience_years >= 8 or 'senior' in text_lower or 'lead' in text_lower:
            level = 'Senior'
        elif experience_years >= 3 or 'mid' in text_lower:
            level = 'Mid-level'
        elif 'junior' in text_lower or 'entry' in text_lower or experience_years < 2:
            level = 'Junior'
        else:
            level = 'Mid-level'  # Default
        
        return {
            'years': experience_years,
            'level': level,
            'mentions': experience_mentions
        }
    
    def extract_education(self, text):
        """Extract education information"""
        education = []
        text_lower = text.lower()
        
        # Common degree patterns
        degree_patterns = [
            r'\b(bachelor|ba|bs|b\.a\.|b\.s\.)\b',
            r'\b(master|ma|ms|m\.a\.|m\.s\.|mba)\b',
            r'\b(phd|ph\.d\.|doctorate|doctoral)\b',
            r'\b(associate|aa|as|a\.a\.|a\.s\.)\b'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                education.extend(matches)
        
        # Look for common fields of study
        fields = [
            'computer science', 'software engineering', 'information technology',
            'electrical engineering', 'mathematics', 'physics', 'data science',
            'business', 'marketing', 'design', 'psychology'
        ]
        
        found_fields = [field for field in fields if field in text_lower]
        
        return {
            'degrees': list(set(education)),
            'fields': found_fields
        }
    
    def calculate_ats_score(self, text, skills_found):
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        score = 0
        
        # Check for contact information
        if '@' in text:  # Email
            score += 15
        if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text):  # Phone
            score += 10
        
        # Check for standard sections
        sections = ['experience', 'education', 'skills', 'summary', 'objective']
        for section in sections:
            if section in text.lower():
                score += 8
        
        # Skills presence
        if len(skills_found) >= 5:
            score += 20
        elif len(skills_found) >= 3:
            score += 15
        elif len(skills_found) >= 1:
            score += 10
        
        # Text formatting (simple checks)
        if len(text.split('\n')) > 10:  # Multiple lines suggest structure
            score += 10
        
        # Quantifiable achievements (numbers)
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 5:
            score += 15
        elif len(numbers) >= 3:
            score += 10
        
        return min(100, score)
    
    def calculate_overall_score(self, text, skills_found, experience_info):
        """Calculate overall resume score"""
        score = 0
        
        # Skills score (30%)
        skills_score = min(30, len(skills_found) * 2)
        score += skills_score
        
        # Experience score (25%)
        exp_score = min(25, experience_info['years'] * 3)
        score += exp_score
        
        # Content quality score (25%)
        word_count = len(text.split())
        if word_count >= 300:
            content_score = 25
        elif word_count >= 200:
            content_score = 20
        elif word_count >= 100:
            content_score = 15
        else:
            content_score = 10
        score += content_score
        
        # Structure score (20%)
        structure_keywords = ['summary', 'experience', 'education', 'skills', 'projects']
        structure_score = sum(4 for keyword in structure_keywords if keyword in text.lower())
        score += structure_score
        
        return min(100, score)
    
    def calculate_keyword_density(self, text):
        """Calculate keyword density for important terms"""
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        # Count important keywords
        important_keywords = [
            'experience', 'developed', 'managed', 'created', 'implemented',
            'designed', 'built', 'led', 'improved', 'optimized'
        ]
        
        density = {}
        for keyword in important_keywords:
            count = text.lower().count(keyword)
            density[keyword] = round((count / total_words) * 100, 2)
        
        return density
    
    def calculate_readability(self, text):
        """Calculate basic readability score"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        if not sentences or not words:
            return 0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability score (lower is better for resumes)
        if avg_sentence_length <= 15:
            return 90
        elif avg_sentence_length <= 20:
            return 75
        elif avg_sentence_length <= 25:
            return 60
        else:
            return 40
    
    def identify_sections(self, text):
        """Identify resume sections"""
        sections = []
        text_lower = text.lower()
        
        section_keywords = {
            'summary': ['summary', 'profile', 'objective', 'about'],
            'experience': ['experience', 'work history', 'employment', 'career'],
            'education': ['education', 'academic', 'degree', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'competencies', 'technologies'],
            'projects': ['projects', 'portfolio', 'work samples'],
            'certifications': ['certifications', 'certificates', 'licensed'],
            'awards': ['awards', 'achievements', 'honors', 'recognition']
        }
        
        for section, keywords in section_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                sections.append(section)
        
        return sections
    
    def generate_suggestions(self, text, skills_found, experience_info):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Skills suggestions
        if len(skills_found) < 5:
            suggestions.append("Add more relevant technical skills to improve keyword matching")
        
        # Quantification suggestions
        numbers = re.findall(r'\d+', text)
        if len(numbers) < 3:
            suggestions.append("Include quantifiable achievements (e.g., 'Improved performance by 30%')")
        
        # Contact information
        if '@' not in text:
            suggestions.append("Ensure your email address is clearly visible")
        
        # Experience level suggestions
        if experience_info['level'] == 'Junior':
            suggestions.append("Highlight projects, internships, and relevant coursework")
        elif experience_info['level'] == 'Senior':
            suggestions.append("Emphasize leadership experience and team management")
        
        # Section suggestions
        sections = self.identify_sections(text)
        if 'summary' not in sections:
            suggestions.append("Add a professional summary at the top of your resume")
        if 'projects' not in sections and experience_info['level'] in ['Junior', 'Mid-level']:
            suggestions.append("Include a projects section to showcase your work")
        
        # ATS optimization
        suggestions.append("Use standard section headings (Experience, Education, Skills)")
        suggestions.append("Save your resume as both PDF and Word formats")
        
        # Content suggestions
        word_count = len(text.split())
        if word_count < 200:
            suggestions.append("Expand your resume content - aim for 300-500 words")
        elif word_count > 800:
            suggestions.append("Consider condensing your resume - keep it concise and relevant")
        
        return suggestions[:8]  # Limit to top 8 suggestions
    
    def find_missing_keywords(self, skills_found):
        """Find important keywords that are missing"""
        # Get trending skills for current year
        trending_skills = [
            'Machine Learning', 'Cloud Computing', 'DevOps', 'Microservices',
            'API Development', 'Agile', 'Docker', 'Kubernetes', 'React',
            'Python', 'JavaScript', 'Git', 'CI/CD', 'AWS'
        ]
        
        # Find missing trending skills
        skills_lower = [skill.lower() for skill in skills_found]
        missing = []
        
        for skill in trending_skills:
            if skill.lower() not in skills_lower:
                missing.append(skill)
        
        return missing[:6]  # Limit to top 6 missing keywords
    
    def get_error_result(self, error_message):
        """Return error result structure"""
        return {
            'error': True,
            'message': error_message,
            'score': 0,
            'ats_score': 0,
            'skills_found': [],
            'missing_keywords': [],
            'suggestions': ['Please upload a valid resume file'],
            'experience_level': 'Unknown',
            'years_experience': 0
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    # Test with sample text
    sample_text = """
    John Doe
    Software Developer
    john.doe@email.com
    (555) 123-4567
    
    SUMMARY
    Experienced software developer with 5 years of experience in Python, JavaScript, and React.
    
    EXPERIENCE
    Senior Developer at TechCorp (2020-2023)
    - Developed web applications using React and Node.js
    - Managed a team of 3 developers
    - Improved application performance by 40%
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2018)
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS
    """
    
    # Simulate file analysis
    results = analyzer.analyze_content(sample_text)
    print(json.dumps(results, indent=2))