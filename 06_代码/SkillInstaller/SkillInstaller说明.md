---
tags: [类型/代码]
---
# SkillInstaller 说明

> 入档:2026-06-03
> 来源:`E:\工具\SkillInstaller`
> 性质:Codex / Claude Skill 安装辅助工具 + FFmpeg 检查与安装工具
> 上级索引:[[代码资产索引]]

## 用途

`SkillInstaller.pyw` 是一个 Windows GUI 小工具,用于帮助非技术用户完成三件事:

1. 选择单文件 `Skill.md`,安装到 `%USERPROFILE%\.codex\skills\<skill-name>\SKILL.md`;
2. 选择单文件 `Skill.md`,安装到 `%USERPROFILE%\.claude\skills\<skill-name>\SKILL.md`;
3. 检查 `ffmpeg` / `ffprobe` 是否可用,并可自动下载 FFmpeg 到 `%USERPROFILE%\.codex-tools\ffmpeg`,再写入当前用户 PATH。

它是 [[CodexSkillInstaller说明]] 的通用升级版:从“只服务 Codex”扩展为“Codex / Claude 双目标安装器”。

## 收录范围

本库只收录:

- `SkillInstaller.pyw`
- `build_exe_windows.cmd`
- `build_exe_windows.ps1`
- `SkillInstaller.spec`
- 本说明文档

不收录:

- `.git/`
- `build/`
- `dist/`
- `SkillInstaller.exe`
- PyInstaller 生成的 `.toc` / `.pyz` / `.zip` 构建产物

原因:知识库公开源码和构建方法,不直接发布二进制。

## 审核结论

源码没有发现明显恶意行为。主要外部操作是:

- 复制用户选择的 `.md` 文件到 `.codex/skills` 或 `.claude/skills`;
- 访问 `https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip` 下载 FFmpeg;
- 解压 FFmpeg 到用户目录;
- 修改当前用户级 PATH;
- 打开本地目录窗口。

入库时做了两处小修:

1. 安装目标已有 `SKILL.md` 时,先弹窗确认是否覆盖。
2. FFmpeg zip 解压从直接 `extractall` 改为 `safe_extract_zip`,防止压缩包出现路径穿越。

## 使用方式

运行源码:

```powershell
python .\SkillInstaller.pyw
```

打包 EXE:

```powershell
.\build_exe_windows.cmd
```

如果 PowerShell 执行策略阻止脚本,可用:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_exe_windows.ps1
```

成功后生成:

```text
dist\SkillInstaller.exe
```

## 适用边界

适合:

- 单文件 `Skill.md`;
- 依赖少、说明清楚的 Skill;
- 需要同时安装到 Codex / Claude 的 Skill;
- 需要 FFmpeg 的视频类 Skill 前置准备。

不适合:

- 复杂 Skill 仓库;
- 需要 Python / Node / helpers / 多文件项目结构的 Skill;
- 需要自动配置完整开发环境的场景。

一句话:

> 它解决的是“把一个合格 Skill.md 放到正确位置”,不是“把复杂仓库变成可运行工作流”。

## 后续改进

- 支持选择 Skill 文件夹而不只是单文件;
- 增加手动 FFmpeg zip 导入;
- 展示 FFmpeg 下载源和 SHA 校验;
- 支持记录安装日志;
- 打包产物发布前增加签名或哈希说明。

## 关联文档

- 入门指南:[[Skill安装与使用入门指南]]
- 旧版工具:[[CodexSkillInstaller说明]]
- 方法论复盘:[[AIGC_Skill到Remotion视频闭环]]
- 视频剪辑方法:[[蒙眼剪辑法_方法论笔记]]
- 代码资产入口:[[代码资产索引]]
