---
tags: [类型/平台工程, 主题/Windows桌面应用]
---
# 炉石传说安装被拒：UBR 判断假正常系统与 Win10 原地升级

> 入档：2026-09-03
> 来源：本机（DESKTOP-JGE3PDQ）战网安装《炉石传说》报错的实测修复，系统 Windows 10 Pro
> 状态：已修复（升级至 22H2 / Build 19045.2965）；诊断路径与「原地升级」方法可复用

> 一句话律：软件报「操作系统不满足最低要求」，先 `winver` 看 Build 号，而不是清缓存、重装客户端——「版本号看着正常」的系统，UBR 可能只有 264，实为六年未更新的假正常系统。

## 现象

暴雪战网安装《炉石传说》时报错：

> 我们无法安装炉石传说，因为您的操作系统未能满足运行该游戏的最低配置要求。您的系统: Windows 10

## 诊断路径（只读，无副作用）

1. 先确认真实版本，不要被「Windows 10」这个大版本误导：

```powershell
winver   # 看 DisplayVersion + Build 号
```

或读注册表（无需 GUI）：

```powershell
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName /v DisplayVersion /v CurrentBuild /v UBR
```

2. 拿 Build 号去对照软件的最低系统要求——**要求给的是具体 Build，不是「Windows 10」**：

| 项目 | 本机实测 | 炉石国服最低要求 |
|---|---|---|
| 版本 | Windows 10 2004 | 21H1 |
| Build | 19041 | 19043 |
| UBR | **264** | 正常 3000+ |

硬件全部远超要求（13 代 i5 / 32G / RTX 4060），瓶颈只在系统版本。

## 根因

两层：

1. **直接原因**：系统是 Windows 10 2004（Build 19041），低于炉石国服最低要求的 21H1（Build 19043），被战网直接拒装。非战网缓存、非客户端误判。

2. **为什么系统停在 2004 六年没动**：`UBR = 264` 是关键信号。Win10 20H1 打满补丁后 UBR 应在 3000 上下，264 说明系统停留在 2020 年夏天的初始状态——**版本号正常，实则六年未成功更新过**。

   Windows Update 组件本身健康（服务全 Running、无组策略禁用、未暂停），问题出在下载被系统性中断：更新协调器进程 `MoUsoCoreWorker.exe` 长期独占 `C:\Windows\SoftwareDistribution\ReportingEvents.log` 文件句柄，导致缓存目录无法重置、下载编排反复中断（据诊断日志：221 次 `AGENT_DOWNLOAD_CANCELED`，仅 4 次成功）。

## 修复

1. **先修 Windows Update 病灶**（否则即便原地升级，后续也会继续更新失败）：
   - 停 WU 相关服务 → 结束 `MoUsoCoreWorker.exe` → 备份并重置 `C:\Windows\SoftwareDistribution`（重命名为 `.bak-日期`）→ 重启服务。
2. **原地升级到 22H2**：用微软官方「Windows 10 更新助手」（`Windows10Upgrade9252.exe`，官方直链 `https://go.microsoft.com/fwlink/?LinkID=799445`），双击点「立即更新」。

关键认知：**2004 → 21H1 → 22H2 是同一内核树（都是 19041 内核，靠启用包切换），原地升级即可，不用重装系统**，文件、软件、账号全部保留。升级后 `winver` 应显示 22H2 / 19045（本例实测 19045.2965）。

## 教训

- **「Windows 10」不等于「满足要求」**。软件最低要求给的是具体 Build（如 21H1/19043），要拿 `winver` 的 Build 号去对照，不能只看大版本。
- **UBR 是判断「假正常系统」的快捷信号**。版本号对、但 UBR 异常低（几百 vs 正常 3000 上下），说明系统长期没更新，背后往往是隐藏的系统性问题。
- **升级/安装类失败，先查系统版本资格，再谈缓存与重装**。清缓存、重装客户端是常见错误方向——本例根因在系统层，与战网缓存、误判无关。
- **系统更新长期失败的隐蔽故障模式**：更新组件「健康」但下载「反复中断」，元凶可能是某进程独占文件句柄。查 `ReportingEvents.log` 的 `AGENT_DOWNLOAD_CANCELED` 计数可快速定位。

## 关联文档

- [[09_平台工程索引]] —— 平台工程区入口
- [[ChatGPT_Windows桌面版安装排障与账号合规边界_v1]] —— 同为「Windows 桌面软件安装失败」排障，但根因在账号/网络链路层；本篇补上「系统版本资格」这一层的展开（对应其第一层「核对系统要求」）
- [[UAC关闭导致提权入口消失_内置Administrator与EnableLUA=0双重归因_v1]] —— 同属 Windows 系统层排障，同为「假正常」信号（UAC 关闭 vs UBR 过低），排查都始于只读读数而非盲目改配置
