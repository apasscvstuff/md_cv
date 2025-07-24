# Strategic Content Identification Guide
**Purpose:** Help Claude distinguish between meaningless procedural requests and strategic professional insights  
**Version:** 1.0  
**Last Updated:** 2025-07-24

---

## Overview

Strategic content often appears embedded within seemingly procedural conversations. The key is recognizing when a user's request reveals something meaningful about their professional approach, decision-making process, or career strategy.

---

## Strategic Content Categories

### **1. Professional Philosophy & Standards**
Content that reveals the user's approach to work quality, authenticity, or professional representation.

**Examples:**
- "I'm not entirely satisfied with the summary" → Quality control standards
- "I don't want to oversell me or lie" → Authenticity philosophy
- "Justify your enhancements and explain them" → Demand for transparency and reasoning

### **2. Strategic Decision-Making Process**
Content showing how the user makes professional decisions or approaches career challenges.

**Examples:**
- "I want to take the best out of different versions and orient it towards the AI Consultant application" → Strategic positioning methodology
- "Let's summarize my 4 professional projects... strengths, weaknesses, opportunities and risks" → Strategic career planning approach
- "I want to re-use the work we've done... the type of adjustment we've actually made" → Process optimization thinking

### **3. Professional Identity & Self-Assessment**
Content revealing how the user sees themselves professionally or assesses their capabilities.

**Examples:**
- "Except I'm not really an AI/ML Engineer, am I?" → Professional identity questioning
- "I have demonstrated experience with all the following competencies" → Self-assessment and capability mapping
- "Did you look into my career assessment? There's description of freelance work... that may be helpful to show consulting skills" → Strategic experience positioning

### **4. Career Development Strategy**
Content showing the user's approach to professional growth, networking, or career transitions.

**Examples:**
- "Are you familiar with mini-pitch? I would be using my Career Assessment to summarize who I am" → Strategic networking approach
- "I now want to create new versions... help me create a 'profile' of modification process" → Systematic professional development
- "What about my experience at IMD and stakeholder interactions at Tandem?" → Strategic experience recognition

---

## Recognition Patterns

### **Look for these SIGNAL WORDS/PHRASES:**

**Decision-Making Signals:**
- "I want to..."
- "Let's focus on..."
- "I'm not satisfied with..."
- "What about..."
- "How should I..."

**Strategic Thinking Signals:**
- "...orient it towards..."
- "...take the best out of..."
- "...systematic approach..."
- "...help me create..."
- "...may be helpful to show..."

**Professional Standards Signals:**
- "...not entirely satisfied..."
- "...justify your..."
- "...I don't want to oversell..."
- "...authentic result..."
- "...matches my actual background..."

**Self-Assessment Signals:**
- "...am I really..."
- "...I have demonstrated..."
- "...my experience with..."
- "...my actual profile..."

---

## Contextual Analysis Framework

### **The "WHY" Test**
Ask: "Does this statement reveal WHY the user wants something done, not just WHAT they want done?"

**Strategic (Include):**
- "Give me latex code... I want to orient it towards the AI Consultant application" → Reveals strategic positioning goal
- "Rethink the summary, I'm not entirely satisfied" → Reveals quality standards and decision criteria

**Procedural (Exclude):**
- "Give me latex code for the experience section" → Only reveals what they want, not why
- "Change the table format for Excel" → Pure formatting request

### **The "PROFESSIONAL INSIGHT" Test**
Ask: "Does this statement reveal something about the user's professional approach, values, or strategic thinking?"

**Strategic (Include):**
- "I want to re-use the work we've done... the type of adjustment we've actually made" → Reveals process optimization mindset
- "Are you familiar with mini-pitch? I would use my Career Assessment..." → Reveals systematic networking strategy

**Procedural (Exclude):**
- "Let's work on the next section" → No professional insight revealed
- "Can you fix the formatting?" → No strategic content

### **The "DECISION PROCESS" Test**
Ask: "Does this statement show the user making a professional decision or revealing their decision-making criteria?"

**Strategic (Include):**
- "Let's look at the other professional experiences... take the best out of different versions" → Strategic decision about content optimization
- "What about my IMD experience and stakeholder interactions?" → Decision to highlight overlooked strategic experience

**Procedural (Exclude):**
- "Look at section 3 next" → Task sequencing, not strategic decision
- "Read the attached file" → Simple instruction

---

## Special Attention Areas

### **Conversation Endings**
Strategic insights often appear in final messages where users:
- Summarize what they learned
- Make decisions about next steps  
- Reveal their overall strategy
- Express satisfaction/dissatisfaction with outcomes

### **User Corrections**
When users correct or clarify assistant suggestions, they often reveal:
- Their professional standards
- Their authenticity requirements
- Their strategic priorities
- Their decision-making criteria

### **Methodology Discussions**
When users discuss HOW they want to approach something, they often reveal:
- Their systematic thinking approach
- Their quality control processes
- Their professional development philosophy
- Their strategic planning methods

---

## Common Mistakes to Avoid

### **False Positives (Don't Include):**
- Pure task instructions: "Read this file", "Generate a table", "Fix the formatting"
- Simple questions: "What do you think?", "Can you help?", "Is this correct?"
- Basic procedural requests: "Let's move to the next item", "Can you analyze this?"

### **False Negatives (Don't Miss):**
- Strategic content embedded in procedural requests
- Professional philosophy revealed through dissatisfaction or corrections
- Decision-making processes disguised as simple questions
- Self-assessment statements that appear casual but reveal strategic thinking

---

## Quick Reference Checklist

Before excluding a user statement, ask:

- [ ] Does it reveal WHY they want something, not just WHAT?
- [ ] Does it show their professional standards or values?
- [ ] Does it demonstrate strategic thinking or decision-making?
- [ ] Does it reveal their professional identity or self-assessment?
- [ ] Does it show their approach to career development or positioning?
- [ ] Does it contain professional philosophy or methodology insights?

**If YES to any of these → INCLUDE in extraction**

---

**Remember:** When in doubt, include the statement and classify as PENDING for user review rather than miss potentially valuable strategic content.