@echo off
title Build SkillInstaller EXE

echo =========================================
echo SkillInstaller + FFmpeg Builder
echo =========================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
    py -3.12 --version >nul 2>nul
    if not errorlevel 1 set PYTHON_CMD=py -3.12
)

if not defined PYTHON_CMD (
    if exist C:\Python312\python.exe set PYTHON_CMD=C:\Python312\python.exe
)

if not defined PYTHON_CMD (
    where py >nul 2>nul
    if not errorlevel 1 set PYTHON_CMD=py -3
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set PYTHON_CMD=python
)

if not defined PYTHON_CMD (
    echo ERROR: Python was not found.
    echo Please install Python 3.10+ from python.org.
    echo IMPORTANT: Check "Add python.exe to PATH" during installation.
    pause
    exit /b 1
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
if exist SkillInstaller.spec del SkillInstaller.spec

echo.
echo Building EXE...
%PYTHON_CMD% -m PyInstaller --noconfirm --onefile --windowed --name SkillInstaller SkillInstaller.pyw
if errorlevel 1 (
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo.
echo SUCCESS.
echo EXE path: dist\SkillInstaller.exe
echo.
pause
