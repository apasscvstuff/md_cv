# LaTeX Resume Content Migration Session Prompt

## Context and Objectives
You are helping migrate content from an existing LaTeX resume repository to the new markdown-based CV generation system. This is a critical data migration task that must preserve all professional information while adapting to the new system's multi-version approach.

## Migration Overview
- **Source**: LaTeX resume files in the local `latex_content` folder (copied from git repository)
- **Target**: YAML content files in the markdown CV system (`content/arthur-*.yaml`)
- **Goal**: Complete content migration with no information loss and proper version targeting

## Local Content Structure
- **Primary Source**: `latex_content/sections/` - Current/most up-to-date LaTeX sections
- **Historical Source**: `latex_content/archive/` - Previous versions with version-specific content
- **Documentation**: `latex_content/content/` - Migration guides and metrics inventories
- **Current YAML**: `content/arthur-*.yaml` - Existing migrated content to enhance, not replace

## Prerequisites - Start Every Session With These Steps

### 1. Local Content Analysis
- [ ] Use `LS` tool to explore the `latex_content/` directory structure
- [ ] Examine current sections in `latex_content/sections/` - these are the most up-to-date
- [ ] Review archived content in `latex_content/archive/` for additional historical information
- [ ] Read documentation files in `latex_content/content/` for context and migration guidance
- [ ] Use `Read` tool to examine main LaTeX files (`.tex` files in sections/ and archive/)
- [ ] Use `Grep` to search for content patterns and understand the structure across all folders

### 2. Current System Analysis
- [ ] Review existing YAML files in `content/` directory to understand current structure
- [ ] Examine `build_system.py` to understand how YAML content is processed
- [ ] Check `CLAUDE.md` for system documentation on content structure
- [ ] Run `python build_system.py --test firmware` to understand current system state

### 3. Content Discovery Phase
- [ ] Read the documentation files in `latex_content/content/` for migration guidance:
  - [ ] `MAINTENANCE_GUIDE.md` - Understanding the LaTeX system structure
  - [ ] `METRICS_INVENTORY.md` - Catalog of quantitative achievements
  - [ ] `METRICS_MAPPING.md` - How metrics map to different CV versions
  - [ ] `VALIDATION_TESTING.md` - Testing and validation approaches
- [ ] Use `WebSearch` for "LaTeX resume parsing techniques" if needed for complex LaTeX structures
- [ ] Create a comprehensive inventory of all content found in LaTeX files
- [ ] Document any special LaTeX packages or formatting that needs special handling

## LaTeX Content Extraction Process

### 1. Personal Information Discovery
```bash
# Search current sections first (most up-to-date)
grep -r -i "name\|email\|phone\|address\|linkedin\|github" latex_content/sections/
grep -r -i "\\\\author\|\\\\title\|href\|url" latex_content/sections/

# Then check archived content for additional details
grep -r -i "name\|email\|phone\|address\|linkedin\|github" latex_content/archive/
```

**Extract and verify:**
- [ ] Full name and any professional designations
- [ ] Complete address information
- [ ] Phone number(s) - international format
- [ ] Email address(es)
- [ ] LinkedIn profile URL
- [ ] GitHub profile URL
- [ ] Any other professional social media or websites
- [ ] Languages and proficiency levels

### 2. Professional Experience Extraction
```bash
# Search current sections first (most up-to-date)
grep -r -i "experience\|employment\|work\|position\|job" latex_content/sections/
grep -rn "\\\\section\|\\\\subsection" latex_content/sections/

# Check archived versions for version-specific experience content
grep -r -i "experience" latex_content/archive/section_experience_*
# Note: Archive contains version-specific files like section_experience_fw.tex, section_experience_cons_ai.tex
```

**For each position, extract:**
- [ ] Company/organization name
- [ ] Position title(s) - including any variations for different audiences
- [ ] Employment dates (start and end)
- [ ] Location (city, country)
- [ ] Reference contact information if provided
- [ ] All bullet points/achievements
- [ ] Any quantitative metrics or results
- [ ] Technical skills mentioned in context

### 3. Education Background Extraction
```bash
# Search current sections first
grep -r -i "education\|degree\|university\|school\|academic" latex_content/sections/
grep -r -i "bachelor\|master\|phd\|diploma\|certificate" latex_content/sections/

# Check archived education content for additional details
grep -r -i "education\|degree" latex_content/archive/section_education.tex
```

**Extract education details:**
- [ ] Institution names
- [ ] Degree types and fields of study
- [ ] Graduation dates or date ranges
- [ ] GPAs or academic honors if mentioned
- [ ] Relevant coursework
- [ ] Thesis or major project titles
- [ ] Academic achievements or publications

### 4. Skills and Technical Expertise
```bash
# Search current sections first
grep -r -i "skills\|technical\|programming\|languages\|tools\|software" latex_content/sections/
grep -r -i "proficient\|expert\|familiar" latex_content/sections/

# Check archived version-specific skills files
grep -r -i "skills" latex_content/archive/section_skills_*
# Note: Archive contains version-specific files like section_skills_fw.tex, section_skills_AI_cons.tex, section_skills_gen.tex
```

**Categorize skills by:**
- [ ] Software Engineering skills (languages, frameworks, tools)
- [ ] AI & LLMs expertise
- [ ] Data Science capabilities
- [ ] Hardware/Embedded systems knowledge
- [ ] Project management and soft skills
- [ ] Proficiency levels (Expert, Proficient, Familiar)

### 5. Projects and Portfolio
```bash
# Search current sections first
grep -r -i "project\|portfolio\|github\|demo\|publication" latex_content/sections/

# Check archived project files for version-specific content
grep -r -i "project" latex_content/archive/section_projects_*
# Note: Archive contains version-specific files like section_projects_fw.tex, section_projects_all.tex, section_projects_scivis.tex
```

**For each project, extract:**
- [ ] Project name and brief description
- [ ] Time period/dates
- [ ] Technologies used
- [ ] Links to repositories, demos, or publications
- [ ] Key achievements or metrics
- [ ] Relevance to different CV versions (firmware, AI, consulting, etc.)

### 6. Publications and Research
```bash
# Search current sections first
grep -r -i "publication\|paper\|research\|conference\|journal" latex_content/sections/

# Check archived content for additional academic content
grep -r -i "publication\|research" latex_content/archive/section_publications_etc.tex
grep -r -i "teaching\|mentor" latex_content/archive/section_teaching_mentoring.tex
grep -r -i "outreach\|volunteer" latex_content/archive/section_outreach_volunteering.tex
```

**Extract research content:**
- [ ] Publication titles
- [ ] Venues (conferences, journals)
- [ ] Co-authors
- [ ] Dates
- [ ] DOIs or URLs
- [ ] Research focus areas

## YAML Content File Structure Mapping

### Content File Architecture
The system uses separate YAML files for different content types:
- `arthur-personal.yaml` - Personal information and contact details
- `arthur-skills.yaml` - Technical skills and competencies  
- `arthur-experience.yaml` - Work experience and achievements
- `arthur-projects.yaml` - Project portfolio
- `arthur-education.yaml` - Academic background

### Version-Specific Content Targeting
Each content element can be targeted to specific CV versions using:
```yaml
versions: ["firmware", "ai", "consulting", "executive", "general"]
priority: 1  # 1=core (all), 2=standard (not executive), 3=detailed (firmware/ai only)
```

### Achievement and Metric Categorization
Classify achievements by type for proper version targeting:
- `techmetric` - Technical performance metrics (firmware, AI versions)
- `leadmetric` - Leadership and team metrics (executive, consulting)
- `businessimpact` - Business value and ROI (consulting, general)
- `academic` - Research and academic achievements (AI version)

## Local Content Analysis Workflow

### Understanding the Content Structure
The `latex_content/` folder contains three key areas:
1. **`sections/`** - Current, most up-to-date LaTeX sections (7 files)
2. **`archive/`** - Previous versions with version-specific content (23+ files)
3. **`content/`** - Documentation and migration guides

### Cross-Reference Analysis Priority
1. **Primary Analysis**: Start with `sections/` files as the source of truth
2. **Historical Context**: Check `archive/` files for additional content that may not be in current sections
3. **Version-Specific Content**: Use archived version-specific files to understand targeting
4. **Documentation Review**: Read `content/*.md` files for migration context

### Key Archived Files to Review
- `section_experience_*.tex` - Version-specific experience descriptions
- `section_headline_*.tex` - Different taglines for different versions
- `section_skills_*.tex` - Version-specific skill sets
- `section_projects_*.tex` - Project descriptions for different audiences
- `section_publications_etc.tex` - Academic and research content
- `section_teaching_mentoring.tex` - Educational impact content
- `section_outreach_volunteering.tex` - Community involvement

## Migration Process Workflow

### Phase 1: Content Extraction and Validation
1. **Complete Local Content Audit**
   ```bash
   # Create comprehensive content inventory from current sections
   grep -r "\\\\.*{.*}" latex_content/sections/ > current_sections_inventory.txt
   
   # Create inventory from archived content for comparison
   grep -r "\\\\.*{.*}" latex_content/archive/ > archived_content_inventory.txt
   
   # Review documentation for migration context
   ls -la latex_content/content/
   ```
   - [ ] Extract all textual content from current sections first
   - [ ] Compare with archived versions to identify additional content
   - [ ] Read documentation files (METRICS_INVENTORY.md, MAINTENANCE_GUIDE.md) for context
   - [ ] Note any special formatting or symbols that need preservation

2. **Cross-Reference Verification and Enhancement**
   - [ ] Compare current sections with archived versions to identify content evolution
   - [ ] Check existing YAML files in `content/` directory against LaTeX content
   - [ ] Identify content in archived files that should be added to current YAML
   - [ ] Use `diff` between sections/ and archive/ files to understand changes
   - [ ] Pay special attention to:
     - Contact information accuracy
     - Date ranges and chronology
     - Technical terminology and metrics
     - Proper names and titles
     - Version-specific content that may be missing from current YAML

### Phase 2: Content Categorization and Version Mapping
1. **Audience Analysis**
   - [ ] Determine which content is relevant for each CV version:
     - **Firmware**: Embedded systems, hardware, real-time systems
     - **AI**: Machine learning, research, educational impact
     - **Consulting**: Business impact, stakeholder management, ROI
     - **Executive**: Leadership, financial results, strategic initiatives
     - **General**: Balanced technical and business content

2. **Achievement Prioritization**
   - [ ] Classify each achievement by priority level (1-3)
   - [ ] Assign appropriate achievement types (techmetric, leadmetric, etc.)
   - [ ] Ensure executive version has appropriate 1-page content limits

### Phase 3: YAML File Generation
1. **Personal Information**
   ```yaml
   # arthur-personal.yaml structure
   personal:
     name: "Full Name"
     taglines:
       firmware: "Embedded Systems Expert | Technical Lead"
       ai: "ML Practitioner | Research Impact"
       # etc.
     contact:
       address: "Full Address"
       phone: "International Format"
       email: "email@domain.com"
       # etc.
   ```

2. **Experience Migration**
   ```yaml
   # arthur-experience.yaml structure
   experience:
     - company: "Company Name"
       location: "City, Country"
       positions:
         - title: "Job Title"
           title_variants:
             executive: "Executive-focused title"
           start_date: "Month YYYY"
           end_date: "Month YYYY"
           versions: ["firmware", "ai", "consulting"]
           achievements:
             - text: "Achievement description"
               type: "techmetric"
               priority: 1
               versions: ["firmware", "ai"]
   ```

3. **Skills Architecture**
   ```yaml
   # arthur-skills.yaml structure
   skills:
     categories:
       software_engineering:
         - skill: "Programming Language"
           proficiency: "Expert"
           versions: ["firmware", "ai", "general"]
   ```

### Phase 4: Final Cross-Check and Quality Assurance
1. **Comprehensive Content Cross-Check**
   ```bash
   # Compare current sections vs archived content
   for file in latex_content/sections/*.tex; do
     base=$(basename "$file")
     if [ -f "latex_content/archive/$base" ]; then
       echo "Comparing $base:"
       diff "$file" "latex_content/archive/$base" || true
     fi
   done
   
   # Check for unique archived content not in current sections
   ls latex_content/archive/ | grep -v "$(ls latex_content/sections/ | sed 's/^/\\\b/' | sed 's/$/\\\b/' | tr '\n' '|' | sed 's/|$//')"
   ```
   - [ ] Compare each current section file with its archived equivalent
   - [ ] Identify archived files that have no current equivalent
   - [ ] Extract any valuable content from unique archived files
   - [ ] Ensure version-specific taglines from archived headline files are preserved
   - [ ] Verify that specialized content (certifications, publications, outreach) is not overlooked

2. **Existing YAML Content Preservation**
   - [ ] Review current `content/arthur-*.yaml` files for any content not found in LaTeX
   - [ ] Ensure existing YAML content is enhanced, not replaced
   - [ ] Merge the best of current YAML with comprehensive LaTeX content
   - [ ] Validate that no manually added YAML content is lost during migration

3. **Content Validation and System Testing**
   ```bash
   # Test system with enhanced content
   python build_system.py --test all
   python build_system.py firmware
   ```
   - [ ] Verify all YAML files parse correctly
   - [ ] Check that all 5 CV versions build successfully
   - [ ] Review generated output for accuracy and completeness

2. **Comparative Review**
   - [ ] Generate all CV versions: `python build_system.py --all-formats all`
   - [ ] Compare generated CVs against original LaTeX resume
   - [ ] Create side-by-side comparison checklist:
     - [ ] All personal information matches
     - [ ] All work experience included
     - [ ] All skills and competencies preserved
     - [ ] All projects and achievements migrated
     - [ ] Dates and timelines accurate
     - [ ] Contact information correct

3. **Version-Specific Validation**
   - [ ] **Executive version**: Verify 1-page limit and leadership focus
   - [ ] **Technical versions**: Ensure all technical details preserved
   - [ ] **Business versions**: Confirm business impact metrics included
   - [ ] **General version**: Validate balanced content representation

## Advanced Migration Considerations

### Handling Complex LaTeX Structures
- **Custom commands**: Research and understand any `\newcommand` definitions
- **Bibliography**: Migrate any `\cite` references to project or publication entries
- **Tables and figures**: Convert formatted tables to YAML structure
- **Special characters**: Ensure proper Unicode handling for international content

### Content Enhancement Opportunities
During migration, consider:
- [ ] Adding version-specific taglines not in original LaTeX
- [ ] Quantifying achievements with specific metrics where possible
- [ ] Adding relevant project links or portfolio URLs
- [ ] Updating contact information or professional profiles
- [ ] Adding skills or technologies acquired since LaTeX resume creation

### Data Integrity Verification
```bash
# Create verification scripts
echo "Original LaTeX word count:"
wc -w *.tex

echo "Migrated YAML content check:"
python -c "
import yaml
from pathlib import Path
total_content = 0
for file in Path('content/').glob('arthur-*.yaml'):
    with open(file) as f:
        data = yaml.safe_load(f)
        # Add content verification logic
"
```

## Troubleshooting Common Migration Issues

### LaTeX Parsing Challenges
- **Nested braces**: Use careful regex or manual extraction
- **Multiple files**: Check for `\input{}` or `\include{}` statements
- **Custom formatting**: Document any special LaTeX packages used

### Content Mapping Difficulties
- **Ambiguous categorization**: When unclear, include in multiple versions
- **Missing context**: Research company/project context if needed using WebSearch
- **Inconsistent formatting**: Standardize date formats and terminology

### Version Targeting Decisions
- **Overlapping content**: Use priority levels to manage inclusion
- **Executive constraints**: Be selective about what fits in 1-page format
- **Technical depth**: Balance detail levels across different versions

## Success Criteria and Final Validation

### Complete Migration Checklist
- [ ] All current LaTeX content from `sections/` successfully extracted and categorized
- [ ] All valuable archived content from `archive/` reviewed and integrated where appropriate
- [ ] Documentation files (`METRICS_INVENTORY.md`, etc.) consulted for context
- [ ] Existing YAML content in `content/` preserved and enhanced, not replaced
- [ ] All 5 CV versions build without errors using enhanced content
- [ ] Generated CVs contain comprehensive information from both LaTeX and existing YAML sources
- [ ] No personal or professional information lost during migration
- [ ] Version-specific content properly targeted and filtered
- [ ] Contact information and dates verified for accuracy
- [ ] Specialized content (certifications, publications, outreach, teaching) properly included

### Quality Metrics
- [ ] **Completeness**: Original content fully represented in new system
- [ ] **Accuracy**: All details match original LaTeX resume
- [ ] **Enhancement**: New system provides better version-specific targeting
- [ ] **Maintainability**: YAML structure allows easy future updates

### Final Deliverables
1. Complete set of YAML content files in `content/` directory
2. Successfully generated HTML and PDF versions for all 5 CV types
3. Migration report documenting any changes or enhancements made
4. Backup of original LaTeX files for reference

Remember: This migration is crucial for preserving professional history. Take time to be thorough and verify accuracy at every step. When in doubt, preserve more information rather than less - content can always be filtered later using the version targeting system.