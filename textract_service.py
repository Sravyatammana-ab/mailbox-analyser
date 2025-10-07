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

from dotenv import load_dotenv
import asyncio
import gemini_service

load_dotenv()

async def extract_text_from_upload(file_path: str, file_bytes: bytes, mime_type_hint: str = None) -> str:
    """Extracts text from various formats. Falls back to Gemini multimodal OCR for scans/images."""

    ext = file_path.lower()
    logging.info(f"extract_text_from_upload called: file_path={file_path}, mime_type={mime_type_hint}, file_size={len(file_bytes)} bytes")

    # 1. Extract text from digital PDFs
    if ext.endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = "".join(page.extract_text() or "" for page in pdf.pages)
            if full_text.strip():
                logging.info("Successfully extracted text using pdfplumber.")
                return full_text.strip()
        except Exception as e:
            logging.warning(f"pdfplumber failed: {e}. Falling back to Gemini OCR.")

    # 2. Extract text from Word documents (.docx)
    elif ext.endswith(".docx"):
        try:
            doc = Document(file_path)
            full_text = "\n".join([para.text for para in doc.paragraphs])
            if full_text.strip():
                logging.info("Successfully extracted text from DOCX.")
                return full_text.strip()
        except Exception as e:
            logging.warning(f"python-docx failed: {e}. Falling back to Gemini OCR.")

    # 3. Extract from Excel and CSV (.xlsx, .csv)
    elif ext.endswith(".xlsx") or ext.endswith(".csv"):
        try:
            if ext.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            full_text = df.to_string(index=False)
            if full_text.strip():
                logging.info("Successfully extracted text from Excel/CSV.")
                return full_text.strip()
        except Exception as e:
            logging.warning(f"pandas failed to extract table: {e}. Falling back to Gemini OCR.")

    # 4. Extract from images (.png, .jpg, .jpeg)
    elif ext.endswith((".png", ".jpg", ".jpeg")):
        try:
            image = Image.open(BytesIO(file_bytes))
            if image.mode != "RGB":
                image = image.convert("RGB")
            logging.info("Image opened successfully. Using Gemini OCR fallback.")
            # We will fallback to Gemini below
        except Exception as e:
            logging.warning(f"PIL failed to open image: {e}. Falling back to Gemini OCR.")

    # 5. Fallback: Gemini OCR (for scans, images, poor PDFs)
    logging.info("Using Gemini for OCR extraction.")
    try:
        # Prefer provided hint, else guess by file extension
        mime_type = mime_type_hint
        if not mime_type:
            mime_type, _ = guess_type(file_path)
        logging.info(f"Calling Gemini with mime_type={mime_type}")
        # Call async Gemini extractor
        result = await gemini_service.extract_text_from_file(file_path, file_bytes, mime_type)
        logging.info(f"Gemini extraction result length: {len(result) if result else 0}")
        return result
    except Exception as e:
        logging.error(f"Gemini OCR error: {e}", exc_info=True)
        return ""
