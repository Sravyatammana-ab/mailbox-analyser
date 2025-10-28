# openai_service.py
import os
import json
import logging
from openai import AsyncOpenAI
from prompts import CLASSIFICATION_PROMPT, ANALYSIS_PROMPTS

# Load OpenAI credentials
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_RETRIES = 3

async def classify_document(text: str) -> dict:
    """Step 1: Classify the document type with retries."""
    logging.info("Classifying document type...")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt}: Sending classification request to OpenAI...")
            response = await client.chat.completions.create(
                model=OPENAI_MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": CLASSIFICATION_PROMPT},
                    {"role": "user", "content": text[:4000]}
                ],
                temperature=0.2
            )
            result = json.loads(response.choices[0].message.content)

            if isinstance(result, dict) and 'document_type' in result:
                return {"document_type": result['document_type']}
            else:
                logging.warning("Unexpected classification format.")
                return {"document_type": str(result)}

        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
    logging.error("All classification attempts failed.")
    return {"document_type": "GeneralDocument"}

async def analyze_document_by_type(text: str, doc_type: str) -> dict:
    """Step 2: Analyze the document using a universal analysis prompt with retries."""
    logging.info(f"Analyzing document. Type: {doc_type}")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt}: Sending analysis request to OpenAI...")
            response = await client.chat.completions.create(
                model=OPENAI_MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": ANALYSIS_PROMPTS},
                    {"role": "user", "content": text}
                ],
                temperature=0.2
            )
            content = response.choices[0].message.content.strip()
            logging.info(f"OpenAI response: {content[:500]}")  # Log first 500 chars
            result = json.loads(content)

            if isinstance(result, dict):
                logging.info(f"Successfully parsed OpenAI response. Keys: {result.keys()}")
                return result
            else:
                logging.warning("Unexpected analysis format.")
                return {"document_type": doc_type, "summary": str(result), "key_points": [], "deadlines": []}

        except Exception as e:
            logging.error(f"Attempt {attempt} failed: {e}", exc_info=True)
    logging.error("All analysis attempts failed.")
    return {"document_type": doc_type, "summary": "Failed to analyze document.", "key_points": [], "deadlines": []}




 # openai_service.py
# import os
# import json
# import logging
# from openai import AsyncOpenAI
# from prompts import CLASSIFICATION_PROMPT, ANALYSIS_PROMPTS  # ANALYSIS_PROMPTS is a string

# # Load OpenAI credentials
# client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# async def classify_document(text: str) -> dict:
#     """Step 1: Classify the document type."""
#     logging.info("Classifying document type...")
#     try:
#         response = await client.chat.completions.create(
#             model=OPENAI_MODEL,
#             response_format={"type": "json_object"},
#             messages=[
#                 {"role": "system", "content": CLASSIFICATION_PROMPT},
#                 {"role": "user", "content": text[:4000]}  # Use a snippet for faster classification
#             ]
#         )
#         result = json.loads(response.choices[0].message.content)
        
#         # Ensure result is a dict with 'document_type'
#         if isinstance(result, dict):
#             doc_type = result.get('document_type', 'GeneralDocument')
#             return {"document_type": doc_type}
#         else:
#             return {"document_type": str(result)}
    
#     except Exception as e:
#         logging.error(f"Error in document classification: {e}")
#         return {"document_type": "GeneralDocument"}

# async def analyze_document_by_type(text: str, doc_type: str) -> dict:
#     """Step 2: Analyze the document using a universal analysis prompt."""
#     logging.info(f"Analyzing document with universal prompt. Detected type: {doc_type}")
    
#     try:
#         response = await client.chat.completions.create(
#             model=OPENAI_MODEL,
#             response_format={"type": "json_object"},
#             messages=[
#                 {"role": "system", "content": ANALYSIS_PROMPTS},
#                 {"role": "user", "content": text}
#             ]
#         )
#         result = json.loads(response.choices[0].message.content)
        
#         if isinstance(result, dict):
#             return result
#         else:
#             return {"result": str(result)}
    
#     except Exception as e:
#         logging.error(f"Error in document analysis: {e}")
#         return {"error": "Failed to analyze document."}
