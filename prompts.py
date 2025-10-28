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
You are an expert document analysis AI. Analyze the following text and respond ONLY with a JSON object.

Extract:
1. document_type: The type of document (e.g., 'Invoice', 'Contract', 'Partnership Agreement', 'BalanceSheet', etc.)
2. summary: A concise 1-2 sentence summary of the document's purpose
3. key_points: Array of 3-5 important points from the document as strings (e.g., "Effective Date: January 1, 2025")
4. deadlines: Array of objects with description and date. Each object should have:
   - description: What the deadline is for
   - date: The deadline date in ISO format (YYYY-MM-DD)

Respond ONLY with valid JSON in this exact structure:

{
  "document_type": "Invoice",
  "summary": "Invoice for office supplies issued to customer.",
  "key_points": [
    "Invoice Number: INV-12345",
    "Date: December 1, 2024",
    "Customer: ABC Corp",
    "Total Amount: $2,400.00"
  ],
  "deadlines": [
    {
      "description": "Payment due date",
      "date": "2024-12-15"
    }
  ]
}

If no deadlines are found, set deadlines to an empty array [].
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
