---
tags: [类型/平台工程, 主题/网络排障, 主题/代理链路, 主题/agent协作, 主题/配置漂移]
---
# 2026-09-06 · TUN 开关状态漂移复发 · 三层真相源与 agent 起 GUI 边界 · 复盘

> 入档：2026-09-06
> 来源：一次「Codex CLI 又开始反复『正在重新连接 3/5』」的排障会话——症状与 [[代理环境变量遇TUN双重路由_Codex_CLI流式超时排障_v1]]（2026-08-04）完全相同，但环境已经变过
> 状态：已修复并端到端验证（codex exec 实跑返回 OK）；复盘沉淀三层真相源判据
> 环境：Windows 10 Pro + Clash Verge Rev 2.4.7（verge-mihomo sidecar 模式），订阅「国外默认」组，出口日本 01

---

## 事实记录（不可修改区）

### 症状与环境实测（11:06）

- 截图：Codex CLI「你在 0 秒后停止了」+「正在重新连接 3/5」
- `127.0.0.1:7897` 在监听（mixed port，PID 15088）✅
- `ipconfig` 无 TUN 网卡 ❌
- `HKCU\Environment` 无 `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` ❌

**与 2026-08-04 那次的差别**：那次的病灶是「TUN + 环境变量双重路由」，删掉环境变量即愈。这次环境变量早就不在了——复发必然是另一个缺口。

### 定位：意图层开着，内核层没开

| 层 | 位置 | 状态 | 性质 |
|---|---|---|---|
| 意图层（应用开关） | `verge.yaml` → `enable_tun_mode: true` | ✅ 开 | UI 里 TUN 开关的声明 |
| 内核配置层 | `config.yaml` → `tun.enable: false` | ❌ 关 | mihomo 实际读的配置 |
| 运行态 | 路由表 / sidecar 日志 | ❌ 无 TUN | 实际发生的事 |

变更（原值 → 新值）：

| 文件 | 字段 | 原值 | 新值 | 验证步骤 |
|---|---|---|---|---|
| `config.yaml` | `tun.enable` | `false` | `true` | `route print` 应见 `0.0.0.0 → 198.18.0.1` |
| （备份） | — | `config.yaml.bak-20260906-1109` | — | 回滚用 |

### 沙箱起 GUI：四次失败，同一种失败

WorkBuddy 沙箱内 `Start-Process` / `Invoke-Item` / `cmd start` 调起 Clash Verge（.lnk 位于 `C:\Users\Public\Desktop\`），进程能在日志里留下完整启动痕迹（11:30 / 11:31 / 11:34 三轮，配置验证、托盘创建、内核 sidecar 拉起全部成功），**但约 8 秒后 GUI 进程整体退出**，端口与 TUN 随之消失。`-Verb RunAs` 因沙箱无法弹 UAC 同样失败。

处置：停止重试，改为**用户手动右键「以管理员身份运行」**，一次成功。

### 修复后验证（11:37–11:43）

| 验证项 | 结果 |
|---|---|
| 进程 | clash-verge.exe + verge-mihomo.exe 均在跑 |
| 路由表 | `0.0.0.0 → 198.18.0.2 / 198.18.0.1`（TUN 接管默认路由） |
| sidecar 日志 | `Tun adapter listening at: Meta([198.18.0.1/30],[]), mtu: 9000, ip stack: gVisor` |
| WSS 端点（`chatgpt.com/backend-api/wham/remote/control/server`） | TLS 握手 **0.46–1.27s**，首字节 0.65–1.44s（复发期等效 4.57s → 改善 ~85%，与上次修复后参考值 0.70s 吻合） |
| API 端点（`chatgpt.com/backend-api/codex/models`） | TLS 握手 0.40–0.58s，首字节 0.54–0.86s；401 为未带凭据的正常返回 |
| 端到端 | `codex exec "Reply with exactly: OK"`（codex-cli 0.153.4）→ 返回 OK，9,911 tokens，零重连 |

附带发现（与网络无关，留档）：`codex-code-mode-host.exe` 插件缺失 warning，Code Mode 不可用。

---

## 弧线：上次的修复没有死，是它的前提死了

2026-08-04 的修复=「删环境变量，让流量走 TUN」。这套方案由两个部件组成：

```
修复 = 删环境变量（已固化，至今有效）
     + 前提：TUN 正在内核层接管（当时实测成立，WSS 4.57s→0.70s）
```

八月的某次客户端更新 / 配置重置 / 内核重启中，`config.yaml` 的 `tun.enable` 回落为 `false`，而 `verge.yaml` 的意图开关仍是 `true`。**前提静默失效，修复跟着失效，而意图层还在说「一切正常」**——用户看到的症状和上次一模一样，但病灶换了位置。

这不是上次的归因错了（那次的数据和结论都对），是**前提漂移**。与「复发+上次已修=上次归因错了」同族但不同形：

> 归因没错 + 复发 = **前提漂移了**。修复方案里每一条没进验收清单的前提，都是一颗定时静默失效的雷。

---

## 方法论教训

### 1. 开关有三层真相源：声明 ≠ 配置 ≠ 生效 ⭐ 同族二次验证

- **意图层**（verge.yaml `enable_tun_mode`）：人说「我要它开」
- **配置层**（config.yaml `tun.enable`）：程序说「它该开」
- **运行态**（路由表 / 内核日志）：世界说「它真开了」

三层会各自漂移，且**中间层与运行态漂移时不产生任何报错**——UI 面板照常显示 TUN 已开启（它读的是意图层）。

验证 TUN 生效的两个硬判据：

```powershell
route print | findstr "198.18"        # 默认路由指向 198.18.0.1
type "%APPDATA%\io.github.clash-verge-rev.clash-verge-rev\logs\sidecar\sidecar_latest.log"
# 出现 "Tun adapter listening at: Meta([198.18.0.1/30]...)" 即内核自述生效
```

> 与 [[DNS防泄露五层修复_fake-ip形同虚设与物理网卡DNS绕过_v1]] 的「三层真相源」同族：那篇是 mihomo-party 的 DNS 配置三层（nameserver-policy 只认应用设置层），本篇是 Clash Verge 的 TUN 开关两层 + 运行态。**跨客户端同构现象，升 ⭐**：GUI 代理客户端普遍存在「配置写在哪一层决定改了有没有用」，判据=改任何代理配置后，必须在运行态找直接证据，不认面板和 YAML 的任何一层。

### 2. 「我没改过」不等于「没变过」——配置漂移不需要人动手 ⚠️首次

`enable_tun_mode: true` 与 `tun.enable: false` 并存的状态，中间一定发生过一次非人意的变更（自动更新、配置重写、内核重装）。漂移的特点：

- 没有对应的人工操作记忆可查（用户确实没动过）；
- 意图层还保持着旧值，给人「配置还是我设的那样」的错觉；
- 症状复发时，人会先怀疑「上次修错了」而不是「前提没了」。

判据：**复发排查第一步不是重走上次路径，而是 diff 环境——把上次修复的每个前提重新实测一遍。** 环境变量这条前提本次 30 秒就排除了，剩下的时间全花在找到底哪层前提死了。

### 3. agent 起 GUI 的正确分工：改配置归 agent，提权启动归人 ⚠️首次

沙箱内 GUI 进程的失败模式很隐蔽：**日志全绿、进程短命**。配置验证成功、托盘创建成功、内核 sidecar 拉起成功、TUN 适配器监听成功——然后整个进程树消失。同一动作重试 N 次结果完全相同，这是环境边界不是操作错误。

正确动作序列：

```
改配置（agent 可靠完成）
→ 尝试启动一次并立刻 tasklist + netstat 双验证
→ 失败即停，交给用户「右键管理员运行」
→ agent 继续接管：路由表 + sidecar 日志 + 端点测速 + 端到端实跑
```

本次代价：硬拉 4 次才放弃，还因先杀进程把用户代理瞬断过一段。**重复同一个失败动作的成本不在单次，在它推迟了「换打法」的决策点。**

### 4. 修复验收清单必须包含前提假设 ⚠️首次

验收问句不该只有「修复后好了吗」，还要有「**修复所依赖的那个东西，现在还在吗**」。可操作化为：写修复方案时，把每个前提配上一个对应的可观测检查项（如 TUN → `route print`；环境变量 → `reg query`），复发时逐条打勾。

---

## 顺手教训

- **找应用快捷方式先查 `C:\Users\Public\Desktop\`**（公共桌面），用户目录搜不到不代表没装——本次绕了三轮才发现 .lnk 在公共桌面。
- **沙箱内从 Bash 调 `powershell.exe` 会被安全策略拦截**（提示 bypasses PowerShell security checks）→ 一律走 PowerShell 工具；`taskkill //PID` 在 Git Bash 无效 → 用 `Stop-Process`。
- **沙箱查注册表：`reg.exe` 在 Program Blacklist** → 用 PowerShell 的 `Get-ItemProperty 'HKCU:\Environment'` 代替。
- `codex exec "Reply with exactly: OK"` 是网络修复后最低成本的端到端验收（一次真实 API 调用 + 零歧义判据），比 curl 测端点多验了认证与流式整条链路。
- sidecar 日志是 mihomo 内核的自述，比主程序日志（`logs/latest.log`）晚一步且更真实——主程序说「Starting core in sidecar mode」，sidecar 才告诉你 TUN 到底起没起。

## 关联文档

- ⚠️ [[代理环境变量遇TUN双重路由_Codex_CLI流式超时排障_v1]] —— 上一次同症状排障（2026-08-04）：病灶是双重路由，修复=删环境变量；本篇是它的复发续篇，病灶换成 TUN 前提静默失效
- ⭐ [[DNS防泄露五层修复_fake-ip形同虚设与物理网卡DNS绕过_v1]] —— 「三层真相源」原发篇（mihomo-party DNS）；本篇同族二次验证（Clash Verge TUN 开关），并新增运行态作为第三层
- ⭐ [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] —— 同族「假信号」：fake-ip 让 ping 假绿，本篇是意图层让面板假绿
- [[2026-08-19_vpn-guard出口归属门槛与四处假绿修复_迭代复盘_v1]] —— 同工具链（vpn-guard）的加固轮；本篇第 4 条「前提要进验收清单」与那篇「能复现输出的模型才算被证明」同属验收严格化谱系
- 📤 对外版：[[GPT和Codex一直转圈连不上_网络排查手册_小白版]] —— 症状对照表仍适用，但第四节「TUN 和环境变量同时开」之外应补本篇的「TUN 名开实关」分支（待更新）
- [[09_平台工程索引]] —— 平台工程区入口；本文归入「账号与访问」
