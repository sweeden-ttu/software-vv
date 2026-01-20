/**
 * Canvas LMS API Integration
 * Fetches and displays Canvas course data
 */

class CanvasIntegration {
    constructor() {
        this.apiUrl = '';
        this.apiKey = '';
        this.init();
    }

    async init() {
        // Load configuration from _config.yml or environment
        await this.loadConfig();
        
        if (this.apiUrl && this.apiKey) {
            this.loadCourses();
        } else {
            this.showSetupMessage();
        }
    }

    async loadConfig() {
        // In a real implementation, you'd fetch this from _config.yml
        // or from a server-side endpoint that reads environment variables
        // For now, we'll check for a config object in the page
        if (window.canvasConfig) {
            this.apiUrl = window.canvasConfig.apiUrl;
            this.apiKey = window.canvasConfig.apiKey;
        }
    }

    async loadCourses() {
        try {
            const response = await fetch(`${this.apiUrl}/api/v1/courses?enrollment_type=student&enrollment_state=active`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                }
            });

            if (!response.ok) {
                throw new Error(`Canvas API error: ${response.status}`);
            }

            const courses = await response.json();
            this.displayCourses(courses);
        } catch (error) {
            console.error('Error loading Canvas courses:', error);
            this.showError(error.message);
        }
    }

    displayCourses(courses) {
        const container = document.getElementById('canvas-courses');
        if (!container) return;

        if (courses.length === 0) {
            container.innerHTML = '<p>No active courses found.</p>';
            return;
        }

        const html = `
            <div class="courses-grid">
                ${courses.map(course => `
                    <div class="course-card">
                        <h3>${course.name || 'Unnamed Course'}</h3>
                        <p class="course-code">${course.course_code || ''}</p>
                        <a href="${this.apiUrl}/courses/${course.id}" target="_blank" class="btn btn-sm">View Course</a>
                    </div>
                `).join('')}
            </div>
        `;

        container.innerHTML = html;
    }

    showSetupMessage() {
        const container = document.getElementById('canvas-courses');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <p>Canvas LMS integration not configured. Please run the agent setup to configure your API keys.</p>
                </div>
            `;
        }
    }

    showError(message) {
        const container = document.getElementById('canvas-courses');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-error">
                    <p>Error loading Canvas courses: ${message}</p>
                </div>
            `;
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new CanvasIntegration();
});
