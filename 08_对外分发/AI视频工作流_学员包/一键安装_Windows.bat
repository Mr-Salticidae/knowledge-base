@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title AI视频工作流 · 一键安装(Windows)

echo.
echo ============================================================
echo            AI 视频工作流 · Windows 一键安装
echo ============================================================
echo.
echo 这个脚本会帮你自动装好地基:
echo    1) Claude Code   —— 你的 AI 总指挥
echo    2) Node.js       —— 剪辑台 Remotion 的运行底座
echo    3) FFmpeg        —— 处理音视频的引擎
echo    4) Python        —— 跑字幕等技术活要用
echo 然后把整支"技能乐队"放到正确的位置。
echo.
echo (画师/配音/作曲那几位是网上的在线服务,不在这里装,
echo  注册办法见 02_安装_照着做一遍.md 的 B 部分。)
echo.
echo 全程你只需要等待。中途如果弹出"是否允许更改",请点"是"。
echo ------------------------------------------------------------
echo.
pause

echo.
echo [检查] 正在确认你的电脑能不能用自动安装工具(winget)...
where winget >nul 2>nul
if errorlevel 1 (
    echo.
    echo [!] 没找到 winget(Windows 自带的应用安装器)。
    echo     解决办法:打开"Microsoft Store"-^> 搜索"应用安装程序"-^> 更新它,
    echo     然后重新双击本脚本。
    echo.
    pause
    exit /b 1
)
echo     OK,winget 可用。
echo.

echo ============================================================
echo [1/5] 安装 Claude Code(AI 总指挥)
echo ============================================================
winget install --id Anthropic.ClaudeCode -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 echo     [提示] 这一步没成功(可能已装过或网络波动),先继续。
echo.

echo ============================================================
echo [2/5] 安装 Node.js(剪辑台底座)
echo ============================================================
winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 echo     [提示] 这一步没成功(可能已装过),先继续。
echo.

echo ============================================================
echo [3/5] 安装 FFmpeg(音视频引擎)
echo ============================================================
winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 echo     [提示] 这一步没成功(可能已装过),先继续。
echo.

echo ============================================================
echo [4/5] 安装 Python(跑字幕等技术活)
echo ============================================================
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 echo     [提示] 这一步没成功(可能已装过),先继续。
echo.

echo ============================================================
echo [5/5] 安装整支"技能乐队"
echo ============================================================
set "SKILL_SRC=%~dp0skills"
set "SKILL_DST=%USERPROFILE%\.claude\skills"
if not exist "%SKILL_SRC%" (
    echo     [!] 没在脚本旁边找到 skills 文件夹,无法安装技能。
    echo         请确认你是把"整个文件夹"解压后,在里面双击本脚本的。
) else (
    if not exist "%SKILL_DST%" mkdir "%SKILL_DST%"
    set "SKILL_COUNT=0"
    for /d %%S in ("%SKILL_SRC%\*") do (
        xcopy "%%S" "%SKILL_DST%\%%~nxS\" /E /I /Y >nul
        if not errorlevel 1 (
            set /a SKILL_COUNT+=1
            echo     已装技能:%%~nxS
        ) else (
            echo     [!] 复制失败:%%~nxS
        )
    )
    echo     ---- 共安装 !SKILL_COUNT! 个技能到:%SKILL_DST%
)
echo.

echo ============================================================
echo                     地基安装基本完成 ✅
echo ============================================================
echo.
echo 还差两件事:
echo.
echo 【一】让总指挥认识你(登录,只需做一次)
echo    1) 关掉这个窗口
echo    2) 在开始菜单搜索并打开"PowerShell"
echo    3) 输入下面这行,按回车:
echo.
echo          claude
echo.
echo    4) 它会自动打开浏览器让你登录,按提示完成即可。
echo       (需要 Claude 会员账号,详见 02 安装教程)
echo.
echo 【二】注册 AI 工具账号(配音 / 作曲 / 画师)
echo    见 02_安装_照着做一遍.md 的 B 部分。新手先备齐"核心三件套"即可。
echo.
echo 之后想做片子,照着 03_第一支片子_完整走一遍.md 来。
echo.
echo 装的过程中有任何一步飘红/报错,打开 02 安装教程,里面有手动兜底办法。
echo.
pause
endlocal
