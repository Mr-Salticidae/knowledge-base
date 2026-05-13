# ============================================================
# Register Windows Scheduled Task for Auto-Sync
# Usage: Open PowerShell *AS ADMINISTRATOR*, cd to repo dir, run:
#        .\_register_schedule.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$taskName = "KnowledgeBase_AutoSync_GitHub"
$scriptPath = "D:\AIGC工作站\知识库\_auto_sync.ps1"
$triggerTime = "22:00"  # Daily at 22:00, change if needed

Write-Host ""
Write-Host "===== Register Windows Scheduled Task =====" -ForegroundColor Cyan
Write-Host ""

# Check admin
$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Please run PowerShell as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell -> Run as Administrator, then cd back and retry" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERROR] Script not found: $scriptPath" -ForegroundColor Red
    exit 1
}

# Remove existing
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[INFO] Task already exists, removing old one" -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Daily $triggerTime auto-push D:\AIGC工作站\知识库 to GitHub" | Out-Null

Write-Host ""
Write-Host "[OK] Scheduled task created:" -ForegroundColor Green
Write-Host "     Name : $taskName"
Write-Host "     When : Daily at $triggerTime"
Write-Host "     Path : $scriptPath"
Write-Host ""
Write-Host "View / edit / remove: Win+R -> taskschd.msc -> Task Scheduler Library" -ForegroundColor Gray
Write-Host "Run once manually:"
Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
Write-Host ""
