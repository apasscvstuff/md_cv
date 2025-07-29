#!/usr/bin/env python3
"""
Arthur Passuello CV Build System
Converts YAML content to markdown with conditional logic preserving LaTeX system behavior
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import argparse

# Add dynamic skills processor with fallback
try:
    from dynamic_skills_processor import DynamicSkillsProcessor
    DYNAMIC_SKILLS_AVAILABLE = True
except ImportError:
    DYNAMIC_SKILLS_AVAILABLE = False
    print("Warning: Dynamic skills processor not available, using legacy mode")


class CVBuilder:
    def __init__(self, content_dir: str = "content", output_dir: str = "output"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)

        # Load version configuration from YAML
        self.versions = self._load_version_config()

        # Personal information loaded from YAML
        self.personal = None  # Will be loaded when needed
        
        # Template configuration
        self.available_templates = self.discover_templates()

    def _load_version_config(self) -> Dict[str, Any]:
        """Load version configuration from YAML file"""
        try:
            version_config = self.load_yaml_file("versions.yaml")
            if "versions" not in version_config:
                raise ValueError("versions.yaml must contain 'versions' key")
            
            versions = version_config["versions"]
            
            # Validate each version has required fields
            required_fields = ["tagline", "toggles", "max_priority", "layout"]
            for version_name, config in versions.items():
                missing_fields = [field for field in required_fields if field not in config]
                if missing_fields:
                    raise ValueError(
                        f"Version '{version_name}' missing required fields: {missing_fields}"
                    )
            
            return versions
            
        except Exception as e:
            print(f"Error loading version configuration: {e}")
            print("Falling back to minimal default configuration")
            # Minimal fallback to allow system to function
            return {
                "general": {
                    "name": "General",
                    "tagline": "Software Engineer",
                    "toggles": ["general"],
                    "max_priority": 3,
                    "layout": "technical",
                    "show_metrics": False,
                    "show_business_impact": False,
                    "executive_summary": False,
                }
            }

    def discover_templates(self) -> Dict[str, str]:
        """Discover available CSS templates for François-style markdown pipeline"""
        templates_dir = Path("templates")
        template_map = {}

        if not templates_dir.exists():
            return {}

        for template_dir in templates_dir.iterdir():
            if template_dir.is_dir():
                template_name = template_dir.name
                
                # Look for CSS file
                css_candidates = ["style.css", "resume.css", "main.css", "theme.css"]
                for css_file in css_candidates:
                    css_path = template_dir / css_file
                    if css_path.exists():
                        template_map[template_name] = str(css_path)
                        break
                else:
                    # Special handling for awesome-cv
                    if template_name == "awesome-cv":
                        awesome_css = template_dir / "src" / "style.css"
                        if awesome_css.exists():
                            template_map[template_name] = str(awesome_css)

        return template_map


    def get_available_templates(self) -> List[str]:
        """Get list of available template names"""
        return list(self.discover_templates().keys())

    def check_dependencies(self) -> Dict[str, bool]:
        """Check availability of PDF generation dependencies"""
        deps = {
            "pandoc": False,
            "chrome": False,
            "weasyprint_cmd": False,
            "weasyprint_python": False,
        }

        # Check pandoc
        try:
            subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
            deps["pandoc"] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Check Chrome/Chromium
        chrome_commands = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "google-chrome",
            "chromium",
            "google-chrome-stable",
        ]
        for chrome_cmd in chrome_commands:
            try:
                if chrome_cmd.startswith("/"):
                    if Path(chrome_cmd).exists():
                        deps["chrome"] = True
                        break
                else:
                    subprocess.run(
                        [chrome_cmd, "--version"], capture_output=True, check=True
                    )
                    deps["chrome"] = True
                    break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        # Check WeasyPrint command line
        try:
            env = subprocess.os.environ.copy()
            env["PKG_CONFIG_PATH"] = (
                "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig"
            )
            env["DYLD_LIBRARY_PATH"] = (
                "/opt/homebrew/lib:/opt/homebrew/Cellar/glib/2.84.3/lib"
            )
            subprocess.run(
                ["weasyprint", "--help"], capture_output=True, check=True, env=env
            )
            deps["weasyprint_cmd"] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Check WeasyPrint Python module
        try:
            import os

            old_env = {}
            env_vars = {
                "PKG_CONFIG_PATH": "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig",
                "DYLD_LIBRARY_PATH": "/opt/homebrew/lib:/opt/homebrew/Cellar/glib/2.84.3/lib",
            }
            for key, value in env_vars.items():
                old_env[key] = os.environ.get(key)
                os.environ[key] = value

            try:
                import weasyprint

                deps["weasyprint_python"] = True
            finally:
                for key, old_value in old_env.items():
                    if old_value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = old_value
        except ImportError:
            pass

        return deps

    def print_dependency_status(self) -> None:
        """Print status of all dependencies"""
        deps = self.check_dependencies()

        print("📋 PDF Generation Dependencies Status:")
        print(f"  Pandoc: {'✅' if deps['pandoc'] else '❌'}")
        print(f"  Chrome/Chromium: {'✅' if deps['chrome'] else '❌'}")
        print(f"  WeasyPrint (command): {'✅' if deps['weasyprint_cmd'] else '❌'}")
        print(f"  WeasyPrint (Python): {'✅' if deps['weasyprint_python'] else '❌'}")

        if not any(deps.values()):
            print("\n⚠️  No PDF generation tools available!")
            print("   Install at least one: Chrome, WeasyPrint, or Pandoc")
        elif (
            not deps["chrome"]
            and not deps["weasyprint_cmd"]
            and not deps["weasyprint_python"]
        ):
            print("\n⚠️  Only pandoc available - may have limited CSS support")
        else:
            print(f"\n✅ PDF generation available")

    def load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Load YAML file with error handling"""
        file_path = self.content_dir / filename
        try:
            with open(file_path, "r", encoding="utf-8") as f:
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
            personal_data = self.load_yaml_file("arthur-personal.yaml")
            personal_info = personal_data.get("personal", {})

            # Process contact information
            contact = personal_info.get("contact", {})

            # Format languages
            languages = personal_info.get("languages", [])
            languages_formatted = " • ".join(
                [f"{lang['language']} ({lang['proficiency']})" for lang in languages]
            )

            self.personal = {
                "name": personal_info.get("name", {}).get("full", "Arthur PASSUELLO"),
                "phone": contact.get("phone", "+(41) 79 176 24 84"),
                "email": contact.get("email", "apassuello@protonmail.com"),
                "address": contact.get(
                    "formatted",
                    "Chemin du Parc-de-Valency 1, 1004 Lausanne, Switzerland",
                ),
                "github": contact.get("github", "apassuello"),
                "linkedin": contact.get("linkedin", "arthur-passuello"),
                "linkedin_name": personal_info.get("name", {}).get(
                    "full", "Arthur Passuello"
                ),
                "languages": languages_formatted,
                "profile_photo": "assets/profile.jpeg",
                "taglines": personal_info.get("taglines", {}),
                "executive_summaries": personal_info.get("executive_summaries", {}),
                "certifications": personal_info.get("certifications", []),
                "interests": personal_info.get("interests", {}),
            }

        return self.personal

    def check_version_condition(
        self, item_versions: List[str], target_version: str
    ) -> bool:
        """Check if item should be included for target version"""
        if not item_versions:
            return True
        if "all" in item_versions:
            return True
        return target_version in item_versions

    def _get_content_for_version(self, content_dict: Dict, target_version: str) -> Any:
        """Get content supporting both single keys ('ai') and multi-version keys ('ai,ds')"""
        if not content_dict:
            return [] if any(isinstance(v, list) for v in content_dict.values() if content_dict) else ""
        
        for key, value in content_dict.items():
            # Split comma-separated keys and check if target_version is included
            versions_in_key = [v.strip() for v in key.split(',')]
            if target_version in versions_in_key:
                return value
        
        # Return appropriate empty value based on content type
        sample_value = next(iter(content_dict.values())) if content_dict else ""
        return [] if isinstance(sample_value, list) else ""

    def format_skill_tags(self, skills_tags_text: str) -> str:
        """
        Convert comma-separated skill tags to individual HTML elements with dual CSS classes.

        SEMANTIC CSS ENHANCEMENT:
        This method was enhanced to include both semantic CSS classes (cv-skill-tag) and
        legacy classes (skill-tag) for backward compatibility with existing templates.

        Each skill tag now has:
        - cv-skill-tag: Semantic class for consistent styling across templates
        - skill-tag: Legacy class for backward compatibility

        Args:
            skills_tags_text: Comma-separated string of skill tags

        Returns:
            HTML string with <span> elements for each tag, including both semantic
            and legacy CSS classes for maximum template compatibility

        Example:
            Input: "Python, Docker, AWS"
            Output: '<span class="cv-skill-tag skill-tag">Python</span><span class="cv-skill-tag skill-tag">Docker</span><span class="cv-skill-tag skill-tag">AWS</span>'
        """
        if not skills_tags_text:
            return ""

        # Split by comma and create individual span elements with dual CSS classes
        # for semantic styling (cv-skill-tag) and backward compatibility (skill-tag)
        tags = [tag.strip() for tag in skills_tags_text.split(",") if tag.strip()]
        tag_elements = [
            f'<span class="cv-skill-tag skill-tag">{tag}</span>' for tag in tags
        ]

        return "".join(tag_elements)

    def convert_markdown_to_html(self, text: str) -> str:
        """Convert basic Markdown syntax to HTML for pure HTML generation"""
        # Convert **bold** to <strong>bold</strong>
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        # Convert *italic* to <em>italic</em>
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        # Convert _italic_ to <em>italic</em>
        text = re.sub(r"_(.*?)_", r"<em>\1</em>", text)
        return text

    def filter_by_priority(self, items: List[Dict], target_version: str) -> List[Dict]:
        """Filter items by priority level based on version"""
        max_priority = self.versions[target_version]["max_priority"]
        return [item for item in items if item.get("priority", 1) <= max_priority]

    def process_skills_section(self, skills_data: Dict, target_version: str) -> Dict:
        """
        Process skills section with dynamic processor support
        
        Supports both:
        - New dynamic format (skill-centric with zero duplication)
        - Legacy format (version-centric with duplication) for backward compatibility
        """
        
        # Check if using new dynamic format
        if (DYNAMIC_SKILLS_AVAILABLE and 
            'skills' in skills_data and 
            'categories' in skills_data and 
            'version_layouts' in skills_data):
            
            # Use new dynamic processor
            try:
                processor = DynamicSkillsProcessor(skills_data)
                result = processor.process_skills_for_version(target_version)
                
                # Add debug flag if in development mode
                if hasattr(self, 'debug_mode') and self.debug_mode:
                    result['debug_mode'] = True
                
                print(f"✅ Dynamic skills processing: {target_version} -> {result['column_count']} columns")
                return result
                
            except Exception as e:
                print(f"Warning: Dynamic skills processing failed: {e}")
                print("Falling back to legacy processing...")
                return self._process_skills_legacy(skills_data, target_version)
        
        else:
            # Use legacy processing for backward compatibility
            return self._process_skills_legacy(skills_data, target_version)

    def _process_skills_legacy(self, skills_data: Dict, target_version: str) -> Dict:
        """Legacy skills processing (renamed from original process_skills_section)"""
        version_config = self.versions[target_version]

        if version_config["layout"] == "executive":
            # Executive layout - 3 streamlined categories
            return {
                "layout": "executive",
                "categories": skills_data.get("executive", {}),
            }
        else:
            # Technical layout - 3-column format
            technical_skills = skills_data.get("technical", {})
            result = {
                "layout": "technical",
                "programming_languages": self._get_content_for_version(technical_skills.get("programming_languages", {}), target_version),
                "core_technologies": self._get_content_for_version(technical_skills.get("core_technologies", {}), target_version),
                "tools_platforms": self._get_content_for_version(technical_skills.get("tools_platforms", {}), target_version),
                "project_management": self._get_content_for_version(technical_skills.get("project_management", {}), target_version),
            }

            # Add domain expertise (version-specific)
            domain_expertise = self._get_content_for_version(technical_skills.get("domain_expertise", {}), target_version)
            if domain_expertise:
                result["domain_expertise"] = domain_expertise

            # Add medical device section if not consulting
            if target_version != "consulting":
                medical_device = technical_skills.get("medical_device", {})
                if medical_device and target_version not in medical_device.get(
                    "exclude_versions", []
                ):
                    result["medical_device"] = medical_device

            return result

    def process_experience_section(
        self, experience_data: Dict, target_version: str
    ) -> List[Dict]:
        """Process experience section with version-specific logic"""
        version_config = self.versions[target_version]
        experiences = experience_data.get("experiences", [])

        filtered_experiences = []

        for exp in experiences:
            # Check if experience should be included for this version
            if not self.check_version_condition(
                exp.get("versions", []), target_version
            ):
                continue

            # Process experience with version-specific content
            processed_exp = {
                "company": exp["company"],
                "location": exp["location"],
                "period": exp["period"],
                "reference": exp.get("reference", ""),
                "position": exp.get("position_variants", {}).get(
                    target_version, exp.get("position_base", "")
                ),
                "skills_tags": self._get_content_for_version(exp.get("skills_tags", {}), target_version),
                "achievements": [],
            }

            # Filter achievements by version and priority
            achievements = exp.get("achievements", [])
            for achievement in achievements:
                # Check version condition
                if not self.check_version_condition(
                    achievement.get("versions", []), target_version
                ):
                    continue

                # Check priority condition
                if achievement.get("priority", 1) > version_config["max_priority"]:
                    continue

                # Add achievement text
                processed_exp["achievements"].append(
                    {
                        "text": achievement["text"],
                        "type": achievement.get("type", "base"),
                        "priority": achievement.get("priority", 1),
                    }
                )

            if processed_exp["achievements"]:  # Only add if has achievements
                filtered_experiences.append(processed_exp)

        return filtered_experiences

    def process_projects_section(
        self, projects_data: Dict, target_version: str
    ) -> List[Dict]:
        """Process projects section with version-specific logic"""
        version_config = self.versions[target_version]

        # Executive version doesn't show projects
        if version_config.get("layout") == "executive":
            return []

        projects = projects_data.get("projects", [])
        filtered_projects = []

        for project in projects:
            # Check if project should be included for this version
            if not self.check_version_condition(
                project.get("versions", []), target_version
            ):
                continue

            # Process project with version-specific content
            processed_project = {
                "name": project["name"],
                "period": project["period"],
                "links": project.get("links", {}),
                "descriptions": self._get_content_for_version(project.get("descriptions", {}), target_version),
                "skills_tags": self._get_content_for_version(project.get("skills_tags", {}), target_version),
            }

            filtered_projects.append(processed_project)

        return filtered_projects

    def generate_skills_markdown(self, skills_data: Dict, target_version: str) -> str:
        """Generate clean markdown for skills section"""
        processed_skills = self.process_skills_section(skills_data, target_version)

        if processed_skills["layout"] == "executive":
            # Executive format - clean paragraph style
            markdown = "## Skills\n\n"
            for category, skills in processed_skills["categories"].items():
                formatted_category = category.replace("_", " ").title()
                
                skill_items = []
                for skill in skills:
                    skill_text = skill["skill"]
                    if skill.get("metric"):
                        skill_text += f" ({skill['metric']})"
                    skill_items.append(skill_text)

                markdown += f"**{formatted_category}**: {' • '.join(skill_items)}\n\n"

            return markdown
            
        elif processed_skills["layout"] == "technical_dynamic":
            # Dynamic format - supports 2-6+ columns automatically
            return self._generate_dynamic_skills_markdown_clean(processed_skills, target_version)
            
        else:
            # Technical format - clean markdown table
            markdown = "## Skills\n\n"

            # Software Engineering category
            col1_items = processed_skills.get(
                "programming_languages", []
            ) + processed_skills.get("core_technologies", [])
            
            # Domain expertise (AI & LLMs)
            col2_items = []
            domain_exp = processed_skills.get("domain_expertise", {})
            if domain_exp:
                col2_items.extend(domain_exp.get("skills", []))
                col2_items.extend(domain_exp.get("secondary_skills", []))

            # Tools and platforms (Data Science)
            col3_items = processed_skills.get(
                "tools_platforms", []
            ) + processed_skills.get("project_management", [])

            if col1_items or col2_items or col3_items:
                # Generate table header
                markdown += "| **Software Engineering** | **ML & LLMs** | **Data Science** |\n"
                markdown += "| :----------------------- | :------------ | :--------------- |\n"
                
                # Create table rows
                max_items = max(len(col1_items), len(col2_items), len(col3_items))

                for i in range(max_items):
                    col1 = f"✓ {col1_items[i]}" if i < len(col1_items) else ""
                    col2 = f"✓ {col2_items[i]}" if i < len(col2_items) else ""
                    col3 = f"✓ {col3_items[i]}" if i < len(col3_items) else ""

                    markdown += f"| {col1} | {col2} | {col3} |\n"

            return markdown + "\n"

    def _generate_dynamic_skills_markdown(self, processed_skills: Dict, target_version: str) -> str:
        """Generate dynamic skills markdown with 2-6+ column support"""
        markdown = '<section class="cv-section cv-skills">\n<h2 class="cv-section-header" id="skills">Skills</h2>\n\n'
        
        categories = processed_skills.get("categories", [])
        column_count = processed_skills.get("column_count", len(categories))
        column_width = processed_skills.get("column_width", f"{100/column_count:.2f}%")
        
        if categories and column_count <= 6:
            # Table layout for 2-6 columns
            markdown += '<div class="cv-skills-table-container">\n'
            markdown += f'<table class="cv-skills-table cv-skills-dynamic" data-columns="{column_count}">\n'
            markdown += "<thead>\n<tr>\n"
            
            # Generate headers
            for category in categories:
                markdown += f'<th class="cv-skills-header" style="width: {column_width};"><strong>{category["name"]}</strong></th>\n'
            
            markdown += "</tr>\n</thead>\n<tbody>\n"
            
            # Calculate maximum number of skills across all categories
            max_skills = max(len(category["skills"]) for category in categories) if categories else 0
            
            # Generate rows dynamically based on max skills
            for i in range(max_skills):
                markdown += '<tr class="cv-skills-row">\n'
                for category in categories:
                    if i < len(category["skills"]):
                        skill = category["skills"][i]
                        markdown += f'<td class="cv-skill-item"><span class="cv-skill-bullet">✓</span> {skill}</td>\n'
                    else:
                        markdown += '<td class="cv-skill-item"></td>\n'
                markdown += "</tr>\n"
            
            markdown += "</tbody>\n</table>\n</div>\n\n"
            
            # Add responsive CSS for dynamic columns
            markdown += self._generate_dynamic_skills_css(column_count, column_width)
            
        elif categories and column_count > 6:
            # List layout for 7+ columns (too many for table)
            markdown += '<div class="cv-skills-list-container">\n'
            for category in categories:
                markdown += f'<div class="cv-skill-category">\n'
                markdown += f'<h3 class="cv-skill-category-header">{category["name"]}</h3>\n'
                markdown += '<div class="cv-skill-items">\n'
                for skill in category["skills"]:
                    markdown += f'<span class="cv-skill-tag">{skill}</span>\n'
                markdown += '</div>\n</div>\n'
            markdown += '</div>\n\n'
            
            # Add list layout CSS
            markdown += self._generate_list_skills_css()
        else:
            # Fallback when no categories are available
            markdown += f'''<div class="cv-skills-notice">
    <p class="cv-notice-text">
        <em>Skills configuration not available for {target_version} version.</em>
    </p>
</div>

'''
        
        markdown += "</section>\n\n"
        return markdown

    def _generate_dynamic_skills_css(self, column_count: int, column_width: str) -> str:
        """Generate responsive CSS for dynamic skills table"""
        css = f'''<style>
/* Dynamic Skills CSS */
.cv-skills-dynamic {{
    table-layout: fixed;
    width: 100%;
    border-collapse: collapse;
}}

.cv-skills-dynamic th,
.cv-skills-dynamic td {{
    width: {column_width};
    overflow-wrap: break-word;
    vertical-align: top;
    padding: 0.3rem 0.5rem;
}}

.cv-skills-dynamic th {{
    background-color: var(--color-accent, #e53e3e);
    color: white;
    font-weight: bold;
    text-align: center;
}}

.cv-skill-bullet {{
    color: var(--color-accent, #e53e3e);
    font-weight: bold;
    margin-right: 0.3rem;
}}

'''

        # Add responsive font sizing based on column count
        if column_count >= 5:
            css += '''/* 5+ columns: smaller font for better fit */
@media print {
    .cv-skills-dynamic {
        font-size: 8pt;
    }
    .cv-skill-item {
        font-size: 7pt;
    }
}

@media screen {
    .cv-skills-dynamic {
        font-size: 0.8rem;
    }
    .cv-skill-item {
        font-size: 0.75rem;
    }
}

'''
        elif column_count == 4:
            css += '''/* 4 columns: medium font */
@media print {
    .cv-skills-dynamic {
        font-size: 9pt;
    }
    .cv-skill-item {
        font-size: 8pt;
    }
}

@media screen {
    .cv-skills-dynamic {
        font-size: 0.85rem;
    }
    .cv-skill-item {
        font-size: 0.8rem;
    }
}

'''
        else:  # 2-3 columns
            css += '''/* 2-3 columns: normal font */
@media print {
    .cv-skills-dynamic {
        font-size: 10pt;
    }
    .cv-skill-item {
        font-size: 9pt;
    }
}

'''
        
        css += '''</style>

'''
        return css

    def _generate_list_skills_css(self) -> str:
        """Generate CSS for list layout (7+ columns)"""
        return '''<style>
/* List layout styling (for 7+ columns) */
.cv-skills-list-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.cv-skill-category {
    margin-bottom: 1rem;
}

.cv-skill-category-header {
    font-size: 1rem;
    font-weight: bold;
    color: var(--color-accent, #e53e3e);
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--color-accent, #e53e3e);
    padding-bottom: 0.2rem;
}

.cv-skill-items {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
}

.cv-skill-tag {
    background-color: var(--color-light-gray, #f5f5f5);
    color: var(--color-text, #2d3748);
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8rem;
    border: 1px solid var(--color-border, #e2e8f0);
}

@media print {
    .cv-skill-tag {
        background-color: transparent;
        border: 1px solid #ccc;
    }
}
</style>

'''

    def _generate_dynamic_skills_markdown_clean(self, processed_skills: Dict, target_version: str) -> str:
        """Generate clean markdown for dynamic skills (2-6+ columns)"""
        markdown = "## Skills\n\n"
        
        categories = processed_skills.get("categories", [])
        column_count = processed_skills.get("column_count", len(categories))
        
        if categories and column_count <= 6:
            # Table layout for 2-6 columns
            # Generate table header
            headers = [f"**{cat['name']}**" for cat in categories]
            markdown += "| " + " | ".join(headers) + " |\n"
            markdown += "| " + " | ".join([":--" for _ in headers]) + " |\n"
            
            # Calculate maximum number of skills across all categories
            max_skills = max(len(category["skills"]) for category in categories) if categories else 0
            
            # Generate rows
            for i in range(max_skills):
                row = []
                for category in categories:
                    if i < len(category["skills"]):
                        skill = category["skills"][i]
                        # Handle different skill formats
                        if isinstance(skill, dict):
                            skill_name = skill.get('name', skill.get('skill', str(skill)))
                        else:
                            skill_name = str(skill)
                        row.append(f"✓ {skill_name}")
                    else:
                        row.append("")
                markdown += "| " + " | ".join(row) + " |\n"
            
        elif categories and column_count > 6:
            # For 7+ columns, use a different format (categories as paragraphs)
            for category in categories:
                markdown += f"**{category['name']}**: "
                skills = []
                for skill in category["skills"]:
                    if isinstance(skill, dict):
                        skill_name = skill.get('name', skill.get('skill', str(skill)))
                    else:
                        skill_name = str(skill)
                    skills.append(skill_name)
                markdown += " • ".join(skills) + "\n\n"
        else:
            # Fallback when no categories are available
            markdown += f"*Skills configuration not available for {target_version} version.*\n"
        
        return markdown + "\n"

    def generate_executive_summary_markdown(self, personal_data: Dict, target_version: str) -> str:
        """
        Generate clean markdown for executive summary section.
        
        Args:
            personal_data: Personal data from YAML including executive summaries
            target_version: CV version being built (affects content selection)
            
        Returns:
            Clean markdown string with executive summary section, or empty string if not applicable
        """
        version_config = self.versions[target_version]
        
        # Check if this version should show executive summary
        if not version_config.get("show_executive_summary", False):
            return ""
        
        # Get version-specific executive summary
        executive_summaries = personal_data.get("executive_summaries", {})
        summary = executive_summaries.get(target_version, "")
        
        if not summary:
            return ""
        
        # Return just the summary text without section header (styled as italic text)
        return f"_{summary}_\n\n"

    def generate_experience_markdown(
        self, experience_data: Dict, target_version: str
    ) -> str:
        """
        Generate clean markdown for experience section.
        
        Args:
            experience_data: Raw experience data from YAML
            target_version: CV version being built (affects content filtering)

        Returns:
            Clean markdown string following the pattern:
            ### Company
            _Location_<br>
            _Date Range_
            
            **Position** · _Reference_
            
            * Achievement 1
            * Achievement 2
            
            _Skills, Tags, Here_
        """
        experiences = self.process_experience_section(experience_data, target_version)

        markdown = "## Work Experience\n\n"

        for exp in experiences:
            # Company header with location/date
            markdown += f"### {exp['company']}\n"
            markdown += f"_{exp['location']}_<br>\n"
            markdown += f"_{exp['period']}_\n\n"
            
            # Position with optional reference
            position = f"**{exp['position']}**"
            if exp.get('reference'):
                position += f" · _{exp['reference']}_"
            markdown += f"{position}\n\n"
            
            # Achievements as bullet list
            if exp['achievements']:
                for achievement in exp['achievements']:
                    markdown += f"* {achievement['text']}\n"
                markdown += "\n"
            
            # Skills tags as italic text
            if exp.get('skills_tags'):
                markdown += f"_{exp['skills_tags']}_\n\n"

        return markdown

    def generate_projects_markdown(
        self, projects_data: Dict, target_version: str
    ) -> str:
        """
        Generate clean markdown for projects section.

        Args:
            projects_data: Raw projects data from YAML
            target_version: CV version being built (affects content filtering)

        Returns:
            Clean markdown string, or empty string if no projects
        """
        projects = self.process_projects_section(projects_data, target_version)

        if not projects:
            return ""

        markdown = "## Projects\n\n"

        for project in projects:
            # Project name with period
            markdown += f"### {project['name']}\n"
            markdown += f"_{project['period']}_\n\n"

            # Add links if available
            if project.get("links"):
                link_parts = []
                for link_type, url in project["links"].items():
                    if link_type == "github":
                        link_parts.append(f"[Github]({url})")
                    elif link_type == "demo":
                        link_parts.append(f"[Demo]({url})")
                    elif link_type == "website":
                        link_parts.append(f"[Website]({url})")
                
                if link_parts:
                    markdown += " | ".join(link_parts) + "\n\n"

            # Add descriptions as bullet points
            if project.get("descriptions"):
                for desc in project["descriptions"]:
                    markdown += f"- {desc}\n"
                markdown += "\n"

            # Add skills tags if available
            if project.get("skills_tags"):
                markdown += f"_{project['skills_tags']}_\n\n"

        return markdown

    def process_education_section(
        self, education_data: Dict, target_version: str
    ) -> List[Dict]:
        """Process education section with version-specific filtering"""
        if "education" not in education_data:
            return []

        education_items = education_data["education"]
        filtered_education = []

        for education in education_items:
            # Process version-specific content
            processed_education = {
                "institution": education.get("institution", ""),
                "institution_full": education.get("institution_full", ""),
                "degree": education.get("degree", ""),
                "field_of_study": education.get("field_of_study", ""),
                "major": education.get("major", ""),
                "start_date": education.get("start_date", ""),
                "end_date": education.get("end_date", ""),
                "location": education.get("location", ""),
                "technical_highlight": self._get_content_for_version(education.get("technical_highlight", {}), target_version),
                "relevant_coursework": self._get_content_for_version(education.get("relevant_coursework", {}), target_version),
                "achievements": [],
            }

            # Filter achievements by version (notable_achievements)
            for achievement in education.get("notable_achievements", []):
                achievement_versions = achievement.get("versions", [])
                if self.check_version_condition(achievement_versions, target_version):
                    processed_education["achievements"].append(
                        achievement["achievement"]
                    )

            # Filter practical experience by version
            for experience in education.get("practical_experience", []):
                experience_versions = experience.get("versions", [])
                if self.check_version_condition(experience_versions, target_version):
                    processed_education["achievements"].append(experience["experience"])

            filtered_education.append(processed_education)

        return filtered_education

    def generate_education_markdown(
        self, education_data: Dict, target_version: str
    ) -> str:
        """Generate clean markdown for education section"""
        processed_education = self.process_education_section(
            education_data, target_version
        )

        if not processed_education:
            return ""

        markdown = "## Education\n\n"

        for education in processed_education:
            # Institution header
            markdown += f"### {education['institution']}\n"
            markdown += f"_{education['location']}_<br>\n"
            
            # Date range
            if education["start_date"] and education["end_date"]:
                markdown += f"_{education['start_date']} - {education['end_date']}_\n\n"
            
            # Degree
            markdown += f"**{education['degree']}**\n"
            
            # Technical highlight if available
            if education.get("technical_highlight"):
                markdown += f"{education['technical_highlight']}\n"
            
            markdown += "\n"

        return markdown

    def process_certifications_section(self, personal_data: Dict, target_version: str) -> List[Dict]:
        """Process certifications section with version-specific filtering"""
        version_config = self.versions[target_version]
        certifications = personal_data.get("certifications", [])
        
        if not certifications:
            return []
        
        filtered_certifications = []
        
        for cert in certifications:
            # Check if certification should be included for this version
            if not self.check_version_condition(cert.get("versions", []), target_version):
                continue
            
            # Check priority condition  
            if cert.get("priority", 1) > version_config["max_priority"]:
                continue
            
            # Process certification with all metadata
            processed_cert = {
                "name": cert.get("name", ""),
                "type": cert.get("type", ""),
                "issuing_organization": cert.get("issuing_organization", ""),
                "year": cert.get("year"),
                "description": cert.get("description", ""),
                "priority": cert.get("priority", 1)
            }
            
            filtered_certifications.append(processed_cert)
        
        # Sort by priority (1=highest) then by year (newest first)
        filtered_certifications.sort(key=lambda x: (x["priority"], -(x["year"] or 0)))
        
        return filtered_certifications

    def generate_certifications_markdown(self, personal_data: Dict, target_version: str) -> str:
        """
        Generate clean markdown for certifications section.
        
        Args:
            personal_data: Personal data from YAML including certifications
            target_version: CV version being built (affects content filtering)
            
        Returns:
            Clean markdown string with certifications, or empty string if none
        """
        version_config = self.versions[target_version]
        
        # Check if this version should show certifications
        if not version_config.get("show_certifications", False):
            return ""
        
        processed_certifications = self.process_certifications_section(personal_data, target_version)
        
        if not processed_certifications:
            return ""
        
        markdown = "## Training & Certifications\n\n"
        
        for cert in processed_certifications:
            # Certification name
            markdown += f"### {cert['name']}\n"
            
            # Organization and year
            org_year_parts = []
            if cert["issuing_organization"]:
                org_year_parts.append(f"_{cert['issuing_organization']}_")
            if cert["year"]:
                org_year_parts.append(f"_{cert['year']}_")
            
            if org_year_parts:
                markdown += " | ".join(org_year_parts) + "\n\n"
            
            # Description if available
            if cert["description"]:
                markdown += f"{cert['description']}\n\n"
        
        return markdown

    def build_version(self, target_version: str, template_name: str = "francois") -> None:
        """Build a specific CV version using François-style markdown generation"""
        self._build_markdown(target_version)

    def _build_markdown(self, target_version: str) -> None:
        """Generate markdown with embedded semantic HTML (François method)"""
        print(f"Building {target_version} version...")

        # Load content files
        skills_data = self.load_yaml_file("arthur-skills.yaml")
        experience_data = self.load_yaml_file("arthur-experience.yaml")
        projects_data = self.load_yaml_file("arthur-projects.yaml")
        education_data = self.load_yaml_file("arthur-education.yaml")

        # Load personal data with version-specific content
        personal_info = self.load_personal_data(target_version)

        # Get version configuration and tagline
        version_config = self.versions[target_version]
        tagline = self._get_content_for_version(personal_info.get("taglines", {}), target_version) or version_config["tagline"]

        # =====================================================================
        # SEMANTIC HTML GENERATION - Enhanced CV Structure
        #
        # This section generates HTML with semantic CSS classes for reliable,
        # maintainable styling across all templates. Each CV element now has:
        # 1. Semantic class (cv-*) for reliable targeting
        # 2. Legacy class for backward compatibility
        # 3. Semantic ID for unique element identification
        #
        # Benefits:
        # - Eliminates fragile CSS selectors like h1+h3+p
        # - Enables consistent styling across templates
        # - Maintains backward compatibility with existing CSS
        # - Provides semantic structure for accessibility
        # =====================================================================

        # Build semantic HTML structure for CSS Grid (guide.md method)
        markdown_content = f"""![{personal_info['name']}]({personal_info['profile_photo']})

# **{personal_info['name']}**
### {tagline}

_{personal_info['address']}_

📞 {personal_info['phone']} | ✉️ [{personal_info['email']}](mailto:{personal_info['email']}) | 🔗 [GitHub](https://github.com/{personal_info['github']}) | 💼 [LinkedIn](https://linkedin.com/in/{personal_info['linkedin']})

**{personal_info['languages']}**
{self.generate_executive_summary_markdown(personal_info, target_version)}
{self.generate_skills_markdown(skills_data, target_version)}

{self.generate_experience_markdown(experience_data, target_version)}

{self.generate_projects_markdown(projects_data, target_version)}

{self.generate_education_markdown(education_data, target_version)}

{self.generate_certifications_markdown(personal_info, target_version)}
"""

        # Save markdown file
        output_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✅ {target_version} version built successfully")
        print(f"📄 Output: {output_path}")

    def build_all_versions(self, template_name: str = "francois") -> None:
        """Build all CV versions using markdown generation"""
        print("Building all CV versions...")

        for version in self.versions.keys():
            self.build_version(version, template_name)

        print("🎉 All versions built successfully!")

    def test_version(self, target_version: str) -> None:
        """Test a specific version for content validation"""
        print(f"Testing {target_version} version...")

        # Load content and test logic
        skills_data = self.load_yaml_file("arthur-skills.yaml")
        experience_data = self.load_yaml_file("arthur-experience.yaml")
        projects_data = self.load_yaml_file("arthur-projects.yaml")
        education_data = self.load_yaml_file("arthur-education.yaml")

        # Test personal data loading
        personal_info = self.load_personal_data(target_version)
        print(f"Personal data loaded: {personal_info['name']}")
        
        # Get tagline from version config
        version_config = self.versions.get(target_version)
        if version_config:
            tagline = version_config.get("tagline", "No tagline configured")
            print(
                f"Version tagline: {tagline[:50]}..."
                if len(tagline) > 50
                else f"Version tagline: {tagline}"
            )
        else:
            print(f"Version '{target_version}' not found in configuration")

        # Test skills processing
        processed_skills = self.process_skills_section(skills_data, target_version)
        print(f"Skills layout: {processed_skills.get('layout', 'unknown')}")

        # Test experience processing
        processed_exp = self.process_experience_section(experience_data, target_version)
        print(f"Experience items: {len(processed_exp)}")

        # Test projects processing
        processed_projects = self.process_projects_section(
            projects_data, target_version
        )
        print(f"Projects: {len(processed_projects)}")

        # Test education processing
        processed_education = self.process_education_section(
            education_data, target_version
        )
        print(f"Education items: {len(processed_education)}")

        print(f"✅ {target_version} version tested successfully")

    def _copy_assets(self, target_version: str, template: str = "francois") -> None:
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

        # Copy CSS files - use template discovery system
        css_source = self.available_templates.get(template)
        css_dest = self.output_dir / target_version / "css_styling.css"
        fonts_dest = self.output_dir / target_version / "css_fonts.css"

        # Copy main CSS - use selected template
        if css_source and Path(css_source).exists():
            shutil.copy2(css_source, css_dest)
            print(f"Using CSS template: {css_source}")
        else:
            # Fallback to old system
            fallback_files = [
                "css_styling.css",
                "css_styling_v2.css",
                "css_styling_original.css",
            ]
            fallback_used = False
            for fallback in fallback_files:
                if Path(fallback).exists():
                    shutil.copy2(fallback, css_dest)
                    print(
                        f"Warning: Template '{template}' not found, using fallback: {fallback}"
                    )
                    fallback_used = True
                    break

            if not fallback_used:
                print(
                    f"Error: No CSS template found for '{template}' and no fallback available"
                )

        # Copy print CSS if exists
        if Path("css_styling_print.css").exists():
            css_print_dest = self.output_dir / target_version / "css_styling_print.css"
            shutil.copy2("css_styling_print.css", css_print_dest)

        # Copy fonts CSS
        if Path("css_fonts.css").exists():
            shutil.copy2("css_fonts.css", fonts_dest)

        # Copy fonts directory
        fonts_src = Path("fonts")
        if fonts_src.exists():
            fonts_output_dest = self.output_dir / target_version / "fonts"
            if fonts_output_dest.exists():
                shutil.rmtree(fonts_output_dest)
            shutil.copytree(fonts_src, fonts_output_dest)

    def build_html_from_existing(self, target_version: str, template: str = "francois", no_enrich: bool = False) -> None:
        """Build HTML version of CV from existing markdown file (no YAML regeneration)"""
        print(f"Building HTML from existing markdown for {target_version} version...")

        # Check if markdown file exists
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        if not md_path.exists():
            print(f"❌ Markdown file not found: {md_path}")
            print(f"   Run without --from-existing to generate markdown from YAML first")
            return

        # Load existing markdown content
        with open(md_path, 'r', encoding='utf-8') as f:
            clean_markdown = f.read()

        self._process_markdown_to_html(clean_markdown, target_version, template, no_enrich)

    def build_html(self, target_version: str, template: str = "francois", no_enrich: bool = False) -> None:
        """Build HTML version of CV from clean markdown with optional enrichment"""
        print(f"Building HTML for {target_version} version...")

        # Build clean markdown first
        self.build_version(target_version)

        # Load clean markdown content
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        with open(md_path, 'r', encoding='utf-8') as f:
            clean_markdown = f.read()

        self._process_markdown_to_html(clean_markdown, target_version, template, no_enrich)

    def _process_markdown_to_html(self, clean_markdown: str, target_version: str, template: str = "francois", no_enrich: bool = False) -> None:
        """Common HTML processing logic for both build methods"""
        
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"

        if no_enrich:
            # Use clean markdown directly (for debugging)
            print("⚠️ Skipping enrichment - using clean markdown directly")
            input_path = md_path
            pandoc_format = "markdown"
        else:
            # Enrich markdown with HTML structure
            from markdown_enricher import MarkdownEnricher
            enricher = MarkdownEnricher()
            enriched_html = enricher.enrich_markdown(clean_markdown)

            # Save enriched HTML to temporary file
            temp_html_path = md_path.with_suffix('.enriched.html')
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(enriched_html)
            
            input_path = temp_html_path
            pandoc_format = "html"

        # Copy assets for proper PDF generation
        self._copy_assets(target_version, template)

        # Convert to final HTML using pandoc
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"

        try:
            cmd = [
                "pandoc",
                str(input_path),
                "-f",
                pandoc_format,
                "-t",
                "html",
                "--css",
                "./css_fonts.css",  # Local fonts first
                "--css",
                "./css_styling.css",  # Main styling second
                "--standalone",
                "-o",
                str(html_path),
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ HTML generated: {html_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ HTML generation failed: {e}")
        except FileNotFoundError:
            print("❌ pandoc not found. Please install pandoc first.")
        finally:
            # Clean up temporary file if it was created
            if not no_enrich:
                temp_html_path.unlink(missing_ok=True)

    def build_pdf_from_existing(self, target_version: str, template: str = "francois") -> None:
        """Attempt to build PDF version of CV from existing markdown (no YAML regeneration)"""
        print(f"Building PDF from existing markdown for {target_version} version...")

        # First ensure HTML exists, generate from existing markdown if needed
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        if not html_path.exists():
            self.build_html_from_existing(target_version, template)

        self._process_pdf_generation(target_version)

    def build_pdf(self, target_version: str, template: str = "francois") -> None:
        """Attempt to build PDF version of CV"""
        print(f"Building PDF for {target_version} version...")

        # First ensure HTML exists
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        if not html_path.exists():
            self.build_html(target_version, template)

        self._process_pdf_generation(target_version)

    def _process_pdf_generation(self, target_version: str) -> None:
        """Common PDF generation logic for both build methods"""
        
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        pdf_path = self.output_dir / target_version / f"arthur-{target_version}.pdf"

        # Try different PDF generation methods
        methods = [
            self._try_chrome_headless_pdf,
            self._try_weasyprint_pdf,
            self._try_pandoc_pdf,
            self._provide_manual_instructions,
        ]

        for method in methods:
            if method(html_path, pdf_path, target_version):
                break

    def _try_chrome_headless_pdf(
        self, html_path: Path, pdf_path: Path, target_version: str
    ) -> bool:
        """Try generating PDF using Chrome headless mode"""
        chrome_commands = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "google-chrome",
            "chromium",
            "google-chrome-stable",
            "/opt/homebrew/bin/chromium",
            "/usr/local/bin/google-chrome",
        ]

        for chrome_cmd in chrome_commands:
            try:
                # Check if the command exists
                if chrome_cmd.startswith("/"):
                    if not Path(chrome_cmd).exists():
                        continue

                cmd = [
                    chrome_cmd,
                    "--headless=new",  # Use new headless mode
                    "--disable-gpu",
                    "--disable-dev-shm-usage",  # Overcome limited resource problems
                    "--no-sandbox",  # Bypass OS security model
                    "--disable-background-timer-throttling",
                    "--disable-renderer-backgrounding",
                    "--disable-backgrounding-occluded-windows",
                    "--print-to-pdf=" + str(pdf_path),
                    "--print-to-pdf-no-header",  # Remove headers/footers
                    "--no-pdf-header-footer",  # Additional header/footer suppression
                    "--hide-scrollbars",  # Clean appearance
                    "--run-all-compositor-stages-before-draw",
                    "file://" + str(html_path.absolute()),
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0 and pdf_path.exists():
                    print(f"✅ PDF generated with Chrome headless: {pdf_path}")
                    return True
                else:
                    print(f"Chrome failed with {chrome_cmd}: {result.stderr}")

            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Chrome error with {chrome_cmd}: {e}")
                continue

        print("Chrome headless not available")
        return False

    def _try_weasyprint_pdf(
        self, html_path: Path, pdf_path: Path, target_version: str
    ) -> bool:
        """Try generating PDF using weasyprint with local fonts and print-optimized CSS"""
        try:
            # Set up environment for WeasyPrint
            import os

            old_env = {}

            # Set required environment variables
            env_vars = {
                "PKG_CONFIG_PATH": "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig",
                "DYLD_LIBRARY_PATH": "/opt/homebrew/lib:/opt/homebrew/Cellar/glib/2.84.3/lib",
            }

            for key, value in env_vars.items():
                old_env[key] = os.environ.get(key)
                os.environ[key] = value

            try:
                from weasyprint import HTML, CSS
                from weasyprint.text.fonts import FontConfiguration

                # Create font configuration with local fonts
                font_config = FontConfiguration()

                # Use the HTML file directly with print CSS
                css_print_path = html_path.parent / "css_styling_print.css"
                if not css_print_path.exists():
                    css_print_path = html_path.parent / "css_styling.css"

                # Load CSS files
                css_files = []
                if css_print_path.exists():
                    css_files.append(
                        CSS(filename=str(css_print_path), font_config=font_config)
                    )

                # Generate PDF with font configuration
                html_doc = HTML(filename=str(html_path))
                html_doc.write_pdf(
                    str(pdf_path), stylesheets=css_files, font_config=font_config
                )

                print(f"✅ PDF generated with weasyprint: {pdf_path}")
                return True

            finally:
                # Restore environment variables
                for key, old_value in old_env.items():
                    if old_value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = old_value

        except ImportError:
            print(
                "WeasyPrint Python library not available, falling back to command line"
            )
            return self._try_weasyprint_command_line(
                html_path, pdf_path, target_version
            )
        except Exception as e:
            print(f"WeasyPrint Python API failed: {e}")
            return self._try_weasyprint_command_line(
                html_path, pdf_path, target_version
            )

    def _try_weasyprint_command_line(
        self, html_path: Path, pdf_path: Path, target_version: str
    ) -> bool:
        """Fallback to WeasyPrint command line"""
        try:
            # Set up environment for WeasyPrint
            env = subprocess.os.environ.copy()
            env["PKG_CONFIG_PATH"] = (
                "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig"
            )
            env["DYLD_LIBRARY_PATH"] = (
                "/opt/homebrew/lib:/opt/homebrew/Cellar/glib/2.84.3/lib:"
                + env.get("DYLD_LIBRARY_PATH", "")
            )

            cmd = ["weasyprint", str(html_path), str(pdf_path)]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60, env=env
            )

            if result.returncode == 0:
                print(f"✅ PDF generated with weasyprint command line: {pdf_path}")
                return True
            else:
                print(f"WeasyPrint command line failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"WeasyPrint command line failed: {e}")
            return False

    def _try_pandoc_pdf(
        self, html_path: Path, pdf_path: Path, target_version: str
    ) -> bool:
        """Try generating PDF using pandoc with HTML-native engines"""

        # Try different PDF engines that preserve HTML/CSS
        pdf_engines = ["weasyprint", "wkhtmltopdf", "prince", "pagedjs-cli"]

        for engine in pdf_engines:
            try:
                cmd = [
                    "pandoc",
                    str(html_path),
                    "-f",
                    "html",
                    "-t",
                    "pdf",
                    "--pdf-engine",
                    engine,
                    "-o",
                    str(pdf_path),
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    print(f"✅ PDF generated with pandoc using {engine}: {pdf_path}")
                    return True
                else:
                    print(f"Pandoc with {engine} failed: {result.stderr}")

            except FileNotFoundError:
                print(f"PDF engine {engine} not found")
                continue
            except Exception as e:
                print(f"Pandoc with {engine} failed: {e}")
                continue

        # Fallback to default LaTeX engine
        try:
            cmd = [
                "pandoc",
                str(html_path),
                "-f",
                "html",
                "-t",
                "pdf",
                "-o",
                str(pdf_path),
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ PDF generated with pandoc (LaTeX fallback): {pdf_path}")
            return True
        except Exception as e:
            print(f"Pandoc LaTeX fallback failed: {e}")
            return False

    def _provide_manual_instructions(
        self, html_path: Path, pdf_path: Path, target_version: str
    ) -> bool:
        """Provide manual PDF generation instructions"""
        print(
            f"""
📋 Manual PDF generation required for {target_version} version:

1. Open this file in your browser: {html_path}
2. Press Cmd+P (Mac) or Ctrl+P (Windows/Linux)
3. Choose 'Save as PDF' or 'Print to PDF'
4. Save as: {pdf_path}

The HTML file is ready with proper CSS styling.
You can also use browser extensions or online converters.
        """
        )
        return True

    def build_all_formats(
        self, target_version: str, template: str = "francois"
    ) -> None:
        """Build all formats (markdown, HTML, PDF) for a version"""
        print(f"Building all formats for {target_version} version...")
        self.build_version(target_version)  # Markdown
        self.build_html(target_version, template)  # HTML
        self.build_pdf(target_version, template)  # PDF



def main():
    # Create a temporary builder to discover templates for argparse choices
    temp_builder = CVBuilder()
    available_templates = temp_builder.get_available_templates()
    print(available_templates)
    default_template = (
        "francois"
        if "francois" in available_templates
        else (available_templates[0] if available_templates else "francois")
    )

    parser = argparse.ArgumentParser(description="Build Arthur Passuello CV versions")
    parser.add_argument(
        "version",
        nargs="?",
        choices=["firmware", "ai", "consulting", "executive", "general", "ds", "all"],
        default="all",
        help="Version to build (default: all)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Test version logic without building"
    )
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML output (requires clean markdown)"
    )
    parser.add_argument(
        "--pdf", action="store_true", help="Generate PDF output (generates HTML automatically)"
    )
    parser.add_argument(
        "--check-deps", action="store_true", help="Check PDF generation dependencies"
    )
    parser.add_argument(
        "--content-dir", default="content", help="Content directory path"
    )
    parser.add_argument("--output-dir", default="output", help="Output directory path")
    parser.add_argument(
        "--template",
        choices=available_templates,
        default=default_template,
        help=f'CSS template to use. Available: {", ".join(available_templates)}',
    )
    parser.add_argument(
        "--no-enrich", action="store_true", help="Skip markdown enrichment (for debugging clean markdown)"
    )
    parser.add_argument(
        "--from-existing", action="store_true", help="Generate HTML/PDF from existing markdown (skip YAML regeneration)"
    )

    args = parser.parse_args()

    builder = CVBuilder(args.content_dir, args.output_dir)

    # Standard build commands
    if args.check_deps:
        builder.print_dependency_status()
        return

    if args.test:
        if args.version == "all":
            for version in builder.versions.keys():
                builder.test_version(version)
        else:
            builder.test_version(args.version)
    elif args.html:
        # Build HTML only
        if args.from_existing:
            # Generate HTML from existing markdown files
            if args.version == "all":
                for version in builder.versions.keys():
                    builder.build_html_from_existing(version, template=args.template, no_enrich=args.no_enrich)
            else:
                builder.build_html_from_existing(args.version, template=args.template, no_enrich=args.no_enrich)
        else:
            # Build markdown + HTML
            if args.version == "all":
                for version in builder.versions.keys():
                    builder.build_html(version, template=args.template, no_enrich=args.no_enrich)
            else:
                builder.build_html(args.version, template=args.template, no_enrich=args.no_enrich)
    elif args.pdf:
        # Build PDF
        if args.from_existing:
            # Generate PDF from existing markdown files
            if args.version == "all":
                for version in builder.versions.keys():
                    builder.build_pdf_from_existing(version, template=args.template)
            else:
                builder.build_pdf_from_existing(args.version, template=args.template)
        else:
            # Build markdown + HTML + PDF
            if args.version == "all":
                for version in builder.versions.keys():
                    builder.build_all_formats(version, template=args.template)
            else:
                builder.build_all_formats(args.version, template=args.template)
    else:
        # Default: build markdown only
        if args.version == "all":
            builder.build_all_versions(args.template)
        else:
            builder.build_version(args.version, args.template)


if __name__ == "__main__":
    main()
