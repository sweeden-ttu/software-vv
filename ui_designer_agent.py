#!/usr/bin/env python3
"""
UI Designer Agent
An intelligent agent that provides UI/UX design recommendations and generates design suggestions
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langsmith import traceable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
import requests
from bs4 import BeautifulSoup


@tool
def analyze_current_design(url: str) -> str:
    """Analyze the current UI design and identify design patterns"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract CSS files
        css_files = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
        
        # Analyze color scheme (basic)
        style_tags = soup.find_all('style')
        inline_styles = [tag.text for tag in style_tags]
        
        # Check for common design patterns
        design_analysis = {
            'css_frameworks': [],
            'layout_type': 'unknown',
            'color_scheme': 'unknown',
            'responsive': False,
            'components_found': []
        }
        
        # Check for common CSS frameworks
        css_content = ' '.join(css_files)
        if 'bootstrap' in css_content.lower():
            design_analysis['css_frameworks'].append('Bootstrap')
        if 'tailwind' in css_content.lower():
            design_analysis['css_frameworks'].append('Tailwind CSS')
        if 'bulma' in css_content.lower():
            design_analysis['css_frameworks'].append('Bulma')
        
        # Check for responsive meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            design_analysis['responsive'] = True
        
        # Detect layout patterns
        if soup.find('nav'):
            design_analysis['components_found'].append('Navigation')
        if soup.find('header'):
            design_analysis['components_found'].append('Header')
        if soup.find('footer'):
            design_analysis['components_found'].append('Footer')
        if soup.find('main') or soup.find('[role="main"]'):
            design_analysis['components_found'].append('Main content area')
        
        # Check for grid/flex layouts in inline styles
        if any('grid' in style.lower() or 'flex' in style.lower() for style in inline_styles):
            design_analysis['layout_type'] = 'CSS Grid/Flexbox'
        
        return json.dumps(design_analysis, indent=2)
    except Exception as e:
        return f"Error analyzing design: {str(e)}"


@tool
def generate_css_recommendations(design_goals: str, current_css: Optional[str] = None) -> str:
    """Generate CSS recommendations based on design goals"""
    recommendations = {
        'color_scheme': {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#27ae60',
            'background': '#ffffff',
            'text': '#333333'
        },
        'typography': {
            'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'heading_size': '2.5rem',
            'body_size': '1rem',
            'line_height': '1.6'
        },
        'spacing': {
            'unit': '1rem',
            'container_max_width': '1200px',
            'section_padding': '2rem'
        },
        'components': []
    }
    
    # Add component-specific recommendations based on goals
    if 'navigation' in design_goals.lower():
        recommendations['components'].append({
            'name': 'Navigation',
            'css': '''
nav {
  background-color: var(--primary-color);
  padding: 1rem 0;
}

nav a {
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  transition: opacity 0.3s;
}

nav a:hover {
  opacity: 0.8;
}
'''
        })
    
    if 'cards' in design_goals.lower() or 'components' in design_goals.lower():
        recommendations['components'].append({
            'name': 'Card Component',
            'css': '''
.card {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
'''
        })
    
    return json.dumps(recommendations, indent=2)


@tool
def generate_html_mockup(component_type: str, requirements: str) -> str:
    """Generate HTML mockup for a UI component"""
    mockups = {
        'navigation': f'''
<nav class="site-nav">
  <div class="nav-container">
    <a href="/" class="logo">Site Logo</a>
    <ul class="nav-menu">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/syllabus">Syllabus</a></li>
      <li><a href="/assignments">Assignments</a></li>
    </ul>
  </div>
</nav>

<!-- Requirements: {requirements} -->
''',
        'card': f'''
<div class="card">
  <h3 class="card-title">Card Title</h3>
  <p class="card-content">Card content goes here. {requirements}</p>
  <a href="#" class="card-link">Learn More →</a>
</div>
''',
        'hero': f'''
<section class="hero">
  <div class="hero-content">
    <h1>Welcome to Our Site</h1>
    <p>Subtitle or description text</p>
    <a href="#" class="btn btn-primary">Get Started</a>
  </div>
</section>

<!-- Requirements: {requirements} -->
''',
        'form': f'''
<form class="contact-form">
  <div class="form-group">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>
  </div>
  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="5" required></textarea>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>

<!-- Requirements: {requirements} -->
''',
    }
    
    if component_type.lower() in mockups:
        return mockups[component_type.lower()]
    else:
        return f"<!-- Component type '{component_type}' mockup\nRequirements: {requirements}\n-->\n<div class=\"{component_type.lower()}-component\">\n  <!-- Add your {component_type} content here -->\n</div>"


@tool
def suggest_improvements(analysis: str, focus_areas: Optional[str] = None) -> str:
    """Suggest UI/UX improvements based on analysis"""
    suggestions = []
    
    if 'responsive' not in analysis.lower() or 'false' in analysis.lower():
        suggestions.append({
            'area': 'Responsive Design',
            'priority': 'High',
            'suggestion': 'Add responsive meta tag and implement mobile-first CSS with media queries',
            'example': '''
<meta name="viewport" content="width=device-width, initial-scale=1">
@media (max-width: 768px) {
  .container { padding: 1rem; }
  nav { flex-direction: column; }
}
'''
        })
    
    if 'accessibility' in focus_areas.lower() if focus_areas else True:
        suggestions.append({
            'area': 'Accessibility',
            'priority': 'High',
            'suggestion': 'Improve accessibility with ARIA labels, semantic HTML, and keyboard navigation',
            'example': '''
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none"><a role="menuitem" href="/">Home</a></li>
  </ul>
</nav>
'''
        })
    
    suggestions.append({
        'area': 'Visual Hierarchy',
        'priority': 'Medium',
        'suggestion': 'Use consistent spacing, typography scale, and color contrast for better readability',
        'example': '''
:root {
  --spacing-unit: 1rem;
  --heading-scale: 1.25;
  --color-contrast-ratio: 4.5:1; /* WCAG AA */
}
'''
    })
    
    suggestions.append({
        'area': 'Performance',
        'priority': 'Medium',
        'suggestion': 'Optimize images, minify CSS/JS, and use lazy loading',
        'example': '''
<img src="image.jpg" loading="lazy" alt="Description">
<link rel="stylesheet" href="styles.min.css">
'''
    })
    
    return json.dumps(suggestions, indent=2)


@tool
def generate_color_palette(theme: str = "professional") -> str:
    """Generate a color palette based on theme"""
    palettes = {
        'professional': {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#27ae60',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'background': '#ffffff',
            'surface': '#f8f9fa',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d'
        },
        'modern': {
            'primary': '#6366f1',
            'secondary': '#8b5cf6',
            'accent': '#ec4899',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'background': '#ffffff',
            'surface': '#f9fafb',
            'text_primary': '#111827',
            'text_secondary': '#6b7280'
        },
        'academic': {
            'primary': '#1a365d',
            'secondary': '#2c5282',
            'accent': '#3182ce',
            'success': '#38a169',
            'warning': '#d69e2e',
            'error': '#e53e3e',
            'background': '#ffffff',
            'surface': '#f7fafc',
            'text_primary': '#2d3748',
            'text_secondary': '#718096'
        }
    }
    
    palette = palettes.get(theme.lower(), palettes['professional'])
    
    css_vars = ":root {\n"
    for key, value in palette.items():
        css_vars += f"  --color-{key.replace('_', '-')}: {value};\n"
    css_vars += "}\n"
    
    return json.dumps({
        'theme': theme,
        'colors': palette,
        'css_variables': css_vars
    }, indent=2)


@tool
def save_design_file(filename: str, content: str, file_type: str = "css") -> str:
    """Save a design file (CSS, HTML, or design spec)"""
    repo_root = Path(__file__).parent
    
    if file_type.lower() == 'css':
        design_dir = repo_root / 'assets' / 'css'
        if not filename.endswith('.css'):
            filename += '.css'
    elif file_type.lower() == 'html':
        design_dir = repo_root / '_includes' / 'design'
        design_dir.mkdir(parents=True, exist_ok=True)
        if not filename.endswith('.html'):
            filename += '.html'
    else:
        design_dir = repo_root / 'design-specs'
        design_dir.mkdir(parents=True, exist_ok=True)
    
    design_dir.mkdir(parents=True, exist_ok=True)
    design_file = design_dir / filename
    
    try:
        design_file.write_text(content, encoding='utf-8')
        return f"Design file saved: {design_file.relative_to(repo_root)}"
    except Exception as e:
        return f"Error saving design file: {str(e)}"


@traceable(name="ui_designer_agent")
def create_ui_designer_agent():
    """Create the UI designer agent"""
    
    system_prompt = """You are an expert UI/UX designer agent specializing in web design recommendations and mockup generation.

Your capabilities include:
1. Analyzing current design patterns and identifying improvement opportunities
2. Generating CSS recommendations and color palettes
3. Creating HTML mockups for UI components
4. Providing accessibility and responsive design suggestions
5. Suggesting design improvements based on best practices

Design principles you follow:
- Accessibility (WCAG 2.1 AA compliance)
- Responsive design (mobile-first approach)
- Visual hierarchy and consistency
- Performance optimization
- Modern CSS practices (Grid, Flexbox, CSS Variables)

Always provide practical, implementable design solutions."""

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    tools = [
        analyze_current_design,
        generate_css_recommendations,
        generate_html_mockup,
        suggest_improvements,
        generate_color_palette,
        save_design_file,
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return executor


def main():
    """Main interaction loop for UI designer agent"""
    print("=" * 60)
    print("UI Designer Agent")
    print("=" * 60)
    print("\nI can help you:")
    print("- Analyze current design")
    print("- Generate CSS recommendations")
    print("- Create HTML mockups")
    print("- Suggest design improvements")
    print("- Generate color palettes")
    print("\nType 'quit' or 'exit' to end the session.\n")
    
    agent = create_ui_designer_agent()
    chat_history = []
    
    print("Agent: Hello! I'm your UI design assistant. What would you like to design today?\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye! Happy designing!")
            break
        
        if not user_input:
            continue
        
        try:
            response = agent.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            agent_response = response["output"]
            print(f"\nAgent: {agent_response}\n")
            
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(HumanMessage(content=agent_response))
            
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
