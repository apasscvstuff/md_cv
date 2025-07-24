# JSON Reading Example - Complete File Coverage

## Correct Approach for Large JSON Files

### **Step 1: Initial Assessment**
```
Read tool: file_path + limit=100
Purpose: Understand JSON structure and format
```

### **Step 2: Systematic Chunk Reading**
```
Read tool: file_path + offset=1 + limit=1000
Read tool: file_path + offset=1001 + limit=1000  
Read tool: file_path + offset=2001 + limit=1000
... continue until "file is shorter than offset"
```

### **Step 3: Content Extraction from Each Chunk**
From each chunk read:
- Look for user messages (any format/structure)
- Look for assistant messages (any format/structure)  
- Extract actual message text content
- Note timestamps if present
- Preserve chronological order

### **Step 4: Complete Coverage Verification**
- Continue reading chunks until Read tool returns file length warning
- Ensure no content is missed, especially conversation endings
- Cross-reference total content with file size if needed

## Why This Approach Works Better:

1. **No Format Assumptions**: Doesn't assume specific JSON structure
2. **Complete Coverage**: Guarantees entire file is read
3. **Both User & Assistant**: Captures all message content
4. **Reliable**: Uses Read tool's built-in offset/limit functionality
5. **Flexible**: Works regardless of JSON formatting variations

## Avoid:
- Grep patterns that might miss content
- Assumptions about JSON field names
- Skipping any sections of the file
- Stopping before complete file coverage