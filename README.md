# Canvas LMS Blog Template

A Jekyll-based blog template that integrates Canvas LMS API, LangChain/LangSmith agents, and Kaggle kernel validation.

## Features

- **Jekyll Blog**: Based on jekyll-text-theme for a clean, text-focused design
- **Canvas LMS Integration**: Display courses and content from your Canvas LMS instance
- **LangChain/LangSmith Agents**: Automated API key collection and validation
- **Kaggle Kernel Validation**: Agentic system to validate and verify kernels from enrolled competitions

## Prerequisites

- Ruby and Jekyll (for the blog)
- Python 3.8+ (for agents)
- API keys for:
  - Composio
  - LangChain/LangSmith
  - Canvas LMS
  - GitHub
  - OpenAI (for LangChain agents)
  - Kaggle (for kernel validation)

## Setup

### 1. Install Jekyll Dependencies

```bash
bundle install
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Kaggle API

Create `~/.kaggle/kaggle.json` with your Kaggle credentials:

```json
{
  "username": "your_username",
  "key": "your_api_key"
}
```

Get your API key from: https://www.kaggle.com/account

### 4. Run Agent Setup

The agent will interview you to collect and validate API keys:

```bash
python agent_setup.py
```

This will:
- Collect Composio API key
- Collect LangChain/LangSmith API key
- Collect Canvas LMS API key and URL
- Collect GitHub repository location
- Validate each key before proceeding
- Save configuration to `.env` file

### 5. Configure Canvas LMS

Update `_config.yml` with your Canvas instance URL:

```yaml
canvas:
  api_url: "https://your-canvas-instance.instructure.com"
  api_key: "your_api_key"
```

### 6. Run Kaggle Kernel Validation Agent

After API keys are configured, run the Kaggle agent:

```bash
python kaggle_agent.py
```

This agent will:
- List your enrolled competitions
- Find top-performing kernels
- Download and validate kernel code
- Analyze code quality
- Provide recommendations

### 7. Run Jekyll Server

```bash
bundle exec jekyll serve
```

Visit `http://localhost:4000` to view your blog.

## Project Structure

```
blog/
├── _config.yml          # Jekyll configuration
├── _layouts/            # Jekyll layouts
├── _posts/              # Blog posts
├── assets/              # CSS and JavaScript
│   ├── css/
│   └── js/
├── agent_setup.py       # API key collection agent
├── kaggle_agent.py      # Kaggle kernel validation agent
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage

### Canvas LMS Integration

The blog automatically fetches and displays your active Canvas courses on the homepage. Make sure your Canvas API key is configured in `_config.yml` or `.env`.

### Kaggle Kernel Validation

The Kaggle agent can be run interactively or integrated into your workflow. It will:

1. Fetch your enrolled competitions
2. Get top kernels by votes/recent activity
3. Download kernel code
4. Validate syntax and structure
5. Analyze code quality metrics
6. Generate reports

### LangSmith Tracing

All agent interactions are traced in LangSmith for observability. Make sure your LangSmith API key is configured to view traces.

## Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

- `COMPOSIO_API_KEY`: Your Composio API key
- `LANGCHAIN_API_KEY`: Your LangChain API key
- `LANGCHAIN_LANGSMITH_API_KEY`: Your LangSmith API key
- `CANVAS_API_KEY`: Your Canvas LMS API key
- `CANVAS_API_URL`: Your Canvas instance URL
- `GITHUB_TOKEN`: Your GitHub personal access token
- `GITHUB_REPOSITORY`: Your repository path (username/repo)
- `OPENAI_API_KEY`: Your OpenAI API key (for LangChain agents)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Canvas LMS API: https://canvas.instructure.com/doc/api/
- LangChain: https://docs.langchain.com/
- LangSmith: https://docs.smith.langchain.com/
- Kaggle API: https://www.kaggle.com/docs/api
