---
tags: [类型/平台工程, 主题/网络排障, 主题/代理链路, 主题/Codex CLI]
---
# 代理环境变量遇 TUN 双重路由 · Codex CLI 流式超时排障

> 入档：2026-08-04
> 来源：一次「Codex CLI 执行指令时反复显示『正在重新连接 2/5』」的排障会话；本机 Windows 10 Pro + Mihomo Party（mihomo v1.x，TUN 模式 + 系统代理 127.0.0.1:7890 同时开启），Codex CLI 0.146.0-alpha.9.2
> 状态：已定位并修复，注册表 + 启动脚本 + vpn-guard 三处落地；验证 10 次取平均，WSS 重连端点延迟下降 85%

## 事实记录（不可修改区）

### 症状与首轮诊断

- 用户主诉：Codex CLI 在执行指令时反复遇到网络错误，界面显示"正在重新连接 2/5"。
- 机器环境：Mihomo Party 运行中，出口 IP 103.151.173.208（东京，日本，UTC+9），TUN 模式活跃，系统代理 127.0.0.1:7890 同时开启。
- `codex doctor` 诊断：数据库健康，219 个 active rollout 文件（2.1 GB），logs_2.sqlite 达 701 MB；无网络层报错。
- 日志数据库（`logs_2.sqlite`）检索到关键条目：
  - `codex_app_server_transport::transport::remote_control::websocket` — 反复 "connecting to app-server remote control websocket"（`wss://chatgpt.com/backend-api/wham/remote/control/server`）
  - `codex_models_manager::manager` — ERROR: "failed to refresh available models: timeout waiting for child process to exit"
  - `codex_memories_write::guard` — "failed to fetch rate limits err=error sending request for url (https://chatgpt.com/backend-api/wham/usage)"

### 关键发现：Codex 的 API 端点不是 api.openai.com

日志里所有请求都打向 `chatgpt.com/backend-api/...`，而非 `api.openai.com`。首轮测试只测了 `api.openai.com`，延迟正常（0.85s），差点误判"网络没问题"。切换到 `chatgpt.com` 端点后才暴露问题。

| 端点 | HTTP | TLS 握手 | 首字节 |
| --- | --- | --- | --- |
| `api.openai.com/v1/models` | 401 | 0.85s | 1.24s |
| `chatgpt.com/` | 403 | 1.09s | 1.39s |
| `chatgpt.com/backend-api/codex/models` | 401 | 2.54s | **3.83s** |
| `chatgpt.com/backend-api/wham/usage` | 401 | 1.55s | 2.01s |
| WSS `chatgpt.com/wham/remote/control/server` | 400 | **3.47s** | **4.57s** |

WSS 端点 4.57 秒——这正是日志中反复重连的那个连接。

### 根因：TUN + HTTP_PROXY 双重路由

注册表 `HKCU\Environment` 中存有用户级环境变量：

```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=http://127.0.0.1:7890
```

Clash Party 配置同时开启了系统代理（`sysProxy.enable: true`）和 TUN 模式。于是 Codex CLI 的请求走了**双重路由**：

```
Codex → HTTP CONNECT 隧道(127.0.0.1:7890) → mihomo 代理解析 → TUN 虚拟网卡 → VPN 隧道 → 目标
```

而 TUN 直连只需：

```
Codex → TUN 虚拟网卡 → VPN 隧道 → 目标
```

多出的 HTTP CONNECT 隧道层增加了 0.4–2.3 秒延迟。对短请求尚可忍受，但 **SSE 长连接和 WebSocket 连接对延迟极敏感**——握手阶段多出 2–4 秒，会触发客户端的超时重连逻辑，表现为"正在重新连接 2/5"。

### 对照实测（5 次 × 2 组）

| 组 | chatgpt.com/backend-api/codex/models 首字节平均 |
| --- | --- |
| 有 `HTTP_PROXY`（代理路径） | 1.660s |
| 无 `HTTP_PROXY`（TUN 直连） | 1.231s |
| 差值 | **0.429s** |

WSS 端点差距更大：

| | 有 `HTTP_PROXY` | 无 `HTTP_PROXY` |
| --- | --- | --- |
| WSS 总耗时 | 4.57s | **0.70s** |
| 改善 | — | **85%** |

### 修复

1. 从 `HKCU\Environment` 移除 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`（TUN 已在内核层路由，代理环境变量冗余）。
2. 更新 `NO_PROXY` 加入 `chatgpt.com,api.openai.com,*.openai.com`（安全网）。
3. vpn-guard 脚本（`app-vpn.ps1`）增加 TUN 活跃分支：显式将代理环境变量置空，避免子进程继承残留值。
4. Codex CLI 启动脚本（`launch-codex-cli.ps1`、`codex.cmd`）和 ChatGPT 桌面应用启动脚本（`launch-codex.ps1`）启动前清除代理环境变量。

### 修复后验证（10 次取平均）

| 端点 | 修复前 | 修复后 | 改善 |
| --- | --- | --- | --- |
| WSS 重连端点 | 4.57s | 0.70s | 85% ↓ |
| codex/models API | 2.30s | 1.47s | 36% ↓ |
| wham/usage API | 2.01s | 1.01s | 50% ↓ |
| api.openai.com | 1.73s | 0.77s | 55% ↓ |

## 一句话总结

**TUN 已在内核层接管全部流量时，HTTP_PROXY 环境变量不会让请求"更安全"——它只会让请求多走一层 HTTP CONNECT 隧道，对 SSE / WebSocket 长连接来说，多出的 2–4 秒就是"正在重新连接"和"正常工作"的区别。**

## 四条可复用 insight

### 1. TUN + 代理环境变量 = 双重路由，有 TUN 就不该设代理变量 ⚠️首次

TUN 模式在内核层创建虚拟网卡，接管**所有**出站流量（TCP / UDP / ICMP）。应用不需要知道代理的存在——它的数据包到了 TUN 网卡，mihomo 自然会路由。

但如果同时设了 `HTTP_PROXY` / `HTTPS_PROXY`，应用会**先**走 HTTP CONNECT 隧道连到代理端口（127.0.0.1:7890），**再**由 mihomo 代理解析后送入 TUN。这比 TUN 直连多了：

- 一次本地 TCP 连接（应用 → 127.0.0.1:7890）
- 一次 HTTP CONNECT 请求解析
- 代理层的连接管理和队列调度

实测代价：普通 API 请求多 0.4 秒，WSS 握手多 3.9 秒。

判据：**TUN 活跃时，代理环境变量是冗余的负担而非安全保障。** 只有在 TUN 关闭、仅靠系统代理时，代理环境变量才对 CLI 工具有意义（因为 Node / Rust / Go 写的 CLI 不读 Windows 注册表里的系统代理）。

> 与 [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] 互补：那篇讲"代理接管了 DNS 导致 ping 假绿"，本篇讲"代理接管了路由导致请求多走一跳"。共同点是——**多出来的代理层不总是好事，它有自己的代价。**

### 2. SSE / WebSocket 长连接对握手延迟远比短请求敏感 ⚠️首次

一次 API GET 请求多 0.4 秒，用户感知不到。但 SSE 流式连接和 WebSocket 连接的**建立阶段**如果多 2–4 秒：

- 客户端有连接超时阈值（Codex CLI 的重连逻辑：5 次重试）
- 握手期间没有任何数据流过，客户端无法区分"正在握手"和"连接挂了"
- 每次重连都要重新走 TLS 握手 + 认证，延迟叠加

本次 WSS 端点 4.57 秒 → 0.70 秒的改善，不是"快了一点"，而是**从"必然超时重连"到"稳定不重连"的质变**。

判据：**诊断流式连接问题时，不能只看"能不能连通"（HTTP code），必须测"握手要多久"（`time_appconnect`）和"首字节要多久"（`time_starttransfer`）。** 一个 200 的响应如果用了 5 秒才到，对 SSE 来说就是坏的。

### 3. 测错了端点就看不到问题 ⭐ 首次

Codex CLI 的 API 端点是 `chatgpt.com/backend-api/codex/...`，不是 `api.openai.com`。首轮测试只测了 `api.openai.com`，延迟 0.85 秒，完全正常——差点收工。

是日志数据库里的 `codex_http_client::client` 模块记录了真实请求 URL（`url=https://chatgpt.com/backend-api/codex/models?client_version=0.14...`），才发现测错了目标。

判据：**诊断"应用网络慢"时，必须从应用日志里确认它实际请求的 URL，不能凭文档或直觉假设。** 同一个服务（OpenAI）的不同域名（`api.openai.com` vs `chatgpt.com`）可能走不同的 CDN 路径、不同的 TLS 配置，延迟可以差好几倍。

> 这与 [[OpenAI兼容止于对话端点_多提供商视频接口分流与真key首测_v1]] 的"模型名不许猜要拉列表"同族：**别假设你知道应用在调哪个端点，去日志里看。**

### 4. 用户级环境变量是全局的——vpn-guard 注入只影响它启动的那个进程，注册表里的影响所有进程 ⚠️首次

vpn-guard 脚本（`app-vpn.ps1`）的设计是"只作用于被启动的那一个进程"——通过 `$inject` 字典在子进程启动前设置环境变量，退出后还原。这没问题。

但 `HKCU\Environment` 里的 `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` 是**全局**的——**所有**从资源管理器、终端、桌面快捷方式启动的进程都会继承。vpn-guard 不启动的进程（比如用户直接在终端里敲 `codex`）也受影响。

判据：**进程级注入和系统级设置是两回事。** vpn-guard 的进程级注入是"给需要代理的程序额外加一层"，系统级环境变量是"给所有程序默认加一层"。当 TUN 已全局接管时，后者是多余的，且 vpn-guard 的进程级还原逻辑管不到它。

## 顺手教训

- **`codex doctor` 是第一步**。它检查配置、认证、数据库完整性、搜索工具等，能快速排除"不是网络的问题"。本次 doctor 报告了 219 个 rollout 文件（2.1 GB）和 logs_2.sqlite 701 MB——虽然不是本次故障的直接原因，但说明日志清理是长期维护项。
- **`curl -w` 的 `time_appconnect` 和 `time_starttransfer` 是诊断代理延迟的金标准**。`time_appconnect` 测 TLS 握手完成时间（含代理 CONNECT 隧道），`time_starttransfer` 测首字节到达时间。这两个值一对比就能看出代理层加了多少钱。[[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] 已提出过这条判据，本次是第二次验证——它对"代理路径 vs 直连路径"的对比同样有效。
- **Windows 环境变量改了之后要广播 `WM_SETTINGCHANGE`**。用 `winreg.SetValueEx` 改了 `HKCU\Environment` 后，已运行的进程不会自动感知；新开的终端会。用 `user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, ...)` 可以通知 Explorer 等托盘应用刷新，但 CLI 进程仍需重启。
- **Mihomo Party 的 `external-controller` 可能是空字符串**（本次实测为 `""`），这意味着 Clash API 端口（9090/9097 等）不可用。不能依赖 API 来查节点信息或切换节点——得直接读配置文件。
- **`codex --help` 有 `doctor` 子命令**，但不接受 `config list` / `config show` 等子命令——配置覆盖通过 `-c key=value` 在命令行传入。Codex 的配置文件是 `~/.codex/config.toml`（TOML 格式），不是 JSON。

## 下次改进

- 诊断 Codex CLI 网络问题时，第一步跑 `codex doctor`，第二步查 `~/.codex/logs_2.sqlite` 里的 `logs` 表（按 `feedback_log_body` 列搜关键词），第三步才跑网络测试。
- 网络测试必须测日志里记录的真实 URL，不能假设端点。`SELECT DISTINCT feedback_log_body FROM logs WHERE feedback_log_body LIKE '%url=%' ORDER BY id DESC LIMIT 20` 是快速取真实端点的方法。
- 改完代理配置后，验证问句是"**重启终端后**还正常吗"——当前进程的环境变量不会变，新进程才反映注册表修改。
- 给 TUN + 系统代理同时开启的环境做排障时，先检查 `HKCU\Environment` 有没有 `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY`——有就是双重路由，去掉就是 TUN 直连。

## 关联文档

- ⭐ [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] —— 同族"代理层的代价"：那篇讲 fake-ip 让 ping 假绿（代理接管 DNS 的副作用），本篇讲 HTTP_PROXY 让请求多走一跳（代理接管路由的副作用）；共同判据=**`curl -w` 的 `time_appconnect` 和 `time_starttransfer` 是诊断代理延迟的金标准**（那篇首次提出，本篇第二次验证）
- [[ChatGPT_Windows桌面版安装排障与账号合规边界_v1]] —— 同目录、同一台机器的 Clash 环境；那篇讲四层排障法（资格 → 商店 → 网络 → 账号），本篇是其"网络链路"层的深入：代理环境变量与 TUN 的冲突
- ⚠️ [[OpenAI区域封锁与Worker就近执行陷阱_北美DO跳板_v1]] —— 同族"出口链路决定一切"：那篇讲调用方 IP 决定能否访问，本篇讲代理路径决定延迟高低
- ⭐ [[OpenAI兼容止于对话端点_多提供商视频接口分流与真key首测_v1]] —— 同族"别假设你知道端点"：那篇讲"OpenAI 兼容"只到对话端点，本篇讲 Codex CLI 的端点是 chatgpt.com 而非 api.openai.com；共同判据=**从日志里确认实际请求 URL，不靠文档假设**
- [[09_平台工程索引]] —— 平台工程区入口；本文归入「账号与访问」
