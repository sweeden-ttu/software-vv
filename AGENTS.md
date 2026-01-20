# AI Agents Documentation

This project includes several intelligent agents powered by LangChain and OpenAI.

## Available Agents

### 1. Agent Setup (`agent_setup.py`)

Interactive agent for collecting and validating API keys.

**Usage:**
```bash
python agent_setup.py
```

**Features:**
- Collects API keys for Composio, LangChain/LangSmith, Canvas LMS, and GitHub
- Validates each key before proceeding
- Saves configuration to `.env` file

---

### 2. UI Test Agent (`ui_test_agent.py`)

Intelligent agent for generating and running UI tests with Playwright.

**Usage:**
```bash
python ui_test_agent.py
```

**Capabilities:**

#### Analyze Page Structure
- Examines HTML structure of web pages
- Identifies headings, links, forms, navigation elements
- Provides structured analysis of page components

#### Generate Playwright Tests
- Creates Playwright test code from natural language descriptions
- Generates tests for specific UI components or user flows
- Saves tests to `tests/playwright/generated/`

#### Run Tests
- Executes Playwright tests
- Provides detailed test results
- Analyzes test outcomes

#### Accessibility Checking
- Checks for missing alt text on images
- Verifies form labels
- Validates heading hierarchy
- Checks for semantic HTML landmarks

**Example Commands:**
```
"Analyze the structure of http://localhost:4000/syllabus"
"Generate a test for the navigation menu"
"Check accessibility of the homepage"
"Run all tests and show me the results"
"Create a test that verifies all links work"
```

**Tools Available:**
- `analyze_page_structure(url)` - Analyze HTML structure
- `generate_playwright_test(description, url)` - Generate test code
- `run_playwright_tests(test_file)` - Execute tests
- `list_existing_tests()` - List all test files
- `save_test_file(filename, code)` - Save test to file
- `check_page_accessibility(url)` - Accessibility audit
- `analyze_test_results(results_file)` - Analyze test outcomes

---

### 3. UI Designer Agent (`ui_designer_agent.py`)

AI-powered design assistant for UI/UX recommendations and mockup generation.

**Usage:**
```bash
python ui_designer_agent.py
```

**Capabilities:**

#### Design Analysis
- Analyzes current design patterns
- Identifies CSS frameworks in use
- Detects layout types and components
- Checks responsive design implementation

#### CSS Recommendations
- Generates CSS code based on design goals
- Provides color schemes and typography recommendations
- Suggests spacing and layout improvements
- Creates component-specific CSS

#### HTML Mockups
- Generates HTML mockups for common components
- Creates navigation, cards, hero sections, forms
- Includes accessibility attributes
- Follows semantic HTML best practices

#### Design Improvements
- Suggests accessibility improvements
- Recommends responsive design enhancements
- Provides performance optimization tips
- Suggests visual hierarchy improvements

#### Color Palettes
- Generates color palettes for different themes
- Provides CSS variables for easy theming
- Supports professional, modern, and academic themes

**Example Commands:**
```
"Analyze the design of http://localhost:4000"
"Generate a color palette for an academic theme"
"Create a mockup for a navigation component"
"Suggest improvements for mobile responsiveness"
"Generate CSS for a card component with hover effects"
```

**Tools Available:**
- `analyze_current_design(url)` - Analyze design patterns
- `generate_css_recommendations(goals, css)` - Generate CSS
- `generate_html_mockup(component_type, requirements)` - Create mockups
- `suggest_improvements(analysis, focus_areas)` - Design suggestions
- `generate_color_palette(theme)` - Color scheme generation
- `save_design_file(filename, content, type)` - Save design files

---

## Prerequisites

All agents require:

1. **OpenAI API Key** - Set in environment variable `OPENAI_API_KEY` or `.env` file
2. **LangSmith API Key** (optional) - For tracing and observability
3. **Python Dependencies** - Install with `pip install -r requirements.txt`

## Environment Setup

Create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_key_here
LANGCHAIN_LANGSMITH_API_KEY=your_langsmith_key_here
```

## Agent Architecture

All agents follow a similar architecture:

1. **Tools** - Specialized functions for specific tasks
2. **LLM** - GPT-4o model for reasoning and generation
3. **Agent Executor** - Orchestrates tool usage and LLM interactions
4. **LangSmith Tracing** - Monitors agent behavior (optional)

## Integration with CI/CD

The UI Test Agent can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Generate UI Tests
  run: |
    python ui_test_agent.py <<EOF
    Generate tests for the navigation menu
    EOF
```

## Best Practices

1. **Be Specific** - Provide clear, specific requests to agents
2. **Iterate** - Use agent feedback to refine requests
3. **Review Output** - Always review generated code before committing
4. **Test Locally** - Run generated tests locally before pushing
5. **Use Tracing** - Enable LangSmith tracing for debugging

## Troubleshooting

### Agent Not Responding
- Check OpenAI API key is set correctly
- Verify internet connection
- Check API rate limits

### Tests Not Running
- Ensure Playwright is installed: `npx playwright install`
- Check Jekyll server is running for local tests
- Verify test file paths are correct

### Design Files Not Saving
- Check file permissions
- Verify directory structure exists
- Check disk space

## Future Enhancements

- Integration with design tools (Figma API)
- Visual regression testing
- Automated screenshot comparison
- Design system generation
- Component library documentation
