# Arthur Passuello CV - Markdown System

A modern, markdown-based CV system that preserves the sophisticated conditional logic of the original LaTeX system while providing the visual appeal of François Quellec's design.

## 🎯 Features

- **5 CV Versions**: Firmware, AI, Consulting, Executive, General
- **Conditional Logic**: Preserves all LaTeX `\whenrole{}` and priority-based logic
- **Modern Design**: François Quellec inspired layout with clean typography
- **Responsive**: Works on web, print, and mobile
- **Maintainable**: Human-readable YAML content files
- **Version Control Friendly**: All files are text-based

## 📁 Project Structure

```
arthur-cv-markdown/
├── content/
│   ├── arthur-personal.yaml      # Personal information
│   ├── arthur-skills.yaml        # Skills with version logic
│   ├── arthur-experience.yaml    # Work experience
│   ├── arthur-projects.yaml      # Projects section
│   └── arthur-education.yaml     # Education & languages
├── assets/
│   ├── profile.jpeg              # Professional photo
│   └── icons/                    # Contact & skill icons
│       ├── phone.png
│       ├── email.png
│       ├── github.png
│       └── linkedin.png
├── styles/
│   ├── cv-base.css              # François Quellec styling
│   ├── cv-print.css             # Print optimizations
│   └── cv-versions.css          # Version-specific styles
├── scripts/
│   ├── build-cv.py              # Main build script
│   └── test-cv-system.py        # Testing framework
└── output/
    ├── firmware/                # Generated firmware CV
    ├── ai/                      # Generated AI CV
    ├── consulting/              # Generated consulting CV
    ├── executive/               # Generated executive CV
    └── general/                 # Generated general CV
```

## 🚀 Quick Start

### 1. Setup

```bash
# Create project directory
mkdir arthur-cv-markdown
cd arthur-cv-markdown

# Run setup script
bash setup-cv-system.sh

# Install dependencies
pip install pyyaml markdown
```

### 2. Add Content

Create and populate the content files:

```bash
# Copy your existing CV content to YAML files
cp arthur-skills.yaml content/
cp arthur-experience.yaml content/
cp arthur-projects.yaml content/
```

### 3. Build CVs

```bash
# Test the system
python scripts/test-cv-system.py

# Build all versions
python scripts/build-cv.py all

# Build specific version
python scripts/build-cv.py firmware
python scripts/build-cv.py ai
python scripts/build-cv.py consulting
python scripts/build-cv.py executive
python scripts/build-cv.py general
```

### 4. View Results

```bash
# Check output files
ls -la output/firmware/
ls -la output/ai/
ls -la output/consulting/
ls -la output/executive/
ls -la output/general/

# Open in browser
open output/firmware/arthur-firmware.html
```

## 📖 Content Structure

### Skills Configuration (arthur-skills.yaml)

```yaml
# Executive version - streamlined for leadership
executive:
  leadership_impact:
    - skill: "Technical Team Leadership"
      metric: "7+ Direct Reports"
      type: "leadmetric"

# Technical versions - 3-column layout
technical:
  programming_languages:
    firmware: ["C/C++ (Expert)", "Python (Expert)"]
    ai: ["Python (Expert)", "JavaScript"]
    consulting: ["Python (Expert)", "SQL"]
```

### Experience Configuration (arthur-experience.yaml)

```yaml
experiences:
  - company: "Tandem Diabetes Care Switzerland"
    versions: ["firmware", "ai", "consulting", "executive", "general"]
    position_variants:
      firmware: "Embedded Software Engineer"
      ai: "Embedded Software Engineer"
      consulting: "Embedded Software Engineer"
    achievements:
      - text: "Led firmware development for Sigi™ insulin pump"
        versions: ["all"]
        priority: 1
      - text: "achieving 96% test coverage through HIL system"
        versions: ["firmware"]
        priority: 1
        type: "techmetric"
```

### Projects Configuration (arthur-projects.yaml)

```yaml
projects:
  - name: "Technical Documentation RAG System"
    versions: ["ai", "consulting", "general", "firmware"]
    descriptions:
      ai:
        - "Architected RAG platform achieving 99.5% chunk quality"
        - "Implemented hybrid retrieval system (FAISS + BM25)"
      firmware:
        - "Designed RISC-V documentation assistant"
        - "Achieved <100ms response times"
```

## 🎨 Version Differences

### Firmware Version
- **Focus**: Embedded systems, real-time programming, hardware integration
- **Tagline**: "Senior Firmware Engineer | Software Architect | Technical Project Lead"
- **Content**: Technical metrics, system performance, hardware details
- **Skills**: C/C++, FreeRTOS, FPGA, communication protocols

### AI Version
- **Focus**: Machine learning, research, technical education
- **Tagline**: "Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Lead"
- **Content**: ML metrics, educational impact, research achievements
- **Skills**: Python, PyTorch, RAG systems, prompt engineering

### Consulting Version
- **Focus**: Business impact, client delivery, strategic technology
- **Tagline**: "Senior Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead"
- **Content**: ROI metrics, stakeholder management, business value
- **Skills**: Strategic consulting, client relations, business analysis

### Executive Version
- **Focus**: Leadership, strategic decisions, team management
- **Tagline**: "Senior Technical Leader | Cross-functional Engineering Manager"
- **Content**: Leadership metrics, financial impact, strategic achievements
- **Length**: ~1 page with Priority 1 content only

### General Version
- **Focus**: Balanced technical and business competencies
- **Tagline**: "Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead"
- **Content**: Broad technical skills, adaptability, versatility
- **Skills**: Mix of firmware and AI expertise

## 🔧 Build System

### Command Line Usage

```bash
# Build all versions
python scripts/build-cv.py all

# Build specific version
python scripts/build-cv.py firmware

# Test logic without building
python scripts/build-cv.py --test firmware

# Custom directories
python scripts/build-cv.py --content-dir custom-content --output-dir custom-output all
```

### Testing Framework

```bash
# Run full test suite
python scripts/test-cv-system.py

# Test specific functionality
python scripts/build-cv.py --test all
```

## 🎯 Conditional Logic

### Version Conditions

```yaml
# Include for specific versions
versions: ["firmware", "ai"]

# Include for all versions
versions: ["all"]

# Exclude specific versions
versions: ["firmware", "ai", "consulting", "general"]  # Excludes executive
```

### Priority System

```yaml
# Priority 1: Always shown (including executive)
priority: 1

# Priority 2: Standard details (hidden in executive)
priority: 2

# Priority 3: Full details (firmware/ai detailed versions only)
priority: 3
```

### Achievement Types

```yaml
# Base achievement
type: "base"

# Technical metric
type: "techmetric"

# Leadership metric
type: "leadmetric"

# Business impact
type: "businessimpact"

# AI/ML focus
type: "ai_focus"

# Consulting focus
type: "consulting_focus"
```

## 🎨 Styling System

### CSS Structure

- **cv-base.css**: Core François Quellec styling
- **cv-print.css**: Print optimization for PDFs
- **cv-versions.css**: Version-specific styling

### Key Design Elements

- **Typography**: Source Sans Pro font family
- **Colors**: Red accent (#dc3545) for headers and links
- **Layout**: Clean, modern design with proper spacing
- **Icons**: SVG icons for contact information
- **Tables**: 3-column skills layout with checkmarks

### Print Optimization

```css
@media print {
    body { font-size: 10pt; }
    .cv-executive { font-size: 11pt; }
    .experience-item { page-break-inside: avoid; }
}
```

## 📊 Testing & Validation

### Test Categories

1. **Version Configurations**: Verify all 5 versions are properly configured
2. **Skills Processing**: Test 3-column layout and executive format
3. **Experience Processing**: Validate conditional logic and priority filtering
4. **Projects Processing**: Check version-specific descriptions
5. **Priority Filtering**: Test executive vs technical content inclusion
6. **Version Conditions**: Verify "all" vs specific version logic
7. **Markdown Generation**: Test output format and content

### Running Tests

```bash
# Full test suite
python scripts/test-cv-system.py

# Test specific version logic
python scripts/build-cv.py --test firmware

# Validate all versions
python scripts/build-cv.py --test all
```

## 🚨 Troubleshooting

### Common Issues

**Issue**: Missing dependencies
```bash
# Solution: Install required packages
pip install pyyaml jinja2 markdown
```

**Issue**: Content not appearing in expected version
```bash
# Solution: Check version conditions in YAML
versions: ["firmware", "ai"]  # Make sure target version is included
```

**Issue**: Priority filtering not working
```bash
# Solution: Check priority levels
priority: 1  # Executive shows only priority 1
priority: 2  # Hidden in executive, shown in others
priority: 3  # Only in detailed versions (firmware/ai)
```

**Issue**: Skills table formatting issues
```bash
# Solution: Check CSS loading
<link rel="stylesheet" href="../../styles/cv-base.css">
```

### Debug Mode

```bash
# Enable verbose output
python scripts/build-cv.py --verbose firmware

# Test specific section
python scripts/build-cv.py --test-section skills firmware
```

## 🔄 Migration from LaTeX

### Content Mapping

| LaTeX Command | YAML Equivalent |
|---------------|----------------|
| `\whenrole{firmware}{}` | `versions: ["firmware"]` |
| `\whennotrole{executive}{}` | `versions: ["firmware", "ai", "consulting", "general"]` |
| `\priority{1}{}` | `priority: 1` |
| `\techmetric{}` | `type: "techmetric"` |
| `\achievement{}{}{}` | `text: "..."` with `type: "base"` |

### Toggle Mapping

| LaTeX Toggle | YAML Versions |
|--------------|---------------|
| `\iftoggle{firmware}{}` | `versions: ["firmware"]` |
| `\iftoggle{ai}{}` | `versions: ["ai"]` |
| `\iftoggle{consulting}{}` | `versions: ["consulting"]` |
| `\iftoggle{executive}{}` | `versions: ["executive"]` |
| `\iftoggle{general}{}` | `versions: ["general"]` |

## 🎯 Best Practices

### Content Organization

1. **Single Source of Truth**: All content in YAML files
2. **Version-Specific Content**: Use `versions` arrays for targeting
3. **Priority Levels**: Use priority 1 for core achievements
4. **Consistent Formatting**: Follow established YAML patterns
5. **Testing**: Always test after content changes

### Maintenance

```bash
# Regular maintenance tasks
python scripts/test-cv-system.py
python scripts/build-cv.py all
git add -A && git commit -m "Update CV content"
```

### Version Control

```bash
# Recommended git workflow
git checkout -b update-cv-content
# Make changes
python scripts/test-cv-system.py
python scripts/build-cv.py all
git add -A
git commit -m "Update: [describe changes]"
git checkout main
git merge update-cv-content
```

## 📈 Performance

### Build Times

- **Single Version**: ~1-2 seconds
- **All Versions**: ~5-10 seconds
- **Test Suite**: ~3-5 seconds

### Output Sizes

- **Markdown**: ~5-15KB per version
- **HTML**: ~20-50KB per version
- **PDF**: ~100-300KB per version

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone [repository-url]
cd arthur-cv-markdown

# Install dependencies
pip install -r requirements.txt

# Run tests
python scripts/test-cv-system.py
```

### Adding New Versions

1. Add version configuration to `CVBuilder.versions`
2. Update content YAML files with new version targeting
3. Add version-specific CSS if needed
4. Update tests to include new version
5. Update documentation

### Adding New Sections

1. Create new YAML content file
2. Add processing logic to `CVBuilder`
3. Create markdown generation method
4. Add to main template
5. Update tests and documentation

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **François Quellec**: Design inspiration from his excellent CV layout
- **LaTeX Community**: Original conditional compilation concepts
- **Python Community**: YAML and Jinja2 templating libraries

---

**Last Updated**: July 2025  
**Version**: 1.0.0  
**Maintainer**: Arthur Passuello