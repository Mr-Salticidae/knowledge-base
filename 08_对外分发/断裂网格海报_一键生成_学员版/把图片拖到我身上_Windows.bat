@echo off
chcp 65001 >nul
title 断裂网格海报生成器
cd /d "%~dp0"

echo ============================================
echo   断裂网格杂志海报 · 一键生成器
echo ============================================
echo.

REM 找 Python：优先 py 启动器，再试 python
where py >nul 2>nul
if %errorlevel%==0 (
    set "PYCMD=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYCMD=python"
    ) else (
        echo [没找到 Python]
        echo 请先安装 Python：https://www.python.org/downloads/
        echo 安装时务必勾选「Add Python to PATH」，装完重开本文件。
        echo.
        pause
        exit /b
    )
)

REM 把拖上来的图片路径 %1 传给脚本；没拖就让脚本自己找
%PYCMD% "%~dp0海报生成器.py" %1

