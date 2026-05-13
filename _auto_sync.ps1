# ============================================================
# Knowledge Base Auto-Sync (called by scheduled task)
# Behavior: detect changes -> commit -> push to GitHub
# Log: .sync-log\sync.log
# ============================================================

$ErrorActionPreference = "Continue"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoPath = "D:\AIGC工作站\知识库"
$logDir = Join-Path $repoPath ".sync-log"
$logFile = Join-Path $logDir "sync.log"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

function Write-Log {
    param([string]$msg, [string]$level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp [$level] $msg" | Out-File -FilePath $logFile -Append -Encoding utf8
}

Write-Log "==========================="
Write-Log "Sync started"

Set-Location $repoPath

if (-not (Test-Path ".git")) {
    Write-Log "Not a Git repository. Run _setup_git.ps1 first." "ERROR"
    exit 1
}

$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Log "No origin remote. Add a GitHub remote first." "ERROR"
    exit 1
}

$changes = git status --porcelain
if (-not $changes) {
    Write-Log "No changes, skip"
    exit 0
}

$changeCount = ($changes -split "`n").Count
Write-Log "Detected $changeCount changes"

git add . 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8

$dateStr = Get-Date -Format "yyyy-MM-dd HH:mm"
$commitMsg = "sync: $dateStr auto sync ($changeCount changes)"

git commit -m "$commitMsg" 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
if ($LASTEXITCODE -ne 0) {
    Write-Log "commit failed" "ERROR"
    exit 1
}
Write-Log "Committed: $commitMsg"

git push origin main 2>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
if ($LASTEXITCODE -ne 0) {
    Write-Log "push failed (check network or GitHub credentials)" "ERROR"
    exit 1
}
Write-Log "Push success"

$logLines = Get-Content $logFile -Encoding utf8
if ($logLines.Count -gt 1000) {
    $logLines | Select-Object -Last 1000 | Set-Content $logFile -Encoding utf8
    Write-Log "Log rotated, kept last 1000 lines"
}

Write-Log "Sync completed"
