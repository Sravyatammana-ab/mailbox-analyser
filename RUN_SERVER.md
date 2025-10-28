# How to Run and Test the Document Analysis API

## Step 1: Navigate to Project Directory

Open PowerShell and run:
```powershell
cd "D:\Cerevyn Solutions\mailbox analyser"
```

## Step 2: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 3: Start the Server

```powershell
uvicorn main:app --reload
```

The server will start at: **http://localhost:8000**

---

## Testing with Postman

### Test 1: Health Check

1. Open Postman
2. Create a new GET request
3. URL: `http://localhost:8000/health`
4. Click **Send**
5. Expected Response:
```json
{
  "status": "ok"
}
```

### Test 2: API Root Endpoint

1. Create a new GET request
2. URL: `http://localhost:8000/`
3. Click **Send**
4. Expected Response:
```json
{
  "message": "Document Analysis API",
  "endpoints": {
    "health": "GET /health",
    "analyze-document": "POST /analyze-document"
  }
}
```

### Test 3: Document Analysis

1. Create a new POST request
2. URL: `http://localhost:8000/analyze-document`
3. In the **Body** tab:
   - Select **form-data**
   - Add a key named `file` (important: the key MUST be `file`)
   - Change the type from "Text" to **"File"** (dropdown next to key name)
   - Click **Select Files** and choose your document (PDF, DOCX, JPG, PNG, etc.)
4. Click **Send**
5. Expected Response:
```json
{
  "filename": "your-document.pdf",
  "document_type": "Invoice",
  "summary": "Brief summary of the document",
  "key_points": [
    "Key Point 1",
    "Key Point 2",
    "Key Point 3"
  ],
  "deadlines": [
    {
      "description": "Payment due date",
      "date": "2024-12-15"
    }
  ]
}
```

---

## Alternative: Using cURL

### Health Check
```powershell
curl http://localhost:8000/health
```

### Document Analysis
```powershell
curl -X POST http://localhost:8000/analyze-document -F "file=@path\to\your\document.pdf"
```

---

## Troubleshooting

### Test OpenAI Connection First

Before running the server, test if OpenAI is working:

```powershell
python test_openai.py
```

If this fails, check your `.env` file has the correct API key.

### If you get "Could not import module 'main'"
Make sure you're in the correct directory: `D:\Cerevyn Solutions\mailbox analyser`

### If you get "Module not found"
Activate the virtual environment: `.\.venv\Scripts\Activate.ps1`

### If OpenAI API error
Check that your `.env` file has the correct `OPENAI_API_KEY`

### If you get empty summary/key_points/deadlines
1. Check the terminal logs - you should see OpenAI responses
2. The most common cause is incorrect API key or API key not loading
3. Run `python test_openai.py` to verify connection
4. Check the `.env` file exists and has valid key

### To stop the server
Press `CTRL + C` in the terminal where the server is running

---

## Files Needed for Testing

You can test with:
- `test_document.txt`
- `test_invoice.docx`
- `test_upload.py` (not for uploading, but reference)
- Or any PDF, DOCX, JPG, PNG file

