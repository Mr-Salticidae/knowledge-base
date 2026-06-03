$ErrorActionPreference = "Stop"

Write-Host "========================================="
Write-Host "Codex Skill Installer CN + FFmpeg Builder"
Write-Host "========================================="
Write-Host ""

$pythonCmd = $null
$pythonArgsPrefix = @()

if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
    $pythonArgsPrefix = @("-3")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} else {
    Write-Host "ERROR: Python was not found."
    Write-Host "Please install Python 3.10+ from python.org and check Add python.exe to PATH."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python command: $pythonCmd"
& $pythonCmd @pythonArgsPrefix --version

Write-Host ""
Write-Host "Installing PyInstaller..."
& $pythonCmd @pythonArgsPrefix -m pip install --upgrade pip
& $pythonCmd @pythonArgsPrefix -m pip install pyinstaller

Write-Host ""
Write-Host "Cleaning old build files..."
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "CodexSkillInstaller_CN.spec") { Remove-Item "CodexSkillInstaller_CN.spec" -Force }

Write-Host ""
Write-Host "Building EXE..."
& $pythonCmd @pythonArgsPrefix -m PyInstaller --noconfirm --onefile --windowed --name CodexSkillInstaller_CN CodexSkillInstaller_CN.pyw

Write-Host ""
Write-Host "SUCCESS."
Write-Host "EXE path: dist\CodexSkillInstaller_CN.exe"
Read-Host "Press Enter to exit"
