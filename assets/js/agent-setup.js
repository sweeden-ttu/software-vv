/**
 * Agent Setup UI Integration
 * Provides frontend interface for agent setup process
 */

class AgentSetup {
    constructor() {
        this.setupButton = document.getElementById('start-setup');
        this.statusDiv = document.getElementById('setup-status');
        this.init();
    }

    init() {
        if (this.setupButton) {
            this.setupButton.addEventListener('click', () => this.startSetup());
        }
    }

    async startSetup() {
        if (!this.setupButton || !this.statusDiv) return;

        this.setupButton.disabled = true;
        this.statusDiv.innerHTML = '<p class="status-loading">Starting agent setup...</p>';

        try {
            // In a real implementation, this would call a backend API
            // that runs the Python agent. For now, we'll show instructions.
            this.statusDiv.innerHTML = `
                <div class="setup-instructions">
                    <h3>Agent Setup Instructions</h3>
                    <ol>
                        <li>Open a terminal in the blog directory</li>
                        <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                        <li>Run the setup agent: <code>python agent_setup.py</code></li>
                        <li>Follow the interactive prompts to enter your API keys</li>
                    </ol>
                    <p><strong>Required API Keys:</strong></p>
                    <ul>
                        <li>Composio API Key</li>
                        <li>LangChain/LangSmith API Key</li>
                        <li>Canvas LMS API Key</li>
                        <li>GitHub Repository Location</li>
                    </ul>
                    <p>After setup, run <code>python kaggle_agent.py</code> to set up Kaggle kernel validation.</p>
                </div>
            `;
        } catch (error) {
            this.statusDiv.innerHTML = `<p class="status-error">Error: ${error.message}</p>`;
        } finally {
            this.setupButton.disabled = false;
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new AgentSetup();
});
