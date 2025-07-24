# CSV Classification Matrix - User Instructions
**File:** `statement_classification_matrix.csv`  
**Purpose:** Single source for reviewing and correcting AI classification errors

---

## Quick Start

### **How to Make Corrections:**
1. **Open the CSV file** in Excel, Google Sheets, or text editor
2. **Find items you want to correct** (look at Category column for my classifications)
3. **Add your correction** in the `User_Category` column
4. **Add explanation** in the `User_Notes` column  
5. **Mark as reviewed** by changing `User_Reviewed` to `YES`
6. **Save the file**

---

## CSV Column Definitions

| Column | Purpose | Your Action |
|--------|---------|-------------|
| `ID` | Unique identifier (don't change) | Leave as-is |
| `Statement` | The actual claim being classified | Leave as-is |
| `Source` | Where I found this claim | Leave as-is |
| `Category` | My original classification | Leave as-is |
| `User_Category` | **YOUR CORRECTIONS** | Edit this to correct me |
| `User_Reviewed` | Review status | Change to YES when done |
| `Evidence_Reference` | Where I found evidence | Leave as-is |
| `User_Notes` | **YOUR EXPLANATIONS** | Add context/reasoning |
| `Last_Updated` | Date stamp | Leave as-is |

---

## Classification Categories

- **ACCURATE** - Statement is completely true as written
- **EMBELLISHMENT** - True core but exaggerated scope/metrics/timeline
- **FABRICATION** - Completely false/invented by AI
- **PENDING** - Need more information to decide

---

## Priority Items for Review

### **🚨 High Priority - Check These First:**
Look for rows where I marked `Category` as `FABRICATION` but you know they're actually true:

**Common Patterns to Check:**
- Metrics I couldn't verify (99.9% uptime, 96% coverage, etc.)
- Technical achievements from conversations I didn't fully analyze
- Real projects I may have missed or misunderstood

### **⚠️ Medium Priority:**
Look for `EMBELLISHMENT` classifications - are these accurate or should they be `ACCURATE`?

---

## Correction Examples

### **Example 1: False Fabrication**
```
Original row:
WE005,"99.9% uptime SLA",Artifacts,FABRICATION,,NO,No user statement found,,2025-07-24

Your correction:
WE005,"99.9% uptime SLA",Artifacts,FABRICATION,ACCURATE,YES,No user statement found,This is real - we achieved 99.9% uptime in production,2025-07-24
```

### **Example 2: Confirm Fabrication**  
```
Original row:
WE007,"Production LLM Implementation",Artifacts,FABRICATION,,NO,No evidence of LLM work,,2025-07-24

Your confirmation:
WE007,"Production LLM Implementation",Artifacts,FABRICATION,FABRICATION,YES,No evidence of LLM work,Confirmed - we never did LLM work at Tandem,2025-07-24
```

### **Example 3: Correct Embellishment**
```
Original row:
SK002,"Python (Expert)",Multiple sources,EMBELLISHMENT,,NO,Strong but may not be Expert level,,2025-07-24

Your correction:
SK002,"Python (Expert)",Multiple sources,EMBELLISHMENT,ACCURATE,YES,Strong but may not be Expert level,Yes Expert level is accurate - 8+ years experience,2025-07-24
```

---

## Workflow Tips

### **Excel/Google Sheets:**
- **Filter by Category** to see all FABRICATION items at once
- **Sort by ID** to keep systematic order
- **Use Find/Replace** to quickly change NO to YES in User_Reviewed column

### **Text Editor:**
- **Search for "FABRICATION"** to find items needing attention
- **Use consistent formatting** for User_Category values
- **Save with UTF-8 encoding** to preserve any special characters

---

## What Happens After Your Review

### **Your corrections will:**
1. **Override my classifications** permanently in all future analysis
2. **Become the truth base** for fact-checking new conversations  
3. **Improve my accuracy** by learning from your feedback patterns
4. **Persist across sessions** - I'll always load your corrections first

### **Quality assurance:**
- Items with `User_Reviewed=YES` are considered final/authoritative
- Your `User_Category` always overrides my original `Category`
- Your `User_Notes` provide context for similar future claims
- I'll never re-classify items you've already corrected

---

## Common Questions

**Q: What if I'm unsure about a classification?**  
A: Use `User_Category=PENDING` and explain what you need to check in `User_Notes`

**Q: Can I add new items to the CSV?**  
A: Yes, but let me do it systematically during analysis to maintain ID consistency

**Q: What if I disagree with the evidence I cited?**  
A: Add your correction in `User_Notes` - your knowledge overrides my evidence search

**Q: How do I know which items need my attention?**  
A: Focus on `Category=FABRICATION` first, then `EMBELLISHMENT`, then anything that looks wrong

---

**Ready to Review:** Open `statement_classification_matrix.csv` and start correcting!  
**Questions?** Just let me know if any classification needs clarification.