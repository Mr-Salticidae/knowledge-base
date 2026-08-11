---
tags: [类型/平台工程, 主题/网络排障, 主题/代理链路, 主题/DNS防泄露]
---
# DNS 防泄露五层修复 · fake-ip 形同虚设与物理网卡 DNS 绕过

> 入档：2026-08-11
> 来源：一次「拉取 vpn-guard 最新代码并本地部署」引发的 DNS 泄露排查演练；本机 Windows + Clash Party（mihomo-party fork，TUN + 系统代理同开），出口香港节点
> 状态：已修复并实测验证——bash.ws 主动实测从「3/3 解析器在中国大陆」到「全部解析器在出口国 Hong Kong」

## 事实记录（不可修改区）

### 起点

`vpn-leak-audit.ps1` 自查 8 项中第 6 项「DNS 解析路径」FAIL：对随机子域发起真实解析后回查，**3/3 个实际应答的解析器都在中国大陆**（中国电信 61.151.230.52、114DNS 出口 221.231.139.96、114DNS IPv6 240e:978:4002:0:114:114:114:102），而出口在香港。静态配置检查同时显示：Mihomo 网卡 DNS = 198.18.0.2（fake-ip 特征，OK），以太网卡 DNS = 114.114.114.114（WARN）。

### 修复链条（五层，每层都靠主动实测逼出下一层）

| 轮次 | 改动 | 复测结果 | 暴露的下一层 |
|---|---|---|---|
| 1 | `mihomo.yaml` 的 `fake-ip-filter` 移除 `"*"` | 仍 FAIL，3/3 国内 | fake-ip 生效了，但 `GEOIP,CN` 规则迫使内核对未匹配域名本地解析（走国内 DoH） |
| 2 | `respect-rules: true` + nameserver 换 dns.google/cloudflare-dns（走隧道）+ geosite:cn 国内 DoH 兜底 | 进步：Cloudflare HK ×2 出现；但 Google US ×1 + 国内 ×1 仍在 | Google DoH 出口地理为美国（非泄露但地理不匹配）；`direct-nameserver` 并发查询嫌疑 |
| 3 | nameserver 只留 cloudflare-dns，`direct-nameserver` 置空 | Google US 消失；但 114DNS 出口 ×2 仍在 | mihomo 配置已完全干净，泄露源在 mihomo 之外——Windows 物理网卡 DNS |
| 4 | 发现 work/config.yaml 每次由 App 重新生成，`nameserver-policy` 只认订阅 profile 或应用设置层（`config.yaml` 的 `useNameserverPolicy`+`nameserverPolicy`），写在 mihomo.yaml 里会丢 | geosite:cn 策略改写到 config.yaml 后持久化 | （配置分层问题，非泄露路径） |
| 5 | 物理网卡 DNS 从 114.114.114.114 改为 198.18.0.2（隧道 fake-ip DNS，需管理员） | ✅ 全绿：解析器全部 Cloudflare HK，与出口一致 | 收尾 |

### 根因分解（两个独立的泄露源）

**泄露源 A：mihomo 的 fake-ip 名存实亡。** 配置写着 `enhanced-mode: fake-ip`，但 `fake-ip-filter` 第一条是 `"*"`——在默认黑名单模式下，`*` 匹配所有域名，等于**所有域名都绕过 fake-ip 做真实解析**，而真实解析的上游是国内 DoH（doh.pub / 阿里）。模式声明与实际行为完全脱节。

**泄露源 B：Windows 多网卡并发 DNS 解析绕过 TUN 劫持。** 物理网卡配了 114.114.114.114。Windows 的 dnscache 会并发查询所有 Up 状态网卡的 DNS：发向 Mihomo 网卡（198.18.0.2）的查询被 TUN 劫持进隧道，但发向以太网卡 114.114.114.114 的查询**从物理网卡直接出门**，TUN 的 `dns-hijack: any:53` 根本看不到这些包。修复后实测证据：114DNS 的 v4/v6 出口同时从 bash.ws 回查中消失。

### 附带对账：NO_PROXY 里的 OpenAI 域名

本次发现用户级 `NO_PROXY` 含 `chatgpt.com,*.chatgpt.com,api.openai.com,*.openai.com,cdn.openai.com`，清回标准值 `localhost,127.0.0.1,::1`。**注意这不是无主垃圾**：回查 [[代理环境变量遇TUN双重路由_Codex_CLI流式超时排障_v1]]，它是 2026-08-04 那次排障留下的「安全网」（当时的架构是：万一代理变量被重新设上，OpenAI 流量绕过 HTTP 代理层直接进 TUN）。本次架构已演进为「TUN 全权接管 + 用户级代理变量不存在 + app-vpn 进程级注入自管 NO_PROXY」，安全网的前提已不存在，移除是架构演进而非纠错——但按 [[有意改动不是故障_v1]] 的要求，此处显式对账记录，不当成「修复了一个错误」。

## 一句话总结

**代理工具的「模式声明」和「网卡的静态配置」都只是声明，DNS 是不是真的走隧道，只有对随机子域发起真实解析、回查实际应答解析器的归属国才知道——被动检查全程绿灯，主动实测一次就现行。**

## 五条可复用 insight

### 1. `enhanced-mode: fake-ip` 写着 ≠ fake-ip 在生效 ⚠️首次

Clash/mihomo 系的 `fake-ip-filter` 默认是**黑名单**（列出的域名不用 fake-ip）。mihomo-party 系客户端的默认模板里第一条是 `"*"`——所有域名命中黑名单，fake-ip 被架空成 redir-host 行为，每个域名都做真实本地解析。

判据：**审计 DNS 是否走隧道，别看 `enhanced-mode` 声明，要看 `fake-ip-filter` 里有没有 `"*"`，并最终以主动实测（解析器归属国）为准。** 同族：[[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] 的「永远绿的信号最没用」——声明层和信号层都可能撒谎，只有真实链路上的实测不会。

### 2. GEOIP 规则是防泄露配置的隐藏泄漏点 ⚠️首次

订阅规则末尾几乎必有 `GEOIP,CN,DIRECT` + `MATCH,代理`。对**没命中任何域名规则**的域名，mihomo 为了判定 GEOIP 必须先本地解析它——用配置里的 nameserver。如果 nameserver 是国内 DoH，这个「兜底解析」就把域名交给了国内运营商系。

关键的不对称：**已命中域名规则的流量（GPT 等）始终在出口端远端解析，一直是安全的；漏的恰恰是"没安排过的"域名。** 修复范式：`respect-rules: true` + nameserver 换境外 DoH（随路由走隧道）+ `nameserver-policy` 里 `geosite:cn` 用国内 DoH 保住国内站点的解析速度与 CDN 亲和。

判据：**检查防泄露配置时，重点审"未匹配域名"的解析路径，不是已匹配域名的。** 已匹配路径是配置的作者想过的，未匹配路径才是没人想过的。

### 3. 客户端的配置真相是分层的，改错层等于没改（二次验证 ⭐⭐）

mihomo-party（Clash Party）三层：`mihomo.yaml`（GUI 内核设置，持久）、`config.yaml`（GUI 应用设置，持久）、`work/config.yaml`（**每次由 App 重新生成，手改会被覆盖**）。且重新生成时字段来源不对称：`fake-ip-filter`/`nameserver` 认 mihomo.yaml，`nameserver-policy` 只认订阅 profile 或 config.yaml 的 `useNameserverPolicy`——写在 mihomo.yaml 里的同名项**静默丢失**。

判据：**改 GUI 客户端的配置，先搞清楚这个字段的真相源在哪一层，改完重启一次让它重新生成，再 diff 生成的运行配置确认字段还在。** 这是 [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] 里「运行态改了≠配置落盘（重启回滚）」的第二次验证，本次补全了下一句：**落盘了也可能没落到会生效的那一层。**

### 4. TUN 的 DNS 劫持管不到从物理网卡直接发出的查询 ⚠️首次

直觉模型：「TUN 开了 + `dns-hijack: any:53`，所有 DNS 都进隧道」。实际：Windows 多网卡并发解析（smart multi-homed name resolution）会向**每一块 Up 网卡各自配置的 DNS** 发起查询；发向物理网卡 DNS（如 114.114.114.114）的查询由该网卡直接发出，不经过 TUN 设备，劫持规则无从生效。

修复：物理网卡 DNS 指向隧道地址（`198.18.0.2`，fake-ip 段内的劫持入口），让所有网卡的查询都进 TUN。代价：**TUN 关闭时该网卡无法解析**（断网），需改回自动获取——这是一对互锁的状态，改的时候就要把回退方法一起写下来。

判据：**TUN 环境下做 DNS 审计，先把所有网卡的 DNS 列一遍（`Get-DnsClientServerAddress`），任何一块配着公网 DNS 都是潜在绕行道。**

### 5. 分层系统的泄露要逐层逼问，一轮修不干净是正常的

五轮修复的顺序：配置声明层（filter 的 `*`）→ 内核解析路由层（respect-rules/nameserver）→ 上游选择层（去 Google/清 direct-nameserver）→ 配置持久层（config.yaml）→ 操作系统网卡层（114→198.18.0.2）。每一轮改完都用同一个主动实测复测，看「解析器归属国清单」里还剩谁，剩谁就问谁的查询路径是什么。

判据：**修复链路型问题，复测指标要选「能区分每一层」的那个**——bash.ws 回查给出的是逐解析器清单而非二元结论，所以每轮都能看到「少了哪个、还剩哪个」，一轮定位一层。如果指标只是「漏/不漏」，五层会全部糊在一起。

## 顺手教训

- **mihomo 提权运行的内核没有 external-controller 时，非提权 shell 杀不动也重启不了它**——改完配置要请用户在托盘「重启内核」。本轮第一次重启还顺带把 TUN 弄掉了（变系统代理模式），重启后必须确认 TUN 仍开。
- **Cloudflare DoH 的出口解析器地理跟随服务位置**（从香港出口打过去，解析器就在香港）；**Google DoH 的出口解析器地理恒为美国**——如果审计按「解析器国家==出口国」判定，nameserver 里混着 dns.google 就永远有一项红。
- **机场订阅的 nameserver-policy 里可能有自定义专用解析**（本例 `+.v51124-4.qpon` 走一条 tcp 自定义 DNS 解析入口域名）——改造时必须先认出来并保留，覆盖掉会连不上节点。
- **测速点 HTTP 429 是节点侧限流信号**，不是本地配置问题；早前同节点实测 139 Mbps，排查时别被它带偏。
- **Git Bash 下 `git -C /e/...` 会报 No such file or directory**，用 Windows 风格路径 `git -C "E:/..."`；PowerShell 重定向输出是 UTF-16，读取要转码。

## 下次改进

- DNS 泄露排查起手式固定为四步：① 列所有网卡 DNS；② 读 mihomo.yaml 的 fake-ip-filter 找 `"*"`；③ 确认 nameserver-policy 的真相层；④ bash.ws 主动实测收尾。前三步任何一步有疑点都先改再测。
- 改代理客户端配置前**先备份三层文件**（本轮备份在 `{E:\vpn-guard}\.workbuddy\backup-*.yaml`）。
- vpn-guard 的 `vpn-leak-audit.ps1` 可考虑加一项静态检查：fake-ip-filter 含 `"*"` 时直接 WARN「fake-ip 名存实亡」——本轮根因 A 可以机检出来。
- 用户级环境变量（NO_PROXY 等）的每次改动，在当次排障文档里写明「这是有意设置，前提是什么」——给未来的自己对账用（本轮对账成本：回读一篇 8-04 旧档）。

## 关联文档

- [[代理环境变量遇TUN双重路由_Codex_CLI流式超时排障_v1]] —— 同目录、同一台机器、同一套 Clash 环境的前篇：那篇讲代理环境变量与 TUN 的双重路由（路由层多一跳），本篇讲 DNS 解析的五层泄露（解析层漏给谁）；本篇的 NO_PROXY 清理是对其「安全网」条款的架构演进对账
- [[ping通不等于路通_fake-ip假信号与节点带宽实测选型_v1]] —— fake-ip 家族的姊妹篇：那篇讲 fake-ip 让 ping 假绿（诊断信号失真），本篇讲 fake-ip-filter 的 `"*"` 让 fake-ip 本身失真（防护机制失效）；「运行态改了≠配置落盘」在本篇二次验证并补全下半句
- [[交付前实测证伪律_v1]] —— 本篇 insight 1/5 的同族上位律：声明与静态配置都是「应该能行」，只有主动实测能证伪
- [[全站文字截断体检_检测工具本身要先被证伪_v1]] —— 反向对照：那篇是检测工具误报（把正常判成缺陷），本篇是配置声明误报（把失效声明成生效）；共同点=判据要先在已知样本上标定
- [[有意改动不是故障_v1]] —— 本篇 NO_PROXY 对账段是该律的正向应用：认出 8-04 的有意安全网，按架构演进处理而非当故障清除
- [[ChatGPT_Windows桌面版安装排障与账号合规边界_v1]] —— 同机环境背景档（四层排障法）
- [[09_平台工程索引]] —— 平台工程区入口；本文归入「账号与访问」
