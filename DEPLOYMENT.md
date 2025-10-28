# Deployment Guide for Document Analysis API

## Decision: Local vs Production

### For Development/Testing:
- Use: `http://localhost:8000/analyze-document`
- Good for testing

### For Production with Supabase:
- Use: **Render deployment** (recommended)
- Your frontend will connect to the Render URL
- Supabase stores the results

---

## Quick Answer: Deploy to Render! 🚀

You should deploy to Render because:
1. ✅ Your frontend needs a public URL (not localhost)
2. ✅ Supabase integration requires a stable endpoint
3. ✅ Production-ready with HTTPS
4. ✅ Automatic deployments from GitHub
5. ✅ Free tier available

---

## Part 1: Push to GitHub

### Step 1: Initialize Git (if not already done)

```powershell
cd "D:\Cerevyn Solutions\mailbox analyser"
git init
```

### Step 2: Add all files

```powershell
git add .
```

### Step 3: Commit

```powershell
git commit -m "Initial commit - Document Analysis API with OpenAI"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click "New repository"
3. Name it: `mailbox-analyser`
4. Don't initialize with README (you already have files)
5. Click "Create repository"

### Step 5: Push to GitHub

```powershell
git remote add origin https://github.com/YOUR_USERNAME/mailbox-analyser.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Part 2: Deploy to Render

### Step 1: Sign Up/Login to Render

1. Go to https://render.com
2. Sign up with your GitHub account

### Step 2: Create New Web Service

1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub account (if not already connected)
4. Find and click on `mailbox-analyser` repository

### Step 3: Configure Service

**Settings:**
```
Name: mailbox-analyser-api
Environment: Python 3
Region: Singapore (or closest to you)

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Advanced Settings:**
```
Instance Type: Free (or paid if you want better performance)
```

### Step 4: Add Environment Variables

Click on "Environment" tab and add these variables:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `Your_OpenAI_API_Key_Here` (Set this in Render dashboard) |
| `OPENAI_MODEL` | `gpt-4o-mini` |

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Get your URL: `https://mailbox-analyser-api.onrender.com` (or similar)

---

## Part 3: Update Frontend to Use Render URL

In your frontend code, change:

**Before (development):**
```javascript
const API_URL = 'http://localhost:8000'
```

**After (production):**
```javascript
const API_URL = 'https://mailbox-analyser-api.onrender.com'
```

---

## Part 4: Connect to Supabase

### Add Supabase Environment Variables (Optional)

If you want to store results in Supabase, add these to Render:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon key |

---

## Troubleshooting

### Render deployment fails
- Check build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Check if Tesseract OCR is needed (might need Docker build)

### API times out
- Free tier has 15-minute timeout
- Consider upgrading to paid tier for production

### CORS issues
- Already configured in `main.py` for all origins
- Should work out of the box

---

## Testing Your Deployed API

### Health Check
```bash
curl https://your-api.onrender.com/health
```

### Test Document Upload
Use Postman:
- URL: `https://your-api.onrender.com/analyze-document`
- Method: POST
- Body: form-data, key: `file`, select file

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Render
3. ✅ Update frontend URL
4. ✅ Test the API
5. ✅ Integrate with Supabase (optional)

