#!/usr/bin/env python3
"""
UI Test Agent
An intelligent agent that generates, runs, and analyzes UI tests using Playwright
"""

import os
import sys
import json
import subprocess
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
def analyze_page_structure(url: str) -> str:
    """Analyze the HTML structure of a web page and return key elements"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        structure = {
            'title': soup.find('title').text if soup.find('title') else 'No title',
            'headings': [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])[:10]],
            'links': len(soup.find_all('a')),
            'forms': len(soup.find_all('form')),
            'images': len(soup.find_all('img')),
            'buttons': len(soup.find_all(['button', 'input[type="submit"]'])),
            'navigation': [nav.text.strip() for nav in soup.find_all('nav')[:3]],
        }
        
        return json.dumps(structure, indent=2)
    except Exception as e:
        return f"Error analyzing page: {str(e)}"


@tool
def generate_playwright_test(test_description: str, page_url: str = "http://localhost:4000") -> str:
    """Generate a Playwright test based on a description"""
    test_template = f'''import {{ test, expect }} from '@playwright/test';

test('{test_description}', async ({{ page }}) => {{
  await page.goto('{page_url}');
  
  // Test implementation
  await expect(page).toHaveTitle(/.*/);
  
  // Add specific test logic based on: {test_description}
}});
'''
    return test_template


@tool
def run_playwright_tests(test_file: Optional[str] = None) -> str:
    """Run Playwright tests and return results"""
    repo_root = Path(__file__).parent
    
    try:
        if test_file:
            cmd = ['npx', 'playwright', 'test', str(repo_root / test_file)]
        else:
            cmd = ['npx', 'playwright', 'test', 'tests/playwright/']
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=repo_root
        )
        
        return f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Test execution timed out after 5 minutes"
    except Exception as e:
        return f"Error running tests: {str(e)}"


@tool
def list_existing_tests() -> str:
    """List all existing Playwright test files"""
    repo_root = Path(__file__).parent
    test_dir = repo_root / 'tests' / 'playwright'
    
    tests = []
    if test_dir.exists():
        for test_file in test_dir.rglob('*.spec.js'):
            tests.append(str(test_file.relative_to(repo_root)))
    
    if tests:
        return "\n".join(tests)
    else:
        return "No test files found"


@tool
def save_test_file(filename: str, test_code: str) -> str:
    """Save a Playwright test file"""
    repo_root = Path(__file__).parent
    test_dir = repo_root / 'tests' / 'playwright' / 'generated'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure filename ends with .spec.js
    if not filename.endswith('.spec.js'):
        filename = filename.replace('.js', '') + '.spec.js'
    
    test_file = test_dir / filename
    
    try:
        test_file.write_text(test_code, encoding='utf-8')
        return f"Test file saved: {test_file.relative_to(repo_root)}"
    except Exception as e:
        return f"Error saving test file: {str(e)}"


@tool
def check_page_accessibility(url: str) -> str:
    """Check basic accessibility features of a page"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        issues = []
        
        # Check for alt text on images
        images_without_alt = soup.find_all('img', alt=False)
        if images_without_alt:
            issues.append(f"{len(images_without_alt)} images without alt text")
        
        # Check for form labels
        inputs_without_labels = []
        for input_elem in soup.find_all(['input', 'textarea', 'select']):
            input_id = input_elem.get('id')
            if input_id:
                label = soup.find('label', {'for': input_id})
                if not label:
                    inputs_without_labels.append(input_id)
        
        if inputs_without_labels:
            issues.append(f"{len(inputs_without_labels)} form inputs without labels")
        
        # Check for heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if not headings:
            issues.append("No headings found")
        
        # Check for main landmark
        main = soup.find('main') or soup.find('[role="main"]')
        if not main:
            issues.append("No main landmark found")
        
        if issues:
            return "Accessibility issues found:\n" + "\n".join(f"- {issue}" for issue in issues)
        else:
            return "No major accessibility issues detected"
            
    except Exception as e:
        return f"Error checking accessibility: {str(e)}"


@tool
def analyze_test_results(results_file: Optional[str] = None) -> str:
    """Analyze Playwright test results and provide insights"""
    repo_root = Path(__file__).parent
    
    # Try to find test results
    report_dir = repo_root / 'playwright-report'
    
    if results_file:
        results_path = repo_root / results_file
    else:
        results_path = report_dir / 'index.html'
    
    if results_path.exists() and results_path.suffix == '.html':
        try:
            with open(results_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract test statistics
            stats = {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0
            }
            
            # Try to find test statistics in the HTML
            for stat_class in ['total', 'passed', 'failed', 'skipped']:
                elements = soup.find_all(class_=lambda x: x and stat_class in x.lower())
                if elements:
                    try:
                        stats[stat_class] = int(elements[0].text.strip())
                    except:
                        pass
            
            summary = f"Test Results Summary:\n"
            summary += f"- Total tests: {stats.get('total', 'N/A')}\n"
            summary += f"- Passed: {stats.get('passed', 'N/A')}\n"
            summary += f"- Failed: {stats.get('failed', 'N/A')}\n"
            summary += f"- Skipped: {stats.get('skipped', 'N/A')}\n"
            
            return summary
        except Exception as e:
            return f"Error analyzing results: {str(e)}"
    else:
        return "No test results file found. Run tests first."


@traceable(name="ui_test_agent")
def create_ui_test_agent():
    """Create the UI test agent"""
    
    system_prompt = """You are an expert UI testing agent specializing in Playwright test generation and execution.

Your capabilities include:
1. Analyzing web page structure and identifying testable elements
2. Generating comprehensive Playwright tests based on requirements
3. Running tests and analyzing results
4. Checking accessibility compliance
5. Providing recommendations for test improvements

When generating tests:
- Use descriptive test names
- Include proper assertions
- Test user interactions (clicks, form submissions, navigation)
- Verify page content and structure
- Check for accessibility issues

Always be thorough and provide actionable feedback."""

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    tools = [
        analyze_page_structure,
        generate_playwright_test,
        run_playwright_tests,
        list_existing_tests,
        save_test_file,
        check_page_accessibility,
        analyze_test_results,
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
    """Main interaction loop for UI test agent"""
    print("=" * 60)
    print("UI Test Agent")
    print("=" * 60)
    print("\nI can help you:")
    print("- Generate Playwright tests")
    print("- Analyze page structure")
    print("- Run and analyze test results")
    print("- Check accessibility")
    print("\nType 'quit' or 'exit' to end the session.\n")
    
    agent = create_ui_test_agent()
    chat_history = []
    
    print("Agent: Hello! I'm your UI testing assistant. What would you like to test today?\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye! Happy testing!")
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
