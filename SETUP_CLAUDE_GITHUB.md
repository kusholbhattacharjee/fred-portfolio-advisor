# 🤖 Setting Up Claude Code with GitHub Actions

## ✅ What I Just Did

I created the GitHub Actions workflow file at:
```
.github/workflows/claude.yml
```

This enables Claude to respond to @claude mentions in:
- ✅ PR comments
- ✅ PR review comments
- ✅ Issue comments
- ✅ New issues

---

## 🔑 Step 1: Get Your Anthropic API Key

### **Option A: If You Have Claude Pro/API Access**

1. Go to: **https://console.anthropic.com/**
2. Sign in
3. Navigate to **API Keys** (left sidebar)
4. Click **"Create Key"**
5. Name it: `github-actions-fred-portfolio`
6. **Copy the key** (starts with `sk-ant-...`)

### **Option B: If You Don't Have API Access**

Claude Code GitHub Actions requires an Anthropic API key. You can:
1. Sign up at: https://console.anthropic.com/
2. Or use the GitHub App method (no API key needed)
   - Install: https://github.com/apps/claude-code

**For this tutorial, we'll use Option A (API key method).**

---

## 🔐 Step 2: Add API Key to GitHub Secrets

1. **Go to your repository:** https://github.com/kusholbhattacharjee/fred-portfolio-advisor

2. **Click "Settings"** (top right)

3. **In left sidebar, click:**
   - Secrets and variables → Actions

4. **Click "New repository secret"**

5. **Add the secret:**
   - Name: `ANTHROPIC_API_KEY`
   - Value: (paste your API key from Step 1)
   - Click "Add secret"

---

## 📤 Step 3: Commit and Push the Workflow File

Let's add the workflow file to your repository:

```bash
cd /Users/kusholb/Documents/Anthropic_Demo/fred-portfolio-advisor

# Add the workflow file
git add .github/workflows/claude.yml

# Commit
git commit -m "Add Claude Code GitHub Actions workflow

Enables @claude mentions in PRs and issues to trigger automated code assistance"

# Push to main
git checkout main
git push origin main

# Also push to your PR branch
git checkout remove-unnecessary-print
git merge main
git push origin remove-unnecessary-print
```

---

## 🎯 Step 4: Test It!

### **Method 1: Test on Your Existing PR**

1. Go to your PR: https://github.com/kusholbhattacharjee/fred-portfolio-advisor/pulls

2. Add a comment:
   ```
   @claude please revert this change and restore the print statement
   ```

3. **Watch the magic happen!**
   - GitHub Actions will trigger
   - Claude will analyze the PR
   - Claude will make the changes
   - Claude will comment back

### **Method 2: Test with a New Issue**

1. Create a new issue: https://github.com/kusholbhattacharjee/fred-portfolio-advisor/issues/new

2. Title: "Test Claude Integration"

3. Body:
   ```
   @claude can you check if all our API endpoints have proper error handling?
   ```

4. Create the issue and watch Claude respond!

---

## 🔍 Verify the Workflow is Active

1. Go to: https://github.com/kusholbhattacharjee/fred-portfolio-advisor/actions

2. You should see the "Claude Code" workflow listed

3. After you comment with @claude, a new run will appear

4. Click on it to see the logs in real-time

---

## 📋 What the Workflow Does

When you tag @claude:

```yaml
Trigger → GitHub Actions → Claude Code Action
   ↓
Claude reads the PR/issue
   ↓
Claude analyzes the code
   ↓
Claude makes requested changes
   ↓
Claude pushes commits
   ↓
Claude comments back
```

### **Permissions Granted:**
- ✅ Read repository code
- ✅ Write to PRs and issues
- ✅ Create commits
- ✅ Push to branches
- ❌ Cannot merge PRs (you still control that)

---

## ⚙️ Customization Options

The workflow is already customized for your Python project:

```yaml
claude_args: |
  --model claude-sonnet-4-5-20250929  # Latest Sonnet model
  --max-turns 15                       # Up to 15 back-and-forth exchanges
  --allowedTools "Bash(python*),..."   # Only Python-related commands
  --system-prompt "..."                # Python/Flask specific instructions
```

### **You Can Modify:**

#### **Change the trigger phrase:**
```yaml
trigger_phrase: "/claude"  # Use /claude instead of @claude
```

#### **Allow more commands:**
```yaml
--allowedTools "Bash(python*),Bash(pip*),Bash(npm*),Bash(docker*)"
```

#### **Change the model:**
```yaml
--model claude-opus-4-1-20250805  # Use Opus for more complex tasks
```

#### **Add environment variables:**
```yaml
settings: |
  {
    "env": {
      "FRED_API_KEY": "${{ secrets.FRED_API_KEY }}",
      "PYTHON_ENV": "test"
    }
  }
```

---

## 🎨 Example Use Cases

### **1. Revert Changes**
```
@claude please revert the changes in backend/app.py
```

### **2. Add Features**
```
@claude add input validation to all API endpoints in backend/app.py
```

### **3. Fix Issues**
```
@claude there's a bug in the analyzer.py file line 102.
The calculation is using the wrong formula. Please fix it.
```

### **4. Code Review**
```
@claude review this PR and check for:
- Security vulnerabilities
- PEP 8 compliance
- Missing error handling
```

### **5. Add Tests**
```
@claude add unit tests for the portfolio_advisor.py module
```

### **6. Update Documentation**
```
@claude update the README.md with the new API endpoints I added
```

---

## 🚨 Important Security Notes

### **What's Protected:**
- ✅ Your FRED API key (in `.env` - gitignored)
- ✅ Your Anthropic API key (in GitHub Secrets)
- ✅ No secrets in code or logs

### **What Claude Can Access:**
- ✅ Public code in your repository
- ✅ PR/issue comments
- ✅ Git history
- ❌ Secrets (unless you explicitly pass them in `settings`)

### **Best Practices:**
1. Never paste API keys in PR comments
2. Review Claude's changes before merging
3. Set up branch protection rules
4. Use CODEOWNERS file for sensitive files

---

## 🔧 Troubleshooting

### **Claude doesn't respond**

**Check:**
1. API key is set in GitHub Secrets (`ANTHROPIC_API_KEY`)
2. Workflow file is in `.github/workflows/claude.yml`
3. You tagged exactly `@claude` (case-sensitive)
4. Check Actions tab for errors

**Fix:**
- Go to Actions tab and check the logs
- Verify API key is valid
- Check workflow has proper permissions

### **"Insufficient permissions" error**

The workflow needs these permissions (already set in the file):
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

If you have branch protection:
- Allow GitHub Actions to bypass
- Or use a Personal Access Token

### **Claude made wrong changes**

Comment back:
```
@claude that's not what I wanted. Please revert and try again with [specific instructions]
```

### **Workflow not triggering**

1. Check `.github/workflows/claude.yml` is on the `main` branch
2. Push to main: `git push origin main`
3. Wait 1-2 minutes for GitHub to register it
4. Try commenting with `@claude` again

---

## 📊 Usage & Costs

### **API Usage:**
- Each @claude interaction uses API credits
- Sonnet 4.5: ~$3 per million input tokens
- Average PR review: ~10-50 cents

### **Monitor Usage:**
- Go to: https://console.anthropic.com/
- Check "Usage" in the dashboard

### **Set Limits:**
- Add spending limits in Anthropic Console
- Or set max-turns lower (e.g., `--max-turns 5`)

---

## ✅ Complete Setup Checklist

- [ ] Get Anthropic API key
- [ ] Add API key to GitHub Secrets as `ANTHROPIC_API_KEY`
- [ ] Commit and push `.github/workflows/claude.yml`
- [ ] Verify workflow appears in Actions tab
- [ ] Test with `@claude` comment on PR
- [ ] Check Actions tab for workflow run
- [ ] See Claude's response in PR

---

## 🎯 Quick Start Commands

Run these to push the workflow:

```bash
cd /Users/kusholb/Documents/Anthropic_Demo/fred-portfolio-advisor

# Switch to main
git checkout main

# Add and commit workflow
git add .github/workflows/claude.yml
git commit -m "Add Claude Code GitHub Actions workflow"

# Push to GitHub
git push origin main

# Update PR branch
git checkout remove-unnecessary-print
git merge main
git push origin remove-unnecessary-print
```

Then:
1. Add API key to GitHub Secrets
2. Comment on PR with `@claude please help`
3. Watch it work!

---

## 📚 Additional Resources

- **Claude Code Docs:** https://docs.anthropic.com/claude-code
- **GitHub Actions:** https://docs.github.com/actions
- **Workflow Syntax:** https://docs.github.com/actions/reference/workflow-syntax
- **API Keys:** https://console.anthropic.com/

---

## 🎉 You're All Set!

Once you:
1. ✅ Add your API key to GitHub Secrets
2. ✅ Push the workflow file
3. ✅ Comment with `@claude`

Claude will automatically respond to all your requests in PRs and issues!

---

**Next Step:** Add your Anthropic API key to GitHub Secrets and push the workflow! 🚀
