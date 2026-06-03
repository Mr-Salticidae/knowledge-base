@echo off
title Build Codex Skill Installer EXE

echo =========================================
echo Codex Skill Installer CN + FFmpeg Builder
echo =========================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
    set PYTHON_CMD=py -3
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo ERROR: Python was not found.
        echo Please install Python 3.10+ from python.org.
        echo IMPORTANT: Check "Add python.exe to PATH" during installation.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python
    )
)

echo Python command: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo Installing PyInstaller...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller.
    pause
    exit /b 1
)

echo.
echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist CodexSkillInstaller_CN.spec del CodexSkillInstaller_CN.spec

echo.
echo Building EXE...
%PYTHON_CMD% -m PyInstaller --noconfirm --onefile --windowed --name CodexSkillInstaller_CN CodexSkillInstaller_CN.pyw
if errorlevel 1 (
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo.
echo SUCCESS.
echo EXE path: dist\CodexSkillInstaller_CN.exe
echo.
pause
