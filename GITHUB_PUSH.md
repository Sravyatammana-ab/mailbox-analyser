# Push to GitHub - Copy/Paste Commands

## Open PowerShell and Run These Commands One by One:

```powershell
# Navigate to your project
cd "D:\Cerevyn Solutions\mailbox analyser"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Document Analysis API with OpenAI integration"

# Create repository on GitHub first, then:
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/mailbox-analyser.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## If You Get Authentication Error:

### Option 1: Use GitHub Desktop (Easiest)
1. Install GitHub Desktop: https://desktop.github.com
2. Add the repository
3. Push with UI

### Option 2: Use Personal Access Token
1. Go to https://github.com/settings/tokens
2. Generate new token
3. Use it as password when pushing

---

## After Pushing to GitHub:

✅ Your code is now on GitHub
✅ Ready to deploy to Render
✅ Follow QUICK_DEPLOY.md for deployment steps

