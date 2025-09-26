/**
 * DevMatch AI Dashboard JavaScript
 * Handles file uploads, analysis results, and user interactions
 */

class DevMatchDashboard {
    constructor() {
        this.currentTab = 'resume';
        this.analysisResults = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFileHandlers();
        this.setupDragAndDrop();
        console.log('🧠💼 DevMatch AI Dashboard initialized');
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // File input handlers
        document.getElementById('resume-file').addEventListener('change', (e) => {
            this.handleFileSelect(e, 'resume');
        });

        document.getElementById('code-file').addEventListener('change', (e) => {
            this.handleFileSelect(e, 'code');
        });

        document.getElementById('portfolio-file').addEventListener('change', (e) => {
            this.handleFileSelect(e, 'portfolio');
        });

        // Modal close handlers
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target.id);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });
    }

    setupFileHandlers() {
        // Setup file input change handlers
        const fileInputs = ['resume-file', 'code-file', 'portfolio-file'];
        fileInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('change', (e) => {
                    const analysisType = inputId.split('-')[0];
                    this.handleFileSelect(e, analysisType);
                });
            }
        });
    }

    setupDragAndDrop() {
        const uploadAreas = document.querySelectorAll('.upload-area');
        
        uploadAreas.forEach(area => {
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('dragover');
            });

            area.addEventListener('dragleave', (e) => {
                e.preventDefault();
                area.classList.remove('dragover');
            });

            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const analysisType = this.currentTab;
                    this.handleFileDrop(files[0], analysisType);
                }
            });
        });
    }

    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;
    }

    handleFileSelect(event, analysisType) {
        const file = event.target.files[0];
        if (file) {
            this.uploadFile(file, analysisType);
        }
    }

    handleFileDrop(file, analysisType) {
        this.uploadFile(file, analysisType);
    }

    async uploadFile(file, analysisType) {
        // Validate file
        if (!this.validateFile(file, analysisType)) {
            return;
        }

        // Show loading
        this.showLoading(`Analyzing ${file.name}...`);

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('analysis_type', analysisType);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.analysisResults[analysisType] = result.results;
                this.displayResults(result.results, analysisType);
                
                // If resume analysis, also get job recommendations
                if (analysisType === 'resume') {
                    await this.getJobRecommendations(result.results);
                }
                
                this.showSuccess(`Analysis complete for ${file.name}`);
            } else {
                this.showError(result.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showError('Failed to upload file. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    validateFile(file, analysisType) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        
        if (file.size > maxSize) {
            this.showError('File size must be less than 16MB');
            return false;
        }

        const allowedTypes = {
            resume: ['pdf', 'doc', 'docx', 'txt'],
            code: ['py', 'cpp', 'c', 'h', 'hpp', 'java', 'go', 'js', 'ts', 'html', 'css'],
            portfolio: ['zip', 'rar', 'tar', 'gz']
        };

        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (!allowedTypes[analysisType].includes(fileExtension)) {
            this.showError(`File type .${fileExtension} not supported for ${analysisType} analysis`);
            return false;
        }

        return true;
    }

    displayResults(results, analysisType) {
        const resultsSection = document.getElementById('results-section');
        const resultsContent = document.getElementById('results-content');
        
        let html = '';

        switch (analysisType) {
            case 'resume':
                html = this.generateResumeResults(results);
                break;
            case 'code':
                html = this.generateCodeResults(results);
                break;
            case 'portfolio':
                html = this.generatePortfolioResults(results);
                break;
        }

        resultsContent.innerHTML = html;
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    generateResumeResults(results) {
        const scoreClass = results.score >= 80 ? '' : results.score >= 60 ? 'warning' : 'danger';
        
        return `
            <div class="result-card fade-in">
                <div class="result-header">
                    <h3 class="result-title">📝 Resume Analysis</h3>
                    <span class="score-badge ${scoreClass}">${results.score}/100</span>
                </div>
                <div class="result-content">
                    <div class="result-item">
                        <h4>🎯 Skills Found</h4>
                        <div class="skills-grid">
                            ${results.skills_found.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                        </div>
                    </div>
                    <div class="result-item">
                        <h4>⚠️ Missing Keywords</h4>
                        <div class="skills-grid">
                            ${results.missing_keywords.map(keyword => `<span class="skill-tag missing">${keyword}</span>`).join('')}
                        </div>
                    </div>
                    <div class="result-item">
                        <h4>💡 Suggestions</h4>
                        <ul>
                            ${results.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="result-item">
                        <h4>🤖 ATS Compatibility</h4>
                        <div class="score-badge ${results.ats_score >= 70 ? '' : 'warning'}">${results.ats_score}/100</div>
                        <p style="margin-top: 0.5rem; color: var(--text-secondary);">
                            Experience Level: <strong>${results.experience_level}</strong>
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    generateCodeResults(results) {
        const scoreClass = results.quality_score >= 80 ? '' : results.quality_score >= 60 ? 'warning' : 'danger';
        
        return `
            <div class="result-card fade-in">
                <div class="result-header">
                    <h3 class="result-title">🧪 Code Quality Analysis</h3>
                    <span class="score-badge ${scoreClass}">${results.quality_score}/100</span>
                </div>
                <div class="result-content">
                    <div class="result-item">
                        <h4>💻 Language: ${results.language.toUpperCase()}</h4>
                        <p><strong>Complexity:</strong> ${results.complexity_score}</p>
                        <p><strong>Maintainability:</strong> ${results.maintainability}</p>
                    </div>
                    <div class="result-item">
                        <h4>🔍 Issues Found</h4>
                        <ul>
                            ${results.issues_found.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="result-item">
                        <h4>✅ Best Practices</h4>
                        <ul>
                            ${results.best_practices.map(practice => `<li>${practice}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    generatePortfolioResults(results) {
        return `
            <div class="result-card fade-in">
                <div class="result-header">
                    <h3 class="result-title">🎨 Portfolio Analysis</h3>
                    <span class="score-badge">${results.overall_rating}</span>
                </div>
                <div class="result-content">
                    <div class="result-item">
                        <h4>📊 Scores</h4>
                        <p><strong>UI Score:</strong> ${results.ui_score}/100</p>
                        <p><strong>UX Score:</strong> ${results.ux_score}/100</p>
                        <p><strong>Technical Score:</strong> ${results.technical_score}/100</p>
                    </div>
                    <div class="result-item">
                        <h4>🛠️ Technologies Detected</h4>
                        <div class="skills-grid">
                            ${results.technologies_detected.map(tech => `<span class="skill-tag">${tech}</span>`).join('')}
                        </div>
                    </div>
                    <div class="result-item">
                        <h4>💡 Improvement Suggestions</h4>
                        <ul>
                            ${results.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    async getJobRecommendations(resumeResults) {
        try {
            const response = await fetch('/job-match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    skills: resumeResults.skills_found,
                    experience_level: resumeResults.experience_level
                })
            });

            const result = await response.json();
            
            if (result.jobs) {
                this.displayJobRecommendations(result.jobs);
            }
        } catch (error) {
            console.error('Job matching error:', error);
        }
    }

    displayJobRecommendations(jobs) {
        const jobsSection = document.getElementById('jobs-section');
        const jobsContent = document.getElementById('jobs-content');
        
        const html = jobs.map(job => `
            <div class="job-card fade-in">
                <div class="job-header">
                    <div class="job-info">
                        <h3>${job.title}</h3>
                        <div class="company">${job.company}</div>
                        <div class="location">${job.location}</div>
                    </div>
                    <div class="match-score">${job.match_score}% Match</div>
                </div>
                <div class="job-details">
                    <div class="salary">${job.salary_range}</div>
                    <div class="job-description">${job.description}</div>
                    <div class="required-skills">
                        ${job.required_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                    </div>
                </div>
            </div>
        `).join('');

        jobsContent.innerHTML = html;
        jobsSection.style.display = 'block';
    }

    async showStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            const statsHtml = `
                <div class="stats-grid">
                    <div class="stat-item">
                        <h4>Total Analyses</h4>
                        <div class="stat-value">${stats.total_analyses}</div>
                    </div>
                    <div class="stat-item">
                        <h4>Resume Analyses</h4>
                        <div class="stat-value">${stats.analysis_breakdown.resume || 0}</div>
                    </div>
                    <div class="stat-item">
                        <h4>Code Analyses</h4>
                        <div class="stat-value">${stats.analysis_breakdown.code || 0}</div>
                    </div>
                    <div class="stat-item">
                        <h4>Portfolio Analyses</h4>
                        <div class="stat-value">${stats.analysis_breakdown.portfolio || 0}</div>
                    </div>
                    <div class="stat-item">
                        <h4>Status</h4>
                        <div class="stat-value">${stats.uptime}</div>
                    </div>
                    <div class="stat-item">
                        <h4>Version</h4>
                        <div class="stat-value">${stats.version}</div>
                    </div>
                </div>
                <style>
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 1rem;
                }
                .stat-item {
                    text-align: center;
                    padding: 1rem;
                    background: var(--bg-secondary);
                    border-radius: var(--radius-md);
                }
                .stat-item h4 {
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                    margin-bottom: 0.5rem;
                }
                .stat-value {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: var(--primary-color);
                }
                </style>
            `;
            
            document.getElementById('stats-content').innerHTML = statsHtml;
            this.showModal('stats-modal');
        } catch (error) {
            console.error('Stats error:', error);
            this.showError('Failed to load statistics');
        }
    }

    exportReport() {
        if (Object.keys(this.analysisResults).length === 0) {
            this.showError('No analysis results to export. Please analyze a file first.');
            return;
        }

        const sessionId = Date.now();
        window.open(`/export-report/${sessionId}`, '_blank');
        this.showSuccess('Report export initiated');
    }

    showLoading(message = 'Processing...') {
        const overlay = document.getElementById('loading-overlay');
        const text = document.getElementById('loading-text');
        text.textContent = message;
        overlay.style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
    }

    showModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'var(--secondary-color)' : type === 'error' ? 'var(--danger-color)' : 'var(--primary-color)'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
        `;

        // Add animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
        `;
        document.head.appendChild(style);

        // Add to DOM
        document.body.appendChild(notification);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }
}

// Global functions for HTML onclick handlers
function showStats() {
    dashboard.showStats();
}

function exportReport() {
    dashboard.exportReport();
}

function closeModal(modalId) {
    dashboard.closeModal(modalId);
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DevMatchDashboard();
});