# Fix: Empty Summary, Key Points, and Deadlines

## Problem
You're getting responses like:
```json
{
    "document_type": "GeneralDocument",
    "summary": "",
    "key_points": [],
    "deadlines": []
}
```

## Solution Steps

### Step 1: Test OpenAI Connection

Run this command to verify your OpenAI API key works:

```powershell
python test_openai.py
```

**Expected Output:**
```
API Key set: True
API Key length: [some number]
SUCCESS: Hello, OpenAI is working!
```

**If you get an error**, your API key is not working. Continue to Step 2.

### Step 2: Check .env File

1. Open the `.env` file in your project directory
2. Verify the API key is correct
3. Make sure there are NO spaces around the `=` sign
4. Make sure the key is on ONE line (no line breaks)

**Correct format:**
```env
OPENAI_API_KEY=sk-proj-KBc4sGVlCu_T7_08pnNebH9QbsLzuBj4MbP9HWj8cKmv6XJGKGh7eUcJTosM7nY6W7empjOyQ_T3Bl fleet_tnmsWDhszQ1UswLLQrB-P_D5QYdz0mDKvXMz87qguvNKaabLoxWUbO4ZAwih04_sA
```

### Step 3: Restart the Server

After fixing the `.env` file:

1. Stop the server (press `CTRL + C`)
2. Start it again:
```powershell
uvicorn main:app --reload
```

### Step 4: Check Server Logs

When you upload a document, watch the terminal for logs. You should see:

```
INFO: Classifying document type...
INFO: Analyzing document. Type: Invoice
INFO: Attempt 1: Sending analysis request to OpenAI...
INFO: OpenAI response: {"document_type":"Invoice","summary":"...","key_points":[...]
INFO: Successfully parsed OpenAI response. Keys: dict_keys(['document_type', 'summary', 'key_points', 'deadlines'])
```

**If you see "ERROR" or "Failed"**, the issue is with the API connection.

### Step 5: Test with Simple Text File

If PDFs don't work, try with a simple text file first:

Create `test.txt`:
```
This is an invoice from ABC Company to XYZ Corp dated December 1, 2024. 
Invoice number is INV-12345. 
Total amount is $2,400.00. 
Payment is due by December 15, 2024.
```

Upload this file via Postman to see if text extraction is working.

## Common Causes

1. **API Key Not Set**: Check `.env` file exists and has valid key
2. **API Key Invalid**: Test with `test_openai.py`
3. **API Key Expired**: The key provided might need to be regenerated
4. **Network Issues**: Check internet connection
5. **Text Extraction Failed**: PDF might be corrupted or scanned (check server logs)

## Quick Fix

If nothing works, create a new `.env` file:

```powershell
# In PowerShell
cd "D:\Cerevyn Solutions\mailbox analyser"
notepad .env
```

Then paste:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Save and restart the server.

