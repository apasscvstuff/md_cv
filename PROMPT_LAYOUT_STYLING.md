# CV Layout and Styling Modification Session Prompt

## Context and Objectives
You are helping modify the layout and styling of a markdown-based CV generation system. The system generates 5 different CV versions (firmware, ai, consulting, executive, general) from YAML content files and applies François Quellec-inspired CSS styling.

## System Overview
- **Core Files**: `build_system.py` (main build script), `css_styling.css` (web display), `css_styling_print.css` (PDF generation)
- **Output**: HTML and PDF versions using WeasyPrint for high-quality PDF generation
- **Current Design**: Professional, clean design with red accent color (#dc3545), optimized typography, and proper spacing
- **Icon System**: 12x12px optimized contact icons (GitHub, LinkedIn, phone, email) from professional icon libraries

## Prerequisites - Start Every Session With These Steps

### 1. System Analysis
- [ ] Run `python build_system.py --test firmware` to understand current system state
- [ ] Examine current CSS files (`css_styling.css` and `css_styling_print.css`) to understand styling approach
- [ ] Review `CLAUDE.md` for system documentation and build commands
- [ ] Check `output/firmware/arthur-firmware.html` and `output/firmware/arthur-firmware.pdf` to see current visual state

### 2. Backup Current State
- [ ] Create backup copies of CSS files before making changes:
  ```bash
  cp css_styling.css css_styling_backup_$(date +%Y%m%d).css
  cp css_styling_print.css css_styling_print_backup_$(date +%Y%m%d).css
  ```

## Available Layout Modification Tasks

### Typography & Visual Hierarchy
- **Font modifications**: Change font families, sizes, weights, line heights
- **Color scheme updates**: Modify accent colors, text colors, background colors
- **Spacing adjustments**: Margins, padding, section spacing, line spacing
- **Header styling**: Name prominence, tagline formatting, contact information layout

### Section Layout Changes
- **Skills section**: Modify 3-column technical layout vs executive streamlined format
- **Experience section**: Achievement bullet formatting, company/role prominence
- **Projects section**: Description layout, link styling, skills tags display
- **Contact information**: Icon positioning, alignment, spacing

### Page Layout & Structure
- **Responsive design**: Ensure proper display across different screen sizes
- **Print optimization**: Page breaks, margins, headers/footers for PDF generation
- **Grid systems**: Section alignment, column layouts, content flow
- **White space management**: Visual breathing room, content density

### Advanced Styling Features
- **CSS animations**: Subtle hover effects, transitions (web only)
- **Print-specific styles**: Different formatting for PDF vs web display
- **Accessibility improvements**: Color contrast, readable fonts, proper sizing
- **Brand consistency**: Maintaining professional appearance across versions

## Workflow and Best Practices

### 1. Iterative Development Process
```bash
# Test changes incrementally
python build_system.py --html firmware    # Generate HTML first
python build_system.py --pdf firmware     # Then generate PDF
# Review in browser and PDF viewer before continuing
```

### 2. CSS Architecture
- **Web styles** (`css_styling.css`): Interactive elements, hover effects, responsive design
- **Print styles** (`css_styling_print.css`): PDF-optimized layout, page breaks, print margins
- **Shared elements**: Maintain consistency between web and print versions

### 3. Testing Protocol
- [ ] Test changes on all 5 CV versions (firmware, ai, consulting, executive, general)
- [ ] Verify both HTML and PDF outputs look correct
- [ ] Check responsive behavior at different screen sizes (web only)
- [ ] Ensure print styles work properly with WeasyPrint

### 4. Version-Specific Considerations
- **Executive version**: 1-page limit, streamlined skills format, leadership focus
- **Technical versions** (firmware/ai): 3-column skills table, technical metrics
- **Business versions** (consulting/general): Business impact emphasis, stakeholder language

## Common Styling Tasks & Implementations

### Color Scheme Modification
```css
/* Primary accent color */
:root {
    --accent-color: #dc3545;  /* Current red */
    --text-primary: #333;
    --text-secondary: #666;
}

/* Update throughout stylesheets */
h2 { border-bottom: 2px solid var(--accent-color); }
.inline-contact a { color: var(--accent-color); }
```

### Typography Updates
```css
/* Font stack modification */
body {
    font-family: 'Your-Font', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
}

/* Hierarchy adjustments */
h1 { font-size: 22pt; font-weight: 700; }
h2 { font-size: 16pt; font-weight: 600; }
h3 { font-size: 13pt; font-weight: 600; }
```

### Layout Structure Changes
```css
/* Skills table modifications */
.skills-table { 
    column-gap: 2em; 
    margin-bottom: 20px; 
}

/* Experience section spacing */
.experience-item {
    margin-bottom: 25px;
    page-break-inside: avoid;
}
```

## Troubleshooting Common Issues

### PDF Generation Problems
- **WeasyPrint errors**: Check CSS syntax, ensure assets are accessible
- **Font rendering**: Use web-safe fonts or include @font-face declarations
- **Page breaks**: Use `page-break-inside: avoid` for keeping content together

### Layout Inconsistencies
- **Cross-version differences**: Check version-specific logic in `build_system.py`
- **Web vs PDF differences**: Ensure print CSS properly overrides web CSS
- **Responsive issues**: Test at different viewport sizes

### Icon and Asset Issues
- **Missing icons**: Verify assets are copied to output directories
- **Icon sizing**: Adjust CSS `.icon` class dimensions (currently 10-14px)
- **Path issues**: Ensure relative paths work in both web and PDF contexts

## Research and Inspiration Sources

### When Seeking Design Inspiration
- [ ] Search for "professional resume CSS templates 2024" for modern trends
- [ ] Look up "academic CV design" for formal layouts
- [ ] Research "executive resume layouts" for leadership-focused designs
- [ ] Check "François Quellec CV" for maintaining design inspiration continuity

### Typography and Color Research
- [ ] Use WebSearch for "professional resume color schemes 2024"
- [ ] Research accessibility guidelines: "WCAG color contrast requirements"
- [ ] Look up font pairing recommendations for professional documents

### CSS Framework Research
- [ ] Search for "CSS Grid resume layouts" for modern grid systems
- [ ] Look up "print CSS best practices" for PDF optimization
- [ ] Research "WeasyPrint CSS support" for compatible styling techniques

## Success Criteria
- [ ] All 5 CV versions build successfully with new styling
- [ ] PDF output maintains high visual quality and professional appearance
- [ ] Layout remains responsive and accessible
- [ ] Design maintains François Quellec aesthetic while incorporating improvements
- [ ] Version-specific formatting (executive vs technical) works correctly
- [ ] Print pagination and page breaks work properly in PDF output

## Final Validation Steps
```bash
# Build all versions
python build_system.py --all-formats all

# Validate output quality
ls -la output/*/arthur-*.pdf  # Check all PDFs were generated
ls -la output/*/arthur-*.html # Check all HTML files exist

# Manual review checklist
# - Open each PDF and verify visual appearance
# - Check HTML versions in browser at different screen sizes
# - Verify icons and assets display correctly
# - Confirm version-specific differences are maintained
```

Remember: Always prioritize readability and professionalism over decorative elements. The CV system is designed for serious professional use in firmware engineering, AI/ML, consulting, and executive contexts.