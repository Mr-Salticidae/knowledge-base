---
tags: [类型/平台工程]
---
# Claude 桌面版接入 LibTV 远程 MCP:临时电脑环境与会话重连

> 入档:2026-09-26
> 来源:76_清月 项目(作者旅行中,用一台公用电脑从零搭环境,两天内完成立项 → 成片 → 三平台发布)
> 验证状态:⚠️首次(一台机器,Windows 10 LTSC + Claude 桌面版 Code 页签)

## 一句话

在一台陌生电脑上,Claude 桌面版可以通过 **LibTV Remote MCP** 直接调 Seedance 2.5 出片,不用装 LibTV CLI。要过三道坎:**桌面版是 MSIX 打包,会话里看到的路径和外部终端里的真实路径不是同一个**;**OAuth 登录必须在交互终端里跑**;**MCP 中途掉线时切换一次会话目录就能重连**。走之前要把 GitHub、LibTV、Chrome 的登录态都清掉。

## 如何使用

### 1. 加 LibTV 远程 MCP

```text
claude mcp add --transport http --scope user LibTV https://mcp.liblib.tv/mcp
claude mcp get LibTV
```

- `--scope user` 写进用户配置,之后新开的会话都能用。
- 授权要跑 `claude mcp login LibTV`。它会打开浏览器让作者登录 LibTV 并同意授权。**这条命令需要 TTY**,在助手的后台 shell 里跑会直接失败。要在桌面版的终端页签里跑,或者请作者在自己的终端里跑。登录和授权都由作者本人完成。
- **2026-09-28 补丁:助手自己给它一个伪终端**(工作站主机实测,作者要求"自己解决授权问题,不要烦我"):
  - `pip install pywinpty`(清华镜像对它返回 403,改用 `-i https://pypi.org/simple`)。
  - 用 `winpty.PtyProcess.spawn` 在 ConPTY 里跑 login,设环境变量 `BROWSER=echo`,不让它自己弹浏览器,从输出里读授权链接。它会在 localhost 上等回调。
  - 用**作者已经登录 LibTV 的 Chrome**(浏览器扩展)打开授权链接,点"允许",回调成功。内置浏览器没登录,只给扫码。
  - `~/.local/bin/claude` 可能是没有 `mcp login` 的旧版,要用桌面版自带的 `claude.exe`。
  - 不要"结束授权进程再往伪终端写回调地址",自动审查会拦。
  - 授权成功后,**当前会话不会自动出现 LibTV 工具**,要重载会话(切一次工作目录或新开会话)。

### 2. MSIX 路径重定向

Claude 桌面版是 MSIX 包,`AppData` 会被重定向:

| 会话里看到的 | 外部终端里的真实位置 |
|---|---|
| `%APPDATA%\Claude\…` | `C:\Users\<用户>\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\…` |
| `%LOCALAPPDATA%\Programs\MinGit\…` | `…\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\Programs\MinGit\…` |

所以在外部终端里找 `claude.exe` 或助手装的 MinGit,要用右列的路径。本次 `claude.exe` 在 `…\LocalCache\Roaming\Claude\claude-code\<版本号>\claude.exe`。

### 3. 其他工具

- **git**:装 MinGit(免安装版)。它不在 PowerShell 工具的 PATH 里,每次要写全路径 `%LOCALAPPDATA%\Programs\MinGit\cmd\git.exe`。
- **GitHub 私有仓库**:非交互 shell 里认证会失败。让作者在终端里跑一次 `git.exe ls-remote <仓库地址>`,Git Credential Manager 会弹出浏览器登录,凭据存进 Windows 凭据管理器,之后助手就能 push。
- **长路径**:桌面版的 scratch 工作区路径本身就很长,在里面 `git clone` 会报 `'$GIT_DIR' too big`。克隆到 `C:\Users\<用户>\<仓库名>` 这样的短路径。
- **大仓库**:作品档案库用 `--filter=blob:none --sparse` 轻量克隆,只检出当前项目目录。
- **ffmpeg / Real-ESRGAN**:都有解压即用的 Windows 包(BtbN 构建、xinntao 发布页),放在 `C:\Users\<用户>\tools\`,不需要管理员权限。用法见 [[AI视频本机超分_RealESRGAN_x4plus与闪烁检查_v1]]。

### 4. 用 LibTV Remote MCP 出片的顺序

1. `doctor` 确认身份与连接 → `create_project` 建画布项目。
2. 上传参考图:`upload_ticket` → 用返回的地址 PUT 到 OSS → `upload_complete`。
3. `create_node` 建图片节点,**再用 `update_node` 把 `data.url` 绑上**。只建不绑,生成时那张图不算参考。
4. `validate_generation_plan` 预检 → `generate_video`,每条带一个稳定的 `idempotencyKey`(例如 `项目-幕-轮次-日期`),防止重试时重复扣费。
5. 看结果不必下载整条视频。存储端是 OSS,URL 后加截帧参数就能取单帧:`?x-oss-process=video/snapshot,t_<毫秒>,f_jpg,w_360,ar_auto`。**不要加 `m_fast`**,它会跳到最近的关键帧,不是你要的那个时间点。
6. 回执里没有积分消耗。要记成本,得另外查余额。

### 5. MCP 中途掉线

本次出 r3 前 LibTV 的工具全部消失。在桌面版里用 `change_directory` 把会话目录切到项目子目录,会话重载时 MCP 重新连上,之后照常提交。切目录前先征得作者同意。

### 6. 浏览器:两个浏览器各有用途

- 桌面版内置浏览器适合看本地页面、读文档。chatgpt.com 在里面会触发 Cloudflare 人机验证。**不要尝试绕过**,改用作者自己的 Chrome。
- Claude in Chrome 用的是作者已登录的 Chrome。它只能操作**自己标签组里的**标签页,单个上传文件上限 10MB。投稿细节见 [[多平台同步投稿_发布页字段与浏览器辅助清单_v1]]。
- 看本地 HTML 工具页(例如音画同步测量页):`file://` 在内置浏览器里打不开,可以用 PowerShell 的 `HttpListener` 起一个本地小服务。

### 7. 离开前清登录态(公用电脑)

```text
cmdkey /delete:git:https://github.com
<claude.exe 真实路径> mcp logout LibTV
```

Chrome 里还要手动退出:GitHub、LibTV、ChatGPT、各发布平台,以及 Claude 扩展本身。

## 边界

- 一台机器、一个桌面版版本(Claude Code 2.1.281)。MSIX 的包名后缀 `pzs8sxrjxfjjc` 是否因安装渠道而变,没验证。
- 「切目录能重连 MCP」只发生过一次,原因没查清楚。

## 关联文档

- 来源复盘:[[2026-09-26_清月_单条15秒角色PV_立项到三平台发布_复盘_v1]]
- 同族(GitHub 凭据走 Windows 凭据管理器):[[Git初始化已有工作区并建GitHub仓库_嵌套仓库submodule引入与MCP无权限ghCLI兜底_v1]]
- 同一台电脑上的后期与发布:[[AI视频本机超分_RealESRGAN_x4plus与闪烁检查_v1]] · [[多平台同步投稿_发布页字段与浏览器辅助清单_v1]]
- 模型行为(本通道的样本已补入):[[Seedance2_5_行为规律_v1]]
- 伪终端授权补丁的来源(工作站主机):[[2026-09-29_右下角的池塘_游戏宣传微电影_实录混剪到双语字幕发布_复盘_v1]]
