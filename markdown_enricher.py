#!/usr/bin/env python3
"""
Markdown Enricher - Transform clean markdown into HTML with semantic CSS classes
"""

import re
from typing import List, Dict, Tuple, Optional


class MarkdownEnricher:
    """
    Post-processor that transforms clean markdown patterns into semantic HTML structure.
    
    This class bridges the gap between human-readable markdown and CSS requirements,
    allowing CV content to be maintained in clean markdown while still producing
    richly styled HTML/PDF output.
    """
    
    def __init__(self):
        # Pre-compile regex patterns for performance
        self.patterns = {
            'header': self._compile_header_patterns(),
            'skills': self._compile_skills_patterns(),
            'experience': self._compile_experience_patterns(),
            'projects': self._compile_project_patterns(),
            'education': self._compile_education_patterns(),
            'executive_summary': self._compile_executive_summary_patterns(),
            'certifications': self._compile_certifications_patterns(),
            'section': self._compile_section_patterns()
        }
    
    def enrich_markdown(self, markdown_content: str) -> str:
        """
        Main entry point for enrichment.
        
        Args:
            markdown_content: Clean markdown content
            
        Returns:
            Enriched HTML with semantic CSS classes
        """
        # Parse markdown into sections
        sections = self._parse_sections(markdown_content)
        
        # Process each section type
        enriched_sections = []
        for section in sections:
            enriched = self._enrich_section(section)
            enriched_sections.append(enriched)
        
        # Join sections and wrap in main content div
        enriched_html = '\n'.join(enriched_sections)
        return self._wrap_main_content(enriched_html)
    
    def _compile_header_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for header section elements"""
        return {
            'profile_image': re.compile(r'^!\[([^\]]+)\]\(([^\)]+)\)$', re.MULTILINE),
            'name': re.compile(r'^# \*\*([^*]+)\*\*$', re.MULTILINE),
            'tagline': re.compile(r'^### (.+)$', re.MULTILINE),
            'address': re.compile(r'^_([^_]+)_$', re.MULTILINE),
            'contact': re.compile(r'^([📞✉️🔗💼].+)$', re.MULTILINE),
            'languages': re.compile(r'^\*\*([^*]+\([^)]+\)[^*]*)\*\*$', re.MULTILINE)
        }
    
    def _compile_skills_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for skills section"""
        return {
            'section_header': re.compile(r'^## Skills$', re.MULTILINE),
            'table_start': re.compile(r'^\|(.+)\|$', re.MULTILINE),
            'table_separator': re.compile(r'^\|[\s:]*-+[\s:]*\|', re.MULTILINE),
            'table_row': re.compile(r'^\|(.+)\|$', re.MULTILINE),
            'executive_skill': re.compile(r'^\*\*([^:]+)\*\*:\s*(.+)$', re.MULTILINE),
            'checkmark': re.compile(r'✓\s*')
        }
    
    def _compile_experience_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for experience section"""
        return {
            'section_header': re.compile(r'^## Work Experience$', re.MULTILINE),
            'company': re.compile(r'^### (.+)$', re.MULTILINE),
            'location_date': re.compile(r'^_([^_]+)_<br>\n_([^_]+)_$', re.MULTILINE),
            'position': re.compile(r'^\*\*([^*]+)\*\*(?:\s*·\s*_([^_]+)_)?$', re.MULTILINE),
            'achievement': re.compile(r'^\* (.+)$', re.MULTILINE),
            'skills_tags': re.compile(r'^_([^_]+)_$', re.MULTILINE)
        }
    
    def _compile_project_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for projects section"""
        return {
            'section_header': re.compile(r'^## (?:Other Projects|Projects|Selected Projects)$', re.MULTILINE),
            'project_name': re.compile(r'^### (.+)$', re.MULTILINE),
            'project_meta': re.compile(r'^_([^_]+)<br>\n([^_]+)_$', re.MULTILINE),
            'project_description': re.compile(r'^- (.+)$', re.MULTILINE),
            'project_link': re.compile(r'_\[([^\]]+)\]\(([^\)]+)\)_')
        }
    
    def _compile_education_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for education section"""
        return {
            'section_header': re.compile(r'^## Education$', re.MULTILINE),
            'institution': re.compile(r'^### (.+)$', re.MULTILINE),
            'location_date': re.compile(r'^_([^_]+)_<br>\n_([^_]+)_$', re.MULTILINE),
            'degree': re.compile(r'^\*\*([^*]+)\*\*(?:\s*<br>\n(.+))?$', re.MULTILINE)
        }
    
    def _compile_executive_summary_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for executive summary section"""
        return {
            'section_header': re.compile(r'^## Executive Summary$', re.MULTILINE),
            'summary_text': re.compile(r'^(.+?)$', re.MULTILINE)
        }
    
    def _compile_certifications_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for certifications section"""
        return {
            'section_header': re.compile(r'^## Training & Certifications$', re.MULTILINE),
            'cert_name': re.compile(r'^### (.+)$', re.MULTILINE),
            'org_year': re.compile(r'^_([^_]+)_(?:\s*\|\s*_([^_]+)_)?$', re.MULTILINE),
            'description': re.compile(r'^([^#\n]+)$', re.MULTILINE)
        }
    
    def _compile_section_patterns(self) -> Dict[str, re.Pattern]:
        """Compile general section patterns"""
        return {
            'any_section': re.compile(r'^## (.+)$', re.MULTILINE),
            'page_break': re.compile(r'<div class="page-break"></div>')
        }
    
    def _parse_sections(self, content: str) -> List[Dict[str, str]]:
        """
        Parse markdown content into logical sections.
        
        Returns list of dicts with 'type' and 'content' keys.
        """
        sections = []
        
        # First, check for header section (before first ## heading)
        first_section_match = self.patterns['section']['any_section'].search(content)
        if first_section_match:
            header_content = content[:first_section_match.start()].strip()
            if header_content:
                sections.append({
                    'type': 'header',
                    'content': header_content
                })
            
            # Parse remaining sections
            remaining_content = content[first_section_match.start():]
            section_splits = self.patterns['section']['any_section'].split(remaining_content)
            
            # Process sections (alternating between titles and content)
            for i in range(1, len(section_splits), 2):
                if i + 1 < len(section_splits):
                    section_title = section_splits[i].strip()
                    section_content = section_splits[i + 1].strip()
                    
                    # Determine section type
                    section_type = self._identify_section_type(section_title)
                    
                    sections.append({
                        'type': section_type,
                        'title': section_title,
                        'content': f"## {section_title}\n\n{section_content}"
                    })
        else:
            # No sections found, treat entire content as header
            sections.append({
                'type': 'header',
                'content': content.strip()
            })
        
        return sections
    
    def _identify_section_type(self, title: str) -> str:
        """Identify section type from title"""
        title_lower = title.lower()
        
        if 'training' in title_lower and 'certification' in title_lower:
            return 'certifications'
        elif 'skill' in title_lower:
            return 'skills'
        elif 'experience' in title_lower or 'work' in title_lower:
            return 'experience'
        elif 'project' in title_lower:
            return 'projects'
        elif 'education' in title_lower:
            return 'education'
        else:
            return 'generic'
    
    def _enrich_section(self, section: Dict[str, str]) -> str:
        """Route section to appropriate enrichment method"""
        section_type = section['type']
        content = section['content']
        
        if section_type == 'header':
            return self._enrich_header(content)
        elif section_type == 'skills':
            return self._enrich_skills(content)
        elif section_type == 'experience':
            return self._enrich_experience(content)
        elif section_type == 'projects':
            return self._enrich_projects(content)
        elif section_type == 'education':
            return self._enrich_education(content)
        elif section_type == 'certifications':
            return self._enrich_certifications(content)
        else:
            return self._enrich_generic_section(content)
    
    def _enrich_header(self, content: str) -> str:
        """Transform header markdown into semantic HTML"""
        html_parts = []
        
        # Start header div
        html_parts.append('<div class="cv-header">')
        html_parts.append('  <div class="cv-header-info">')
        
        # Extract and process each header element
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Profile image (will be moved to profile container)
            profile_match = self.patterns['header']['profile_image'].match(line)
            if profile_match:
                continue  # Process later
            
            # Name
            name_match = self.patterns['header']['name'].match(line)
            if name_match:
                name = name_match.group(1)
                html_parts.append(f'    <h1 class="cv-name" id="cv-name"><strong>{name}</strong></h1>')
                continue
            
            # Tagline
            tagline_match = self.patterns['header']['tagline'].match(line)
            if tagline_match:
                tagline = tagline_match.group(1)
                html_parts.append(f'    <h3 class="cv-tagline" id="cv-tagline">{tagline}</h3>')
                html_parts.append('    ')
                continue
            
            # Address
            address_match = self.patterns['header']['address'].match(line)
            if address_match:
                address = address_match.group(1)
                html_parts.append(f'    <p class="cv-address" id="cv-address"><em>{address}</em></p>')
                html_parts.append('    ')
                continue
            
            # Contact info
            if any(icon in line for icon in ['📞', '✉️', '🔗', '💼']):
                contact_html = self._enrich_contact_line(line)
                html_parts.append(f'    <div class="cv-contact inline-contact" id="cv-contact">')
                html_parts.append(f'      {contact_html}')
                html_parts.append('    </div>')
                html_parts.append('    ')
                continue
            
            # Languages
            lang_match = self.patterns['header']['languages'].match(line)
            if lang_match:
                languages = lang_match.group(1)
                html_parts.append(f'    <p class="cv-languages" id="cv-languages"><strong>{languages}</strong></p>')
                continue
            
            # Executive summary text (plain paragraph after languages)
            # This will be a longer text paragraph, not matching other patterns
            if (len(line) > 50 and not line.startswith('**') and not line.startswith('_') 
                and not any(icon in line for icon in ['📞', '✉️', '🔗', '💼']) 
                and not line.startswith('#')):
                formatted_summary = self._process_markdown_formatting(line)
                html_parts.append(f'    <div class="cv-executive-summary-inline">')
                html_parts.append(f'      <p class="cv-executive-summary-text">{formatted_summary}</p>')
                html_parts.append(f'    </div>')
                continue
        
        # Close header info div
        html_parts.append('  </div>')
        html_parts.append('  ')
        
        # Add profile container if image was found
        profile_match = self.patterns['header']['profile_image'].search(content)
        if profile_match:
            alt_text = profile_match.group(1)
            img_path = profile_match.group(2)
            html_parts.append('  <div class="cv-profile-container">')
            html_parts.append(f'    <img src="{img_path}" alt="{alt_text}" class="cv-profile-pic profile-pic" />')
            html_parts.append('  </div>')
        
        # Close header div
        html_parts.append('</div>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_contact_line(self, line: str) -> str:
        """Transform contact line with emoji icons into HTML"""
        # Map emoji to icon files
        icon_mapping = {
            '📞': ('phone.png', 'Phone'),
            '✉️': ('email.png', 'Email'),
            '🔗': ('github.png', 'GitHub'),
            '💼': ('linkedin.png', 'LinkedIn')
        }
        
        # Process each icon and its associated text
        parts = []
        segments = line.split('|')
        
        for segment in segments:
            segment = segment.strip()
            for emoji, (icon_file, alt_text) in icon_mapping.items():
                if emoji in segment:
                    # Extract text after emoji
                    text = segment.replace(emoji, '').strip()
                    
                    # Check if it's a link
                    link_match = re.match(r'\[([^\]]+)\]\(([^\)]+)\)', text)
                    if link_match:
                        link_text = link_match.group(1)
                        link_url = link_match.group(2)
                        parts.append(f'<img src="assets/icons/{icon_file}" class="cv-contact-icon icon" alt="{alt_text}" /> <a href="{link_url}">{link_text}</a>')
                    else:
                        parts.append(f'<img src="assets/icons/{icon_file}" class="cv-contact-icon icon" alt="{alt_text}" /> {text}')
                    break
        
        return ' | '.join(parts)
    
    def _enrich_skills(self, content: str) -> str:
        """Transform skills markdown into semantic HTML"""
        html_parts = []
        
        # Start skills section
        html_parts.append('<section class="cv-section cv-skills">')
        html_parts.append('<h2 class="cv-section-header" id="skills">Skills</h2>')
        html_parts.append('')
        
        # Check if it's executive format (paragraph style)
        if '**' in content and ':' in content and '|' not in content:
            # Executive format
            for line in content.split('\n'):
                skill_match = self.patterns['skills']['executive_skill'].match(line)
                if skill_match:
                    category = skill_match.group(1)
                    skills = skill_match.group(2)
                    html_parts.append(f'<div class="cv-skill-category cv-executive-skills">')
                    html_parts.append(f'<p class="cv-skill-category-header"><strong>{category}</strong>: {skills}</p>')
                    html_parts.append('</div>')
                    html_parts.append('')
        else:
            # Table format
            table_lines = []
            in_table = False
            
            for line in content.split('\n'):
                if self.patterns['skills']['table_start'].match(line):
                    in_table = True
                    table_lines.append(line)
                elif in_table and (self.patterns['skills']['table_separator'].match(line) or 
                                 self.patterns['skills']['table_row'].match(line)):
                    table_lines.append(line)
                elif in_table and line.strip() == '':
                    # End of table
                    enriched_table = self._enrich_skills_table(table_lines)
                    html_parts.append(enriched_table)
                    in_table = False
                    table_lines = []
            
            # Handle case where table extends to end of content
            if table_lines:
                enriched_table = self._enrich_skills_table(table_lines)
                html_parts.append(enriched_table)
        
        html_parts.append('</section>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_skills_table(self, table_lines: List[str]) -> str:
        """Transform markdown table into semantic HTML table"""
        if not table_lines:
            return ''
        
        html_parts = []
        
        # Parse headers
        header_line = table_lines[0]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]
        column_count = len(headers)
        column_width = f"{100/column_count:.1f}%"
        
        # Start table
        html_parts.append('<div class="cv-skills-table-container">')
        html_parts.append(f'<table class="cv-skills-table cv-skills-dynamic" data-columns="{column_count}">')
        html_parts.append('<thead>')
        html_parts.append('<tr>')
        
        # Add headers
        for header in headers:
            # Clean header (remove ** markers)
            clean_header = header.replace('**', '')
            html_parts.append(f'<th class="cv-skills-header" style="width: {column_width};"><strong>{clean_header}</strong></th>')
        
        html_parts.append('</tr>')
        html_parts.append('</thead>')
        html_parts.append('<tbody>')
        
        # Parse rows (skip header and separator)
        for line in table_lines[2:]:
            if line.strip():
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html_parts.append('<tr class="cv-skills-row">')
                
                for cell in cells:
                    if cell:
                        # Check for checkmark
                        if '✓' in cell:
                            cell_content = cell.replace('✓', '<span class="cv-skill-bullet">✓</span>')
                        else:
                            cell_content = cell
                        html_parts.append(f'<td class="cv-skill-item">{cell_content}</td>')
                    else:
                        html_parts.append('<td class="cv-skill-item"></td>')
                
                html_parts.append('</tr>')
        
        html_parts.append('</tbody>')
        html_parts.append('</table>')
        html_parts.append('</div>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_experience(self, content: str) -> str:
        """Transform experience markdown into semantic HTML"""
        html_parts = []
        
        # Start experience section
        html_parts.append('<section class="cv-section cv-experience">')
        html_parts.append('<h2 class="cv-section-header" id="work-experience">Work Experience</h2>')
        html_parts.append('')
        
        # Process content line by line
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Company header
            company_match = self.patterns['experience']['company'].match(line)
            if company_match:
                company = company_match.group(1)
                company_id = f"cv-exp-{company.lower().replace(' ', '-')}"
                
                html_parts.append(f'<div class="cv-experience-item" id="{company_id}">')
                html_parts.append('<div class="cv-entry-header">')
                html_parts.append(f'  <h3 class="cv-company-name">{company}</h3>')
                
                # Look for location and date on next lines
                if i + 2 < len(lines):
                    location_date_text = lines[i+1] + '\n' + lines[i+2]
                    loc_date_match = self.patterns['experience']['location_date'].search(location_date_text)
                    if loc_date_match:
                        location = loc_date_match.group(1)
                        html_parts.append(f'  <span class="cv-company-location"><em>{location}</em></span>')
                        i += 2  # Skip processed lines
                
                html_parts.append('</div>')
                html_parts.append('')
                
                # Look for position on next line
                if i + 1 < len(lines):
                    i += 1
                    # Skip empty line if present
                    if i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    if i < len(lines):
                        position_match = self.patterns['experience']['position'].match(lines[i])
                        if position_match:
                            position = position_match.group(1)
                            reference = position_match.group(2) if position_match.group(2) else ''
                            
                            html_parts.append('<div class="cv-position-header">')
                            html_parts.append(f'  <p class="cv-position-title"><strong>{position}</strong>')
                            if reference:
                                html_parts.append(f' <span class="cv-reference">· <em>{reference}</em></span>')
                            html_parts.append('</p>')
                            
                            # Add date from previous location_date_match
                            if 'loc_date_match' in locals() and loc_date_match:
                                date = loc_date_match.group(2)
                                html_parts.append(f'  <span class="cv-company-period"><em>{date}</em></span>')
                            
                            html_parts.append('</div>')
                            html_parts.append('')
                
                # Process achievements
                achievements = []
                skills_tags = None
                i += 1
                while i < len(lines):
                    if lines[i].strip() == '':
                        i += 1
                        continue
                    
                    achievement_match = self.patterns['experience']['achievement'].match(lines[i])
                    if achievement_match:
                        achievements.append(achievement_match.group(1))
                        i += 1
                    else:
                        # Check if it's skills tags (italics at end) - save for later
                        if i < len(lines) and lines[i].startswith('_') and lines[i].endswith('_'):
                            skills_tags = lines[i][1:-1]
                            i += 1
                        break
                
                # Add achievements first
                if achievements:
                    html_parts.append('<ul class="cv-achievements">')
                    for achievement in achievements:
                        formatted_achievement = self._process_markdown_formatting(achievement)
                        html_parts.append(f'<li class="cv-achievement">{formatted_achievement}</li>')
                    html_parts.append('</ul>')
                    html_parts.append('')
                
                # Add skills tags after achievements
                if skills_tags:
                    html_parts.append(f'<div class="cv-skills-tags skills-tags">{self._format_skill_tags(skills_tags)}</div>')
                    html_parts.append('')
                
                html_parts.append('</div>')
                continue
            
            i += 1
        
        html_parts.append('</section>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_projects(self, content: str) -> str:
        """Transform projects markdown into semantic HTML"""
        html_parts = []
        
        # Extract section title
        section_match = self.patterns['section']['any_section'].search(content)
        section_title = section_match.group(1) if section_match else 'Other Projects'
        
        # Start projects section
        html_parts.append('<section class="cv-section cv-projects">')
        html_parts.append(f'<h2 class="cv-section-header" id="projects">{section_title}</h2>')
        html_parts.append('')
        
        # Process projects line by line
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Project name (### Project Name)
            project_match = self.patterns['projects']['project_name'].match(line)
            if project_match:
                project_name = project_match.group(1)
                project_id = f"cv-project-{project_name.lower().replace(' ', '-').replace('(', '').replace(')', '')}"
                
                html_parts.append(f'<div class="cv-project-item" id="{project_id}">')
                
                # Look for date on next line (_Date_)
                i += 1
                date = None
                if i < len(lines) and lines[i].strip().startswith('_') and lines[i].strip().endswith('_'):
                    date = lines[i].strip()[1:-1]  # Remove underscores
                    i += 1
                
                # Create project header with right-aligned date (similar to experience)
                html_parts.append('<div class="cv-entry-header">')
                html_parts.append(f'  <h3 class="cv-project-name">{project_name}</h3>')
                if date:
                    html_parts.append(f'  <span class="cv-project-period"><em>{date}</em></span>')
                html_parts.append('</div>')
                html_parts.append('')
                
                # Skip empty line after date
                if i < len(lines) and lines[i].strip() == '':
                    i += 1
                
                # Look for links line ([Link1](url) | [Link2](url))
                if i < len(lines) and ('[' in lines[i] and '](' in lines[i]):
                    links_line = lines[i].strip()
                    if links_line:
                        # Process links
                        link_parts = []
                        # Find all [text](url) patterns
                        import re
                        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
                        matches = re.findall(link_pattern, links_line)
                        for text, url in matches:
                            if text.lower() == 'github':
                                link_parts.append(f'<a href="{url}" class="cv-project-link cv-github-link">{text}</a>')
                            elif text.lower() == 'demo':
                                link_parts.append(f'<a href="{url}" class="cv-project-link cv-demo-link">{text}</a>')
                            else:
                                link_parts.append(f'<a href="{url}" class="cv-project-link cv-website-link">{text}</a>')
                        
                        if link_parts:
                            html_parts.append(f'<p class="cv-project-links">{" | ".join(link_parts)}</p>')
                    i += 1
                
                # Skip empty line
                if i < len(lines) and lines[i].strip() == '':
                    i += 1
                
                # Process descriptions (- Description text)
                descriptions = []
                while i < len(lines):
                    line = lines[i].strip()
                    if not line:
                        i += 1
                        continue
                    
                    if line.startswith('- '):
                        description = line[2:]  # Remove '- '
                        descriptions.append(description)
                        i += 1
                    else:
                        break
                
                if descriptions:
                    html_parts.append('<ul class="cv-project-descriptions">')
                    for desc in descriptions:
                        formatted_desc = self._process_markdown_formatting(desc)
                        html_parts.append(f'<li class="cv-project-description">{formatted_desc}</li>')
                    html_parts.append('</ul>')
                
                # Look for skills tags (_Skills, Tags_)
                if i < len(lines) and lines[i].strip().startswith('_') and lines[i].strip().endswith('_'):
                    skills = lines[i].strip()[1:-1]  # Remove underscores
                    formatted_tags = self._format_skill_tags(skills)
                    html_parts.append(f'<div class="cv-skills-tags skills-tags">{formatted_tags}</div>')
                    i += 1
                
                html_parts.append('</div>')
                html_parts.append('')
                continue
            
            i += 1
        
        html_parts.append('</section>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_education(self, content: str) -> str:
        """Transform education markdown into semantic HTML"""
        html_parts = []
        
        # Start education section
        html_parts.append('<section class="cv-section cv-education">')
        html_parts.append('<h2 class="cv-section-header" id="education">Education</h2>')
        html_parts.append('')
        
        # Process education entries line by line
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Institution (### Institution Name)
            inst_match = self.patterns['education']['institution'].match(line)
            if inst_match:
                institution = inst_match.group(1)
                inst_id = f"cv-edu-{institution.lower().replace(' ', '-').replace('.', '')[:20]}"
                
                html_parts.append(f'<div class="cv-education-item" id="{inst_id}">')
                
                # Create entry header (like experience format)
                html_parts.append('<div class="cv-entry-header">')
                html_parts.append(f'  <h3 class="cv-institution-name">{institution}</h3>')
                
                i += 1
                
                # Look for location on next line (_Location_<br>)
                if i < len(lines) and lines[i].strip().startswith('_') and '<br>' in lines[i]:
                    location_line = lines[i].strip()
                    location = location_line.replace('_', '').replace('<br>', '')
                    html_parts.append(f'  <span class="cv-education-location"><em>{location}</em></span>')
                    i += 1
                
                html_parts.append('</div>')
                html_parts.append('')
                
                # Look for date on next line (_Date_)
                if i < len(lines) and lines[i].strip().startswith('_') and lines[i].strip().endswith('_'):
                    date = lines[i].strip()[1:-1]  # Remove underscores
                    
                    # Create position header with date alignment (like experience)
                    html_parts.append('<div class="cv-position-header">')
                    
                    # Skip empty line and look for degree
                    i += 1
                    if i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    if i < len(lines) and lines[i].strip().startswith('**'):
                        degree_line = lines[i].strip()
                        degree = degree_line.replace('**', '')  # Remove bold markers
                        html_parts.append(f'  <p class="cv-degree-title"><strong>{degree}</strong></p>')
                        i += 1
                        
                    html_parts.append(f'  <span class="cv-education-period"><em>{date}</em></span>')
                    html_parts.append('</div>')
                    html_parts.append('')
                    
                    # Add technical highlight below the header (if exists)
                    if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('###'):
                        highlight = lines[i].strip()
                        html_parts.append(f'<div class="cv-education-highlight">{highlight}</div>')
                        html_parts.append('')
                
                html_parts.append('</div>')
                html_parts.append('')
                continue
            
            i += 1
        
        html_parts.append('</section>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _enrich_generic_section(self, content: str) -> str:
        """Enrich a generic section that doesn't match specific patterns"""
        # For now, just wrap in a section
        section_match = self.patterns['section']['any_section'].search(content)
        if section_match:
            title = section_match.group(1)
            section_id = title.lower().replace(' ', '-')
            
            return f'<section class="cv-section cv-{section_id}">\n{content}\n</section>\n'
        
        return content
    
    def _enrich_certifications(self, content: str) -> str:
        """Transform certifications markdown into semantic HTML"""
        html_parts = []
        
        # Start certifications section
        html_parts.append('<section class="cv-section cv-certifications">')
        html_parts.append('<h2 class="cv-section-header" id="training-certifications">Training & Certifications</h2>')
        html_parts.append('')
        
        # Process certifications line by line
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Certification name (### Certification Name)
            cert_match = self.patterns['certifications']['cert_name'].match(line)
            if cert_match:
                cert_name = cert_match.group(1)
                cert_id = f"cv-cert-{cert_name.lower().replace(' ', '-').replace('/', '-')[:20]}"
                
                html_parts.append(f'<div class="cv-certification-item" id="{cert_id}">')
                
                # Create certification header (similar to experience/education format)
                html_parts.append('<div class="cv-entry-header">')
                html_parts.append(f'  <h3 class="cv-certification-name">{cert_name}</h3>')
                
                i += 1
                
                # Look for organization and year on next line
                if i < len(lines) and ('_' in lines[i]):
                    org_year_line = lines[i].strip()
                    org_year_match = self.patterns['certifications']['org_year'].match(org_year_line)
                    if org_year_match:
                        organization = org_year_match.group(1)
                        year = org_year_match.group(2) if org_year_match.group(2) else ''
                        
                        if organization:
                            html_parts.append(f'  <span class="cv-certification-org"><em>{organization}</em></span>')
                        if year:
                            html_parts.append(f'  <span class="cv-certification-year"><em>{year}</em></span>')
                        i += 1
                
                html_parts.append('</div>')
                html_parts.append('')
                
                # Look for description
                if i < len(lines) and lines[i].strip() == '':
                    i += 1  # Skip empty line
                
                if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('###'):
                    description = lines[i].strip()
                    formatted_desc = self._process_markdown_formatting(description)
                    html_parts.append(f'<div class="cv-certification-description">')
                    html_parts.append(f'  <p class="cv-certification-desc-text">{formatted_desc}</p>')
                    html_parts.append('</div>')
                    html_parts.append('')
                    i += 1
                
                html_parts.append('</div>')
                html_parts.append('')
                continue
            
            i += 1
        
        html_parts.append('</section>')
        html_parts.append('')
        
        return '\n'.join(html_parts)
    
    def _format_skill_tags(self, skills: str) -> str:
        """Format comma-separated skills into span tags"""
        skill_list = [s.strip() for s in skills.split(',')]
        formatted_tags = []
        
        for skill in skill_list:
            formatted_tags.append(f'<span class="cv-skill-tag skill-tag">{skill}</span>')
        
        return '\n'.join(formatted_tags)
    
    def _process_markdown_formatting(self, text: str) -> str:
        """Convert markdown formatting to HTML"""
        # Bold text (**text** -> <strong>text</strong>)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Italic text (*text* -> <em>text</em>)
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
        
        # Code spans (`code` -> <code>code</code>)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        return text
    
    def _process_project_links(self, text: str) -> str:
        """Process project links in italic format"""
        # Convert _[text](url)_ to <em><a href="url">text</a></em>
        pattern = r'_\[([^\]]+)\]\(([^\)]+)\)_'
        replacement = r'<em><a href="\2">\1</a></em>'
        return re.sub(pattern, replacement, text)
    
    def _wrap_main_content(self, content: str) -> str:
        """Wrap content properly - header separate from main content"""
        # Split content into header and sections
        lines = content.split('\n')
        header_content = []
        main_content = []
        in_header = True
        
        for line in lines:
            if line.startswith('<div class="cv-header">'):
                in_header = True
                header_content.append(line)
            elif line.startswith('</div>') and in_header and len([l for l in header_content if '<div class="cv-header">' in l]) > 0:
                header_content.append(line)
                in_header = False
            elif in_header:
                header_content.append(line)
            else:
                main_content.append(line)
        
        # Join header and main content properly
        header_html = '\n'.join(header_content)
        main_html = '\n'.join(main_content).strip()
        
        if main_html:
            return f'{header_html}\n\n<div class="cv-main-content">\n{main_html}\n</div>'
        else:
            return header_html