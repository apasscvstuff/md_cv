#!/usr/bin/env python3
"""
Arthur Passuello CV Build System
Converts YAML content to markdown with conditional logic preserving LaTeX system behavior
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import sys
import argparse


class CVBuilder:
    def __init__(self, content_dir: str = "content", output_dir: str = "output"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        
        # Version configuration matching LaTeX system
        self.versions = {
            'firmware': {
                'toggles': ['firmware', 'technical', 'detailed'],
                'tagline': 'Senior Firmware Engineer | Software Architect | Technical Project Lead',
                'max_priority': 3,
                'show_metrics': True,
                'show_business_impact': False,
                'executive_summary': False,
                'layout': 'technical'
            },
            'ai': {
                'toggles': ['ai', 'technical', 'detailed'],
                'tagline': 'Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Lead',
                'max_priority': 3,
                'show_metrics': True,
                'show_business_impact': False,
                'executive_summary': False,
                'layout': 'technical'
            },
            'consulting': {
                'toggles': ['consulting', 'ai', 'businessfocus', 'quantified'],
                'tagline': 'Senior Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead',
                'max_priority': 3,
                'show_metrics': True,
                'show_business_impact': True,
                'executive_summary': False,
                'layout': 'technical'
            },
            'executive': {
                'toggles': ['executive', 'quantified', 'onepage'],
                'tagline': 'Senior Technical Leader | Cross-functional Engineering Manager',
                'max_priority': 1,
                'show_metrics': True,
                'show_business_impact': True,
                'executive_summary': True,
                'layout': 'executive'
            },
            'general': {
                'toggles': ['firmware', 'ai', 'general'],
                'tagline': 'Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead',
                'max_priority': 2,
                'show_metrics': False,
                'show_business_impact': False,
                'executive_summary': False,
                'layout': 'technical'
            }
        }
        
        # Personal information loaded from YAML
        self.personal = None  # Will be loaded when needed
    
    def load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Load YAML file with error handling"""
        file_path = self.content_dir / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found, using empty dict")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing {filename}: {e}")
            return {}
    
    def load_personal_data(self, target_version: str) -> Dict[str, Any]:
        """Load and process personal information with version-specific content"""
        if self.personal is None:
            personal_data = self.load_yaml_file('arthur-personal.yaml')
            personal_info = personal_data.get('personal', {})
            
            # Process contact information
            contact = personal_info.get('contact', {})
            
            # Format languages
            languages = personal_info.get('languages', [])
            languages_formatted = ' • '.join([f"{lang['language']} ({lang['proficiency']})" for lang in languages])
            
            self.personal = {
                'name': personal_info.get('name', {}).get('full', 'Arthur PASSUELLO'),
                'phone': contact.get('phone', '+(41) 79 176 24 84'),
                'email': contact.get('email', 'apassuello@protonmail.com'),
                'address': contact.get('formatted', 'Chemin du Parc-de-Valency 1, 1004 Lausanne, Switzerland'),
                'github': contact.get('github', 'apassuello'),
                'linkedin': contact.get('linkedin', 'arthur-passuello'),
                'linkedin_name': personal_info.get('name', {}).get('full', 'Arthur Passuello'),
                'languages': languages_formatted,
                'profile_photo': 'assets/profile.jpeg',
                'taglines': personal_info.get('taglines', {}),
                'certifications': personal_info.get('certifications', []),
                'interests': personal_info.get('interests', {})
            }
        
        return self.personal
    
    def check_version_condition(self, item_versions: List[str], target_version: str) -> bool:
        """Check if item should be included for target version"""
        if not item_versions:
            return True
        if "all" in item_versions:
            return True
        return target_version in item_versions
    
    def check_toggle_condition(self, toggles: List[str], target_version: str) -> bool:
        """Check if toggles are active for target version"""
        version_toggles = self.versions[target_version]['toggles']
        return any(toggle in version_toggles for toggle in toggles)
    
    def filter_by_priority(self, items: List[Dict], target_version: str) -> List[Dict]:
        """Filter items by priority level based on version"""
        max_priority = self.versions[target_version]['max_priority']
        return [item for item in items if item.get('priority', 1) <= max_priority]
    
    def process_skills_section(self, skills_data: Dict, target_version: str) -> Dict:
        """Process skills section with version-specific logic"""
        version_config = self.versions[target_version]
        
        if version_config['layout'] == 'executive':
            # Executive layout - 3 streamlined categories
            return {
                'layout': 'executive',
                'categories': skills_data.get('executive', {})
            }
        else:
            # Technical layout - 3-column format
            technical_skills = skills_data.get('technical', {})
            result = {
                'layout': 'technical',
                'programming_languages': technical_skills.get('programming_languages', {}).get(target_version, []),
                'core_technologies': technical_skills.get('core_technologies', {}).get(target_version, []),
                'tools_platforms': technical_skills.get('tools_platforms', {}).get(target_version, []),
                'project_management': technical_skills.get('project_management', {}).get(target_version, [])
            }
            
            # Add domain expertise (version-specific)
            domain_expertise = technical_skills.get('domain_expertise', {}).get(target_version, {})
            if domain_expertise:
                result['domain_expertise'] = domain_expertise
            
            # Add medical device section if not consulting
            if target_version != 'consulting':
                medical_device = technical_skills.get('medical_device', {})
                if medical_device and target_version not in medical_device.get('exclude_versions', []):
                    result['medical_device'] = medical_device
            
            return result
    
    def process_experience_section(self, experience_data: Dict, target_version: str) -> List[Dict]:
        """Process experience section with version-specific logic"""
        version_config = self.versions[target_version]
        experiences = experience_data.get('experiences', [])
        
        filtered_experiences = []
        
        for exp in experiences:
            # Check if experience should be included for this version
            if not self.check_version_condition(exp.get('versions', []), target_version):
                continue
            
            # Process experience with version-specific content
            processed_exp = {
                'company': exp['company'],
                'location': exp['location'],
                'period': exp['period'],
                'reference': exp.get('reference', ''),
                'position': exp.get('position_variants', {}).get(target_version, exp.get('position_base', '')),
                'skills_tags': exp.get('skills_tags', {}).get(target_version, ''),
                'achievements': []
            }
            
            # Filter achievements by version and priority
            achievements = exp.get('achievements', [])
            for achievement in achievements:
                # Check version condition
                if not self.check_version_condition(achievement.get('versions', []), target_version):
                    continue
                
                # Check priority condition
                if achievement.get('priority', 1) > version_config['max_priority']:
                    continue
                
                # Add achievement text
                processed_exp['achievements'].append({
                    'text': achievement['text'],
                    'type': achievement.get('type', 'base'),
                    'priority': achievement.get('priority', 1)
                })
            
            if processed_exp['achievements']:  # Only add if has achievements
                filtered_experiences.append(processed_exp)
        
        return filtered_experiences
    
    def process_projects_section(self, projects_data: Dict, target_version: str) -> List[Dict]:
        """Process projects section with version-specific logic"""
        version_config = self.versions[target_version]
        
        # Executive version doesn't show projects
        if version_config.get('layout') == 'executive':
            return []
        
        projects = projects_data.get('projects', [])
        filtered_projects = []
        
        for project in projects:
            # Check if project should be included for this version
            if not self.check_version_condition(project.get('versions', []), target_version):
                continue
            
            # Process project with version-specific content
            processed_project = {
                'name': project['name'],
                'period': project['period'],
                'links': project.get('links', {}),
                'descriptions': project.get('descriptions', {}).get(target_version, []),
                'skills_tags': project.get('skills_tags', {}).get(target_version, '')
            }
            
            filtered_projects.append(processed_project)
        
        return filtered_projects
    
    def generate_skills_markdown(self, skills_data: Dict, target_version: str) -> str:
        """Generate skills section markdown"""
        processed_skills = self.process_skills_section(skills_data, target_version)
        
        if processed_skills['layout'] == 'executive':
            # Executive format - 3 streamlined categories
            markdown = "## Skills\n\n"
            for category, skills in processed_skills['categories'].items():
                formatted_category = category.replace('_', ' ').title()
                markdown += f"**{formatted_category}**: "
                
                skill_items = []
                for skill in skills:
                    skill_text = skill['skill']
                    if skill.get('metric'):
                        skill_text += f" ({skill['metric']})"
                    skill_items.append(skill_text)
                
                markdown += " • ".join(skill_items) + "\n\n"
            
            return markdown
        else:
            # Technical 3-column format
            markdown = "## Skills\n\n"
            markdown += "| **Software Engineering**      | **AI & LLMs**                              | **Data Science**                          |\n"
            markdown += "| :---------------------------- | :----------------------------------------- | :---------------------------------------- |\n"
            
            # Get max length for proper table formatting
            max_rows = max(
                len(processed_skills.get('programming_languages', [])) + len(processed_skills.get('core_technologies', [])),
                len(processed_skills.get('domain_expertise', {}).get('skills', [])) + len(processed_skills.get('domain_expertise', {}).get('secondary_skills', [])),
                len(processed_skills.get('tools_platforms', [])) + len(processed_skills.get('project_management', []))
            )
            
            # Build the table rows
            col1_items = processed_skills.get('programming_languages', []) + processed_skills.get('core_technologies', [])
            
            # Column 2 - Domain expertise
            col2_items = []
            domain_exp = processed_skills.get('domain_expertise', {})
            if domain_exp:
                col2_items.extend(domain_exp.get('skills', []))
                col2_items.extend(domain_exp.get('secondary_skills', []))
            
            # Column 3 - Tools and project management
            col3_items = processed_skills.get('tools_platforms', []) + processed_skills.get('project_management', [])
            
            # Create table rows
            max_items = max(len(col1_items), len(col2_items), len(col3_items))
            
            for i in range(max_items):
                col1 = f"• {col1_items[i]}" if i < len(col1_items) else ""
                col2 = f"• {col2_items[i]}" if i < len(col2_items) else ""
                col3 = f"• {col3_items[i]}" if i < len(col3_items) else ""
                
                markdown += f"| {col1:<28} | {col2:<42} | {col3:<40} |\n"
            
            return markdown
    
    def generate_experience_markdown(self, experience_data: Dict, target_version: str) -> str:
        """Generate experience section markdown"""
        experiences = self.process_experience_section(experience_data, target_version)
        
        markdown = "## Work Experience\n\n"
        
        for exp in experiences:
            markdown += f"### {exp['company']}  \n"
            markdown += f"<div class=\"date-location\">_{exp['period']}_ <span class=\"location\">_{exp['location']}_</span></div>\n\n"
            
            markdown += f"**{exp['position']}**"
            if exp['reference']:
                markdown += f" {exp['reference']}"
            markdown += "\n\n"
            
            # Add achievements
            for achievement in exp['achievements']:
                markdown += f"* {achievement['text']}\n"
            
            # Add skills tags if available
            if exp['skills_tags']:
                markdown += f"\n<div class=\"skills-tags\">{exp['skills_tags']}</div>\n"
            
            markdown += "\n"
        
        return markdown
    
    def generate_projects_markdown(self, projects_data: Dict, target_version: str) -> str:
        """Generate projects section markdown"""
        projects = self.process_projects_section(projects_data, target_version)
        
        if not projects:
            return ""
        
        markdown = "## Projects\n\n"
        
        for project in projects:
            markdown += f"### {project['name']}\n"
            markdown += f"<div class=\"date-location\">_{project['period']}_</div>\n\n"
            
            # Add links
            if project['links']:
                link_parts = []
                for link_type, url in project['links'].items():
                    if link_type == 'github':
                        link_parts.append(f"[Github]({url})")
                    elif link_type == 'demo':
                        link_parts.append(f"[Demo]({url})")
                    elif link_type == 'website':
                        link_parts.append(f"[Website]({url})")
                
                if link_parts:
                    markdown += " | ".join(link_parts) + "\n\n"
            
            # Add descriptions
            for desc in project['descriptions']:
                markdown += f"- {desc}\n"
            
            # Add skills tags if available
            if project['skills_tags']:
                markdown += f"\n<div class=\"skills-tags\">{project['skills_tags']}</div>\n"
            
            markdown += "\n"
        
        return markdown
    
    def process_education_section(self, education_data: Dict, target_version: str) -> List[Dict]:
        """Process education section with version-specific filtering"""
        if 'education' not in education_data:
            return []
        
        education_items = education_data['education']
        filtered_education = []
        
        for education in education_items:
            # Process version-specific content
            processed_education = {
                'institution': education.get('institution', ''),
                'institution_full': education.get('institution_full', ''),
                'degree': education.get('degree', ''),
                'field_of_study': education.get('field_of_study', ''),
                'major': education.get('major', ''),
                'start_date': education.get('start_date', ''),
                'end_date': education.get('end_date', ''),
                'location': education.get('location', ''),
                'focus_area': education.get('focus_areas', {}).get(target_version, ''),
                'relevant_coursework': education.get('relevant_coursework', {}).get(target_version, []),
                'achievements': []
            }
            
            # Filter achievements by version
            for achievement in education.get('notable_achievements', []):
                achievement_versions = achievement.get('versions', [])
                if self.check_version_condition(achievement_versions, target_version):
                    processed_education['achievements'].append(achievement['achievement'])
            
            filtered_education.append(processed_education)
        
        return filtered_education
    
    def generate_education_markdown(self, education_data: Dict, target_version: str) -> str:
        """Generate education section markdown"""
        processed_education = self.process_education_section(education_data, target_version)
        
        if not processed_education:
            return ""
        
        markdown = "## Education\n\n"
        
        for education in processed_education:
            # Institution and degree
            if education['institution_full']:
                markdown += f"### {education['institution_full']}\n"
            else:
                markdown += f"### {education['institution']}\n"
            
            # Date range and location
            if education['start_date'] and education['end_date']:
                period = f"{education['start_date']} - {education['end_date']}"
                markdown += f"<div class=\"date-location\">_{period}_ <span class=\"location\">_{education['location']}_</span></div>\n\n"
            
            # Degree information
            markdown += f"**{education['degree']}**"
            if education['major']:
                markdown += f", Major in {education['major']}"
            markdown += "\n\n"
            
            # Focus area (version-specific)
            if education['focus_area']:
                markdown += f"*Focus: {education['focus_area']}*\n\n"
            
            # Relevant coursework (version-specific)
            if education['relevant_coursework']:
                markdown += "**Key Coursework:** "
                markdown += " • ".join(education['relevant_coursework']) + "\n\n"
            
            # Achievements (version-specific)
            if education['achievements']:
                for achievement in education['achievements']:
                    markdown += f"* {achievement}\n"
                markdown += "\n"
        
        return markdown
    
    def build_version(self, target_version: str) -> None:
        """Build a specific CV version"""
        print(f"Building {target_version} version...")
        
        # Load content files
        skills_data = self.load_yaml_file('arthur-skills.yaml')
        experience_data = self.load_yaml_file('arthur-experience.yaml')
        projects_data = self.load_yaml_file('arthur-projects.yaml')
        education_data = self.load_yaml_file('arthur-education.yaml')
        
        # Load personal data with version-specific content
        personal_info = self.load_personal_data(target_version)
        
        # Get version configuration and tagline
        version_config = self.versions[target_version]
        tagline = personal_info.get('taglines', {}).get(target_version, version_config['tagline'])
        
        # Build markdown content
        markdown_content = f"""<img src="{personal_info['profile_photo']}" alt="{personal_info['name']}" class="profile-pic" />

# **{personal_info['name']}**
### {tagline}

_{personal_info['address']}_

<p class="inline-contact">
  <img src="assets/icons/phone.png" class="icon" alt="Phone" /> {personal_info['phone']} | 
  <img src="assets/icons/email.png" class="icon" alt="Email" /> <a href="mailto:{personal_info['email']}">{personal_info['email']}</a> | 
  <img src="assets/icons/github.png" class="icon" alt="GitHub" /> <a href="https://github.com/{personal_info['github']}">{personal_info['github']}</a> | 
  <img src="assets/icons/linkedin.png" class="icon" alt="LinkedIn" /> <a href="https://linkedin.com/in/{personal_info['linkedin']}">{personal_info['linkedin_name']}</a>
</p>

**{personal_info['languages']}**

{self.generate_skills_markdown(skills_data, target_version)}

{self.generate_experience_markdown(experience_data, target_version)}

{self.generate_projects_markdown(projects_data, target_version)}

{self.generate_education_markdown(education_data, target_version)}
"""
        
        # Save markdown file
        output_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ {target_version} version built successfully")
        print(f"📄 Output: {output_path}")
    
    def build_all_versions(self) -> None:
        """Build all CV versions"""
        print("Building all CV versions...")
        
        for version in self.versions.keys():
            self.build_version(version)
        
        print("🎉 All versions built successfully!")
    
    def test_version(self, target_version: str) -> None:
        """Test a specific version for content validation"""
        print(f"Testing {target_version} version...")
        
        # Load content and test logic
        skills_data = self.load_yaml_file('arthur-skills.yaml')
        experience_data = self.load_yaml_file('arthur-experience.yaml')
        projects_data = self.load_yaml_file('arthur-projects.yaml')
        education_data = self.load_yaml_file('arthur-education.yaml')
        
        # Test personal data loading
        personal_info = self.load_personal_data(target_version)
        print(f"Personal data loaded: {personal_info['name']}")
        tagline = personal_info.get('taglines', {}).get(target_version, 'No version-specific tagline')
        print(f"Version tagline: {tagline[:50]}..." if len(tagline) > 50 else f"Version tagline: {tagline}")
        
        # Test skills processing
        processed_skills = self.process_skills_section(skills_data, target_version)
        print(f"Skills layout: {processed_skills.get('layout', 'unknown')}")
        
        # Test experience processing
        processed_exp = self.process_experience_section(experience_data, target_version)
        print(f"Experience items: {len(processed_exp)}")
        
        # Test projects processing
        processed_projects = self.process_projects_section(projects_data, target_version)
        print(f"Projects: {len(processed_projects)}")
        
        # Test education processing
        processed_education = self.process_education_section(education_data, target_version)
        print(f"Education items: {len(processed_education)}")
        
        print(f"✅ {target_version} version tested successfully")
    
    def _copy_assets(self, target_version: str) -> None:
        """Copy assets to output directory for proper PDF generation"""
        import shutil
        
        output_assets_dir = self.output_dir / target_version / "assets"
        output_assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy profile image
        profile_src = Path("assets/profile.jpeg")
        if profile_src.exists():
            shutil.copy2(profile_src, output_assets_dir / "profile.jpeg")
        
        # Copy icons
        icons_dir = output_assets_dir / "icons"
        icons_dir.mkdir(exist_ok=True)
        
        for icon in ["phone.png", "email.png", "github.png", "linkedin.png"]:
            icon_src = Path(f"assets/icons/{icon}")
            if icon_src.exists():
                shutil.copy2(icon_src, icons_dir / icon)
        
        # Copy CSS files
        css_dest = self.output_dir / target_version / "css_styling.css"
        css_print_dest = self.output_dir / target_version / "css_styling_print.css"
        shutil.copy2("css_styling.css", css_dest)
        shutil.copy2("css_styling_print.css", css_print_dest)

    def build_html(self, target_version: str) -> None:
        """Build HTML version of CV from markdown"""
        print(f"Building HTML for {target_version} version...")
        
        # Build markdown first
        self.build_version(target_version)
        
        # Copy assets for proper PDF generation
        self._copy_assets(target_version)
        
        # Convert markdown to HTML using pandoc
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        
        try:
            cmd = [
                'pandoc', str(md_path),
                '-f', 'markdown',
                '-t', 'html',
                '--css', './css_styling.css',  # Local CSS for better WeasyPrint support
                '--standalone',
                '-o', str(html_path)
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ HTML generated: {html_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ HTML generation failed: {e}")
        except FileNotFoundError:
            print("❌ pandoc not found. Please install pandoc first.")
    
    def build_pdf(self, target_version: str) -> None:
        """Attempt to build PDF version of CV"""
        print(f"Building PDF for {target_version} version...")
        
        # First ensure HTML exists
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        if not html_path.exists():
            self.build_html(target_version)
        
        pdf_path = self.output_dir / target_version / f"arthur-{target_version}.pdf"
        
        # Try different PDF generation methods
        methods = [
            self._try_chrome_headless_pdf,
            self._try_weasyprint_pdf,
            self._try_pandoc_pdf,
            self._provide_manual_instructions
        ]
        
        for method in methods:
            if method(html_path, pdf_path, target_version):
                break
    
    def _try_chrome_headless_pdf(self, html_path: Path, pdf_path: Path, target_version: str) -> bool:
        """Try generating PDF using Chrome headless mode"""
        chrome_commands = [
            'google-chrome',
            'chromium',
            'google-chrome-stable',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ]
        
        for chrome_cmd in chrome_commands:
            try:
                cmd = [
                    chrome_cmd,
                    '--headless',
                    '--disable-gpu',
                    '--print-to-pdf=' + str(pdf_path),
                    'file://' + str(html_path.absolute())
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and pdf_path.exists():
                    print(f"✅ PDF generated with Chrome headless: {pdf_path}")
                    return True
            except Exception:
                continue
        
        print("Chrome headless not available")
        return False
    
    def _try_weasyprint_pdf(self, html_path: Path, pdf_path: Path, target_version: str) -> bool:
        """Try generating PDF using weasyprint with print-optimized CSS"""
        try:
            # Set up environment for WeasyPrint
            env = subprocess.os.environ.copy()
            env['PKG_CONFIG_PATH'] = "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig"
            env['DYLD_LIBRARY_PATH'] = "/opt/homebrew/lib:" + env.get('DYLD_LIBRARY_PATH', '')
            
            # Create a temporary HTML file with print-optimized CSS
            temp_html = html_path.parent / f"temp_{html_path.name}"
            
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace CSS reference with print-optimized version
            html_content = html_content.replace('./css_styling.css', './css_styling_print.css')
            
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            cmd = ['weasyprint', str(temp_html), str(pdf_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)
            
            # Clean up temp file
            temp_html.unlink(missing_ok=True)
            
            if result.returncode == 0:
                print(f"✅ PDF generated with weasyprint: {pdf_path}")
                return True
            else:
                print(f"WeasyPrint failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"WeasyPrint failed: {e}")
            return False
    
    def _try_pandoc_pdf(self, html_path: Path, pdf_path: Path, target_version: str) -> bool:
        """Try generating PDF using pandoc"""
        try:
            cmd = [
                'pandoc', str(html_path),
                '-f', 'html',
                '-t', 'pdf',
                '-o', str(pdf_path)
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ PDF generated with pandoc: {pdf_path}")
            return True
        except Exception as e:
            print(f"Pandoc PDF failed: {e}")
            return False
    
    def _provide_manual_instructions(self, html_path: Path, pdf_path: Path, target_version: str) -> bool:
        """Provide manual PDF generation instructions"""
        print(f"""
📋 Manual PDF generation required for {target_version} version:

1. Open this file in your browser: {html_path}
2. Press Cmd+P (Mac) or Ctrl+P (Windows/Linux)
3. Choose 'Save as PDF' or 'Print to PDF'
4. Save as: {pdf_path}

The HTML file is ready with proper CSS styling.
You can also use browser extensions or online converters.
        """)
        return True
    
    def build_all_formats(self, target_version: str) -> None:
        """Build all formats (markdown, HTML, PDF) for a version"""
        print(f"Building all formats for {target_version} version...")
        self.build_version(target_version)  # Markdown
        self.build_html(target_version)     # HTML
        self.build_pdf(target_version)      # PDF


def main():
    parser = argparse.ArgumentParser(description='Build Arthur Passuello CV versions')
    parser.add_argument('version', nargs='?', choices=['firmware', 'ai', 'consulting', 'executive', 'general', 'all'], 
                       default='all', help='Version to build (default: all)')
    parser.add_argument('--test', action='store_true', help='Test version logic without building')
    parser.add_argument('--html', action='store_true', help='Generate HTML output')
    parser.add_argument('--pdf', action='store_true', help='Generate PDF output (requires HTML)')
    parser.add_argument('--all-formats', action='store_true', help='Generate all formats (markdown, HTML, PDF)')
    parser.add_argument('--content-dir', default='content', help='Content directory path')
    parser.add_argument('--output-dir', default='output', help='Output directory path')
    
    args = parser.parse_args()
    
    builder = CVBuilder(args.content_dir, args.output_dir)
    
    if args.test:
        if args.version == 'all':
            for version in builder.versions.keys():
                builder.test_version(version)
        else:
            builder.test_version(args.version)
    elif args.all_formats:
        if args.version == 'all':
            for version in builder.versions.keys():
                builder.build_all_formats(version)
        else:
            builder.build_all_formats(args.version)
    elif args.html:
        if args.version == 'all':
            for version in builder.versions.keys():
                builder.build_html(version)
        else:
            builder.build_html(args.version)
    elif args.pdf:
        if args.version == 'all':
            for version in builder.versions.keys():
                builder.build_pdf(version)
        else:
            builder.build_pdf(args.version)
    else:
        # Default: build markdown only
        if args.version == 'all':
            builder.build_all_versions()
        else:
            builder.build_version(args.version)


if __name__ == '__main__':
    main()