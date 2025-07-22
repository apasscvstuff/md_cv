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

- `build_system.py` - Main build script and CVBuilder class with multi-engine PDF generation
- `content/arthur-*.yaml` - Content source files (personal, skills, experience, projects, education)
- `css_styling.css` - François Quellec exact design implementation with CSS custom properties
- `css_fonts.css` - Local font declarations (@font-face) for PDF compatibility
- `fonts/` - Local font files (Roboto and Source Sans Pro families)
- `cv.md` - Example François CV showing target format
- `docs/francois-reference.pdf` - Design reference for exact layout reproduction
- `system_readme.md` - Comprehensive documentation

### Font and Asset Structure
```
fonts/                           # Local font files for PDF generation
├── Roboto-Regular.ttf          # Primary font family
├── Roboto-Medium.ttf
├── Roboto-Bold.ttf
├── Roboto-Black.ttf
├── SourceSans3-Regular.ttf     # Secondary font family
├── SourceSans3-Medium.ttf
├── SourceSans3-Semibold.ttf
└── SourceSans3-Bold.ttf

output/{version}/               # Generated output per version
├── arthur-{version}.md         # Markdown source
├── arthur-{version}.html       # HTML with embedded CSS
├── arthur-{version}.pdf        # Final PDF output
├── css_fonts.css               # Copied font declarations
├── css_styling.css             # Copied main styling
├── fonts/                      # Copied font directory
└── assets/                     # Profile image and icons
    ├── profile.jpeg
    └── icons/
        ├── phone.png, email.png
        ├── github.png, linkedin.png
        └── ...
```

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

The system uses a multi-engine approach for PDF generation:
1. **Chrome Headless** (Primary, best CSS support with local fonts)
2. **WeasyPrint** (Backup Python-based, complex setup)
3. **Pandoc with HTML engines** (Backup with wkhtmltopdf/weasyprint/prince)
4. **Pandoc LaTeX** (Fallback, limited CSS support)

### Font System Implementation

**Problem Solved**: Original system used Google Fonts CDN which failed in PDF generation, causing fallback to Helvetica.

**Solution**: Local font loading system with proper CSS integration:

1. **Font Download and Storage**:
   ```bash
   fonts/
   ├── Roboto-Regular.ttf, Roboto-Medium.ttf, Roboto-Bold.ttf, Roboto-Black.ttf
   └── SourceSans3-Regular.ttf, SourceSans3-Medium.ttf, etc.
   ```

2. **CSS Font Declarations** (`css_fonts.css`):
   ```css
   @font-face {
       font-family: 'Roboto';
       src: local('Roboto-Regular'),
            url('file:///absolute/path/fonts/Roboto-Regular.ttf') format('truetype'),
            url('./fonts/Roboto-Regular.ttf') format('truetype');
       font-weight: 400;
       font-style: normal;
   }
   ```

3. **HTML Generation Integration**:
   - Modified `build_html()` to include both `css_fonts.css` and `css_styling.css`
   - Updated `_copy_assets()` to copy fonts directory to each version output
   - Pandoc command: `--css ./css_fonts.css --css ./css_styling.css`

### François Quellec Design Implementation

**Objective**: Reproduce exact François Quellec CV layout from reference PDF.

**Analysis Process**:
1. Analyzed `docs/francois-reference.pdf` and `cv.md` for design patterns
2. Identified key design elements: typography, colors, spacing, layout
3. Researched Awesome CV LaTeX template design principles

**Key Design Elements Implemented**:

1. **Color Scheme**:
   ```css
   --color-accent: #e53e3e;        /* Vibrant red for accents */
   --color-primary: #1a202c;       /* Dark blue-gray for headers */
   --color-secondary: #2c3e50;     /* Medium blue-gray */
   --color-text: #2d3748;          /* Main text color */
   ```

2. **Typography Scale**:
   ```css
   --size-name: 28pt;              /* Main title */
   --size-tagline: 13pt;           /* Subtitle */
   --size-section: 16pt;           /* Section headers */
   --size-body: 10pt;              /* Body text */
   ```

3. **Professional Layout Features**:
   - CSS custom properties for consistent theming
   - Profile picture: 100px circular, top-right float
   - Section headers: Red accent with bottom border, uppercase
   - François date format: `->_Location_<br>_Date_`
   - Skills: 3-column table with checkmark bullets
   - Achievement bullets: Red accent dots
   - Print optimization with @page rules

**Technical Implementation**:

1. **Created `css_styling_v2.css`** with exact François design
2. **Replaced original CSS** while keeping backup
3. **Used CSS custom properties** for maintainable theming
4. **Implemented responsive design** with print-specific optimizations

### Current PDF Workflow
```bash
# Recommended workflow (fully automated)
python build_system.py --pdf all          # Generate all PDF versions
python build_system.py --html firmware    # HTML-only for browser testing
python build_system.py --all-formats ai   # Complete build pipeline
```

### PDF Quality Verification
The system now generates PDFs with:
- ✅ Correct fonts: Roboto-Bold (titles), SourceSans3-Regular (body)
- ✅ Proper font sizes: 24pt titles, appropriate scaling
- ✅ Professional color scheme with #e53e3e accents
- ✅ François-inspired layout with optimal spacing
- ✅ Print-ready A4 format with proper margins

## Testing Strategy

The system includes comprehensive testing for:
- Version configuration validation
- Skills processing (3-column vs executive layout)
- Experience filtering by version and priority
- Project inclusion logic
- Markdown generation and formatting
- HTML generation with CSS styling
- PDF generation fallback methods