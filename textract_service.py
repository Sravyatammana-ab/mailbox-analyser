from dotenv import load_dotenv
load_dotenv()

import os
import logging
import pdfplumber
import pandas as pd
from docx import Document
from PIL import Image
from io import BytesIO
from mimetypes import guess_type
import asyncio
import pytesseract

load_dotenv()

# Configure Tesseract path for Windows
# Common installation paths for Windows
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.getenv('TESSERACT_CMD')  # Custom path from environment variable
]

# Set Tesseract path if found
for path in TESSERACT_PATHS:
    if path and os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        logging.info(f"Tesseract configured at: {path}")
        break
else:
    logging.warning("Tesseract executable not found. OCR functionality may not work.")

async def _run_blocking(func, *args, **kwargs):
    """Run blocking I/O operations in executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

async def extract_text_from_upload(file_path: str, file_bytes: bytes, mime_type_hint: str = None) -> str:
    """Extracts text from various formats. Uses OCR for scanned documents and images."""

    ext = file_path.lower()
    logging.info(f"extract_text_from_upload called: file_path={file_path}, mime_type={mime_type_hint}, file_size={len(file_bytes)} bytes")

    # 1. Extract text from digital PDFs
    if ext.endswith(".pdf"):
        try:
            def _extract_pdf():
                with pdfplumber.open(file_path) as pdf:
                    return "".join(page.extract_text() or "" for page in pdf.pages)
            
            full_text = await _run_blocking(_extract_pdf)
            if full_text.strip():
                logging.info("Successfully extracted text using pdfplumber.")
                return full_text.strip()
            else:
                # PDF appears to be scanned, try OCR
                logging.info("PDF appears to be scanned. Trying OCR...")
                return await _extract_with_ocr(file_bytes)
        except Exception as e:
            logging.warning(f"pdfplumber failed: {e}. Trying OCR fallback.")
            return await _extract_with_ocr(file_bytes)

    # 2. Extract text from Word documents (.docx)
    elif ext.endswith(".docx"):
        try:
            def _extract_docx():
                doc = Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            
            full_text = await _run_blocking(_extract_docx)
            if full_text.strip():
                logging.info("Successfully extracted text from DOCX.")
                return full_text.strip()
            else:
                logging.warning("DOCX appears empty. Trying OCR fallback.")
                return await _extract_with_ocr(file_bytes)
        except Exception as e:
            logging.warning(f"python-docx failed: {e}. Trying OCR fallback.")
            return await _extract_with_ocr(file_bytes)

    # 3. Extract from plain text files (.txt)
    elif ext.endswith(".txt"):
        try:
            def _extract_txt():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            full_text = await _run_blocking(_extract_txt)
            if full_text.strip():
                logging.info("Successfully extracted text from TXT file.")
                return full_text.strip()
        except Exception as e:
            logging.warning(f"Failed to read text file: {e}")
            return ""

    # 4. Extract from Excel and CSV (.xlsx, .csv)
    elif ext.endswith(".xlsx") or ext.endswith(".csv"):
        try:
            def _extract_excel():
                if ext.endswith(".csv"):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                return df.to_string(index=False)
            
            full_text = await _run_blocking(_extract_excel)
            if full_text.strip():
                logging.info("Successfully extracted text from Excel/CSV.")
                return full_text.strip()
        except Exception as e:
            logging.warning(f"pandas failed to extract table: {e}")
            return ""

    # 5. Extract from images (.png, .jpg, .jpeg) - use OCR
    elif ext.endswith((".png", ".jpg", ".jpeg")):
        logging.info("Image detected. Using OCR extraction.")
        return await _extract_with_ocr(file_bytes)

    # Unsupported file type
    else:
        logging.warning(f"Unsupported file type: {ext}")
        return ""

async def _extract_with_ocr(file_bytes: bytes) -> str:
    """Extract text using pytesseract OCR for scanned documents and images."""
    try:
        def _run_ocr():
            image = Image.open(BytesIO(file_bytes))
            if image.mode != "RGB":
                image = image.convert("RGB")
            text = pytesseract.image_to_string(image)
            return text.strip()
        
        text = await _run_blocking(_run_ocr)
        logging.info(f"OCR extraction successful. Extracted {len(text)} characters.")
        return text
    except Exception as e:
        logging.error(f"OCR extraction failed: {e}", exc_info=True)
        return ""
