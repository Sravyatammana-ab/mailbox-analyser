# Document Analysis API

A production-ready FastAPI service for document upload, text extraction, and AI-based analysis using OpenAI.

## Features

- ✅ Accepts multiple document types: PDF, DOCX, JPG, PNG, TXT, CSV, XLSX
- ✅ Automatic text extraction using:
  - **pdfplumber** for digital PDFs
  - **pytesseract** (Tesseract OCR) for scanned documents and images
  - **python-docx** for Word documents
- ✅ AI-powered document analysis using OpenAI GPT-4o-mini
- ✅ Extracts document type, summary, and deadlines in ISO format
- ✅ Returns structured JSON for easy frontend integration

## API Endpoints

### POST `/analyze-document`
Upload and analyze a document.

**Request:** Multipart form data with a file upload

**Response:**
```json
{
  "filename": "document.pdf",
  "document_type": "Partnership Agreement",
  "summary": "This document outlines the partnership terms between ABC Pvt. Ltd. and XYZ Corp.",
  "key_points": [
    "Effective Date: January 1, 2025",
    "Expiry Date: December 31, 2026",
    "Parties: ABC Pvt. Ltd. and XYZ Corp."
  ],
  "deadlines": [
    {
      "description": "Agreement expiry",
      "date": "2026-12-31"
    }
  ]
}
```

### GET `/health`
Health check endpoint.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Tesseract OCR installed on your system

### Installation

1. **Install Tesseract OCR:**
   - **Windows:** Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS:** `brew install tesseract`
   - **Linux:** `sudo apt-get install tesseract-ocr`

2. **Clone the repository and install dependencies:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

一字文装dependencies
pip install -r requirements.txt
```

3. **Configure environment variables:**
   - Copy `env.example` to `.env`
   - Add your OpenAI API key (provided in the env.example)

4. **Run the server:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-4o-mini`)
- `GEMINI_API_KEY`: Optional Gemini API key for fallback
- `SUPABASE_URL`: Supabase URL (optional)
- `SUPABASE_KEY`: Supabase API key (optional)

## Production Deployment

### Using Render
The project includes `render.yaml` for easy deployment on Render.

```yaml
buildCommand: pip install -r requirements.txt
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Using Docker
Build and run with Docker:

```bash
docker build -t document-analysis-api .
docker run -p 8000:8000 --env-file .env document-analysis-api
```

## Frontend Integration

### Mailbox Page
Use the `summary` field to display the AI-generated summary.

### Deadlines Page
Use the `deadlines` array to display extracted deadlines.

Example fetch request:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/analyze-document', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Summary:', result.summary);
console.log('Key Points:', result.key_points);
console.log('Deadlines:', result.deadlines);
```

## Supported File Types

- **PDF** (digital and scanned)
- **DOCX** (Word documents)
- **JPG/JPEG/PNG** (images - uses OCR)
- **TXT** (text files)
- **CSV/XLSX** (spreadsheets)

## Error Handling

The API includes robust error handling for:
- Unsupported file types
- Corrupted files
- OCR failures
- OpenAI API errors

## License

MIT

