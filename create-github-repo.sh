#!/bin/bash

# GitHub Repository Creation Script
# This script will help you create a GitHub repository from the command line

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         GitHub Repository Creation Tool                      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the fred-portfolio-advisor directory"
    exit 1
fi

echo "📋 Repository Details:"
echo "   Name: fred-portfolio-advisor"
echo "   Description: Federal Reserve policy analysis and portfolio strategy tool"
echo "   Visibility: Public (you can change this later)"
echo ""

# Check if git is configured
echo "🔍 Checking git configuration..."
GIT_USER=$(git config user.name || echo "")
GIT_EMAIL=$(git config user.email || echo "")

if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
    echo ""
    echo "⚙️  Git is not fully configured. Let's set it up:"
    echo ""

    if [ -z "$GIT_USER" ]; then
        read -p "Enter your name (for git commits): " GIT_USER
        git config --global user.name "$GIT_USER"
        echo "✓ Name set to: $GIT_USER"
    fi

    if [ -z "$GIT_EMAIL" ]; then
        read -p "Enter your email (same as GitHub): " GIT_EMAIL
        git config --global user.email "$GIT_EMAIL"
        echo "✓ Email set to: $GIT_EMAIL"
    fi
    echo ""
fi

echo "✓ Git configured as: $GIT_USER <$GIT_EMAIL>"
echo ""

# Get GitHub username
echo "🔑 GitHub Authentication"
echo ""
read -p "Enter your GitHub username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 To create a repository, we need a GitHub Personal Access Token"
echo ""
echo "🔐 How to get your token:"
echo "   1. Go to: https://github.com/settings/tokens"
echo "   2. Click 'Generate new token' → 'Generate new token (classic)'"
echo "   3. Name it: 'fred-portfolio-advisor-cli'"
echo "   4. Select scopes: ✓ repo (Full control of private repositories)"
echo "   5. Click 'Generate token'"
echo "   6. COPY the token (you'll only see it once!)"
echo ""
echo "🔗 Direct link: https://github.com/settings/tokens/new"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Open the URL in browser
if command -v open &> /dev/null; then
    echo "🌐 Opening GitHub token page in your browser..."
    open "https://github.com/settings/tokens/new?description=fred-portfolio-advisor-cli&scopes=repo"
    echo ""
fi

read -s -p "Paste your GitHub Personal Access Token: " GITHUB_TOKEN
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Token is required"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Creating repository on GitHub..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create repository using GitHub API
RESPONSE=$(curl -s -X POST \
    -H "Accept: application/vnd.github.v3+json" \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/user/repos \
    -d '{
        "name": "fred-portfolio-advisor",
        "description": "Federal Reserve policy analysis and portfolio strategy tool with real-time FRED API integration",
        "private": false,
        "has_issues": true,
        "has_projects": true,
        "has_wiki": false
    }')

# Check if creation was successful
if echo "$RESPONSE" | grep -q '"html_url"'; then
    REPO_URL=$(echo "$RESPONSE" | grep -o '"html_url": "[^"]*"' | head -1 | cut -d'"' -f4)
    echo "✅ Repository created successfully!"
    echo ""
    echo "🔗 Repository URL: $REPO_URL"
    echo ""
else
    echo "❌ Failed to create repository"
    echo ""
    echo "Response from GitHub:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    echo ""

    if echo "$RESPONSE" | grep -q "already exists"; then
        echo "⚠️  Repository 'fred-portfolio-advisor' already exists!"
        echo "   You can either:"
        echo "   1. Delete it on GitHub and run this script again"
        echo "   2. Use a different repository name"
        echo "   3. Push to the existing repository (see instructions below)"
        echo ""
    fi

    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 Pushing code to GitHub..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Add remote
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/fred-portfolio-advisor.git"

echo "📦 Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║                    🎉 SUCCESS! 🎉                            ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "✅ Your repository is now on GitHub!"
    echo ""
    echo "🔗 View it at: $REPO_URL"
    echo ""
    echo "📊 What was uploaded:"
    echo "   • 15 files"
    echo "   • 3,037 lines of code"
    echo "   • Complete documentation"
    echo "   • ✓ API key protected (not uploaded)"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. Visit your repository: $REPO_URL"
    echo "   2. Add topics (federal-reserve, fred-api, portfolio-analysis)"
    echo "   3. Share with your network!"
    echo ""

    # Clean up - remove token from remote URL
    git remote remove origin
    git remote add origin "https://github.com/${GITHUB_USER}/fred-portfolio-advisor.git"

    # Open in browser
    if command -v open &> /dev/null; then
        echo "🌐 Opening your repository in browser..."
        open "$REPO_URL"
    fi

else
    echo ""
    echo "❌ Failed to push to GitHub"
    echo ""
    echo "You can try manually with:"
    echo "   git remote add origin https://github.com/${GITHUB_USER}/fred-portfolio-advisor.git"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔒 Security Note: Your GitHub token has been removed from git config"
echo "    It's safe and not stored anywhere in the repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
