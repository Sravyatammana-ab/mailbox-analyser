# Tesseract OCR Installation Guide

## Why Install Tesseract OCR?
Your document analysis project uses Tesseract OCR to extract text from scanned documents and images (PNG, JPG, JPEG files).

## Step-by-Step Installation for Windows

### Step 1: Download Tesseract
1. Visit the official Tesseract Windows installer page:
   - https://github.com/UB-Mannheim/tesseract/wiki
   
2. Download the latest 64-bit Windows installer:
   - Look for: `tesseract-ocr-w64-setup-5.x.x.xxxx.exe` (latest version)
   - Example: `tesseract-ocr-w64-setup-5.4.0.20240606.exe`

### Step 2: Install Tesseract
1. **Run the installer** you just downloaded
2. Click **Next** on the welcome screen
3. Accept the license agreement and click **Next**
4. Choose installation folder (default is recommended):
   - Default: `C:\Program Files\Tesseract-OCR`
   - Or: `C:\Program Files (x86)\Tesseract-OCR`
5. **IMPORTANT**: On the "Additional Tasks" screen, check these boxes:
   - ✓ Add Tesseract OCR to PATH
   - ✓ Set Tesseract OCR environment variable
6. Click **Next**, then **Install**
7. Wait for installation to complete
8. Click **Finish**

### Step 3: Verify Installation
1. **Close and reopen** your terminal/PowerShell (to refresh environment variables)
2. Run this command:
   ```powershell
   tesseract --version
   ```
3. You should see output like:
   ```
   tesseract 5.4.0
    leptonica-1.84.4
    ...
   ```

### Step 4: Configure Your Project
Your `textract_service.py` file has been updated to automatically detect Tesseract in these locations:
- `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`

**If Tesseract is installed in a different location**, add this to your `.env` file:
```env
TESSERACT_CMD=C:\Your\Custom\Path\to\tesseract.exe
```

### Step 5: Test the Installation
1. Make sure you have a `.env` file in your project root (copy from `env.example`)
2. Run your application:
   ```powershell
   python main.py
   ```
3. Try uploading an image file (PNG, JPG, JPEG) - it should extract text using OCR

## Troubleshooting

### Issue: "tesseract is not recognized"
**Solution**: Tesseract is not in your PATH
1. Check if Tesseract is installed in one of these locations:
   - `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`
2. If found, manually add it to PATH:
   - Search for "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Program Files\Tesseract-OCR`
   - Restart your terminal

### Issue: "tesseract_cmd is not set"
**Solution**: Set the path in your `.env` file
```env
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Issue: Installation hangs or fails
**Solution**: 
1. Try running the installer as Administrator (right-click → Run as administrator)
2. Temporarily disable antivirus software during installation
3. Download a different version from the GitHub releases page

## Alternative: Use System Package Manager
If you have Chocolatey or Scoop installed:
```powershell
# Using Chocolatey
choco install tesseract

# Using Scoop
scoop install tesseract
```

## What Files Use OCR?
Your project uses OCR for:
- ✅ Scanned PDFs (when text extraction fails)
- ✅ Scanned Word documents (when text extraction fails)
- ✅ Images (PNG, JPG, JPEG files)
- ✅ Any document that appears to be scanned

## Additional Resources
- Tesseract Documentation: https://tesseract-ocr.github.io/
- GitHub Repository: https://github.com/tesseract-ocr/tesseract
- Python Wrapper (pytesseract): https://pypi.org/project/pytesseract/

---

**Note**: If you choose not to install Tesseract, your application will still work for digital documents (non-scanned PDFs, Word docs, etc.), but OCR-based text extraction will not function.

