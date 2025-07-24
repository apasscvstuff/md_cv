# Claude Analysis Session Start Instructions

**CONTEXT**: I need you to analyze conversations from my job search where Claude (AI assistant) generated content about my professional profile. Previous analysis found extensive fabrications in AI-generated CV content that need systematic correction.

**YOUR TASK**: Analyze individual conversations using the established validation framework with CSV-based classification tracking.

**CRITICAL SETUP STEPS**:

1. **Load Truth Base**: Read `/Users/apa/Documents/md_cv/JLL_Complete_Extraction/statement_classification_matrix.csv` 
   - User corrections in `User_Category` column override `Category` column
   - Items with `User_Reviewed=YES` are authoritative truth
   - Apply these corrections to all new classification decisions

2. **OPTIMAL WORKFLOW SEQUENCE** (prevents methodology drift - PER CONVERSATION):
   a. Load statement_classification_matrix.csv first (once per session)
   b. Load ONE conversation data at a time (original_conversation.json primary + ALL named artifacts for this conversation)
   c. **THEN RE-READ** the protocol documents BEFORE analyzing each conversation:
      - `validation_progress_tracker.md` (methodology and workflow)
      - `conversation_analysis_template.md` (structured analysis format)
      - `truth_base_update_protocol.md` (correction integration)
      - `strategic_content_identification_guide.md` (strategic vs procedural content recognition)
   d. Only after re-reading protocols, begin extraction and classification for THIS conversation and its artifacts
   e. Update CSV with findings from THIS conversation
   f. Generate individual conversation report
   g. Repeat steps b-f for each conversation

**ANALYSIS APPROACH** (PER CONVERSATION):
- Proceed one conversation at a time. Re-read the protocols after each conversation
- **JSON-first approach**: Use original_conversation.json as primary data source
- **Complete JSON reading**: Use Grep tool for large JSON files with pattern matching
- **Fallback to conversation.txt**: Only if JSON is incomplete or corrupted

**JSON PROCESSING PROTOCOL:**
- **Primary Method**: Use Read tool with offset/limit parameters to read JSON files bit by bit
- **Start Small**: Read first 100 lines to understand JSON structure and format
- **Read in Chunks**: Continue reading in 500-1000 line chunks using progressive offsets  
- **Extract All Content**: Look for both user and assistant messages in each chunk
- **Complete Coverage**: Keep reading until Read tool indicates "file is shorter than offset"
- **Preserve Order**: Track reading progress to maintain message chronology

**LARGE FILE HANDLING PROTOCOL:**
- **JSON files are always large**: Use systematic chunk-by-chunk reading approach
- **Read completely**: Never skip sections, always read entire file
- **For conversation.txt**: Use same offset/limit approach if JSON unavailable
- **CRITICAL**: Pay special attention to final chunks where strategic conclusions often appear
- **Verification**: Ensure complete file coverage by reading until end-of-file indication

**TWO-PHASE EXTRACTION PROCESS:**
1. **COMPREHENSIVE EXTRACTION** (no pre-filtering): Extract ALL user statements from conversation AND artifacts
2. **RELEVANCE ASSESSMENT** (post-extraction): Evaluate which statements contain meaningful strategic or factual content

- **Artifact inclusion**: Analyze ALL named text files (.md, .txt, .yaml, .css) from conversation's artifacts folder
- **Artifact exclusion**: Skip binary files (.png, .svg), code files (.py, .js), and unnamed temporary files
- **Expanded relevance assessment**: Post-extraction evaluation for:
  - Profile/experience information and factual claims
  - **Strategic discussions about positioning and career decisions**
  - **Professional insights and strategic thinking revealed**
  - **Decision-making processes and rationale**
  - **User corrections and clarifications of approach**
  - **Professional philosophy and quality standards**
  - **Strategic content embedded within procedural requests**
- **CSV integration**: Check existing classifications before making new ones
- **Evidence-based**: Cross-reference against career assessment + user statements + artifact content
- **CRITICAL CSV REQUIREMENT**: ADD ALL MEANINGFUL CLAIMS TO CSV regardless of accuracy level
  - **ACCURATE claims**: Build positive truth base and track verified information
  - **EMBELLISHMENT/FABRICATION claims**: Identify patterns and prevent future errors
  - **PENDING claims**: Flag uncertain items requiring user review

**MEANINGFUL CONTENT SCOPE:** Extract statements representing:
- Substantive claims about user's professional profile
- Strategic discussions about career positioning and decisions
- Professional insights and strategic thinking revealed
- User corrections and clarifications of professional approach
- Decision-making processes and rationale
- Professional philosophy and quality standards
- Exclude only: Pure procedural requests with no strategic context, basic task instructions

**OUTPUT REQUIREMENTS**:
1. **Individual conversation analysis report** using the established template
2. **Updated CSV file** with ALL meaningful claims added as rows from this conversation and its artifacts (preserve existing user corrections)
3. **User review items** clearly flagged for correction

**QUALITY CONTROL**:
- Never re-classify items user has already corrected
- Use corrected truth base to improve accuracy on similar claims
- Mark uncertain items as `PENDING` rather than guessing
- Provide source citations for all new classifications

**CONVERSATION SELECTION PRIORITY**:
1. **Highest Priority**: Conv 06 (AI Skills Architecture Design) - Severe fabrication risk
2. **High Priority**: Conv 13, 21 - Significant fabrication potential  
3. **Medium Priority**: Conversations needing re-analysis with enhanced methodology
4. **Completed**: Conv 27, 28, 30 - Already analyzed with enhanced methodology

**KEY REMINDER**: Your previous analysis contained fabrication errors that I corrected in the CSV. Learn from those corrections to avoid similar mistakes.

---

**NEXT STEPS**: Select the highest priority conversation for analysis and follow the optimal workflow sequence exactly as outlined above.