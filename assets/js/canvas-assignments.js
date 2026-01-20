/**
 * Canvas Assignments Dynamic Updates
 * Fetches and displays assignment status, due dates, and submission info
 */

class CanvasAssignments {
    constructor() {
        this.apiUrl = '';
        this.apiKey = '';
        this.courseId = null;
        this.assignments = [];
        this.init();
    }

    async init() {
        await this.loadConfig();
        
        if (this.apiUrl && this.apiKey) {
            await this.loadAssignmentsFromCanvas();
            this.displayAssignments();
        } else {
            // Fallback to static JSON data
            await this.loadAssignmentsFromJSON();
            this.displayAssignments();
        }
    }

    async loadConfig() {
        // Try to load from window config (set by Jekyll/layout)
        if (window.canvasConfig) {
            this.apiUrl = window.canvasConfig.apiUrl;
            this.apiKey = window.canvasConfig.apiKey;
            this.courseId = window.canvasConfig.courseId;
        }
        
        // Or load from static JSON if available
        if (!this.apiKey) {
            try {
                const response = await fetch('/software-vv/_data/assignments.json');
                if (response.ok) {
                    const data = await response.json();
                    this.assignments = data;
                }
            } catch (e) {
                console.warn('Could not load assignments from JSON:', e);
            }
        }
    }

    async loadAssignmentsFromCanvas() {
        if (!this.courseId) {
            // Try to get course ID from courses list
            try {
                const response = await fetch(
                    `${this.apiUrl}/api/v1/courses?enrollment_type=student&enrollment_state=active`,
                    {
                        headers: { 'Authorization': `Bearer ${this.apiKey}` }
                    }
                );
                
                if (response.ok) {
                    const courses = await response.json();
                    // Find verification/validation course
                    const course = courses.find(c => 
                        c.name.toLowerCase().includes('verification') || 
                        c.name.toLowerCase().includes('validation')
                    ) || courses[0];
                    
                    this.courseId = course.id;
                }
            } catch (e) {
                console.error('Error fetching courses:', e);
                return;
            }
        }

        try {
            const response = await fetch(
                `${this.apiUrl}/api/v1/courses/${this.courseId}/assignments`,
                {
                    headers: { 'Authorization': `Bearer ${this.apiKey}` }
                }
            );

            if (response.ok) {
                const assignments = await response.json();
                this.assignments = assignments.map(a => ({
                    id: a.id,
                    name: a.name,
                    due_at: a.due_at,
                    points_possible: a.points_possible,
                    html_url: a.html_url,
                    submission: a.submission,
                    has_submitted_submissions: a.has_submitted_submissions
                }));
            }
        } catch (e) {
            console.error('Error fetching assignments:', e);
            // Fall back to JSON
            await this.loadAssignmentsFromJSON();
        }
    }

    async loadAssignmentsFromJSON() {
        try {
            const response = await fetch('/software-vv/_data/assignments.json');
            if (response.ok) {
                this.assignments = await response.json();
            }
        } catch (e) {
            console.warn('Could not load assignments from JSON:', e);
        }
    }

    displayAssignments() {
        const container = document.getElementById('assignment-list');
        if (!container) return;

        if (this.assignments.length === 0) {
            container.innerHTML = '<p>No assignments found.</p>';
            return;
        }

        // Filter to upcoming assignments (due in next 30 days)
        const now = new Date();
        const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
        
        const upcoming = this.assignments
            .filter(a => {
                if (!a.due_at) return false;
                const dueDate = new Date(a.due_at);
                return dueDate >= now && dueDate <= thirtyDaysFromNow;
            })
            .sort((a, b) => new Date(a.due_at) - new Date(b.due_at))
            .slice(0, 5);

        if (upcoming.length === 0) {
            container.innerHTML = '<p>No upcoming assignments in the next 30 days.</p>';
            return;
        }

        const html = `
            <ul class="assignment-list">
                ${upcoming.map(assignment => {
                    const dueDate = new Date(assignment.due_at);
                    const isOverdue = dueDate < now;
                    const daysUntilDue = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24));
                    
                    let statusClass = 'upcoming';
                    let statusText = `Due in ${daysUntilDue} day${daysUntilDue !== 1 ? 's' : ''}`;
                    
                    if (isOverdue) {
                        statusClass = 'overdue';
                        statusText = `Overdue by ${Math.abs(daysUntilDue)} day${Math.abs(daysUntilDue) !== 1 ? 's' : ''}`;
                    } else if (daysUntilDue === 0) {
                        statusClass = 'due-today';
                        statusText = 'Due today';
                    } else if (daysUntilDue <= 3) {
                        statusClass = 'due-soon';
                        statusText = `Due in ${daysUntilDue} day${daysUntilDue !== 1 ? 's' : ''}`;
                    }
                    
                    return `
                        <li class="assignment-item ${statusClass}">
                            <div class="assignment-header">
                                <h4>${assignment.name}</h4>
                                <span class="assignment-status">${statusText}</span>
                            </div>
                            <div class="assignment-details">
                                <span class="assignment-due-date">
                                    Due: ${dueDate.toLocaleDateString('en-US', { 
                                        weekday: 'short', 
                                        year: 'numeric', 
                                        month: 'short', 
                                        day: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </span>
                                ${assignment.points_possible ? `<span class="assignment-points">${assignment.points_possible} points</span>` : ''}
                                ${assignment.html_url ? `<a href="${assignment.html_url}" class="assignment-link" target="_blank">View on Canvas</a>` : ''}
                            </div>
                        </li>
                    `;
                }).join('')}
            </ul>
        `;

        container.innerHTML = html;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new CanvasAssignments();
});
