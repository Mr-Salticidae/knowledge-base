# ============================================================
# Knowledge Base - Git One-Time Setup
# Usage: Open PowerShell, cd to D:\AIGC工作站\知识库, then run:
#        .\_setup_git.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoPath = "D:\AIGC工作站\知识库"

Write-Host ""
Write-Host "===== Knowledge Base Git Setup =====" -ForegroundColor Cyan
Write-Host ""

# 1. Check Git
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not found. Install from: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# 2. Go to repo dir
Set-Location $repoPath
Write-Host "[OK] Working dir: $repoPath" -ForegroundColor Green

# 3. Check / set Git identity
$userName = git config --global user.name
$userEmail = git config --global user.email
if (-not $userName -or -not $userEmail) {
    Write-Host ""
    Write-Host "Git global identity not set, configuring now:" -ForegroundColor Yellow
    $inputName = Read-Host "Enter your GitHub username"
    $inputEmail = Read-Host "Enter your GitHub email (recommend noreply email)"
    git config --global user.name "$inputName"
    git config --global user.email "$inputEmail"
    Write-Host "[OK] Git identity set" -ForegroundColor Green
} else {
    Write-Host "[OK] Git identity: $userName <$userEmail>" -ForegroundColor Green
}

# 4. Init repo
if (Test-Path ".git") {
    Write-Host "[SKIP] Already a Git repository" -ForegroundColor Yellow
} else {
    git init -b main
    Write-Host "[OK] Initialized Git repo (default branch: main)" -ForegroundColor Green
}

# 5. First add + commit
git add .
$staged = git diff --cached --name-only
if ($staged) {
    git commit -m "init: knowledge base initial snapshot"
    Write-Host "[OK] First commit done" -ForegroundColor Green
} else {
    Write-Host "[SKIP] Nothing to commit" -ForegroundColor Yellow
}

# 6. Next steps
Write-Host ""
Write-Host "===== Next Step: Connect to GitHub Private Repo =====" -ForegroundColor Cyan
Write-Host ""
Write-Host "1) Open https://github.com/new and create a *Private* repository"
Write-Host "   Suggested name: knowledge-base or ai-knowledge-vault"
Write-Host "   Do NOT check: Add README / .gitignore / license"
Write-Host ""
Write-Host "2) After creation, copy the HTTPS URL, e.g.:"
Write-Host "   https://github.com/<your-username>/knowledge-base.git"
Write-Host ""
Write-Host "3) Back in this PowerShell window, run (replace with your URL):"
Write-Host "   git remote add origin https://github.com/<your-username>/knowledge-base.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "First push will pop up GitHub auth, follow the prompts." -ForegroundColor Gray
Write-Host ""
