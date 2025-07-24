# Claude Analysis Session Start Instructions

**CONTEXT**: Analyze conversations to identify AI fabrications in professional profile content using systematic validation framework.

**MANDATORY WORKFLOW ADHERENCE**: 
- **NEVER deviate** from established sequence
- **RE-READ protocols** before each conversation analysis  
- **COMPLETE each step** before proceeding to next
- If you find yourself lost or confused, **STOP and re-read these instructions**

## Core Setup (Once Per Session)

1. **Load Truth Base**: Read `statement_classification_matrix.csv`
   - User corrections (`User_Category` column) override AI classifications  
   - Items with `User_Reviewed=YES` are authoritative truth

2. **Read Protocol Documents**:
   - `conversation_analysis_template.md` (analysis format)
   - `strategic_content_identification_guide.md` (content relevance)
   - `validation_progress_tracker.md` (methodology)

## Per-Conversation Workflow (MANDATORY SEQUENCE)

**BEFORE each conversation analysis, RE-READ**:
- `conversation_analysis_template.md` 
- `strategic_content_identification_guide.md`
- `truth_base_update_protocol.md`

**Then execute**:
1. **Load data**: Read original_conversation.json + ALL named artifacts
2. **Extract claims**: ALL user statements + AI-generated content  
3. **Classify**: ACCURATE/EMBELLISHMENT/FABRICATION/PENDING
4. **Update CSV**: Add ALL meaningful claims as new rows
5. **Generate report**: Using established template

## JSON Reading Protocol (CRITICAL)

- **Primary source**: original_conversation.json
- **Method**: Read tool with offset/limit in chunks (100 lines first, then 500-1000 line chunks)
- **Complete coverage**: Read until "file is shorter than offset" 
- **Extract**: Both user and assistant messages from each chunk
- **Fallback**: conversation.txt only if JSON corrupted

## Claim Relevance (EXPANDED SCOPE)

**EXTRACT all statements containing**:
- Professional background/skills/achievements
- **Mention any project, experience from Arthur's resume/career assessment**
- **Directly mentions CV content or content suggestions**
- **Strategic career discussions and decision-making**
- **Professional insights and philosophy** 
- **User corrections of AI content**
- **Career positioning rationale**
- **Quality standards and authenticity concerns**

**Exclude only**: Pure procedural requests with zero strategic context

**CONVERSATION SELECTION**: Conversation 05

**CRITICAL**: If methodology feels unclear at any point, **STOP and re-read these instructions completely**