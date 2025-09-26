# prompts.py

# Step 1: For initial classification (lightweight)
CLASSIFICATION_PROMPT = """
Analyze the following text to identify the document type. Respond ONLY with a JSON object 
containing a single 'document_type' key. Choose from: 'Invoice', 'BalanceSheet', 
'ProfitAndLossStatement', 'Contract', 'GeneralDocument'.
Example: {"document_type": "Invoice"}
"""

# Step 2: For basic multilingual document understanding (user-friendly, minimal output)
ANALYSIS_PROMPTS = """
You are an expert document analysis AI. Your task is to analyze the following text, which can be in any language.

Perform the following actions:
1. Detect and include the document's 'language' (e.g., 'English', 'Dutch', 'Spanish').
2. Identify the document's type (e.g., 'Invoice', 'BalanceSheet', etc.).
3. Provide a 1-3 sentence 'summary' of the document’s purpose.
4. Extract only clearly visible key-value pairs. Use human-friendly keys (e.g., 'Invoice Date', 'Customer Name').
5. Respond in a clean, readable JSON with the structure:

{
  "language": "English",
  "document_type": "Invoice",
  "summary": "This document is an invoice issued by ABC Corp to XYZ Ltd for the purchase of office supplies.",
  "extracted_data": {
    "Invoice Number": "123456",
    "Date": "2024-12-01",
    "Customer": "XYZ Ltd",
    "Total Amount": "$2,400.00"
  }
}
"""




# ANALYSIS_PROMPTS = """
# You are an expert multilingual document analysis AI.

# Analyze the provided text and respond ONLY with a valid JSON object in the exact format below. Do not include any explanation or extra text.

# Perform the following actions:

# 1. Detect and include the document's 'language' (e.g., "English", "Dutch", "Spanish").
# 2. Identify the document's 'document_type' (e.g., "Invoice", "BalanceSheet", "Contract", or "GeneralDocument").
# 3. Provide a brief 'summary' of the document's purpose (1–2 sentences).
# 4. Extract only explicitly present key-value pairs into an 'extracted_data' object.
#    - Use descriptive keys based on context (e.g., "Invoice Number", "Due Date", "Contract Period").
#    - If a key or value is not present in the document, omit it entirely.
#    - Do not hallucinate or invent values.

# Respond only with a valid JSON object in this structure:

# {
#   "language": "<Detected Language>",
#   "document_type": "<Type>",
#   "summary": "<Brief summary>",
#   "extracted_data": {
#     "Key1": "Value1",
#     "Key2": "Value2"
#   }
# }
# """
