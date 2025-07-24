# Truth Base Update Protocol
**Purpose:** System for incorporating user corrections into future analysis sessions  
**Version:** 1.0  
**Last Updated:** 2025-07-24

---

## Overview

This protocol ensures that user corrections to AI classifications persist across sessions and improve the accuracy of all future analysis. The truth base evolves from static sources to a dynamic, user-corrected knowledge system.

## Truth Base Architecture

### **Level 1: Static Truth Sources** (Never change)
- **Career Assessment Document** (`career-assessment-template-translation.md`)
- **Original User Statements** (Direct quotes from conversations)
- **Factual Timeline** (Dates, employers, education progression)

### **Level 2: Dynamic Truth Sources** (Updated by user corrections)
- **Classification Matrix** (`statement_classification_matrix.csv`)
- **User Corrections Database** (User_Category column in CSV)
- **Verified Claims Registry** (Claims with User_Reviewed=YES)
- **Strategic Insights Database** (User positioning decisions and professional approach)

### **Level 3: Analysis Rules** (Derived from corrections)
- **Classification Patterns** (What types of claims are typically fabricated)
- **Verification Requirements** (What evidence is needed for specific claim types)
- **Risk Indicators** (Patterns that suggest fabrication)

---

## Update Process

### **CRITICAL TIMING: The Optimal Analysis Workflow (PER CONVERSATION)**

**DO NOT start analysis immediately after loading truth base!**

**MANDATORY Sequence FOR EACH CONVERSATION (prevents methodology drift):**
1. Load statement_classification_matrix.csv and truth base (once per session)
2. Load SINGLE conversation data (original_conversation.json primary + ALL named artifacts for this conversation)
3. **MANDATORY RE-READ** protocol documents BEFORE analyzing each conversation:
   - `conversation_analysis_template.md` (especially two-phase extraction process)
   - `truth_base_update_protocol.md` (this file - correction integration) 
   - `validation_progress_tracker.md` (methodology reminders)
   - `strategic_content_identification_guide.md` (strategic vs procedural content recognition)
4. **Complete JSON reading**: Use Read tool with offset/limit parameters to read entire JSON file bit by bit, extract both user and assistant messages from each chunk
5. **Two-phase extraction**: Extract ALL statements first, then assess relevance
6. **Classification with truth base**: Check existing CSV entries before classifying new claims
7. Update CSV with findings from THIS conversation and artifacts only
8. Generate individual conversation report
9. **REPEAT steps 2-8** for next conversation (don't batch process)

**CRITICAL EMPHASIS:** Steps 3-4 are where errors occur. The re-reading of protocols and complete JSON processing are non-negotiable for each conversation.

### **Before Each Conversation Analysis:**

1. **Load Current Truth Base** (once per session)
   ```
   - Read career assessment (static)
   - Load statement_classification_matrix.csv
   - Filter for User_Reviewed=YES items as authoritative truth
   - Note items with User_Category corrections
   ```

2. **Apply Correction Rules**
   ```
   - Items marked "User_Reviewed: YES" = Authoritative
   - User_Category overrides original AI classification
   - User_Notes provide context for similar claims
   - Pending items flagged for user follow-up
   ```

3. **Update Classification Logic**
   ```
   - Learn from correction patterns
   - Adjust fabrication detection rules
   - Improve embellishment recognition
   - Reduce false positives based on user feedback
   ```

### **During Analysis:**

1. **New Claim and Strategic Content Processing**
   ```
   - Check against corrected classification matrix first
   - Compare to user-verified similar claims
   - Apply updated classification rules
   - Distinguish between factual claims and strategic insights
   - ADD ALL MEANINGFUL CLAIMS regardless of accuracy (ACCURATE, EMBELLISHMENT, FABRICATION, PENDING)
   - Flag uncertain items for user review
   - NEVER write to User_Category column (reserved for user corrections only)
   - ALWAYS set User_Reviewed=NO for new items
   - Document strategic positioning decisions separately from factual claims
   ```

2. **Evidence Weighting**
   ```
   - User corrections = Highest authority
   - Career assessment = High authority  
   - User statements = High authority
   - Cross-conversation consistency = Medium authority
   - AI inference = Lowest authority
   ```

### **After Analysis:**

1. **Matrix Updates**
   ```
   - Add new claims to classification matrix
   - Preserve user corrections from previous sessions
   - Flag items needing user review
   - Update with consistent IDs for tracking
   - Leave User_Category column EMPTY for new items
   - Set User_Reviewed=NO for all new items
   ```

2. **User Review Package**
   ```
   - Present only items needing correction/confirmation
   - Highlight potential classification errors
   - Provide evidence for user verification
   - Track correction completion status
   ```

---

## User Correction Integration

### **Correction Types and Handling:**

#### **False Fabrication (AI Error)**
```
Original: FABRICATION → User: ACCURATE
Impact: Add to verified claims registry
Action: Update detection rules to avoid similar errors
Learning: Improve evidence search methodology
```

#### **Missed Embellishment (AI Error)**
```
Original: ACCURATE → User: EMBELLISHMENT  
Impact: Add exaggeration pattern to detection rules
Action: Adjust threshold for embellishment detection
Learning: Better scope/scale analysis needed
```

#### **Fabrication Confirmation (AI Correct)**
```
Original: FABRICATION → User: FABRICATION
Impact: Confirm detection accuracy
Action: Reinforce fabrication identification patterns
Learning: Validate current detection methodology
```

#### **Context Addition (User Enhancement)**
```
Original: [Any category] → User: [Same + context]
Impact: Enhance understanding of claim background
Action: Improve future evidence gathering
Learning: Better context extraction needed
```

### **Correction Persistence Rules:**

1. **User corrections are PERMANENT** - Never override user-verified classifications
2. **Context accumulates** - User notes enhance understanding over time  
3. **Evidence hierarchy** - User input > Career assessment > AI inference
4. **Error learning** - Correction patterns improve future accuracy

---

## Session Continuity Protocol

### **Session Start Checklist:**
- [ ] Load classification matrix with all user corrections
- [ ] Review pending items from previous session
- [ ] Apply user-verified truth base to new analysis
- [ ] Note any outstanding clarification requests

### **Quality Control Measures:**
- [ ] Verify user corrections are properly loaded
- [ ] Check for conflicts between new claims and corrected truth base
- [ ] Ensure corrected items don't get re-categorized incorrectly
- [ ] Maintain source attribution accuracy

### **Conversation End Requirements (After Each Conversation):**
- [ ] Update classification matrix with new findings from this conversation
- [ ] Preserve all previous user corrections
- [ ] Generate individual conversation report
- [ ] Document any truth base updates made for this conversation

---

## Error Prevention System

### **Common AI Errors to Avoid:**
Based on user corrections, watch for these patterns:

1. **False Fabrication Triggers**
   - Metrics not explicitly mentioned in sampled conversations
   - Technical achievements from unanalyzed conversations
   - Real accomplishments with different phrasing than expected

2. **Missed Embellishment Indicators**
   - Scale inflation (personal → enterprise)
   - Timeline compression (learning → production)
   - Role expansion (contributor → leader)

3. **Context Misunderstanding**
   - Educational vs professional experience
   - Individual vs team accomplishments
   - Current vs historical capabilities

### **Verification Enhancement:**
- **Multiple Source Requirement**: Don't mark as fabrication based on single source absence
- **User Context Priority**: Weight user explanations heavily in classification
- **Conservative Classification**: When uncertain, mark as PENDING for user review

---

## Implementation Example

### **Before Session:**
```
1. Load statement_classification_matrix.csv
2. Read User_Category column for corrections (overrides Category column)
3. Filter User_Reviewed=YES items as authoritative truth base  
4. Apply user corrections to classification rules
```

### **During Analysis:**
```
1. New claim: "99% system reliability"
2. Check matrix: Similar metrics previously corrected by user
3. Apply corrected classification pattern
4. If uncertain, mark as PENDING with evidence
```

### **After Session:**
```
1. Add new claims as rows to statement_classification_matrix.csv
2. Preserve all existing User_Category and User_Notes columns  
3. Set new items User_Reviewed=NO for user review
4. Update Last_Updated timestamps
5. CRITICAL: Leave User_Category column EMPTY for all new items
6. CRITICAL: NEVER write to User_Category column - reserved exclusively for user corrections
```

**CRITICAL CSV UPDATE RULES:**
- **User_Category column**: NEVER write to this column - it is exclusively for user corrections
- **User_Reviewed column**: ALWAYS set to "NO" for new items added by analysis
- Only the user should change User_Reviewed from "NO" to "YES" after reviewing items

---

## Quality Metrics

### **Correction Tracking:**
- **User Correction Rate**: % of AI classifications corrected by user
- **Error Pattern Analysis**: Most common types of AI errors
- **Accuracy Improvement**: Reduction in errors over time
- **User Review Efficiency**: Time required for user corrections

### **Success Indicators:**
- Decreasing false fabrication rate
- Improved embellishment detection
- Reduced user correction requirements
- Higher classification confidence

---

**Status:** Protocol established and ready for implementation  
**Next Steps:** Apply protocol to individual conversation analysis with corrected truth base  
**Dependencies:** User corrections to classification matrix completed