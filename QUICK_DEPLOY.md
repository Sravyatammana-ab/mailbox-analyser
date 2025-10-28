# Quick Deployment Steps 🚀

## Deploy to Render in 5 Steps

### Step 1: Push to GitHub

```powershell
cd "D:\Cerevyn Solutions\mailbox analyser"
git init
git add .
git commit -m "Document Analysis API ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/mailbox-analyser.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub and select `mailbox-analyser`
4. Configure:
   - **Name**: `mailbox-analyser-api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable:
   - Key: `OPENAI_API_KEY`
   - Value: `Your_OpenAI_API_Key_Here` (Enter your API key from https://platform.openai.com/api-keys)
6. Click "Create Web Service"
7. Wait 5-10 minutes

### Step 3: Get Your API URL

Once deployed, your API will be at:
```
https://mailbox-analyser-api.onrender.com
```

### Step 4: Test It

```bash
curl https://mailbox-analyser-api.onrender.com/health
```

Expected: `{"status":"ok"}`

### Step 5: Use in Frontend

Update your frontend API URL to:
```javascript
const API_URL = 'https://mailbox-analyser-api.onrender.com/analyze-document'
```

---

## Important Notes

### About Deadlines
✅ The API already handles this correctly:
- If document has deadlines → returns them
- If no deadlines → returns empty array `[]`

### Render Free Tier
⚠️ Free tier limitations:
- 15-minute timeout
- Sleeps after 15 min inactivity
- First request after sleep takes ~30 seconds

### Tesseract OCR
The Dockerfile includes Tesseract for OCR (scanned documents).
This works automatically in Render.

---

## For Production (Recommended)

If you need better performance:
1. Upgrade to paid tier ($7/month)
2. Or use Railway.app (better free tier)
3. Or use Fly.io

---

## Support

If deployment fails:
1. Check Render build logs
2. Verify environment variables
3. Test locally first: `uvicorn main:app --reload`

