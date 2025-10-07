# main.py

import os
import tempfile
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import textract_service
import gemini_service

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Document Analysis API")
logging.basicConfig(level=logging.INFO)

# Configure CORS for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://yourfrontend.com"] in production
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Allowed file extensions
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".csv", ".xlsx", ".png", ".jpg", ".jpeg"]

def validate_file(file: UploadFile):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

@app.get("/")
async def root():
    return {
        "message": "Document Analysis API",
        "endpoints": {
            "health": "GET /health",
            "analyze": "POST /analyze"
        }
    }

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Main endpoint to upload and analyze a document."""
    tmp_path = None
    try:
        validate_file(file)  # ✅ Check file extension

        # Save file temporarily to disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            file_bytes = await file.read()
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # 1. Extract text using the hybrid service
        logging.info(f"Processing file: {file.filename}, content_type: {file.content_type}")
        extracted_text = await textract_service.extract_text_from_upload(
            tmp_path,
            file_bytes,
            file.content_type if hasattr(file, "content_type") else None
        )
        logging.info(f"Extracted text length: {len(extracted_text) if extracted_text else 0}")
        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=422, 
                detail="Failed to extract text from document. Check if GEMINI_API_KEY is set and file is readable."
            )

        # 2. Classify the document type
        classification_result = await gemini_service.classify_document(extracted_text)
        logging.info(f"classification_result type: {type(classification_result)}, value: {classification_result}")
        if not isinstance(classification_result, dict):
            classification_result = {"document_type": str(classification_result)}
        doc_type = classification_result.get("document_type", "GeneralDocument")

        # 3. Perform specialized analysis
        analysis_result = await gemini_service.analyze_document_by_type(extracted_text, doc_type)
        
        # ✅ Ensure analysis_result is a dictionary
        if not isinstance(analysis_result, dict):
            logging.warning("OpenAI returned non-dict analysis result. Wrapping it.")
            analysis_result = {"analysis_output": str(analysis_result)}

        # ✅ Optional debug logging
        logging.info(f"analysis_result type: {type(analysis_result)}, value: {analysis_result}")

        return {
            "filename": file.filename,
            "document_type": doc_type,
            "analysis": analysis_result
        }

    except Exception as e:
        logging.error("An error occurred in the /analyze endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
