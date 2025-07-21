# 📄 Arthur Passuello CV System

A sophisticated markdown-based CV generation system that creates multiple targeted CV versions from YAML content files. Inspired by François Quellec's elegant design, this system preserves advanced conditional logic while providing modern maintainability.

## 🎯 What This System Does

This system transforms structured YAML content into beautiful, professional CVs in multiple formats:

- **5 Targeted CV Versions**: Firmware, AI, Consulting, Executive, General
- **3 Output Formats**: Markdown, HTML, PDF
- **Conditional Content**: Smart filtering based on audience and priorities
- **Professional Design**: François Quellec-inspired layout with modern typography
- **Version Control Friendly**: All content stored as human-readable YAML

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install pyyaml

# Install pandoc for HTML generation
brew install pandoc  # macOS
# or: sudo apt install pandoc  # Ubuntu/Debian

# Install WeasyPrint dependencies (for best PDF quality)
brew install gobject-introspection cairo pango gdk-pixbuf libffi
```

### Basic Usage

```bash
# Generate all CV versions (markdown only)
python build_system.py all

# Generate HTML versions (recommended)
python build_system.py --html all

# Generate PDF versions (high quality)
python build_system.py --pdf all

# Generate everything (markdown + HTML + PDF)
python build_system.py --all-formats all

# Generate specific version
python build_system.py --all-formats firmware
```

## 📁 System Architecture

### Content Structure

```
content/
├── arthur-personal.yaml     # Personal info, contact details, languages
├── arthur-skills.yaml       # Technical skills with version targeting
├── arthur-experience.yaml   # Work experience with conditional content
├── arthur-projects.yaml     # Projects with version-specific descriptions
└── arthur-education.yaml    # Education and certifications
```

### Output Structure

```
output/
├── firmware/               # Embedded systems focused
├── ai/                    # AI/ML practitioner focused  
├── consulting/            # Business impact focused
├── executive/             # Leadership focused (1-page)
└── general/               # Balanced technical/business
```

Each version directory contains:
- `arthur-{version}.md` - Source markdown
- `arthur-{version}.html` - Styled HTML with assets
- `arthur-{version}.pdf` - High-quality PDF
- `assets/` - Profile image and contact icons
- `css_styling.css` - Web version styling
- `css_styling_print.css` - PDF-optimized styling

## 🔧 How the Conditional Logic Works

### Version Targeting

Content can be targeted to specific CV versions using the `versions` array:

```yaml
# Include only in specific versions
versions: ["firmware", "ai"]

# Include in all versions  
versions: ["all"]

# Exclude from executive (include in others)
versions: ["firmware", "ai", "consulting", "general"]
```

### Priority System

Content is filtered by priority levels:

```yaml
priority: 1  # Core content (shown in ALL versions, including executive)
priority: 2  # Standard details (hidden in executive, shown in others)
priority: 3  # Full details (only in detailed versions: firmware/ai)
```

### Achievement Types

Different achievement types for targeted emphasis:

```yaml
type: "base"              # Standard achievement
type: "techmetric"        # Technical measurement (96% test coverage)
type: "leadmetric"        # Leadership impact (7+ direct reports)
type: "businessimpact"    # Business value (10x performance improvement)
type: "ai_focus"          # AI/ML specific
type: "consulting_focus"  # Client/business focused
```

## 📝 Content Modification Guide

### 1. Personal Information (`arthur-personal.yaml`)

```yaml
personal:
  name: "Arthur PASSUELLO"
  phone: "+(41) 79 176 24 84"
  email: "apassuello@protonmail.com"
  address: "Chemin du Parc-de-Valency 1, 1004 Lausanne, Suisse"
  github: "apassuello"
  linkedin: "arthur-passuello" 
  linkedin_name: "Arthur Passuello"
  languages: "French (native) • English (Professional) • German (B1)"
  profile_photo: "assets/profile.jpeg"
```

**To modify**: Update any field directly. The system will automatically use these values across all CV versions.

### 2. Skills Configuration (`arthur-skills.yaml`)

The skills system supports two layouts:

#### Executive Layout (streamlined)
```yaml
executive:
  leadership_impact:
    - skill: "Technical Team Leadership"
      metric: "7+ Direct Reports"
      type: "leadmetric"
  business_results:
    - skill: "Cost Optimization"  
      metric: "€2M+ Annual Savings"
      type: "businessimpact"
```

#### Technical Layout (3-column table)
```yaml
technical:
  programming_languages:
    firmware: ["C/C++ (Expert)", "Python (Expert)", "VHDL"]
    ai: ["Python (Expert)", "PyTorch", "TensorFlow"]
    consulting: ["Python (Expert)", "SQL", "R"]
  
  core_technologies:
    firmware: ["FreeRTOS", "STM32", "FPGA Development"]
    ai: ["OpenAI/Anthropic APIs", "RAG Systems", "Vector Databases"]
```

**To add new skills**:
1. Add to appropriate category in `technical` section
2. Specify which versions should show each skill
3. For executive version, add to `executive` section with metrics

### 3. Work Experience (`arthur-experience.yaml`)

```yaml
experiences:
  - company: "Tandem Diabetes Care Switzerland"
    location: "Lausanne, Switzerland"
    period: "December 2022 - June 2025"
    versions: ["firmware", "ai", "consulting", "executive", "general"]
    
    # Different job titles per version
    position_variants:
      firmware: "Embedded Software Engineer"
      ai: "Embedded Software Engineer"
      executive: "Senior Technical Lead"
    
    reference: "(Ref. Patrick Segura)"
    
    # Version-specific skill tags
    skills_tags:
      firmware: "C/C++ • FreeRTOS • Medical Devices"
      ai: "Python • ML • System Integration"
    
    achievements:
      # Core achievement (all versions)
      - text: "Led firmware development for Sigi™ insulin pump"
        versions: ["all"]
        priority: 1
        type: "base"
      
      # Technical detail (not in executive)
      - text: "achieving 96% test coverage through HIL system"
        versions: ["firmware", "ai", "consulting", "general"] 
        priority: 2
        type: "techmetric"
      
      # Detailed technical info (only detailed versions)
      - text: "Established test infrastructure for medical-grade firmware verification"
        versions: ["firmware", "ai"]
        priority: 3
        type: "base"
```

**To add new experience**:
1. Copy the structure above
2. Customize `position_variants` for different audiences
3. Use `versions` and `priority` to control content visibility
4. Add relevant `type` for proper emphasis

### 4. Projects (`arthur-projects.yaml`)

```yaml
projects:
  - name: "Technical Documentation RAG System"
    period: "Jan 2025 - Present"
    versions: ["ai", "consulting", "general", "firmware"]
    
    links:
      github: "https://github.com/apassuello/technical-doc-rag/"
      demo: "https://huggingface.co/spaces/ArthyP/technical-rag-assistant"
    
    # Different descriptions per version
    descriptions:
      ai:
        - "Architected RAG platform achieving 99.5% chunk quality"
        - "Implemented hybrid retrieval system (FAISS + BM25)"
      firmware:
        - "Designed RISC-V documentation assistant"
        - "Achieved <100ms response times for embedded queries"
      consulting:
        - "Delivered AI solution reducing manual research by 85%"
        - "Client-ready system with comprehensive documentation"
    
    skills_tags:
      ai: "Python • RAG • Vector Databases"
      firmware: "RISC-V • Real-time Systems"
```

**To add new project**:
1. Define which versions should include it
2. Write version-specific descriptions focusing on relevant aspects
3. Add appropriate links and skills tags

## 🎨 Layout Modification Framework

### CSS Customization System

The system uses two CSS files for different purposes:

#### `css_styling.css` (Web/HTML viewing)
- Full François Quellec design with modern web features
- Perfect for viewing CVs in browsers
- Supports hover effects, smooth scrolling

#### `css_styling_print.css` (PDF generation)
- Print-optimized version for WeasyPrint
- A4 page sizing with proper margins
- Page break control and typography optimization

### Easy Layout Modifications with Claude Code

This system is designed for easy customization using Claude Code. Here's how:

#### 1. **Color Scheme Changes**

Ask Claude Code:
```
"Change the accent color from red (#dc3545) to blue throughout the CV system"
```

Claude will:
- Update both CSS files consistently
- Modify the profile picture border color
- Update link colors and section dividers
- Ensure print and web versions match

#### 2. **Typography Adjustments**

Ask Claude Code:
```
"Make the CV more compact by reducing font sizes and line spacing by 15%"
```

Claude will:
- Proportionally adjust all font sizes in both CSS files
- Maintain visual hierarchy while reducing space usage
- Update print margins for better page utilization

#### 3. **Layout Structure Changes**

Ask Claude Code:
```
"Change the skills table from 3 columns to 2 columns and make the profile picture smaller"
```

Claude will:
- Modify the skills generation logic in `build_system.py`
- Update CSS grid layouts
- Adjust profile picture sizing
- Ensure consistency across all CV versions

#### 4. **Section Reordering**

Ask Claude Code:
```
"Move the Projects section before Work Experience in all versions"
```

Claude will:
- Reorder sections in the markdown generation methods
- Ensure proper spacing and flow
- Maintain conditional logic for all versions

#### 5. **Content Format Changes**

Ask Claude Code:
```
"Add a new 'Certifications' section that appears after Skills but only in technical versions"
```

Claude will:
- Add YAML structure for certifications
- Create processing logic with version conditions
- Generate appropriate markdown formatting
- Update all relevant files consistently

### Custom Modification Instructions

When working with Claude Code on this system, use these patterns:

#### For Content Changes:
```
"Add a new [content type] to the [version(s)] that includes [specific fields]"
"Modify the [section] to emphasize [aspect] for [target audience]"
"Create version-specific content for [section] that shows [different information]"
```

#### For Visual Changes:
```
"Update the visual design to be more [characteristic] by changing [specific elements]"
"Make the PDF version more suitable for [use case] by adjusting [layout aspects]"
"Improve readability for [audience] by modifying [typography/spacing/colors]"
```

#### For System Behavior:
```
"Change the priority system to have [number] levels instead of 3"
"Add a new CV version called '[name]' that focuses on [domain]"
"Modify the asset handling to support [new requirement]"
```

### Advanced Customization Points

The system is designed with these extensible components:

1. **Version Configuration** (`build_system.py` lines 22-68)
   - Easy to add new CV versions
   - Configurable toggles and priorities per version

2. **Content Processing Methods** (lines 114-340)
   - Modular processing for each content section
   - Easy to modify conditional logic

3. **Asset Management** (`_copy_assets` method)
   - Centralized asset handling
   - Easy to extend for new file types

4. **PDF Generation Pipeline** (`build_pdf` method)
   - Multiple fallback methods
   - Easy to add new PDF generators

## 🔧 Technical Implementation Details

### Build System (`build_system.py`)

The core `CVBuilder` class handles:

- **Version Management**: 5 predefined CV versions with unique configurations
- **Content Processing**: YAML → filtered content → Markdown
- **Asset Management**: Copies images, icons, and CSS files to output directories  
- **Multi-format Output**: Markdown → HTML → PDF pipeline
- **Conditional Logic**: Complex filtering based on versions, priorities, and types

### Key Methods:

- `build_version()`: Generates markdown for specific version
- `build_html()`: Converts markdown to styled HTML with assets
- `build_pdf()`: Multi-method PDF generation (WeasyPrint → Pandoc → Manual)
- `process_*_section()`: Version-specific content filtering for each section

### PDF Generation Pipeline:

1. **WeasyPrint** (preferred): Best quality, preserves CSS styling
2. **Chrome Headless**: Browser-based rendering (if available)  
3. **Pandoc**: LaTeX-based fallback
4. **Manual Instructions**: User guidance for browser print-to-PDF

## 🚨 What's Still Missing

### Essential Assets Needed

1. **Professional Profile Photo**
   - Current: Placeholder file (`assets/profile.jpeg.placeholder`)
   - Needed: High-quality headshot (square format, 300x300px minimum)
   - Format: JPEG, optimized for both web and print

2. **Contact Icons**  
   - Current: PNG placeholders in `assets/icons/`
   - Needed: Professional SVG icons for:
     - 📞 Phone: Clean, minimalist phone icon
     - 📧 Email: Modern envelope icon  
     - 🔗 GitHub: GitHub logo (official)
     - 💼 LinkedIn: LinkedIn logo (official)
   - Specifications: 16x16px SVG, consistent style

3. **Brand Consistency**
   - Consider personal branding colors beyond the current red theme
   - Consistent typography choices across all materials

### Content Improvements

1. **Complete Work Experience Details**
   - Add missing achievement metrics and quantifiable results
   - Include more reference contacts where appropriate
   - Add skills tags for better version targeting

2. **Expanded Projects Portfolio**
   - Add more projects with version-specific descriptions
   - Include live demo links and comprehensive documentation
   - Technical metrics and business impact data

3. **Education & Certifications Section**
   - Implement the education YAML structure
   - Add relevant certifications and professional development
   - Include academic projects and research work

### Technical Enhancements

1. **Advanced Layout Options**
   - Multi-column project descriptions
   - Sidebar layouts for executive version
   - Responsive design improvements

2. **Asset Optimization**
   - Automatic image compression and resizing
   - SVG icon support with fallbacks
   - Better print vs. web asset handling

3. **Content Validation**
   - YAML schema validation
   - Content completeness checks
   - Version-specific requirement verification

4. **Enhanced PDF Generation**
   - Custom page headers/footers
   - Better page break handling
   - Watermark support for draft versions

### Integration Possibilities

1. **Version Control Integration**
   - Git hooks for automatic CV generation
   - Change tracking for content updates
   - Branch-based version management

2. **Web Hosting Integration**
   - Automatic deployment of HTML versions
   - CDN integration for fast loading
   - Analytics for CV viewing

3. **Application Integration**
   - API endpoints for dynamic CV generation
   - Database integration for content management
   - Multi-language support system

## 🛠️ Troubleshooting

### Common Issues

#### WeasyPrint Not Working
```bash
# Install system dependencies
brew install gobject-introspection cairo pango gdk-pixbuf libffi

# Check environment
echo $PKG_CONFIG_PATH
echo $DYLD_LIBRARY_PATH
```

#### Assets Not Showing in PDF
- Verify assets exist in `assets/` directory (not just `.placeholder` files)
- Check that `build_html()` was run before `build_pdf()`
- Ensure proper file permissions

#### Content Not Appearing in Expected Version
```yaml
# Check version targeting in YAML
versions: ["firmware", "ai"]  # Make sure target version is included

# Check priority levels
priority: 1  # Executive shows only priority 1
priority: 2  # Hidden in executive, shown in others  
priority: 3  # Only in detailed versions
```

#### PDF Quality Issues
- Use WeasyPrint for best quality: `--pdf` flag
- For manual control: Generate HTML first, then print to PDF in browser
- Check `css_styling_print.css` for print-specific optimizations

### Debug Commands

```bash
# Test content processing without building
python build_system.py --test firmware

# Generate HTML only (always works)
python build_system.py --html all

# Verbose output for troubleshooting
python build_system.py --verbose firmware
```

## 📚 Further Reading

- **YAML Syntax**: [yaml.org](https://yaml.org/spec/1.2/spec.html)
- **WeasyPrint Documentation**: [weasyprint.org](https://weasyprint.org/)
- **Pandoc User Guide**: [pandoc.org](https://pandoc.org/MANUAL.html)
- **François Quellec Design Reference**: See `cv.md` for layout inspiration

---

**Last Updated**: July 2025  
**Version**: 2.0.0  
**Maintainer**: Arthur Passuello

This system is designed to grow with your career. As you gain new experiences and skills, simply update the YAML content files, and the system will automatically generate beautiful, targeted CVs for any opportunity.