#!/usr/bin/env python3
"""
Canvas LMS to Jekyll Site Generator
Fetches course data from Canvas LMS and generates Jekyll site structure
based on syllabus, modules, and assignments.
"""

import os
import sys
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
import html2text
from bs4 import BeautifulSoup


class CanvasSyncError(Exception):
    """Custom exception for Canvas sync errors"""
    pass


class CanvasSiteSync:
    """Main class for syncing Canvas course data to Jekyll site"""
    
    def __init__(self, api_url: str, api_key: str, course_id: Optional[int] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.course_id = course_id
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.site_root = Path(__file__).parent
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.body_width = 0
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request to Canvas"""
        url = f"{self.api_url}/api/v1{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise CanvasSyncError(f"API request failed: {e}")
    
    def fetch_course_data(self) -> Dict:
        """Fetch course information including syllabus"""
        if not self.course_id:
            # Try to find course with "verification" or "validation" in name
            courses = self._make_request('/courses', {'enrollment_type': 'student', 'enrollment_state': 'active'})
            
            print("Available courses:")
            for i, course in enumerate(courses):
                print(f"  {i+1}. {course.get('name', 'Unnamed')} (ID: {course.get('id')})")
            
            # Find relevant course
            for course in courses:
                course_name = course.get('name', '').lower()
                if any(term in course_name for term in ['verification', 'validation', 'vv', 'software']):
                    self.course_id = course.get('id')
                    print(f"\nUsing course: {course.get('name')} (ID: {self.course_id})")
                    break
            
            if not self.course_id and courses:
                self.course_id = courses[0].get('id')
                print(f"\nUsing first course: {courses[0].get('name')} (ID: {self.course_id})")
            
            if not self.course_id:
                raise CanvasSyncError("No courses found")
        
        # Fetch course with syllabus
        course = self._make_request(f'/courses/{self.course_id}', {'include[]': 'syllabus_body'})
        return course
    
    def fetch_modules(self) -> List[Dict]:
        """Fetch all course modules"""
        modules = self._make_request(f'/courses/{self.course_id}/modules')
        
        # Fetch items for each module
        for module in modules:
            try:
                items = self._make_request(f"/courses/{self.course_id}/modules/{module['id']}/items")
                module['items'] = items
            except CanvasSyncError:
                module['items'] = []
        
        return modules
    
    def fetch_assignments(self) -> List[Dict]:
        """Fetch all course assignments"""
        assignments = self._make_request(f'/courses/{self.course_id}/assignments')
        return assignments
    
    def parse_syllabus_structure(self, syllabus_html: str) -> Dict[str, Any]:
        """Parse syllabus HTML to extract structure"""
        if not syllabus_html:
            return {}
        
        soup = BeautifulSoup(syllabus_html, 'html.parser')
        structure = {
            'schedule': [],
            'objectives': [],
            'topics': []
        }
        
        # Try to find schedule table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    week_data = {
                        'week': cells[0].get_text().strip() if len(cells) > 0 else '',
                        'topic': cells[1].get_text().strip() if len(cells) > 1 else '',
                        'readings': cells[2].get_text().strip() if len(cells) > 2 else '',
                        'assignments': cells[3].get_text().strip() if len(cells) > 3 else ''
                    }
                    structure['schedule'].append(week_data)
        
        # Look for learning objectives
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'strong']):
            text = heading.get_text().strip().lower()
            if 'objective' in text or 'outcome' in text:
                next_elem = heading.find_next_sibling()
                if next_elem:
                    if next_elem.name == 'ul':
                        for li in next_elem.find_all('li'):
                            structure['objectives'].append(li.get_text().strip())
                    elif next_elem.name in ['p', 'div']:
                        structure['objectives'].append(next_elem.get_text().strip())
        
        return structure
    
    def generate_syllabus_page(self, course_data: Dict) -> None:
        """Generate syllabus.md from Canvas course data"""
        syllabus_dir = self.site_root
        syllabus_file = syllabus_dir / 'syllabus.md'
        
        course_name = course_data.get('name', 'Course')
        course_code = course_data.get('course_code', '')
        syllabus_body = course_data.get('syllabus_body', '')
        
        # Convert HTML to Markdown
        syllabus_markdown = ''
        if syllabus_body:
            syllabus_markdown = self.html_converter.handle(syllabus_body)
        
        # Parse structure
        structure = self.parse_syllabus_structure(syllabus_body)
        
        # Generate front matter and content
        front_matter = {
            'layout': 'default',
            'title': f'Syllabus - {course_name}',
            'permalink': '/syllabus/'
        }
        
        content = f"""# {course_name}

**Course Code:** {course_code}

## Course Description

{syllabus_markdown}

"""
        
        # Add parsed schedule if found
        if structure.get('schedule'):
            content += "## Course Schedule\n\n"
            content += "| Week | Topic | Readings | Assignments |\n"
            content += "|------|-------|----------|-------------|\n"
            for item in structure['schedule']:
                content += f"| {item.get('week', '')} | {item.get('topic', '')} | {item.get('readings', '')} | {item.get('assignments', '')} |\n"
            content += "\n"
        
        # Add objectives if found
        if structure.get('objectives'):
            content += "## Learning Objectives\n\n"
            for obj in structure['objectives']:
                content += f"- {obj}\n"
            content += "\n"
        
        # Write file
        yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        full_content = f"---\n{yaml_content}---\n{content}\n"
        
        syllabus_file.write_text(full_content, encoding='utf-8')
        print(f"✓ Generated: {syllabus_file}")
    
    def generate_module_pages(self, modules: List[Dict]) -> None:
        """Generate module/week pages from Canvas modules"""
        modules_dir = self.site_root / 'modules'
        modules_dir.mkdir(exist_ok=True)
        
        for module in modules:
            module_name = module.get('name', 'Module')
            module_id = module.get('id')
            
            # Extract week number if present
            week_match = re.search(r'week\s*(\d+)', module_name.lower())
            week_num = week_match.group(1) if week_match else str(module.get('position', module_id))
            
            # Generate filename
            safe_name = re.sub(r'[^\w\s-]', '', module_name).strip().lower().replace(' ', '-')
            filename = f"week-{week_num.zfill(2)}-{safe_name[:30]}.md"
            if not safe_name or safe_name == f"week-{week_num}":
                filename = f"week-{week_num.zfill(2)}.md"
            
            module_file = modules_dir / filename
            
            # Generate content
            front_matter = {
                'layout': 'default',
                'title': module_name,
                'permalink': f'/modules/week-{week_num}/'
            }
            
            content = f"# {module_name}\n\n"
            
            if module.get('description'):
                desc_md = self.html_converter.handle(module['description'])
                content += f"{desc_md}\n\n"
            
            # Add module items
            items = module.get('items', [])
            if items:
                content += "## Module Contents\n\n"
                for item in items:
                    item_title = item.get('title', 'Untitled')
                    item_type = item.get('type', '').lower()
                    
                    content += f"- **{item_title}** ({item_type})\n"
                    
                    if item.get('html_url'):
                        content += f"  - [View on Canvas]({item['html_url']})\n"
            
            # Write file
            yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
            full_content = f"---\n{yaml_content}---\n{content}\n"
            
            module_file.write_text(full_content, encoding='utf-8')
            print(f"✓ Generated: {module_file}")
    
    def generate_assignment_pages(self, assignments: List[Dict]) -> None:
        """Generate assignment pages from Canvas assignments"""
        assignments_dir = self.site_root / 'assignments'
        assignments_dir.mkdir(exist_ok=True)
        
        assignments_data = []
        
        for i, assignment in enumerate(assignments, 1):
            assignment_name = assignment.get('name', 'Assignment')
            assignment_id = assignment.get('id')
            
            # Generate filename
            safe_name = re.sub(r'[^\w\s-]', '', assignment_name).strip().lower().replace(' ', '-')
            filename = f"assignment-{str(i).zfill(2)}-{safe_name[:40]}.md"
            
            assignment_file = assignments_dir / filename
            
            # Generate content
            front_matter = {
                'layout': 'default',
                'title': assignment_name,
                'permalink': f'/assignments/assignment-{i}/'
            }
            
            content = f"# {assignment_name}\n\n"
            
            # Assignment details
            if assignment.get('points_possible'):
                content += f"**Points:** {assignment['points_possible']}\n\n"
            
            if assignment.get('due_at'):
                due_date = datetime.fromisoformat(assignment['due_at'].replace('Z', '+00:00'))
                content += f"**Due Date:** {due_date.strftime('%B %d, %Y at %I:%M %p')}\n\n"
            
            if assignment.get('description'):
                desc_md = self.html_converter.handle(assignment['description'])
                content += f"## Description\n\n{desc_md}\n\n"
            
            if assignment.get('html_url'):
                content += f"[View Assignment on Canvas]({assignment['html_url']})\n"
            
            # Write file
            yaml_content = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
            full_content = f"---\n{yaml_content}---\n{content}\n"
            
            assignment_file.write_text(full_content, encoding='utf-8')
            print(f"✓ Generated: {assignment_file}")
            
            # Store for JSON
            assignments_data.append({
                'id': assignment_id,
                'name': assignment_name,
                'due_at': assignment.get('due_at'),
                'points_possible': assignment.get('points_possible'),
                'html_url': assignment.get('html_url'),
                'permalink': f'/assignments/assignment-{i}/'
            })
        
        # Generate assignments.json for dynamic updates
        data_dir = self.site_root / '_data'
        data_dir.mkdir(exist_ok=True)
        json_file = data_dir / 'assignments.json'
        json_file.write_text(json.dumps(assignments_data, indent=2), encoding='utf-8')
        print(f"✓ Generated: {json_file}")
    
    def generate_navigation(self, course_data: Dict, modules: List[Dict], assignments: List[Dict]) -> None:
        """Generate _data/navigation.yml based on course structure"""
        data_dir = self.site_root / '_data'
        data_dir.mkdir(exist_ok=True)
        nav_file = data_dir / 'navigation.yml'
        
        nav_structure = {
            'main': [
                {'title': 'Home', 'url': '/'},
                {'title': 'Syllabus', 'url': '/syllabus/'}
            ]
        }
        
        # Add modules
        if modules:
            module_links = []
            for module in sorted(modules, key=lambda m: m.get('position', 0)):
                module_name = module.get('name', 'Module')
                week_match = re.search(r'week\s*(\d+)', module_name.lower())
                week_num = week_match.group(1) if week_match else str(module.get('position', module.get('id')))
                module_links.append({
                    'title': module_name,
                    'url': f'/modules/week-{week_num}/'
                })
            nav_structure['main'].append({'title': 'Modules', 'children': module_links})
        
        # Add assignments
        if assignments:
            assignment_links = []
            for i, assignment in enumerate(assignments, 1):
                assignment_links.append({
                    'title': assignment.get('name', f'Assignment {i}'),
                    'url': f'/assignments/assignment-{i}/'
                })
            nav_structure['main'].append({'title': 'Assignments', 'children': assignment_links})
        
        # Add existing links
        nav_structure['main'].extend([
            {'title': 'Blog Posts', 'url': '/posts/'},
            {'title': 'About', 'url': '/about/'}
        ])
        
        # Write YAML
        with open(nav_file, 'w', encoding='utf-8') as f:
            yaml.dump(nav_structure, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✓ Generated: {nav_file}")
    
    def sync(self) -> None:
        """Main sync method - fetches all data and generates site"""
        print("Starting Canvas LMS to Jekyll site sync...")
        print(f"Canvas URL: {self.api_url}")
        print(f"Course ID: {self.course_id or 'Auto-detect'}\n")
        
        try:
            # Fetch data
            print("Fetching course data...")
            course_data = self.fetch_course_data()
            self.course_id = course_data.get('id')
            
            print("Fetching modules...")
            modules = self.fetch_modules()
            
            print("Fetching assignments...")
            assignments = self.fetch_assignments()
            
            # Generate pages
            print("\nGenerating site structure...")
            self.generate_syllabus_page(course_data)
            self.generate_module_pages(modules)
            self.generate_assignment_pages(assignments)
            self.generate_navigation(course_data, modules, assignments)
            
            print("\n✓ Site sync completed successfully!")
            print(f"\nCourse: {course_data.get('name')}")
            print(f"Modules: {len(modules)}")
            print(f"Assignments: {len(assignments)}")
            
        except CanvasSyncError as e:
            print(f"\n✗ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)


def load_config() -> tuple[str, str, Optional[int]]:
    """Load configuration from _config.yml"""
    config_file = Path(__file__).parent / '_config.yml'
    
    api_url = os.getenv('CANVAS_API_URL', 'https://texastech.instructure.com')
    api_key = os.getenv('CANVAS_API_KEY', '')
    course_id = None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
            canvas_config = config.get('canvas', {})
            api_url = canvas_config.get('api_url', api_url)
            api_key = canvas_config.get('api_key', api_key)
            
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
    
    if not api_key:
        raise CanvasSyncError("Canvas API key not found. Set CANVAS_API_KEY env var or configure in _config.yml")
    
    return api_url, api_key, course_id


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        course_id = int(sys.argv[1])
    else:
        course_id = None
    
    try:
        api_url, api_key, default_course_id = load_config()
        if course_id is None:
            course_id = default_course_id
    except CanvasSyncError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    sync = CanvasSiteSync(api_url, api_key, course_id)
    sync.sync()


if __name__ == '__main__':
    main()
