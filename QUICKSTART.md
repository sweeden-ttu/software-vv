# Quick Start Guide

Get up and running with the Canvas LMS Blog Template in minutes.

## Prerequisites

- Python 3.8+
- Ruby (for Jekyll)
- API keys (collected during setup)

## Installation

### Option 1: Automated Setup

```bash
./setup.sh
```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   # or with uv:
   uv pip install -r requirements.txt
   ```

2. **Install Jekyll dependencies:**
   ```bash
   bundle install
   ```

3. **Configure Kaggle API:**
   ```bash
   mkdir -p ~/.kaggle
   # Create ~/.kaggle/kaggle.json with your credentials
   ```

## Configuration

### Step 1: Run Agent Setup

The interactive agent will collect and validate your API keys:
your-site
```bash
python3 agent_setup.py
```

You'll be prompted for:
- Composio API Key
- LangChain/LangSmith API Key
- Canvas LMS API Key (and instance URL)
- GitHub Repository Location

### Step 2: Configure Canvas LMS

Edit `_config.yml` and add your Canvas instance URL:

```yaml
canvas:
  api_url: "https://texastech.instructure.com"
```

### Step 3: Set Up Kaggle Kernel Validation

Run the Kaggle agent to validate kernels from your enrolled competitions:

```bash
python3 kaggle_agent.py
```

## Running the Blog

Start the Jekyll development server:

```bash
bundle exec jekyll serve
```

Visit `http://localhost:4000` to view your blog.

## Features Overview

### Canvas LMS Integration
- Automatically displays your active courses
- Fetches course information via Canvas API
- View courses directly in the blog

### LangChain Agents
- Interactive API key collection
- Automatic validation
- LangSmith tracing for observability

### Kaggle Kernel Validation
- Lists enrolled competitions
- Finds top-performing kernels
- Validates and analyzes code
- Generates quality reports

## Troubleshooting

### Jekyll Issues
- Ensure Ruby and Bundler are installed
- Run `bundle update` if dependencies are outdated
our-canvas-instance
### Python Agent Issues
- Verify all API keys are correct
- Check that required packages are installed
- Ensure OpenAI API key is set for LangChain agents

### Canvas API Issues
- Verify your Canvas API key has proper permissions
- Check that your Canvas instance URL is correct
- Ensure CORS is configured if accessing from browser

## Next Steps

1. Customize the blog theme in `_config.yml`
2. Add your own blog posts in `_posts/`
3. Customize layouts in `_layouts/`
4. Integrate additional Canvas LMS features
5. Extend the Kaggle validation agent

## Support

For detailed documentation, see `README.md`.
