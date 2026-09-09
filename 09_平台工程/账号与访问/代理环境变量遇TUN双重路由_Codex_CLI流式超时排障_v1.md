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

## 复发记录（2026-09-08）：同症状，不同根因

**症状**：Codex CLI（v0.153.4）再次反复「正在重新连接 4/5」，与本文主案一致。

**诊断顺序与实测**：

1. 先复查旧根因是否回滚：`HKCU\Environment` 仍无 `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`（本文修复保持完好），TUN 在线（Meta Tunnel，198.18.0.1）——双重路由**未复发**。
2. 端点小包测试：WSS 端点 TLS 握手 1.44s、首字节 1.9s，401/426 正常返回——**偏慢但能通，容易误判为"没大问题"**。
3. 吞吐实测现形：`speed.cloudflare.com` 仅 **11.4 KB/s**（≈0.09 Mbps），TLS 握手 8.99s——命中对外手册第五节「节点带宽垫底」。

**修复与验证**：Clash Verge GUI 手动切节点后复测：吞吐 11.4 KB/s → **8.49 MB/s（≈68 Mbps，745 倍）**；WSS 首字节 1.9s → 0.63-0.77s；models 端点 → 0.69-0.88s，全部回到或优于本文修复后基准。

**环境变化记录**：代理客户端已从 Mihomo Party 迁移至 **Clash Verge**（D:\Clash Verge\，verge-mihomo，混合端口 7897）；`external-controller` API（9090/9097）依然不可用，切节点只能 GUI 手点（脚本切换不落盘 + 全节点扫描造成账号跨国跳变，均不可用）。

**三条增量判据**：

- **同一症状复发时，先复查旧根因是否回滚，再按排查手册顺序下探**——本例旧根因未回滚，下探两节命中节点带宽。不要凭"上次修过什么"直接套修法。
- **小包能通 ≠ 链路健康**：401/426 错误页只有几 KB，11 KB/s 的链路也能 2 秒内返回；但 models 刷新、SSE/WSS 长连接必然超时。诊断流式应用问题，吞吐实测不可省略——这是「`time_appconnect`/`time_starttransfer` 金标准」的互补面（第三次实证）：时延字段看握手，吞吐字段看载重，缺一不可。
- **诊断环境自身可能注入代理**：在 IDE/沙箱类工具（如 WorkBuddy）的终端里测用户真实链路时，会话可能自带 `HTTP_PROXY`（本次为 127.0.0.1:64519），必须 `curl --noproxy '*'` 才能复刻 Codex 进程（无代理变量、走 TUN）的真实视角。

## 复发记录·续（2026-09-08 下午）：二阶根因——26MB 大会话 × WS 传输

换节点后用户反馈「修复失败，还在转圈」。深挖后锁定**第二阶根因**，比节点问题更本质：

### 错误本体与故障画像

- 日志金句：`stream disconnected before completion: failed to send websocket request: IO error: 远程主机强迫关闭了一个现有的连接。 (os error 10054)`
- 画像：**WSS 握手每次成功（1-2 秒 101 升级），发送 responses 请求时被 RST**，5/5 重试稳定复现，无一幸免。
- 关键数据（日志 `Compressed request body` 记录）：出问题的 turn 属于 9/7 开启的长会话，**请求体 26.4MB → zstd 压缩后 19.3MB**（≈168K tokens 上下文）；同时段轻量 turn 仅 0.1MB，全部正常。

### 排除过程（每项都有实测）

1. **WS 帧存活探针**（Python 纯 socket 复刻 Codex 握手+发帧，绕过 IDE 沙箱代理注入）：4KB 未压缩帧、协商 permessage-deflate 后的压缩帧，三轮全部收发正常——**小帧过、大流死**。
2. **代理变量路径分歧**：HKCU/HKLM 注册表均无 PROXY 变量；Codex（Rust reqwest）与探针（Python socket）同走 TUN 直连——路径一致，排除。
3. **自动回退验证**：重试 5/5 耗尽后触发 `falling back to HTTP`（codex_core::client WARN），随后 `POST /backend-api/codex/responses 200 OK`，turn 正常推进——**HTTP 通道能传 19MB，WS 通道不能**。

### 机制结论

- Codex 0.153.4 的默认传输由服务端 models 清单的 `prefer_websockets: true` 驱动（0.146 时代是 SSE）——**版本升级把流式传输从 HTTP/SSE 换成了 WebSocket**。
- 大会话（≈20MB 级上行）的 WS 流在当前代理隧道上被 RST；HTTP/SSE 大上传稳定。8 月同机同链路无此问题，正是 SSE 时代的缘故。
- 用户感知的「转圈」= 每次 turn 先烧 ~15 秒 WS 重试（5 次退避）→ 回退 HTTP → 19MB 上行 → 168K token 大上下文推理，分钟级。

### 修复（按优先级）

1. **`/compact` 或开新会话**——请求体降回 0.1MB 级，WS 传输恢复秒级响应（轻量 turn 已实证正常）。
2. 长会话必须继续时：容忍每 turn 的「15 秒重试 + 分钟级回退传输」，别在重试中途 Esc（中断会丢掉自动回退的机会）。
3. 会话上下文逼近 `auto_compact_scope_limit`（本例 244800）前主动 compact。

### 四条增量判据

- **「握手通、发送 RST」先查请求体大小**（日志搜 `Compressed request body`），别只怀疑链路杀协议——本例链路对小帧完全放行。
- **探针体量要对标真实负载**：4KB 探针通过 ≠ 20MB 流通过。诊断工具复刻的是「应用行为」而不只是「协议握手」。
- **TUN 模式下的 10054「远程主机强迫关闭」要按分层解读**：可能是隧道上游、节点出口或服务端网关的 RST 被转发下来，不等于「目标服务器拒绝你」。
- **feature flag 扫描先行**：怀疑新版客户端行为时，先扫二进制里的配置键/环境变量（本例确认 0.153.4 无禁用 WS 的官方开关），再决定修链路还是修用法。

## 关联文档

- [[DNS防泄露五层修复_fake-ip形同虚设与物理网卡DNS绕过_v1]] —— 同机同环境续篇(2026-08-11):本篇修复第 2 条把 OpenAI 域名加进 NO_PROXY 当「安全网」,续篇在「TUN 全权 + 用户级代理变量已不存在」的新架构下将其清回标准值——前提已消失,属架构演进不是纠错;续篇讲 DNS 解析层,本篇讲路由层
- ⭐ [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] —— 同族"代理层的代价"：那篇讲 fake-ip 让 ping 假绿（代理接管 DNS 的副作用），本篇讲 HTTP_PROXY 让请求多走一跳（代理接管路由的副作用）；共同判据=**`curl -w` 的 `time_appconnect` 和 `time_starttransfer` 是诊断代理延迟的金标准**（那篇首次提出，本篇第二次验证）
- [[ChatGPT_Windows桌面版安装排障与账号合规边界_v1]] —— 同目录、同一台机器的 Clash 环境；那篇讲四层排障法（资格 → 商店 → 网络 → 账号），本篇是其"网络链路"层的深入：代理环境变量与 TUN 的冲突
- ⚠️ [[OpenAI区域封锁与Worker就近执行陷阱_北美DO跳板_v1]] —— 同族"出口链路决定一切"：那篇讲调用方 IP 决定能否访问，本篇讲代理路径决定延迟高低
- ⭐ [[OpenAI兼容止于对话端点_多提供商视频接口分流与真key首测_v1]] —— 同族"别假设你知道端点"：那篇讲"OpenAI 兼容"只到对话端点，本篇讲 Codex CLI 的端点是 chatgpt.com 而非 api.openai.com；共同判据=**从日志里确认实际请求 URL，不靠文档假设**
- [[09_平台工程索引]] —— 平台工程区入口；本文归入「账号与访问」
- 📤 对外版：`08_对外分发/GPT和Codex一直转圈连不上_网络排查手册_小白版.md` —— 以本篇症状（Codex CLI「正在重新连接」）为头号元凶，合流同目录另五篇与 vpn-guard README 的小白排查手册；2026-08-31 经飞书助理小桁发布为云文档（互联网可阅读只读）：https://ncnnb044q88x.feishu.cn/docx/OvFidNmQjoyMgpxsP7Ac9iEznke；另有公众号版与 8 张 MJ 配图提示词（同目录 `_公众号版.md` / `_公众号配图MJ提示词.md`，沿用 sref 5692463053 navy 现代极简）
