# Software Verification and Validation Course Site

A Jekyll-based course website that integrates Canvas LMS API, automated UI validation, and LangChain/LangSmith agents.

## Features

- **Jekyll Blog**: Based on jekyll-text-theme for a clean, text-focused design
- **Canvas LMS Integration**: Display courses and content from your Canvas LMS instance
- **Automated UI Validation**: Playwright tests generated from PR commit messages
- **LangChain/LangSmith Agents**: Automated API key collection and validation
- **UI Test Agent**: Intelligent agent for generating and running UI tests
- **UI Designer Agent**: AI-powered design recommendations and mockup generation
- **Kaggle Kernel Validation**: Agentic system to validate and verify kernels from enrolled competitions

## Prerequisites

- Ruby and Jekyll (for the blog)
- Python 3.8+ (for agents and test generation)
- Node.js 18+ (for Playwright UI tests)
- API keys for:
  - Composio
  - LangChain/LangSmith
  - Canvas LMS
  - GitHub
  - OpenAI (for LangChain agents)
  - Kaggle (for kernel validation)

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt
# or with uv:
uv pip install -r requirements.txt

# Node.js dependencies (for UI tests)
npm install

# Jekyll dependencies
bundle install
```

### 2. Install Playwright Browsers

```bash
npx playwright install --with-deps
```

### 3. Configure API Keys

Run the interactive agent setup:

```bash
python agent_setup.py
```

Or manually configure in `_config.yml` or `.env` file.

### 4. Sync Canvas Course Data

```bash
python sync_canvas_site.py
```

This will generate:
- `syllabus.md` from Canvas syllabus
- Module pages in `modules/`
- Assignment pages in `assignments/`
- Navigation structure in `_data/navigation.yml`

### 5. Run Jekyll Server

```bash
bundle exec jekyll serve
```

Visit `http://localhost:4000` to view your blog.

## UI Validation Tests

### Automated Test Generation

When you create a Pull Request, the GitHub Actions workflow automatically:

1. Extracts commit messages from the PR
2. Analyzes commit messages for UI-related keywords
3. Generates Playwright tests based on detected features
4. Runs tests against the Jekyll site
5. Comments on the PR with test results

### Running Tests Locally

```bash
# Start Jekyll server in one terminal
bundle exec jekyll serve

# Run tests in another terminal
npm test
```

### Test Generation Logic

The test generator (`scripts/generate_ui_tests.py`) analyzes commit messages for:

- **Navigation**: Tests menu, sidebar, navigation elements
- **UI Changes**: General UI validation and page load tests
- **Forms**: Form input and submission validation
- **Links**: Link functionality and routing tests
- **Content**: Content presence and readability checks
- **Assignments**: Assignment-related page tests
- **Syllabus**: Syllabus page validation

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ui-validation.yml    # CI/CD workflow for UI tests
├── _config.yml                  # Jekyll configuration
├── _layouts/                    # Jekyll layouts
├── _posts/                      # Blog posts
├── _data/                       # Generated navigation and data
├── assets/                      # CSS and JavaScript
├── modules/                     # Generated module pages
├── assignments/                 # Generated assignment pages
├── scripts/
│   └── generate_ui_tests.py    # Test generation script
├── tests/
│   └── playwright/              # Playwright test files
├── sync_canvas_site.py         # Canvas sync script
├── agent_setup.py              # API key setup agent
├── package.json                 # Node.js dependencies
├── playwright.config.js        # Playwright configuration
└── requirements.txt            # Python dependencies
```

## GitHub Actions Workflow

The UI validation workflow runs automatically on:
- Pull request opened
- Pull request synchronized (new commits)
- Pull request reopened
- Manual workflow dispatch

See `.github/workflows/ui-validation.yml` for details.

## Canvas LMS Integration

The site automatically fetches and displays your active Canvas courses. Configure your Canvas API key in `_config.yml`:

```yaml
canvas:
  api_url: "https://your-canvas-instance.instructure.com"
  api_key: "your_api_key"
```

## AI Agents

### UI Test Agent

An intelligent agent that helps with UI testing:

```bash
python ui_test_agent.py
```

**Capabilities:**
- Analyze page structure and identify testable elements
- Generate Playwright tests based on descriptions
- Run tests and analyze results
- Check accessibility compliance
- Provide test improvement recommendations

**Example interactions:**
- "Generate a test for the navigation menu"
- "Check accessibility of the homepage"
- "Analyze the structure of /syllabus page"
- "Run all tests and show me the results"

### UI Designer Agent

An AI-powered design assistant:

```bash
python ui_designer_agent.py
```

**Capabilities:**
- Analyze current design patterns
- Generate CSS recommendations and color palettes
- Create HTML mockups for components
- Suggest accessibility and responsive design improvements
- Provide design best practices

**Example interactions:**
- "Analyze the design of http://localhost:4000"
- "Generate a color palette for an academic theme"
- "Create a mockup for a navigation component"
- "Suggest improvements for mobile responsiveness"

See [AGENTS.md](AGENTS.md) for detailed documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with descriptive commit messages
4. Create a pull request
5. UI validation tests will run automatically

### Commit Message Guidelines

For best test generation, use descriptive commit messages:

- `feat: add navigation menu` → Generates navigation tests
- `fix: update assignment page layout` → Generates UI change tests
- `docs: update syllabus content` → Generates content tests

## License

GPL-3.0 License - see LICENSE file for details

## Support

For issues and questions:
- Canvas LMS API: https://canvas.instructure.com/doc/api/
- LangChain: https://docs.langchain.com/
- Playwright: https://playwright.dev/
