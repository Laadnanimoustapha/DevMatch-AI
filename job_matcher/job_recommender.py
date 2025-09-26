"""
DevMatch AI - Job Recommender Module
Intelligent job matching based on skills and experience analysis
"""

import json
import random
from datetime import datetime
from collections import Counter
import re

class JobRecommender:
    def __init__(self):
        self.load_job_database()
        self.load_skill_weights()
        self.load_salary_data()
    
    def load_job_database(self):
        """Load comprehensive job database"""
        self.job_database = {
            'frontend_developer': {
                'titles': ['Frontend Developer', 'UI Developer', 'React Developer', 'Vue.js Developer', 'Angular Developer'],
                'required_skills': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript'],
                'preferred_skills': ['sass', 'webpack', 'git', 'responsive design', 'ui/ux', 'bootstrap', 'tailwind'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (45000, 65000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (65000, 90000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (90000, 130000)}
                },
                'companies': ['TechCorp', 'WebSolutions Inc.', 'Digital Innovations', 'StartupHub', 'CreativeAgency'],
                'locations': ['Remote', 'New York, NY', 'San Francisco, CA', 'Austin, TX', 'Seattle, WA'],
                'descriptions': [
                    'Build responsive web applications using modern JavaScript frameworks',
                    'Create engaging user interfaces with attention to detail and user experience',
                    'Collaborate with designers and backend developers to deliver high-quality products',
                    'Develop and maintain frontend components using React and TypeScript'
                ]
            },
            'backend_developer': {
                'titles': ['Backend Developer', 'API Developer', 'Server-Side Developer', 'Python Developer', 'Node.js Developer'],
                'required_skills': ['python', 'java', 'node.js', 'sql', 'api', 'database', 'rest'],
                'preferred_skills': ['docker', 'kubernetes', 'aws', 'mongodb', 'postgresql', 'redis', 'microservices'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (50000, 70000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (70000, 95000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (95000, 140000)}
                },
                'companies': ['DataSoft Solutions', 'CloudTech Systems', 'Enterprise Solutions', 'ScaleUp Technologies'],
                'locations': ['Remote', 'Chicago, IL', 'Boston, MA', 'Denver, CO', 'Portland, OR'],
                'descriptions': [
                    'Design and implement scalable backend systems and APIs',
                    'Work with databases and ensure optimal performance and security',
                    'Build microservices architecture for enterprise applications',
                    'Collaborate with frontend teams to integrate APIs and services'
                ]
            },
            'fullstack_developer': {
                'titles': ['Full Stack Developer', 'Software Engineer', 'Web Developer', 'Application Developer'],
                'required_skills': ['javascript', 'python', 'react', 'node.js', 'sql', 'html', 'css'],
                'preferred_skills': ['typescript', 'mongodb', 'aws', 'docker', 'git', 'agile', 'rest api'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (55000, 75000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (75000, 100000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (100000, 150000)}
                },
                'companies': ['Innovation Labs', 'TechStartup Co.', 'Digital Solutions', 'AgileWorks', 'CodeCraft'],
                'locations': ['Remote', 'San Francisco, CA', 'New York, NY', 'Los Angeles, CA', 'Miami, FL'],
                'descriptions': [
                    'Develop end-to-end web applications using modern technology stack',
                    'Work on both frontend and backend components of web applications',
                    'Collaborate in an agile environment to deliver high-quality software',
                    'Build and maintain scalable web applications from concept to deployment'
                ]
            },
            'data_scientist': {
                'titles': ['Data Scientist', 'ML Engineer', 'Data Analyst', 'AI Specialist', 'Research Scientist'],
                'required_skills': ['python', 'r', 'machine learning', 'statistics', 'sql', 'pandas', 'numpy'],
                'preferred_skills': ['tensorflow', 'pytorch', 'scikit-learn', 'jupyter', 'tableau', 'spark', 'aws'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (60000, 80000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (80000, 120000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (120000, 180000)}
                },
                'companies': ['DataCorp Analytics', 'AI Innovations', 'Research Institute', 'BigData Solutions'],
                'locations': ['Remote', 'San Francisco, CA', 'Boston, MA', 'Seattle, WA', 'Austin, TX'],
                'descriptions': [
                    'Analyze large datasets to extract meaningful insights and patterns',
                    'Build and deploy machine learning models for business applications',
                    'Work with stakeholders to understand business requirements and translate them into data solutions',
                    'Develop predictive models and algorithms to solve complex business problems'
                ]
            },
            'devops_engineer': {
                'titles': ['DevOps Engineer', 'Site Reliability Engineer', 'Cloud Engineer', 'Infrastructure Engineer'],
                'required_skills': ['docker', 'kubernetes', 'aws', 'linux', 'bash', 'ci/cd', 'git'],
                'preferred_skills': ['terraform', 'ansible', 'jenkins', 'monitoring', 'python', 'helm', 'prometheus'],
                'experience_levels': {
                    'junior': {'min_years': 1, 'max_years': 3, 'salary_range': (60000, 85000)},
                    'mid': {'min_years': 3, 'max_years': 6, 'salary_range': (85000, 120000)},
                    'senior': {'min_years': 6, 'max_years': 15, 'salary_range': (120000, 170000)}
                },
                'companies': ['CloudOps Solutions', 'Infrastructure Inc.', 'DevOps Consulting', 'ScaleOps'],
                'locations': ['Remote', 'Seattle, WA', 'San Francisco, CA', 'Austin, TX', 'Denver, CO'],
                'descriptions': [
                    'Design and maintain CI/CD pipelines for automated deployment',
                    'Manage cloud infrastructure and ensure high availability',
                    'Implement monitoring and alerting systems for production environments',
                    'Collaborate with development teams to improve deployment processes'
                ]
            },
            'mobile_developer': {
                'titles': ['Mobile Developer', 'iOS Developer', 'Android Developer', 'React Native Developer', 'Flutter Developer'],
                'required_skills': ['swift', 'kotlin', 'react native', 'flutter', 'mobile', 'ios', 'android'],
                'preferred_skills': ['firebase', 'api integration', 'ui/ux', 'app store', 'git', 'agile'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (55000, 75000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (75000, 105000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (105000, 145000)}
                },
                'companies': ['MobileFirst', 'AppDev Studios', 'Mobile Solutions Inc.', 'CrossPlatform Co.'],
                'locations': ['Remote', 'San Francisco, CA', 'New York, NY', 'Los Angeles, CA', 'Chicago, IL'],
                'descriptions': [
                    'Develop native and cross-platform mobile applications',
                    'Work with designers to create intuitive mobile user experiences',
                    'Integrate mobile apps with backend services and APIs',
                    'Optimize mobile applications for performance and user engagement'
                ]
            },
            'qa_engineer': {
                'titles': ['QA Engineer', 'Test Engineer', 'Quality Assurance Specialist', 'Automation Tester'],
                'required_skills': ['testing', 'qa', 'automation', 'selenium', 'test cases', 'bug tracking'],
                'preferred_skills': ['python', 'java', 'cypress', 'jest', 'postman', 'jira', 'agile'],
                'experience_levels': {
                    'junior': {'min_years': 0, 'max_years': 2, 'salary_range': (45000, 65000)},
                    'mid': {'min_years': 2, 'max_years': 5, 'salary_range': (65000, 85000)},
                    'senior': {'min_years': 5, 'max_years': 15, 'salary_range': (85000, 115000)}
                },
                'companies': ['QualityFirst', 'TestLab Solutions', 'Automation Experts', 'QA Consulting'],
                'locations': ['Remote', 'Austin, TX', 'Raleigh, NC', 'Phoenix, AZ', 'Tampa, FL'],
                'descriptions': [
                    'Design and execute comprehensive test plans for software applications',
                    'Develop automated test scripts and maintain test frameworks',
                    'Collaborate with development teams to ensure quality standards',
                    'Identify, document, and track software defects through resolution'
                ]
            }
        }
    
    def load_skill_weights(self):
        """Load skill importance weights for different roles"""
        self.skill_weights = {
            'programming_languages': 3.0,
            'frameworks': 2.5,
            'databases': 2.0,
            'cloud_platforms': 2.0,
            'tools': 1.5,
            'methodologies': 1.0,
            'soft_skills': 1.0
        }
    
    def load_salary_data(self):
        """Load salary adjustment factors"""
        self.location_multipliers = {
            'San Francisco, CA': 1.4,
            'New York, NY': 1.3,
            'Seattle, WA': 1.2,
            'Los Angeles, CA': 1.15,
            'Boston, MA': 1.1,
            'Austin, TX': 1.0,
            'Chicago, IL': 1.0,
            'Denver, CO': 0.95,
            'Remote': 1.1,
            'Default': 0.9
        }
    
    def recommend_jobs(self, skills, experience_level='Mid-level', years_experience=3, location_preference=None):
        """Generate job recommendations based on skills and experience"""
        try:
            # Normalize inputs
            skills_lower = [skill.lower() for skill in skills]
            exp_level = self.normalize_experience_level(experience_level)
            
            # Calculate job matches
            job_matches = []
            
            for job_type, job_data in self.job_database.items():
                match_score = self.calculate_match_score(skills_lower, job_data, exp_level)
                
                if match_score >= 30:  # Minimum threshold
                    jobs = self.generate_job_listings(job_data, exp_level, match_score, location_preference)
                    job_matches.extend(jobs)
            
            # Sort by match score and return top matches
            job_matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            return job_matches[:10]  # Return top 10 matches
            
        except Exception as e:
            print(f"Job recommendation error: {e}")
            return self.get_fallback_recommendations()
    
    def normalize_experience_level(self, experience_level):
        """Normalize experience level to standard format"""
        level_map = {
            'junior': 'junior',
            'entry': 'junior',
            'entry-level': 'junior',
            'mid': 'mid',
            'mid-level': 'mid',
            'middle': 'mid',
            'senior': 'senior',
            'lead': 'senior',
            'principal': 'senior'
        }
        
        return level_map.get(experience_level.lower().replace(' ', '-'), 'mid')
    
    def calculate_match_score(self, user_skills, job_data, experience_level):
        """Calculate how well user skills match job requirements"""
        required_skills = [skill.lower() for skill in job_data['required_skills']]
        preferred_skills = [skill.lower() for skill in job_data['preferred_skills']]
        
        # Calculate required skills match
        required_matches = sum(1 for skill in required_skills if any(user_skill in skill or skill in user_skill for user_skill in user_skills))
        required_score = (required_matches / len(required_skills)) * 70 if required_skills else 0
        
        # Calculate preferred skills match
        preferred_matches = sum(1 for skill in preferred_skills if any(user_skill in skill or skill in user_skill for user_skill in user_skills))
        preferred_score = (preferred_matches / len(preferred_skills)) * 30 if preferred_skills else 0
        
        # Experience level bonus
        exp_bonus = 0
        if experience_level in job_data['experience_levels']:
            exp_bonus = 10
        
        total_score = required_score + preferred_score + exp_bonus
        
        # Apply skill weight bonuses
        bonus_score = self.calculate_skill_bonuses(user_skills, job_data)
        
        return min(100, total_score + bonus_score)
    
    def calculate_skill_bonuses(self, user_skills, job_data):
        """Calculate bonus points for high-value skills"""
        bonus = 0
        
        # High-demand skills bonus
        high_demand_skills = ['react', 'python', 'aws', 'docker', 'kubernetes', 'machine learning', 'typescript']
        
        for skill in user_skills:
            if skill in high_demand_skills:
                bonus += 2
        
        return min(15, bonus)  # Cap bonus at 15 points
    
    def generate_job_listings(self, job_data, experience_level, match_score, location_preference=None):
        """Generate specific job listings for a job type"""
        jobs = []
        
        # Generate 1-3 jobs per job type based on match score
        num_jobs = 3 if match_score >= 80 else 2 if match_score >= 60 else 1
        
        for _ in range(num_jobs):
            job = self.create_job_listing(job_data, experience_level, match_score, location_preference)
            jobs.append(job)
        
        return jobs
    
    def create_job_listing(self, job_data, experience_level, match_score, location_preference=None):
        """Create a single job listing"""
        # Select random elements for variety
        title = random.choice(job_data['titles'])
        company = random.choice(job_data['companies'])
        description = random.choice(job_data['descriptions'])
        
        # Select location
        if location_preference and location_preference in job_data['locations']:
            location = location_preference
        else:
            location = random.choice(job_data['locations'])
        
        # Calculate salary range
        salary_range = self.calculate_salary_range(job_data, experience_level, location)
        
        # Select required skills (subset for display)
        required_skills = random.sample(
            job_data['required_skills'] + job_data['preferred_skills'][:3], 
            min(6, len(job_data['required_skills']) + 3)
        )
        
        return {
            'title': title,
            'company': company,
            'location': location,
            'salary_range': salary_range,
            'match_score': int(match_score),
            'required_skills': [skill.title() for skill in required_skills],
            'description': description,
            'experience_level': experience_level.title(),
            'posted_date': self.generate_posted_date(),
            'job_type': 'Full-time',
            'remote_friendly': location == 'Remote' or random.choice([True, False])
        }
    
    def calculate_salary_range(self, job_data, experience_level, location):
        """Calculate salary range based on experience and location"""
        if experience_level not in job_data['experience_levels']:
            experience_level = 'mid'  # Default
        
        base_range = job_data['experience_levels'][experience_level]['salary_range']
        multiplier = self.location_multipliers.get(location, self.location_multipliers['Default'])
        
        min_salary = int(base_range[0] * multiplier)
        max_salary = int(base_range[1] * multiplier)
        
        return f"${min_salary:,} - ${max_salary:,}"
    
    def generate_posted_date(self):
        """Generate a realistic posted date"""
        days_ago = random.randint(1, 30)
        if days_ago == 1:
            return "1 day ago"
        elif days_ago < 7:
            return f"{days_ago} days ago"
        elif days_ago < 14:
            return "1 week ago"
        elif days_ago < 21:
            return "2 weeks ago"
        else:
            return "3+ weeks ago"
    
    def get_market_insights(self, skills, experience_level):
        """Get market insights for given skills and experience"""
        insights = {
            'skill_demand': self.analyze_skill_demand(skills),
            'salary_trends': self.get_salary_trends(experience_level),
            'growth_areas': self.identify_growth_areas(skills),
            'recommendations': self.get_career_recommendations(skills, experience_level)
        }
        
        return insights
    
    def analyze_skill_demand(self, skills):
        """Analyze demand for user's skills"""
        high_demand = ['python', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'machine learning']
        medium_demand = ['java', 'node.js', 'angular', 'vue', 'sql', 'mongodb', 'git']
        
        skill_analysis = {}
        
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in high_demand:
                skill_analysis[skill] = 'High Demand'
            elif skill_lower in medium_demand:
                skill_analysis[skill] = 'Medium Demand'
            else:
                skill_analysis[skill] = 'Stable Demand'
        
        return skill_analysis
    
    def get_salary_trends(self, experience_level):
        """Get salary trend information"""
        trends = {
            'junior': {
                'average_increase': '15-25% annually',
                'market_outlook': 'Strong entry-level demand',
                'top_paying_skills': ['Python', 'React', 'AWS']
            },
            'mid': {
                'average_increase': '8-15% annually',
                'market_outlook': 'Excellent growth opportunities',
                'top_paying_skills': ['Machine Learning', 'DevOps', 'Cloud Architecture']
            },
            'senior': {
                'average_increase': '5-12% annually',
                'market_outlook': 'Leadership and specialization focus',
                'top_paying_skills': ['AI/ML', 'System Architecture', 'Team Leadership']
            }
        }
        
        exp_level = self.normalize_experience_level(experience_level)
        return trends.get(exp_level, trends['mid'])
    
    def identify_growth_areas(self, skills):
        """Identify areas for skill growth"""
        growth_suggestions = []
        
        skill_categories = {
            'frontend': ['html', 'css', 'javascript', 'react', 'vue', 'angular'],
            'backend': ['python', 'java', 'node.js', 'sql', 'api'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'data': ['python', 'r', 'machine learning', 'sql', 'pandas'],
            'mobile': ['swift', 'kotlin', 'react native', 'flutter']
        }
        
        user_skills_lower = [skill.lower() for skill in skills]
        
        # Suggest complementary skills
        for category, category_skills in skill_categories.items():
            matches = sum(1 for skill in category_skills if skill in user_skills_lower)
            if matches >= 2:  # User has some skills in this category
                missing_skills = [skill for skill in category_skills if skill not in user_skills_lower]
                if missing_skills:
                    growth_suggestions.append({
                        'category': category.title(),
                        'suggested_skills': missing_skills[:3],
                        'reason': f'Complement your existing {category} skills'
                    })
        
        # Always suggest trending skills
        trending_skills = ['machine learning', 'docker', 'kubernetes', 'typescript', 'graphql']
        missing_trending = [skill for skill in trending_skills if skill not in user_skills_lower]
        
        if missing_trending:
            growth_suggestions.append({
                'category': 'Trending Technologies',
                'suggested_skills': missing_trending[:3],
                'reason': 'High-demand skills in the current market'
            })
        
        return growth_suggestions[:4]  # Limit to top 4 suggestions
    
    def get_career_recommendations(self, skills, experience_level):
        """Get career path recommendations"""
        recommendations = []
        
        skill_lower = [skill.lower() for skill in skills]
        exp_level = self.normalize_experience_level(experience_level)
        
        # Frontend path
        if any(skill in skill_lower for skill in ['html', 'css', 'javascript', 'react', 'vue', 'angular']):
            recommendations.append({
                'path': 'Frontend Specialization',
                'next_steps': ['Master TypeScript', 'Learn advanced React patterns', 'Study UI/UX principles'],
                'timeline': '6-12 months'
            })
        
        # Backend path
        if any(skill in skill_lower for skill in ['python', 'java', 'node.js', 'sql', 'api']):
            recommendations.append({
                'path': 'Backend/API Development',
                'next_steps': ['Learn microservices', 'Master cloud platforms', 'Study system design'],
                'timeline': '8-15 months'
            })
        
        # Data path
        if any(skill in skill_lower for skill in ['python', 'r', 'sql', 'machine learning', 'statistics']):
            recommendations.append({
                'path': 'Data Science/ML Engineering',
                'next_steps': ['Advanced ML algorithms', 'Big data tools', 'MLOps practices'],
                'timeline': '12-18 months'
            })
        
        # Leadership path for senior developers
        if exp_level == 'senior':
            recommendations.append({
                'path': 'Technical Leadership',
                'next_steps': ['Team management', 'Architecture design', 'Mentoring skills'],
                'timeline': '6-12 months'
            })
        
        return recommendations[:3]  # Limit to top 3 recommendations
    
    def get_fallback_recommendations(self):
        """Provide fallback recommendations when analysis fails"""
        return [
            {
                'title': 'Software Developer',
                'company': 'TechCorp Inc.',
                'location': 'Remote',
                'salary_range': '$60,000 - $80,000',
                'match_score': 75,
                'required_skills': ['JavaScript', 'Python', 'Git', 'SQL'],
                'description': 'Join our team to build innovative software solutions.',
                'experience_level': 'Mid',
                'posted_date': '2 days ago',
                'job_type': 'Full-time',
                'remote_friendly': True
            },
            {
                'title': 'Web Developer',
                'company': 'Digital Solutions',
                'location': 'New York, NY',
                'salary_range': '$55,000 - $75,000',
                'match_score': 70,
                'required_skills': ['HTML', 'CSS', 'JavaScript', 'React'],
                'description': 'Create engaging web experiences for our clients.',
                'experience_level': 'Mid',
                'posted_date': '1 week ago',
                'job_type': 'Full-time',
                'remote_friendly': False
            }
        ]

# Example usage and testing
if __name__ == "__main__":
    recommender = JobRecommender()
    
    # Test job recommendations
    test_skills = ['Python', 'JavaScript', 'React', 'SQL', 'Git', 'Docker']
    recommendations = recommender.recommend_jobs(test_skills, 'Mid-level', 3)
    
    print("Job Recommendations:")
    for job in recommendations[:3]:
        print(f"- {job['title']} at {job['company']} ({job['match_score']}% match)")
    
    # Test market insights
    insights = recommender.get_market_insights(test_skills, 'Mid-level')
    print(f"\nMarket Insights:")
    print(f"Skill Demand: {insights['skill_demand']}")
    print(f"Growth Areas: {len(insights['growth_areas'])} suggestions")