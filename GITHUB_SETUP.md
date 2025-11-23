# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Repository name: `interview-practice-partner` (or your preferred name)
4. Description: "AI-powered conversational agent for mock interview practice"
5. Choose Public or Private
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/anshjain/interview_practice_partner

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/interview-practice-partner.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/interview-practice-partner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify

1. Go to your GitHub repository page
2. You should see all your files
3. The README.md will be displayed on the repository homepage

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
cd /Users/anshjain/interview_practice_partner
gh repo create interview-practice-partner --public --source=. --remote=origin --push
```

## Important Notes

- The `.env` file is in `.gitignore` and won't be pushed (this is correct - keep API keys private!)
- Users will need to create their own `.env` file from `.env.example`
- All source code and documentation will be pushed

