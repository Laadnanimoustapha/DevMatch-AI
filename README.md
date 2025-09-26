# 🧠💼 DevMatch AI - Offline Resume & Code Analyzer Platform

An intelligent platform that analyzes developer resumes and code quality to provide personalized job matching and improvement suggestions.

## 🔧 Features

- **📝 Resume Analyzer**: ML-powered resume analysis with keyword extraction and skill scoring
- **🧪 Code Quality Test**: Multi-language code analysis (C++, Java, Go, Python, JavaScript)
- **🔍 Job Matcher**: Intelligent job recommendations based on detected skills
- **📊 Portfolio Analyzer**: UI/UX analysis and improvement suggestions
- **🌐 Offline Web Dashboard**: Complete privacy with local processing
- **📦 Export Tools**: Generate optimized resumes and detailed reports

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Start the Application**:
   ```bash
   python app.py
   ```

3. **Open Dashboard**:
   Navigate to `http://localhost:8080` in your browser

## 📁 Project Structure

```
DevMatch-AI/
├── frontend/              # Web dashboard (HTML/CSS/JS)
├── php_backend/          # PHP backend for file handling
├── resume_scanner/       # Python NLP & ML modules
├── code_analyzers/       # Multi-language code analysis
│   ├── cpp_analyzer/     # C++ code analysis
│   ├── java_analyzer/    # Java code analysis
│   ├── go_analyzer/      # Go code analysis
│   └── js_analyzer/      # JavaScript analysis
├── job_matcher/          # Job recommendation engine
├── portfolio_analyzer/   # Portfolio analysis tools
├── output_reports/       # Generated reports and exports
└── uploads/              # User uploaded files
```

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python (Flask), PHP
- **ML/NLP**: scikit-learn, NLTK, spaCy
- **Code Analysis**: Custom analyzers for each language
- **Database**: SQLite (local storage)

## 📊 Analysis Capabilities

### Resume Analysis
- Keyword extraction and matching
- Skill level assessment
- Experience quantification
- ATS compatibility scoring
- Improvement suggestions

### Code Quality Analysis
- **C++**: Memory management, performance optimization
- **Java**: OOP principles, design patterns
- **Go**: Concurrency patterns, error handling
- **Python**: Code style, best practices
- **JavaScript**: Modern ES6+ features, performance

### Job Matching
- Skill-based job recommendations
- Salary estimation
- Market demand analysis
- Career progression suggestions

## 🔒 Privacy & Security

- **100% Offline Processing**: All analysis happens locally
- **No Data Collection**: Your files never leave your machine
- **Secure File Handling**: Temporary files are automatically cleaned
- **Local Database**: All data stored in local SQLite database

## 📈 Export Options

- **Optimized Resume**: ATS-friendly format with improvements
- **Detailed Analysis Report**: Complete breakdown of findings
- **Job Recommendations**: Tailored job suggestions with match scores
- **Portfolio Improvements**: UI/UX enhancement suggestions

## 🎯 Use Cases

- **Job Seekers**: Optimize resume and showcase code quality
- **Freelancers**: Improve portfolio and find relevant gigs
- **Students**: Learn best practices and prepare for interviews
- **Career Changers**: Identify skill gaps and improvement areas

## 💰 Licensing

- **DevMatch Lite**: Free version with basic resume analysis
- **DevMatch Pro**: Full featured version with code analysis and job matching

---

Built with ❤️ for developers, by developers.