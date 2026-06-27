@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title AI卡点剪辑 · 一键安装(Windows)

echo.
echo ============================================================
echo            AI 卡点剪辑 · Windows 一键安装
echo ============================================================
echo.
echo 这个脚本会帮你自动装好三样东西:
echo    1) Claude Code   —— 你的 AI 剪辑助理
echo    2) FFmpeg        —— 真正干剪辑活的引擎
echo    3) Python        —— AI 写的剪辑代码靠它运行
echo 然后把"剪辑技能说明书"放到正确的位置。
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
    echo     这通常说明系统较旧或商店组件需要更新。
    echo     解决办法:打开"Microsoft Store"-^> 搜索"应用安装程序"-^> 更新它,
    echo     然后重新双击本脚本。
    echo.
    echo     如果你不想折腾,请把这段话发给帮你的朋友,他能手动帮你装。
    echo.
    pause
    exit /b 1
)
echo     OK,winget 可用。
echo.

echo ============================================================
echo [1/4] 安装 Claude Code(AI 剪辑助理)
echo ============================================================
winget install --id Anthropic.ClaudeCode -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo     [提示] Claude Code 这一步没成功(可能已经装过,或网络波动)。
    echo            先继续,稍后可在教程里看手动安装办法。
)
echo.

echo ============================================================
echo [2/4] 安装 FFmpeg(剪辑引擎)
echo ============================================================
winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo     [提示] FFmpeg 这一步没成功(可能已经装过)。先继续。
)
echo.

echo ============================================================
echo [3/4] 安装 Python(运行剪辑代码)
echo ============================================================
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo     [提示] Python 这一步没成功(可能已经装过)。先继续。
)
echo.

echo ============================================================
echo [4/4] 安装"剪辑技能说明书"
echo ============================================================
set "SKILL_SRC=%~dp0skills\blind-editing-workflow"
set "SKILL_DST=%USERPROFILE%\.claude\skills\blind-editing-workflow"
if not exist "%SKILL_SRC%\SKILL.md" (
    echo     [!] 没在脚本旁边找到 skills 文件夹,无法安装技能。
    echo         请确认你是把"整个文件夹"解压后,在里面双击本脚本的。
) else (
    if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"
    xcopy "%SKILL_SRC%" "%SKILL_DST%\" /E /I /Y >nul
    if errorlevel 1 (
        echo     [!] 技能复制失败,请把这条信息发给帮你的朋友。
    ) else (
        echo     OK,技能已装到:%SKILL_DST%
    )
)
echo.

echo ============================================================
echo                     安装基本完成 ✅
echo ============================================================
echo.
echo 还差最后一步:让 AI 助理认识你(登录,只需做一次)
echo.
echo    1) 关掉这个窗口
echo    2) 在开始菜单搜索并打开"Windows Terminal"或"PowerShell"
echo    3) 输入下面这行,按回车:
echo.
echo          claude
echo.
echo    4) 它会自动打开浏览器让你登录,按提示完成即可。
echo       (需要 Claude 的会员账号,详见 02 安装教程)
echo.
echo 之后想做片子,就照着 03_第一支片子_完整走一遍.md 来。
echo.
echo 装的过程中有任何一步飘红/报错,不用慌——
echo 打开 02_安装_照着做一遍.md,里面有手动兜底办法。
echo.
pause
endlocal
