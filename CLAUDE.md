# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a markdown-based CV system that generates multiple CV versions from YAML content files. The system preserves sophisticated conditional logic from LaTeX systems while providing the visual appeal of François Quellec's design. It builds 5 different CV versions: Firmware, AI, Consulting, Executive, and General.

## Core Commands

### Building CVs
- `python build_system.py all` - Build all CV versions (markdown only)
- `python build_system.py firmware` - Build specific version (firmware/ai/consulting/executive/general)
- `python scripts/build-cv.py all` - Alternative build script location

### HTML Generation
- `python build_system.py --html all` - Generate HTML for all versions
- `python build_system.py --html firmware` - Generate HTML for specific version

### PDF Generation
- `python build_system.py --pdf all` - Generate PDF for all versions (tries automated then manual)
- `python build_system.py --pdf firmware` - Generate PDF for specific version
- `python build_system.py --all-formats firmware` - Build markdown, HTML, and PDF

### Testing
- `python test_system.py` - Run system tests
- `python scripts/test-cv-system.py` - Alternative test script location
- `python build_system.py --test firmware` - Test version logic without building

### Setup
- `bash setup_script.sh` - Initial project setup
- `pip install pyyaml markdown` - Install dependencies
- `brew install pandoc` - Install pandoc for HTML/PDF generation (macOS)

## Architecture

### Content System
- **YAML Content Files** (`content/`): Personal info, skills, experience, projects, education
- **Version Configuration**: 5 CV versions with different taglines, priorities, and content filters
- **Conditional Logic**: Version-specific content using `versions` arrays and priority levels
- **Priority System**: 1=core (all versions), 2=standard (not executive), 3=detailed (firmware/ai only)

### Build System
- **CVBuilder Class** (`build_system.py`): Core processing engine with version-specific logic
- **Template Processing**: Converts YAML to markdown with conditional filtering
- **Skills Layout**: Executive format vs 3-column technical format
- **Experience Processing**: Version-specific position titles and achievement filtering

### Output Structure
```
output/
├── firmware/     # Embedded systems focused
├── ai/          # ML/AI practitioner focused  
├── consulting/  # Business impact focused
├── executive/   # Leadership focused (1 page)
└── general/     # Balanced technical/business
```

### Version Differences
- **Firmware**: Technical metrics, hardware details, embedded systems focus
- **AI**: ML metrics, research achievements, educational impact
- **Consulting**: ROI metrics, stakeholder management, business value
- **Executive**: Leadership metrics, financial impact, 1-page format
- **General**: Balanced technical and business competencies

## Key Files

- `build_system.py` - Main build script and CVBuilder class
- `content/arthur-*.yaml` - Content source files (personal, skills, experience, projects, education)
- `styles/cv-*.css` - François Quellec inspired styling
- `cv.md` - Example François CV showing target format
- `system_readme.md` - Comprehensive documentation

## Content Structure

### Skills Configuration
- `executive`: Streamlined categories with metrics
- `technical`: 3-column format (Software Engineering | AI & LLMs | Data Science)
- Version-specific skill lists using `target_version` keys

### Experience Configuration
- `versions` array for targeting specific CV versions
- `position_variants` for version-specific job titles
- `achievements` with priority levels and version targeting
- `type` field for achievement categorization (techmetric, leadmetric, businessimpact)

### Projects Configuration
- Version-specific descriptions using `target_version` keys
- Skills tags and links per version
- Executive version excludes projects entirely

## PDF Generation

The system attempts multiple PDF generation methods:
1. **WeasyPrint** (Python-based, best CSS support)
2. **Pandoc** (LaTeX-based, requires LaTeX installation)  
3. **Manual browser print** (fallback with instructions)

### Common PDF Issues
- **WeasyPrint dependencies**: May require `brew install cairo pango gdk-pixbuf libffi`
- **LaTeX Unicode errors**: Use manual browser print for best results
- **Missing assets**: Ensure profile images and icons are in proper paths

### Recommended PDF Workflow
```bash
# Generate HTML first (always works)
python build_system.py --html firmware

# Open HTML in browser and print to PDF manually
# This gives the best visual results with proper CSS styling
```

## Testing Strategy

The system includes comprehensive testing for:
- Version configuration validation
- Skills processing (3-column vs executive layout)
- Experience filtering by version and priority
- Project inclusion logic
- Markdown generation and formatting
- HTML generation with CSS styling
- PDF generation fallback methods