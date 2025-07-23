#!/usr/bin/env python3
"""
Arthur Passuello CV Build System
Converts YAML content to markdown with conditional logic preserving LaTeX system behavior
"""

import yaml
import json
import re
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
            "firmware": {
                "toggles": ["firmware", "technical", "detailed"],
                "tagline": "Senior Firmware Engineer | Software Architect | Technical Project Lead",
                "max_priority": 3,
                "show_metrics": True,
                "show_business_impact": False,
                "executive_summary": False,
                "layout": "technical",
            },
            "ai": {
                "toggles": ["ai", "technical", "detailed"],
                "tagline": "Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Lead",
                "max_priority": 3,
                "show_metrics": True,
                "show_business_impact": False,
                "executive_summary": False,
                "layout": "technical",
            },
            "consulting": {
                "toggles": ["consulting", "ai", "businessfocus", "quantified"],
                "tagline": "Senior Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead",
                "max_priority": 3,
                "show_metrics": True,
                "show_business_impact": True,
                "executive_summary": False,
                "layout": "technical",
            },
            "executive": {
                "toggles": ["executive", "quantified", "onepage"],
                "tagline": "Senior Technical Leader | Cross-functional Engineering Manager",
                "max_priority": 1,
                "show_metrics": True,
                "show_business_impact": True,
                "executive_summary": True,
                "layout": "executive",
            },
            "general": {
                "toggles": ["firmware", "ai", "general"],
                "tagline": "Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead",
                "max_priority": 2,
                "show_metrics": False,
                "show_business_impact": False,
                "executive_summary": False,
                "layout": "technical",
            },
        }

        # Personal information loaded from YAML
        self.personal = None  # Will be loaded when needed

    def discover_templates(self) -> Dict[str, str]:
        """Discover available templates by scanning templates directory"""
        templates_dir = Path("templates")
        template_map = {}

        if not templates_dir.exists():
            # Fallback to old system if templates directory doesn't exist
            print("COUCOU")
            return {
                "francois": "css_styling_v2.css",
                "professional": "css_styling.css",
                "original": "css_styling_original.css",
            }

        for template_dir in templates_dir.iterdir():
            if template_dir.is_dir():
                template_name = template_dir.name
                print(template_name)
                # Look for common CSS filenames
                css_candidates = ["style.css", "resume.css", "main.css", "theme.css"]

                for css_file in css_candidates:
                    css_path = template_dir / css_file
                    if css_path.exists():
                        template_map[template_name] = str(css_path)
                        break
                else:
                    # Special handling for awesome-cv with nested structure
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

    def check_toggle_condition(self, toggles: List[str], target_version: str) -> bool:
        """Check if toggles are active for target version"""
        version_toggles = self.versions[target_version]["toggles"]
        return any(toggle in version_toggles for toggle in toggles)

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
        """Process skills section with version-specific logic"""
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
                "programming_languages": technical_skills.get(
                    "programming_languages", {}
                ).get(target_version, []),
                "core_technologies": technical_skills.get("core_technologies", {}).get(
                    target_version, []
                ),
                "tools_platforms": technical_skills.get("tools_platforms", {}).get(
                    target_version, []
                ),
                "project_management": technical_skills.get(
                    "project_management", {}
                ).get(target_version, []),
            }

            # Add domain expertise (version-specific)
            domain_expertise = technical_skills.get("domain_expertise", {}).get(
                target_version, {}
            )
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
                "skills_tags": exp.get("skills_tags", {}).get(target_version, ""),
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
                "descriptions": project.get("descriptions", {}).get(target_version, []),
                "skills_tags": project.get("skills_tags", {}).get(target_version, ""),
            }

            filtered_projects.append(processed_project)

        return filtered_projects

    def generate_skills_markdown(self, skills_data: Dict, target_version: str) -> str:
        """Generate skills section markdown with semantic Grid containers"""
        processed_skills = self.process_skills_section(skills_data, target_version)

        if processed_skills["layout"] == "executive":
            # Executive format - 3 streamlined categories with semantic classes
            markdown = '<section class="cv-section cv-skills">\n<h2 class="cv-section-header" id="skills">Skills</h2>\n\n'
            for category, skills in processed_skills["categories"].items():
                formatted_category = category.replace("_", " ").title()
                markdown += f'<div class="cv-skill-category cv-executive-skills"><p class="cv-skill-category-header"><strong>{formatted_category}</strong>: '

                skill_items = []
                for skill in skills:
                    skill_text = skill["skill"]
                    if skill.get("metric"):
                        skill_text += f" ({skill['metric']})"
                    skill_items.append(skill_text)

                markdown += " • ".join(skill_items) + "</p></div>\n\n"

            markdown += "</section>\n\n"
            return markdown
        else:
            # Technical format - 3-column skills table with semantic classes
            markdown = '<section class="cv-section cv-skills">\n<h2 class="cv-section-header" id="skills">Skills</h2>\n\n'

            # Software Engineering category
            col1_items = processed_skills.get(
                "programming_languages", []
            ) + processed_skills.get("core_technologies", [])
            if col1_items:
                markdown += '<div class="cv-skills-table-container">\n'
                markdown += '<table class="cv-skills-table">\n'
                markdown += "<thead>\n"
                markdown += "<tr>\n"
                markdown += '<th class="cv-skills-header"><strong>Software Engineering</strong></th>\n'
                markdown += (
                    '<th class="cv-skills-header"><strong>ML &amp; LLMs</strong></th>\n'
                )
                markdown += (
                    '<th class="cv-skills-header"><strong>Data Science</strong></th>\n'
                )
                markdown += "</tr>\n"
                markdown += "</thead>\n"
                markdown += "<tbody>\n"

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

                # Create table rows
                max_items = max(len(col1_items), len(col2_items), len(col3_items))

                for i in range(max_items):
                    col1 = f"✓ {col1_items[i]}" if i < len(col1_items) else ""
                    col2 = f"✓ {col2_items[i]}" if i < len(col2_items) else ""
                    col3 = f"✓ {col3_items[i]}" if i < len(col3_items) else ""

                    markdown += '<tr class="cv-skills-row">\n'
                    markdown += f'<td class="cv-skill-item">{col1}</td>\n'
                    markdown += f'<td class="cv-skill-item">{col2}</td>\n'
                    markdown += f'<td class="cv-skill-item">{col3}</td>\n'
                    markdown += "</tr>\n"

                markdown += "</tbody>\n"
                markdown += "</table>\n"
                markdown += "</div>\n\n"

            markdown += "</section>\n\n"
            return markdown

    def generate_experience_markdown(
        self, experience_data: Dict, target_version: str
    ) -> str:
        """
        Generate experience section markdown with semantic HTML structure.

        SEMANTIC CSS ENHANCEMENT:
        This method was enhanced to generate HTML with semantic CSS classes:
        - cv-section-header: Section title with unique ID
        - cv-experience-item: Container for each work experience
        - cv-company-name: Company name styling
        - cv-company-location/cv-company-period: Location and date info
        - cv-position-title: Job title with emphasis
        - cv-reference: Reference contact information
        - cv-achievements/cv-achievement: Achievement list items
        - cv-skills-tags: Container for skill tags

        Args:
            experience_data: Raw experience data from YAML
            target_version: CV version being built (affects content filtering)

        Returns:
            Markdown string with embedded semantic HTML classes
        """
        experiences = self.process_experience_section(experience_data, target_version)

        markdown = '<section class="cv-section cv-experience">\n<h2 class="cv-section-header" id="work-experience">Work Experience</h2>\n\n'

        for exp in experiences:
            markdown += f'<div class="cv-experience-item" id="cv-exp-{exp["company"].lower().replace(" ", "-")}">\n'
            # Create two-line header structure for proper François layout
            markdown += f'<div class="cv-entry-header">\n'
            markdown += f'  <h3 class="cv-company-name">{exp["company"]}</h3>\n'
            markdown += f'  <span class="cv-company-location"><em>{exp["location"]}</em></span>\n'
            markdown += f"</div>\n\n"

            # Create position header with date alignment
            markdown += f'<div class="cv-position-header">\n'
            markdown += (
                f'  <p class="cv-position-title"><strong>{exp["position"]}</strong>'
            )
            if exp["reference"]:
                markdown += f' <span class="cv-reference">{exp["reference"]}</span>'
            markdown += f"</p>\n"
            markdown += (
                f'  <span class="cv-company-period"><em>{exp["period"]}</em></span>\n'
            )
            markdown += f"</div>\n\n"

            # Add achievements
            if exp["achievements"]:
                markdown += '<ul class="cv-achievements">\n'
                for achievement in exp["achievements"]:
                    achievement_text = self.convert_markdown_to_html(
                        achievement["text"]
                    )
                    markdown += f'<li class="cv-achievement">{achievement_text}</li>\n'
                markdown += "</ul>\n\n"

            # Add skills tags if available
            if exp["skills_tags"]:
                formatted_tags = self.format_skill_tags(exp["skills_tags"])
                markdown += (
                    f'<div class="cv-skills-tags skills-tags">{formatted_tags}</div>\n'
                )

            markdown += "</div>\n\n"

        markdown += "</section>\n\n"
        return markdown

    def generate_projects_markdown(
        self, projects_data: Dict, target_version: str
    ) -> str:
        """
        Generate projects section markdown with semantic HTML structure.

        SEMANTIC CSS ENHANCEMENT:
        This method generates HTML with semantic CSS classes for project elements:
        - cv-project-item: Container for each project with unique ID
        - cv-project-name: Project title styling
        - cv-project-period: Project timeline
        - cv-project-links: Container for project links (GitHub, Demo, etc.)
        - cv-project-link: Individual link styling with semantic classes
        - cv-project-descriptions/cv-project-description: Project description lists

        Args:
            projects_data: Raw projects data from YAML
            target_version: CV version being built (affects content filtering)

        Returns:
            Markdown string with embedded semantic HTML classes, or empty string if no projects
        """
        projects = self.process_projects_section(projects_data, target_version)

        if not projects:
            return ""

        markdown = '<section class="cv-section cv-projects">\n<h2 class="cv-section-header" id="projects">Projects</h2>\n\n'

        for project in projects:
            safe_project_id = (
                project["name"]
                .lower()
                .replace(" ", "-")
                .replace("'", "")
                .replace('"', "")
            )
            markdown += (
                f'<div class="cv-project-item" id="cv-proj-{safe_project_id}">\n'
            )
            markdown += f'<h3 class="cv-project-name">{project["name"]} <span class="cv-project-period"><em>{project["period"]}</em></span></h3>\n\n'

            # Add links
            if project["links"]:
                link_parts = []
                for link_type, url in project["links"].items():
                    if link_type == "github":
                        link_parts.append(
                            f'<a href="{url}" class="cv-project-link cv-github-link">Github</a>'
                        )
                    elif link_type == "demo":
                        link_parts.append(
                            f'<a href="{url}" class="cv-project-link cv-demo-link">Demo</a>'
                        )
                    elif link_type == "website":
                        link_parts.append(
                            f'<a href="{url}" class="cv-project-link cv-website-link">Website</a>'
                        )

                if link_parts:
                    markdown += (
                        f'<p class="cv-project-links">{" | ".join(link_parts)}</p>\n\n'
                    )

            # Add descriptions
            if project["descriptions"]:
                markdown += '<ul class="cv-project-descriptions">\n'
                for desc in project["descriptions"]:
                    desc_text = self.convert_markdown_to_html(desc)
                    markdown += f'<li class="cv-project-description">{desc_text}</li>\n'
                markdown += "</ul>\n\n"

            # Add skills tags if available
            if project["skills_tags"]:
                formatted_tags = self.format_skill_tags(project["skills_tags"])
                markdown += (
                    f'<div class="cv-skills-tags skills-tags">{formatted_tags}</div>\n'
                )

            markdown += "</div>\n\n"

        markdown += "</section>\n\n"
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
                "technical_highlight": education.get("technical_highlight", {}).get(
                    target_version, ""
                ),
                "relevant_coursework": education.get("relevant_coursework", {}).get(
                    target_version, []
                ),
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
        """Generate education section markdown"""
        processed_education = self.process_education_section(
            education_data, target_version
        )

        if not processed_education:
            return ""

        markdown = '<section class="cv-section cv-education">\n<h2 class="cv-section-header" id="education">Education</h2>\n\n'

        for education in processed_education:
            # Institution and degree
            institution_name = (
                education["institution_full"]
                if education["institution_full"]
                else education["institution"]
            )
            safe_institution_id = (
                institution_name.lower()
                .replace(" ", "-")
                .replace("'", "")
                .replace("é", "e")
            )
            markdown += (
                f'<div class="cv-education-item" id="cv-edu-{safe_institution_id}">\n'
            )

            # Create two-line header structure matching experience format
            markdown += f'<div class="cv-entry-header">\n'
            markdown += (
                f'  <h3 class="cv-institution-name">{education["institution"]}</h3>\n'
            )
            markdown += f'  <span class="cv-education-location"><em>{education["location"]}</em></span>\n'
            markdown += f"</div>\n\n"

            # Create degree header with date alignment - MINIMAL CLEAN DESIGN
            markdown += f'<div class="cv-position-header">\n'
            markdown += f'  <p class="cv-degree-title"><strong>{education["degree"]}</strong></p>\n'
            if education["start_date"] and education["end_date"]:
                markdown += f'  <span class="cv-education-period"><em>{education["start_date"]} - {education["end_date"]}</em></span>\n'
            markdown += f"</div>\n\n"

            # Add single technical highlight line (subtle like bullet points but without bullet)
            if education["technical_highlight"]:
                markdown += f'<div class="cv-education-highlight">{education["technical_highlight"]}</div>\n\n'

            markdown += "</div>\n\n"

        markdown += "</section>\n\n"
        return markdown

    def build_version(self, target_version: str) -> None:
        """Build a specific CV version"""
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
        tagline = personal_info.get("taglines", {}).get(
            target_version, version_config["tagline"]
        )

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
        markdown_content = f"""<div class="cv-header">
  <div class="cv-header-info">
    <h1 class="cv-name" id="cv-name"><strong>{personal_info['name']}</strong></h1>
    <h3 class="cv-tagline" id="cv-tagline">{tagline}</h3>
    
    <p class="cv-address" id="cv-address"><em>{personal_info['address']}</em></p>
    
    <div class="cv-contact inline-contact" id="cv-contact">
      <img src="assets/icons/phone.png" class="cv-contact-icon icon" alt="Phone" /> {personal_info['phone']} | 
      <img src="assets/icons/email.png" class="cv-contact-icon icon" alt="Email" /> <a href="mailto:{personal_info['email']}">{personal_info['email']}</a> | 
      <img src="assets/icons/github.png" class="cv-contact-icon icon" alt="GitHub" /> <a href="https://github.com/{personal_info['github']}">{personal_info['github']}</a> | 
      <img src="assets/icons/linkedin.png" class="cv-contact-icon icon" alt="LinkedIn" /> <a href="https://linkedin.com/in/{personal_info['linkedin']}">{personal_info['linkedin_name']}</a>
    </div>
    
    <p class="cv-languages" id="cv-languages"><strong>{personal_info['languages']}</strong></p>
  </div>
  
  <div class="cv-profile-container">
    <img src="{personal_info['profile_photo']}" alt="{personal_info['name']}" class="cv-profile-pic profile-pic" />
  </div>
</div>

<div class="cv-main-content">
{self.generate_skills_markdown(skills_data, target_version)}

{self.generate_experience_markdown(experience_data, target_version)}

{self.generate_projects_markdown(projects_data, target_version)}

{self.generate_education_markdown(education_data, target_version)}
</div>
"""

        # Save markdown file
        output_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
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
        skills_data = self.load_yaml_file("arthur-skills.yaml")
        experience_data = self.load_yaml_file("arthur-experience.yaml")
        projects_data = self.load_yaml_file("arthur-projects.yaml")
        education_data = self.load_yaml_file("arthur-education.yaml")

        # Test personal data loading
        personal_info = self.load_personal_data(target_version)
        print(f"Personal data loaded: {personal_info['name']}")
        tagline = personal_info.get("taglines", {}).get(
            target_version, "No version-specific tagline"
        )
        print(
            f"Version tagline: {tagline[:50]}..."
            if len(tagline) > 50
            else f"Version tagline: {tagline}"
        )

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
        template_map = self.discover_templates()

        css_source = template_map.get(template)
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

    def build_html(self, target_version: str, template: str = "francois") -> None:
        """Build HTML version of CV from markdown"""
        print(f"Building HTML for {target_version} version...")

        # Build markdown first
        self.build_version(target_version)

        # Copy assets for proper PDF generation
        self._copy_assets(target_version, template)

        # Convert markdown to HTML using pandoc
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"

        try:
            cmd = [
                "pandoc",
                str(md_path),
                "-f",
                "html",
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

    def build_pdf(self, target_version: str, template: str = "francois") -> None:
        """Attempt to build PDF version of CV"""
        print(f"Building PDF for {target_version} version...")

        # First ensure HTML exists
        html_path = self.output_dir / target_version / f"arthur-{target_version}.html"
        if not html_path.exists():
            self.build_html(target_version, template)

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

    # Add this method to your CVBuilder class
    def build_html_enhanced(
        self, target_version: str, template: str = "francois"
    ) -> None:
        """Build HTML with enhanced CSS styling"""
        print(f"Building enhanced HTML for {target_version} version...")

        # Build markdown first if it doesn't exist
        md_path = self.output_dir / target_version / f"arthur-{target_version}.md"
        if not md_path.exists():
            self.build_version(target_version)

        # Create output directory
        html_dir = self.output_dir / target_version
        html_dir.mkdir(parents=True, exist_ok=True)

        # Choose template CSS
        template_dir = Path("templates") / template
        if template == "francois":
            css_file = template_dir / "style-enhanced.css"
            if not css_file.exists():
                css_file = template_dir / "style.css"  # Fallback
        else:
            css_file = template_dir / "style.css"

        # Copy assets and CSS
        self._copy_assets(html_dir)

        # Copy enhanced CSS
        if css_file.exists():
            import shutil

            shutil.copy2(css_file, html_dir / "css_styling.css")

        # Generate HTML using pandoc
        html_path = html_dir / f"arthur-{target_version}.html"

        pandoc_cmd = [
            "pandoc",
            str(md_path),
            "-o",
            str(html_path),
            "--standalone",
            "--css",
            "./css_fonts.css",
            "--css",
            "./css_styling.css",
            "--metadata",
            f"title=Arthur Passuello - {target_version.title()} CV",
            "--template",
            (
                "templates/html-template.html"
                if Path("templates/html-template.html").exists()
                else None
            ),
        ]

        # Remove None values
        pandoc_cmd = [arg for arg in pandoc_cmd if arg is not None]

        try:
            result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Enhanced HTML generated: {html_path}")
            else:
                print(f"❌ Pandoc error: {result.stderr}")
        except Exception as e:
            print(f"❌ HTML generation failed: {e}")


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
        choices=["firmware", "ai", "consulting", "executive", "general", "all"],
        default="all",
        help="Version to build (default: all)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Test version logic without building"
    )
    parser.add_argument(
        "--enhanced",
        action="store_true",
        default=True,
        help="Use enhanced CSS templates with improved typography and layout",
    )
    parser.add_argument("--html", action="store_true", help="Generate HTML output")
    parser.add_argument(
        "--pdf", action="store_true", help="Generate PDF output (requires HTML)"
    )
    parser.add_argument(
        "--all-formats",
        action="store_true",
        help="Generate all formats (markdown, HTML, PDF)",
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

    elif args.all_formats:
        if args.version == "all":
            for version in builder.versions.keys():
                builder.build_all_formats(version, template=args.template)
        else:
            builder.build_all_formats(args.version, template=args.template)
    elif args.html:
        if args.version == "all":
            for version in builder.versions.keys():
                builder.build_html(version, template=args.template)
        else:
            builder.build_html(args.version, template=args.template)
    elif args.pdf:
        if args.version == "all":
            for version in builder.versions.keys():
                builder.build_pdf(version, template=args.template)
        else:
            builder.build_pdf(args.version, template=args.template)
    else:
        # Default: build markdown only
        if args.version == "all":
            builder.build_all_versions()
        else:
            builder.build_version(args.version)


if __name__ == "__main__":
    main()
