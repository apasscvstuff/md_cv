# Phase Analysis Report Template
**Phase:** [A-H]  
**Conversations:** [List conversation numbers and titles]  
**Analysis Date:** [Date]  
**Analyst:** Claude Code

**CRITICAL WORKFLOW REMINDER (PER CONVERSATION):**
**FOR EACH CONVERSATION IN THE PHASE:**
1. Load ONE conversation data (conversation.txt + JSON file + ALL named artifacts for this conversation)
2. RE-READ this template and the protocol documents BEFORE analyzing this conversation
3. Extract and classify statements from THIS conversation AND its artifacts only
4. Update CSV with findings from THIS conversation and artifacts
5. Repeat for next conversation in phase

**AFTER ALL CONVERSATIONS COMPLETED:**
6. Generate consolidated phase report using this template

---

## Phase Overview

### **Conversations Analyzed**
| Conv # | Title | Messages | Artifacts | Primary Focus |
|--------|-------|----------|-----------|---------------|
| [##] | [Title] | [Count] | [Count] | [Description] |

### **Data Sources Processed**
- [ ] conversation.txt files (complete reading)
- [ ] original_conversation.json files (structured extraction)
- [ ] All named text artifacts analyzed (.md, .txt, .yaml, .css files)
- [ ] Binary/code files appropriately excluded (.png, .svg, .py, .js files)

---

## Content Extraction Results

### **Content Extraction Guidelines**

**CRITICAL TWO-PHASE PROCESS:**

#### **PHASE 1: COMPREHENSIVE EXTRACTION (No Filtering)**
Extract ALL user statements from the conversation, including:
- Direct factual claims about background/experience
- Procedural requests that contain strategic context
- Questions that reveal professional thinking
- Corrections and clarifications
- Decision-making processes
- Professional philosophy statements
- Any statement that reveals something about the user's approach, values, or professional identity

**DO NOT FILTER DURING EXTRACTION** - Capture everything first.

#### **PHASE 2: RELEVANCE ASSESSMENT (Post-Extraction)**
After complete extraction, use the `strategic_content_identification_guide.md` to assess which statements represent:

**FACTUAL CLAIMS about the user's:**
- Professional background and experience
- Technical skills and capabilities  
- Project achievements and outcomes
- Educational credentials
- Quantifiable metrics and results

**STRATEGIC CONTENT about the user's:**
- Career positioning decisions and rationale
- Professional development strategies and philosophy
- Application and job search approaches
- Strategic insights about career direction
- User corrections that reveal professional standards
- Decision-making processes and reasoning
- Professional values and constraints
- Quality control and authenticity concerns

**STRATEGIC CONTENT OFTEN APPEARS WITHIN PROCEDURAL REQUESTS:**

**Examples of STRATEGIC CONTENT within procedural requests:**
- "Give me latex code... I want to take the best out of different versions and orient it towards the AI Consultant application" → Strategic positioning approach
- "Rethink the summary, I'm not entirely satisfied" → Quality control philosophy and authenticity standards
- "I want to re-use the work we've done... the type of adjustment we've actually made" → Systematic professional development approach
- "Are you familiar with mini-pitch? I would be using my Career Assessment to summarize who I am" → Strategic networking methodology

**Examples to STILL EXCLUDE after assessment:**
- "Look at my resume and analyze it" (pure procedural with no strategic insight)
- "Let's work on the next section" (task management only)
- "Change the table format for Excel" (formatting request only)

**CRITICAL:** Pay special attention to conversation endings where strategic conclusions, decisions, and next steps are often revealed.

**APPLY THE STRATEGIC CONTENT TESTS:**
Before excluding any user statement, apply the tests from `strategic_content_identification_guide.md`:
- The "WHY" Test: Does it reveal WHY they want something, not just WHAT?
- The "PROFESSIONAL INSIGHT" Test: Does it reveal professional approach, values, or strategic thinking?
- The "DECISION PROCESS" Test: Does it show professional decision-making or criteria?

**When in doubt, INCLUDE and mark as PENDING for user review.**

### **User Statements (Complete Extraction)**

#### **Profile/Background Information**
```
[Direct quotes from user about their experience, background, education, skills]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Why user mentioned this]
```

#### **Career Goals and Objectives**
```
[User statements about career direction, job targets, transition plans]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Conversation context]
```

#### **Project and Achievement Descriptions**
```
[User's own description of their work, projects, accomplishments]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Project context or job application relevance]
```

#### **Skills and Technical Experience**
```
[User statements about their technical abilities, certifications, tools]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Learning vs professional context]
```

#### **User Corrections/Clarifications**
```
[Instances where user corrected or clarified assistant claims]
Source: Conv [##], Message [##] / JSON index [##]
Context: [What was being corrected]
```

#### **Strategic Positioning Decisions**
```
[User decisions about how to position themselves professionally]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Strategic context and reasoning]
```

#### **Professional Development Insights**
```
[User insights about career strategy, learning approaches, transition planning]
Source: Conv [##], Message [##] / JSON index [##]
Context: [Professional development context]
```

### **Assistant-Generated Claims**

#### **Experience and Background Claims**
```
[Assistant statements about user's professional history]
Source: Conv [##], Assistant response / Artifact: [filename]
Claim: [Specific claim made]
```

#### **Project Descriptions and Achievements**
```
[Assistant-generated project descriptions, metrics, outcomes]
Source: Conv [##], Assistant response / Artifact: [filename]
Claim: [Specific claim made]
```

#### **Skills and Technical Proficiency**
```
[Assistant claims about user's technical abilities and experience levels]
Source: Conv [##], Assistant response / Artifact: [filename]
Claim: [Specific claim made]
```

#### **Quantified Metrics and Results**
```
[Specific numbers, percentages, measurements claimed by assistant]
Source: Conv [##], Assistant response / Artifact: [filename]
Claim: [Specific metric claimed]
```

### **Artifact Content Analysis**

#### **Relevant Artifacts Processed**
| Filename | Type | Content Summary | Profile Relevance |
|----------|------|-----------------|-------------------|
| [filename.ext] | [.md/.txt/.yaml] | [Brief description] | [High/Medium/Low] |

#### **Key Generated Content**
```
[Important CV content, templates, or profile descriptions from artifacts]
Source: Artifact [filename]
Content Type: [CV section, template, analysis, etc.]
```

---

## Classification Matrix Integration

### **Truth Base Application**
**Pre-Analysis Setup:**
- [ ] Load current `statement_classification_matrix.csv` 
- [ ] Read User_Category column for corrections (overrides Category column)
- [ ] Filter User_Reviewed=YES items as authoritative truth base
- [ ] Apply corrected classification rules to new analysis

### **Classification Process**
For each new claim identified:
1. **Check existing CSV** for similar claims and user corrections
2. **Apply truth base hierarchy** (User_Category > Career assessment > Cross-reference)
3. **Use updated detection rules** based on user feedback patterns
4. **Assign new ID** and add as row to CSV

### **CSV Updates for This Phase**
**New rows added to statement_classification_matrix.csv:**

**CRITICAL: ADD ALL MEANINGFUL CLAIMS** - Both accurate and inaccurate claims must be added to maintain comprehensive truth base.

```csv
ID,Statement,Source,Category,User_Category,User_Reviewed,Evidence_Reference,User_Notes,Last_Updated
[NEW_ID],[New claim found],Conv [##],[ACCURATE/EMBELLISHMENT/FABRICATION/PENDING],,NO,[Evidence],[],2025-07-24
```

**Classification Requirements:**
- **ACCURATE claims**: Add to build positive truth base and track verified information
- **EMBELLISHMENT/FABRICATION claims**: Add to identify and prevent future errors
- **PENDING claims**: Add when classification is uncertain and requires user review

### **Truth Source Cross-Reference**

#### **User-Corrected Truth Base** (Highest Authority)
Reference to CSV rows where User_Reviewed=YES:
- Load from statement_classification_matrix.csv
- User_Category column overrides original Category classification
- User_Notes provide context for similar new claims

#### **Career Assessment Verification** (High Authority)
| **User Claim** | **Career Assessment Match** | **Verification Status** |
|----------------|----------------------------|-------------------------|
| [User statement] | [Matching section/form] | ✅ Verified / ❌ Conflicted / ⚠️ Unclear |

#### **Cross-Conversation Consistency** (Medium Authority)
| **Claim** | **First Mention** | **Subsequent Mentions** | **Consistency** |
|-----------|-------------------|------------------------|-----------------|
| [Specific claim] | Conv [##] | Conv [##], [##] | ✅ Consistent / ❌ Conflicted |

### **Enhanced Categorized Findings**

#### **✅ ACCURATE Claims** (User-verified or strongly evidenced)
- **[Claim]** (Matrix ID: [ID])
  - **Source:** [Conv ##, Message ##]
  - **Truth Base Status:** [User-verified / Career assessment match / Cross-confirmed]
  - **Evidence:** [Direct quote or reference]
  - **Matrix Notes:** [Any user corrections or context]

#### **⚠️ EMBELLISHED Claims** (User-corrected or detected pattern)
- **[Claim]** (Matrix ID: [ID])
  - **Source:** [Conv ##, Assistant response]
  - **Truth Base:** [What user actually said/did]
  - **Exaggeration Pattern:** [How it matches known embellishment types]
  - **User Correction:** [If previously corrected by user]
  - **Risk Level:** [Based on user feedback patterns]

#### **❌ FABRICATED Claims** (Clear invention, user-confirmed safe to mark)
- **[Claim]** (Matrix ID: [ID])
  - **Source:** [Conv ##, Assistant response / Artifact]
  - **Fabrication Pattern:** [Type of invention based on learned patterns]
  - **Evidence Search:** [What was checked for verification]
  - **User Guidance:** [Any relevant user corrections from similar claims]
  - **Risk Level:** [Based on potential impact]

#### **🔄 PENDING Claims** (Require user review before classification)
- **[Claim]** (Matrix ID: [ID])
  - **Source:** [Conv ##, Response/Artifact]
  - **Uncertainty Reason:** [Why classification is unclear]
  - **Similar Matrix Items:** [Related claims user has reviewed]
  - **Review Priority:** [High/Medium/Low based on impact]

---

## Actionable Insights

### **Verified Information for Resume/Applications**
- **[Insight]**: [Verified fact about user's background/skills/achievements]
  - **Source Verification:** [Career assessment / User statement]
  - **Application Value:** [How this can be used in job applications]

### **Profile Clarifications Needed**
- **[Item]**: [Something that needs user confirmation or clarification]
  - **Reason:** [Why verification is needed]
  - **Impact:** [Importance for job applications]

### **Content Corrections Required**
- **[Item]**: [Specific content that must be changed/removed]
  - **Issue:** [Fabrication/embellishment/inaccuracy]
  - **Correction:** [What it should say instead]
  - **Priority:** [Critical/High/Medium]

---

## Risk Assessment

### **High-Risk Fabrications** (Potential resume fraud)
- [List of completely false claims that could damage credibility]

### **Medium-Risk Embellishments** (Could be questioned in interviews)
- [List of exaggerated but partially true claims]

### **Low-Risk Inconsistencies** (Minor corrections needed)
- [List of small inaccuracies or unclear statements]

---

## User Review Items

### **For Confirmation**
- [ ] [Item needing user verification]
- [ ] [Timeline or detail to confirm]
- [ ] [Technical claim to validate]

### **For Correction**
- [ ] [Fabricated content to remove]
- [ ] [Embellished claim to tone down]
- [ ] [Metric to verify or delete]

### **For Clarification**
- [ ] [Ambiguous statement to clarify]
- [ ] [Context needed for proper positioning]

---

## Phase Summary

**Total Statements Extracted:** [##] user statements, [##] assistant claims  
**Artifacts Analyzed:** [##] relevant files  
**Verification Results:** [##] accurate, [##] embellished, [##] fabricated  
**Critical Findings:** [Brief summary of major issues]  
**Next Phase Dependencies:** [What needs to be resolved before continuing]

---

**Quality Control Checklist:**
- [ ] Complete file reading completed
- [ ] JSON parsing for structured extraction
- [ ] All relevant artifacts processed
- [ ] Exhaustive statement extraction performed
- [ ] **MEANINGFUL CLAIMS FILTER APPLIED:** Excluded procedural requests and contextual statements
- [ ] Relevance assessment completed
- [ ] Fact-checking against truth sources done
- [ ] Categorization with evidence provided
- [ ] User review items identified
- [ ] Risk assessment completed

**Status:** [Complete/In Progress/Needs Review]  
**Next Steps:** [What happens next in the analysis process]