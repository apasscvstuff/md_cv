CLAUDE ARTIFACT: CLAUDE.md - LaTeX CV Refactoring Context
============================================================
From Conversation: Resume Enhancement Strategy
Found at path: root.chat_messages[11].content[2]
Artifact ID: claude-md-context
Type: text/markdown
Created: 2025-07-11T09:22:16.909717Z
Updated: 2025-07-11T09:23:33.898953Z
============================================================

ARTIFACT CONTENT:
----------------------------------------
# CLAUDE.md - LaTeX CV Tag-Based Refactoring Project

## Project Overview
Transform Arthur Passuello's multi-file LaTeX CV system into a single-source, tag-based conditional compilation system using etoolbox. This enables generating role-specific CV versions (firmware, AI, consulting, executive, general) from one source.

## Critical Requirements
1. **Preserve ALL existing content** - No content should be lost during refactoring
2. **Maintain visual formatting** - Output PDFs must look identical to current versions
3. **Test incrementally** - Verify each step before proceeding
4. **Use version control** - Commit after each major phase
5. **Create backup** - Always backup before modifying existing files

## Current System Analysis
```
Current Structure:
├── documentMETADATA.cls       # Custom LaTeX class
├── cv.tex                     # Main file
├── section_headline_*.tex     # 3 versions (fw, gen, cons_ai)
├── section_experience_*.tex   # 3 versions
├── section_skills_*.tex       # 3 versions
├── section_education.tex      # Single version
├── section_projects_*.tex     # 2 versions
└── section_languages.tex      # Single version
```

## Implementation Phases

### Phase 1: Infrastructure Setup
Create the following files and directories:

#### 1.1 Create Directory Structure
```bash
mkdir -p config sections archive
```

#### 1.2 File: `config/cv-versions.tex`
```latex
% CV Version Definitions
% Each version sets specific toggles to create targeted output

\newcommand{\cvVersionFirmware}{
  \toggletrue{firmware}
  \toggletrue{technical}
  \toggletrue{detailed}
  \togglefalse{ai}
  \togglefalse{consulting}
  \togglefalse{executive}
  \togglefalse{quantified}
}

\newcommand{\cvVersionAI}{
  \toggletrue{ai}
  \toggletrue{technical}
  \togglefalse{firmware}
  \togglefalse{consulting}
  \togglefalse{executive}
  \toggletrue{detailed}
}

\newcommand{\cvVersionConsulting}{
  \toggletrue{consulting}
  \toggletrue{ai}
  \toggletrue{businessfocus}
  \togglefalse{firmware}
  \togglefalse{executive}
  \toggletrue{quantified}
}

\newcommand{\cvVersionExecutive}{
  \toggletrue{executive}
  \toggletrue{quantified}
  \togglefalse{technical}
  \togglefalse{detailed}
  \togglefalse{firmware}
  \togglefalse{ai}
  \togglefalse{consulting}
  \toggletrue{onepage}
}

\newcommand{\cvVersionGeneral}{
  \toggletrue{firmware}
  \toggletrue{ai}
  \togglefalse{detailed}
  \togglefalse{executive}
  \togglefalse{consulting}
  \toggletrue{general}
}
```

#### 1.3 File: `Makefile`
```makefile
# CV Build System
LATEX = pdflatex
FLAGS = -interaction=nonstopmode -halt-on-error
MAIN = cv.tex

all: firmware ai consulting executive general

firmware:
	@echo "Building Firmware CV..."
	$(LATEX) $(FLAGS) -jobname=cv_firmware "\def\cvversion{firmware}\input{$(MAIN)}"
	$(LATEX) $(FLAGS) -jobname=cv_firmware "\def\cvversion{firmware}\input{$(MAIN)}"

ai:
	@echo "Building AI/ML CV..."
	$(LATEX) $(FLAGS) -jobname=cv_ai "\def\cvversion{ai}\input{$(MAIN)}"
	$(LATEX) $(FLAGS) -jobname=cv_ai "\def\cvversion{ai}\input{$(MAIN)}"

consulting:
	@echo "Building Consulting CV..."
	$(LATEX) $(FLAGS) -jobname=cv_consulting "\def\cvversion{consulting}\input{$(MAIN)}"
	$(LATEX) $(FLAGS) -jobname=cv_consulting "\def\cvversion{consulting}\input{$(MAIN)}"

executive:
	@echo "Building Executive Summary..."
	$(LATEX) $(FLAGS) -jobname=cv_executive "\def\cvversion{executive}\input{$(MAIN)}"
	$(LATEX) $(FLAGS) -jobname=cv_executive "\def\cvversion{executive}\input{$(MAIN)}"

general:
	@echo "Building General CV..."
	$(LATEX) $(FLAGS) -jobname=cv_general "\def\cvversion{general}\input{$(MAIN)}"
	$(LATEX) $(FLAGS) -jobname=cv_general "\def\cvversion{general}\input{$(MAIN)}"

clean:
	rm -f *.aux *.log *.out *.toc cv_*.pdf

.PHONY: all firmware ai consulting executive general clean
```

### Phase 2: Document Class Modifications

#### Modify: `documentMETADATA.cls`
Add after the existing `\RequirePackage` statements (around line 53):

```latex
% Conditional compilation system
\RequirePackage{etoolbox}
\RequirePackage{xstring}

% Define all available toggles
% Role-based toggles
\newtoggle{firmware}
\newtoggle{ai}
\newtoggle{consulting}
\newtoggle{executive}
\newtoggle{general}

% Feature toggles
\newtoggle{technical}
\newtoggle{detailed}
\newtoggle{quantified}
\newtoggle{businessfocus}

% Length control toggles
\newtoggle{onepage}
\newtoggle{twopage}
\newtoggle{fullversion}

% Default all toggles to false
\togglefalse{firmware}
\togglefalse{ai}
\togglefalse{consulting}
\togglefalse{executive}
\togglefalse{general}
\togglefalse{technical}
\togglefalse{detailed}
\togglefalse{quantified}
\togglefalse{businessfocus}
\togglefalse{onepage}
\togglefalse{twopage}
\toggletrue{fullversion}

% Utility commands for conditional content
\newcommand{\whenrole}[2]{%
  \iftoggle{#1}{#2}{}%
}

\newcommand{\whennotrole}[2]{%
  \iftoggle{#1}{}{#2}%
}

\newcommand{\whenany}[2]{%
  % Usage: \whenany{role1,role2}{content}
  % Note: Simple implementation - for complex cases use nested conditions
  #2%
}

% Length-aware commands
\newcommand{\whenonepage}[1]{\iftoggle{onepage}{#1}{}}
\newcommand{\whentwopage}[1]{\iftoggle{twopage}{#1}{}}
\newcommand{\whenfull}[1]{\iftoggle{fullversion}{#1}{}}
```

### Phase 3: Main CV File Refactoring

#### New: `cv.tex`
```latex
% !TEX TS-program = luatex
\documentclass[localFont,alternative]{documentMETADATA}

% Load version configuration
\input{config/cv-versions}

% Detect and set version
\ifdefined\cvversion
  \ifdefstring{\cvversion}{firmware}{\cvVersionFirmware}{}
  \ifdefstring{\cvversion}{ai}{\cvVersionAI}{}
  \ifdefstring{\cvversion}{consulting}{\cvVersionConsulting}{}
  \ifdefstring{\cvversion}{executive}{\cvVersionExecutive}{}
  \ifdefstring{\cvversion}{general}{\cvVersionGeneral}{}
\else
  % Default to general version if no version specified
  \cvVersionGeneral
\fi

% Conditional name and tagline
\name{Arthur}{PASSUELLO}

\iftoggle{firmware}{
  \tagline{Senior Firmware Engineer | Software Architect | Technical Project Lead}
}{}
\iftoggle{ai}{
  \iftoggle{consulting}{
    \tagline{Senior Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead}
  }{
    \tagline{Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Lead}
  }
}{}
\iftoggle{consulting}{
  \iftoggle{ai}{}{
    \tagline{Technical Consultant | Systems Architect | Project Lead}
  }
}{}
\iftoggle{executive}{
  \tagline{Senior Technical Leader | Cross-functional Engineering Manager}
}{}
\iftoggle{general}{
  \tagline{Embedded Systems Engineer | Applied AI/ML Practitioner | Technical Project Lead}
}{}

\socialinfo{
  \smartphone{+(41) 79 176 24 84}
  \email{apassuello@protonmail.com}\\
  \address{Chemin du Parc-de-Valency 1, 1004 Lausanne, Suisse}
  \newline
  \linkedin{arthur-passuello/}
  \github{apassuello}
}

\begin{document}
  \makecvheader
  
  \input{sections/section_headline}
  \input{sections/section_experience}
  \input{sections/section_education}
  \input{sections/section_skills}
  \input{sections/section_projects}
  \input{sections/section_languages}
  
  \makecvfooter{}{}{\thepage}
\end{document}
```

### Phase 4: Section Consolidation Patterns

#### Pattern for Headline Section
Merge all headline variants into `sections/section_headline.tex`:

```latex
\vspace*{-3mm}\par{%
\iftoggle{firmware}{%
  % Content from section_headline_firmware.tex
}{}%
\iftoggle{ai}{%
  \iftoggle{consulting}{%
    % Content from section_headline_cons_ai.tex
  }{%
    % AI-specific content
  }%
}{}%
\iftoggle{executive}{%
  % Executive summary content
}{}%
\iftoggle{general}{%
  % Content from section_headline_gen.tex
}{}%
}
```

#### Pattern for Experience Section
Key patterns for merging experience sections:

```latex
\sectionTitle{Experience}{\faSuitcase}
\begin{experiences}
  \experience
    {End Date}{Title\whenrole{executive}{/Senior Level}}{Company}{Reference}
    {Start Date}{
      \begin{itemize}
        % Core bullets - always shown
        \item Main achievement
        
        % Role-specific bullets
        \whenrole{firmware}{\item Firmware-specific detail}
        \whenrole{ai}{\item AI/ML-specific detail}
        \whenrole{consulting}{\item Consulting-focused detail}
        
        % Conditional details
        \whennotrole{executive}{\item Technical implementation detail}
        \whenrole{quantified}{ achieving 40\% improvement}
      \end{itemize}
    }
    {Skills tags based on role}
\end{experiences}
```

#### Pattern for Skills Section
```latex
\sectionTitle{Technical Expertise}{\faTasks}
\begin{keywords}
  % Always included
  \keywordsentry{Core Skills}{...}
  
  % Conditionally included
  \whenrole{firmware}{
    \keywordsentry{Embedded Systems}{...}
  }
  \whenrole{ai}{
    \keywordsentry{AI/ML \& Data Science}{...}
  }
\end{keywords}
```

## Content Mapping Guide

### From Multiple Files to Single Source
Map content from existing files to conditional blocks:

1. **section_headline_firmware.tex** → `\iftoggle{firmware}{...}`
2. **section_headline_gen.tex** → `\iftoggle{general}{...}`
3. **section_headline_cons_ai.tex** → `\iftoggle{ai}{\iftoggle{consulting}{...}}`

### Experience Section Mapping
- Tandem experience: Core bullets + role-specific additions
- ADEPT experience: Include for all except executive
- IMD experience: Emphasize for AI/consulting roles
- Bleu Lézard: Include only for consulting role

### Skills Consolidation
- Medical Device Development: firmware + general
- AI/ML expertise: ai + consulting
- Project Management: consulting + executive
- Embedded Systems: firmware + general

### Projects Selection
- MultiModal Insight Engine: ai + consulting + general
- Technical Documentation RAG: ai + consulting
- ASIC Medical Device: all except executive  
- High-Performance Genomic: firmware + general

## Testing Protocol

### Test Each Version
After implementing each phase, test:
```bash
make firmware
make ai
make consulting
make executive
make general
```

### Validation Checklist
For each generated PDF, verify:
- [ ] Correct tagline appears
- [ ] Appropriate experience bullets shown
- [ ] Skills match role focus
- [ ] Projects align with version
- [ ] Page count is appropriate
- [ ] No LaTeX errors in log

### Common Issues and Solutions

**Issue**: Content appears in wrong version
- Check toggle settings in cv-versions.tex
- Verify conditional logic uses correct toggle names

**Issue**: Undefined control sequence
- Ensure etoolbox is loaded before toggle usage
- Check for typos in toggle names

**Issue**: Formatting differences
- Compare spacing and indentation
- Check for missing {} after conditionals

**Issue**: Missing content
- Verify all content was transferred
- Check conditional logic covers all cases

## Best Practices

1. **Always backup** before modifying files
2. **Test incrementally** - don't wait until end
3. **Use consistent indentation** in conditionals
4. **Comment complex logic** for future maintenance
5. **Preserve original keywords** for ATS compatibility
6. **Group related conditionals** together
7. **Minimize nesting** where possible

## Git Workflow
```bash
git checkout -b feature/tag-based-cv
# After each phase:
git add -A
git commit -m "Phase X: Description"
# After completion:
git push origin feature/tag-based-cv
```

## Final Validation
1. Generate all 5 PDFs
2. Compare visually with original versions
3. Check file sizes are reasonable
4. Verify no content lost
5. Test build system works correctly
6. Update README with new instructions