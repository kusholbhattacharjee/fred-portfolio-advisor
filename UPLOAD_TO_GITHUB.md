# 🚀 Upload to GitHub - Interactive Guide

I'll walk you through creating your GitHub repository from the command line!

---

## 📋 **What We'll Do:**

1. Set up your git identity (if needed)
2. Get a GitHub Personal Access Token
3. Create the repository on GitHub using the API
4. Push your code

**Estimated time:** 3-5 minutes

---

## ✅ **Step 1: Configure Git (One-time setup)**

Run these commands and **replace with your information**:

```bash
# Your name (how it appears on commits)
git config --global user.name "Your Name"

# Your email (should match your GitHub email)
git config --global user.email "your.email@example.com"
```

**Example:**
```bash
git config --global user.name "Kushol Bhattacharjee"
git config --global user.email "kushol@example.com"
```

---

## 🔑 **Step 2: Get GitHub Personal Access Token**

### **Why?**
GitHub requires a token (instead of password) to create repos via command line.

### **How to get it:**

1. **Click this link:** https://github.com/settings/tokens/new

2. **Fill in the form:**
   - Note: `fred-portfolio-advisor-cli`
   - Expiration: `90 days` (or your choice)
   - Select scopes: ✅ **repo** (check the top "repo" box - it checks all sub-boxes)

3. **Click** "Generate token" (green button at bottom)

4. **COPY the token** - it looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   ⚠️ **You'll only see it once!** Keep it safe for the next step.

---

## 🏗️ **Step 3: Create Repository on GitHub**

Now run this command. When prompted, **paste your token** (you won't see it as you paste - that's normal for security):

```bash
cd /Users/kusholb/Documents/Anthropic_Demo/fred-portfolio-advisor

# This will prompt you for:
# 1. Your GitHub username
# 2. Your Personal Access Token (from Step 2)

curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -u YOUR_GITHUB_USERNAME \
  https://api.github.com/user/repos \
  -d '{"name":"fred-portfolio-advisor","description":"Federal Reserve policy analysis and portfolio strategy tool with real-time FRED API integration","private":false}'
```

**What to replace:**
- Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username

**When prompted:**
- Enter your **Personal Access Token** (not your password!)

---

## 📤 **Step 4: Push Your Code**

After the repository is created, run these commands:

```bash
cd /Users/kusholb/Documents/Anthropic_Demo/fred-portfolio-advisor

# Add GitHub as remote (REPLACE YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/fred-portfolio-advisor.git

# Push to GitHub
git push -u origin main
```

**When prompted for password:** Use your **Personal Access Token** (not your GitHub password)

---

## 🎉 **Done!**

Your repository should now be live at:
```
https://github.com/YOUR_USERNAME/fred-portfolio-advisor
```

---

## 🤔 **Alternative: Easier Interactive Method**

If the above seems complex, here's an even simpler approach:

### **Just run this ONE command:**

```bash
cd /Users/kusholb/Documents/Anthropic_Demo/fred-portfolio-advisor && \
echo "" && \
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && \
echo "📋 GitHub Repository Setup" && \
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && \
echo "" && \
echo "I'll guide you through creating your GitHub repository!" && \
echo "" && \
read -p "🔑 Enter your GitHub username: " GITHUB_USER && \
echo "" && \
echo "🔐 Now get your Personal Access Token:" && \
echo "   1. Go to: https://github.com/settings/tokens/new" && \
echo "   2. Note: fred-portfolio-advisor-cli" && \
echo "   3. Check: repo (full control)" && \
echo "   4. Click: Generate token" && \
echo "   5. Copy the token (ghp_...)" && \
echo "" && \
open "https://github.com/settings/tokens/new?description=fred-portfolio-advisor-cli&scopes=repo" 2>/dev/null || echo "   Visit: https://github.com/settings/tokens/new" && \
echo "" && \
read -s -p "📝 Paste your token here: " GITHUB_TOKEN && \
echo "" && \
echo "" && \
echo "🚀 Creating repository..." && \
RESPONSE=$(curl -s -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"fred-portfolio-advisor","description":"Federal Reserve policy analysis and portfolio strategy tool with real-time FRED API integration","private":false}') && \
if echo "$RESPONSE" | grep -q '"html_url"'; then \
  REPO_URL=$(echo "$RESPONSE" | grep -o '"html_url": "[^"]*"' | head -1 | cut -d'"' -f4) && \
  echo "✅ Repository created: $REPO_URL" && \
  echo "" && \
  echo "📤 Pushing code to GitHub..." && \
  git remote remove origin 2>/dev/null || true && \
  git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/fred-portfolio-advisor.git" && \
  git push -u origin main && \
  git remote remove origin && \
  git remote add origin "https://github.com/${GITHUB_USER}/fred-portfolio-advisor.git" && \
  echo "" && \
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && \
  echo "🎉 SUCCESS! Your repository is live!" && \
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && \
  echo "" && \
  echo "🔗 View it at: $REPO_URL" && \
  echo "" && \
  open "$REPO_URL" 2>/dev/null || echo "   Open in browser: $REPO_URL" ; \
else \
  echo "❌ Error creating repository" && \
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE" ; \
fi
```

**This single command will:**
1. ✅ Ask for your GitHub username
2. ✅ Open the token creation page in your browser
3. ✅ Wait for you to paste the token
4. ✅ Create the repository
5. ✅ Push all your code
6. ✅ Open the repository in your browser
7. ✅ Clean up (remove token from config)

---

## 🆘 **Troubleshooting**

### "Repository already exists"
The repo name is taken. Either:
- Delete the existing repo on GitHub
- Choose a different name

### "Authentication failed"
- Make sure you're using your **token**, not your password
- Check the token has `repo` scope enabled

### "Permission denied"
- Verify your token hasn't expired
- Create a new token if needed

---

## 🔒 **Security Notes**

✅ Your `.env` file (with API key) will **NOT** be uploaded
✅ Only `.env.example` (template) is public
✅ The token is removed from git config after pushing
✅ Your code is safe!

---

## 📞 **Need Help?**

Just tell me:
- Your GitHub username
- Any error messages you see

I'll guide you through it! 🤝

---

**Ready? Pick either the step-by-step method or the one-command method above!** 🚀
