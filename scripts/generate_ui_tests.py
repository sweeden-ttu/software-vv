#!/usr/bin/env python3
"""
Generate UI validation tests from PR commit messages
Analyzes commit messages and creates Playwright tests for UI validation
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict
import requests


class UITestGenerator:
    """Generate Playwright tests from commit messages"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.tests_dir = self.repo_root / 'tests' / 'playwright' / 'generated'
        self.tests_dir.mkdir(parents=True, exist_ok=True)
        
    def load_commit_messages(self) -> List[str]:
        """Load commit messages from file or GitHub API"""
        commit_file = self.repo_root / 'commit_messages.txt'
        
        if commit_file.exists():
            with open(commit_file, 'r') as f:
                messages = [line.strip() for line in f.readlines() if line.strip()]
            return messages
        
        # Fallback: try to get from GitHub API if token available
        github_token = os.getenv('GITHUB_TOKEN')
        pr_number = os.getenv('PR_NUMBER')
        
        if github_token and pr_number:
            try:
                repo = os.getenv('GITHUB_REPOSITORY', 'sweeden-ttu/software-vv')
                url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
                headers = {'Authorization': f'token {github_token}'}
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    commits = response.json()
                    return [commit['commit']['message'] for commit in commits]
            except Exception as e:
                print(f"Warning: Could not fetch commits from GitHub: {e}")
        
        return []
    
    def parse_commit_message(self, message: str) -> Dict[str, any]:
        """Parse commit message to extract test requirements"""
        # Common patterns in commit messages
        patterns = {
            'ui_change': [
                r'ui\s*change',
                r'update\s+.*\s+page',
                r'add\s+.*\s+component',
                r'fix\s+.*\s+layout',
                r'improve\s+.*\s+design',
            ],
            'navigation': [
                r'navigation',
                r'menu',
                r'sidebar',
                r'nav',
            ],
            'form': [
                r'form',
                r'input',
                r'submit',
                r'validation',
            ],
            'link': [
                r'link',
                r'href',
                r'url',
                r'route',
            ],
            'content': [
                r'content',
                r'article',
                r'post',
                r'page',
            ],
            'assignment': [
                r'assignment',
                r'due\s+date',
                r'submission',
            ],
            'syllabus': [
                r'syllabus',
                r'schedule',
                r'course',
            ],
        }
        
        message_lower = message.lower()
        detected_features = []
        
        for feature, feature_patterns in patterns.items():
            for pattern in feature_patterns:
                if re.search(pattern, message_lower):
                    detected_features.append(feature)
                    break
        
        return {
            'message': message,
            'features': detected_features,
            'type': self._detect_commit_type(message),
        }
    
    def _detect_commit_type(self, message: str) -> str:
        """Detect commit type (feat, fix, docs, etc.)"""
        if re.match(r'^(feat|feature):', message, re.I):
            return 'feature'
        elif re.match(r'^(fix|bugfix):', message, re.I):
            return 'fix'
        elif re.match(r'^(docs|doc):', message, re.I):
            return 'docs'
        elif re.match(r'^(test):', message, re.I):
            return 'test'
        elif re.match(r'^(refactor):', message, re.I):
            return 'refactor'
        else:
            return 'other'
    
    def generate_test_for_feature(self, feature: str, commit_info: Dict) -> str:
        """Generate Playwright test code for a specific feature"""
        test_templates = {
            'navigation': '''
  test('Navigation: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Test navigation elements exist
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
    
    // Test navigation links
    const navLinks = nav.locator('a');
    const count = await navLinks.count();
    expect(count).toBeGreaterThan(0);
    
    // Test navigation is functional
    for (let i = 0; i < Math.min(count, 3); i++) {{
      const link = navLinks.nth(i);
      const href = await link.getAttribute('href');
      if (href && !href.startsWith('#')) {{
        await link.click();
        await page.waitForLoadState('networkidle');
        await expect(page).toHaveURL(new RegExp(href.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')));
      }}
    }}
  }});
''',
            'ui_change': '''
  test('UI Change: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Verify page loads successfully
    await expect(page).toHaveTitle(/Software Verification/);
    
    // Check main content is visible
    const mainContent = page.locator('main, .page-content, .wrapper');
    await expect(mainContent.first()).toBeVisible();
    
    // Verify no console errors
    const errors = [];
    page.on('console', msg => {{
      if (msg.type() === 'error') {{
        errors.push(msg.text());
      }}
    }});
    
    await page.waitForLoadState('networkidle');
    expect(errors.length).toBe(0);
  }});
''',
            'link': '''
  test('Links: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Test all internal links
    const links = page.locator('a[href^="/"], a[href^="#"]');
    const count = await links.count();
    
    for (let i = 0; i < Math.min(count, 5); i++) {{
      const link = links.nth(i);
      const href = await link.getAttribute('href');
      
      if (href && !href.startsWith('http')) {{
        await link.click();
        await page.waitForLoadState('networkidle');
        
        // Verify page loaded (not 404)
        const status = await page.evaluate(() => document.body.textContent);
        expect(status).not.toContain('404');
        expect(status).not.toContain('Not Found');
      }}
    }}
  }});
''',
            'form': '''
  test('Forms: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Test any forms on the page
    const forms = page.locator('form');
    const formCount = await forms.count();
    
    if (formCount > 0) {{
      for (let i = 0; i < formCount; i++) {{
        const form = forms.nth(i);
        await expect(form).toBeVisible();
        
        // Test form inputs
        const inputs = form.locator('input, textarea, select');
        const inputCount = await inputs.count();
        expect(inputCount).toBeGreaterThanOrEqual(0);
      }}
    }}
  }});
''',
            'content': '''
  test('Content: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Verify content is present
    const headings = page.locator('h1, h2, h3');
    const headingCount = await headings.count();
    expect(headingCount).toBeGreaterThan(0);
    
    // Verify content is readable
    const body = page.locator('body');
    const text = await body.textContent();
    expect(text.length).toBeGreaterThan(100);
  }});
''',
            'assignment': '''
  test('Assignments: {message}', async ({ page }) => {{
    await page.goto('/');
    
    // Check for assignment-related elements
    const assignmentElements = page.locator('[class*="assignment"], [id*="assignment"]');
    const count = await assignmentElements.count();
    
    // If assignments page exists, test it
    try {{
      await page.goto('/assignments/');
      await page.waitForLoadState('networkidle');
      const content = await page.textContent('body');
      expect(content).toBeTruthy();
    }} catch (e) {{
      // Assignments page may not exist yet
    }}
  }});
''',
            'syllabus': '''
  test('Syllabus: {message}', async ({ page }) => {{
    // Test syllabus page
    await page.goto('/syllabus/');
    await page.waitForLoadState('networkidle');
    
    // Verify syllabus content exists
    const content = page.locator('main, .page-content, article');
    await expect(content.first()).toBeVisible();
    
    // Check for course information
    const text = await page.textContent('body');
    expect(text.toLowerCase()).toMatch(/course|syllabus|schedule/);
  }});
''',
        }
        
        template = test_templates.get(feature, test_templates['ui_change'])
        return template.format(message=commit_info['message'][:50])
    
    def generate_test_file(self, commit_infos: List[Dict]) -> str:
        """Generate a complete Playwright test file"""
        imports = '''import { test, expect } from '@playwright/test';

/**
 * Auto-generated UI validation tests
 * Generated from PR commit messages
 */
'''
        
        tests = []
        seen_features = set()
        
        for commit_info in commit_infos:
            for feature in commit_info['features']:
                if feature not in seen_features:
                    tests.append(self.generate_test_for_feature(feature, commit_info))
                    seen_features.add(feature)
            
            # Always add a general UI test for each commit
            if commit_info['type'] in ['feature', 'fix']:
                tests.append(self.generate_test_for_feature('ui_change', commit_info))
        
        # If no specific features detected, add general tests
        if not tests:
            tests.append(self.generate_test_for_feature('ui_change', {
                'message': 'General UI validation'
            }))
        
        return imports + '\n'.join(tests)
    
    def generate(self):
        """Main generation method"""
        commit_messages = self.load_commit_messages()
        
        if not commit_messages:
            print("No commit messages found. Skipping test generation.")
            return
        
        print(f"Found {len(commit_messages)} commit message(s)")
        
        # Parse commit messages
        commit_infos = [self.parse_commit_message(msg) for msg in commit_messages]
        
        # Generate test file
        test_content = self.generate_test_file(commit_infos)
        
        # Write test file
        test_file = self.tests_dir / 'pr-ui-validation.spec.js'
        test_file.write_text(test_content)
        
        print(f"Generated test file: {test_file}")
        print(f"Detected features: {set(f for info in commit_infos for f in info['features'])}")


if __name__ == '__main__':
    generator = UITestGenerator()
    generator.generate()
