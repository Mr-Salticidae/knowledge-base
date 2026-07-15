---
tags: [类型/平台工程, 主题/踩坑]
---
# OpenAI 区域封锁与 Worker 就近执行陷阱 · 北美 DO 跳板

> 一句话：**OpenAI 的区域封锁跟"调用方 IP"走，Cloudflare Worker 就近在调用方的节点执行——被封区域的服务器挂 Worker 等于没挂**；免费产品线里唯一能钉死执行区域的原语是 `locationHint` 的 Durable Object。

> 入档：2026-07-15
> 来源：《镜像自我·人生预演》线上站 AI 读心中转代理搭建实录（香港服务器 → gpt-5.5）
> 状态：全链路上线并验证（公网流式读心首字 3.0s / 完稿 12.7s，安全闸逐个实测拦截）

## 事故

线上站读心"全是片汤话"——发布安全闸按设计剔除了 apiKey，前端落模板兜底。解法是在自有香港服务器挂同域中转代理（密钥服务器端注入）。代理本身一次写通，但出网连撞三堵墙：

1. **香港服务器直连 api.openai.com → 403** `unsupported_country_region_territory`（OpenAI 按 IP 封锁香港/大陆）
2. **加 Cloudflare Worker 跳板 → 还是同一个 403**。Worker 在离调用方最近的 PoP 执行——香港服务器调用，Worker 就在香港节点跑，出口 IP 还是香港
3. **开 Smart Placement → 预热 18 请求 + 每分钟重测，20 分钟不生效**。它优化的是延迟不是区域合规，且 api.openai.com 本身在 Cloudflare 后面，别指望

**定性判据（值这篇档案的核心实验）**：同一个 Worker，本机调用（梯子出口在受支持区域）返回 200，香港服务器调用返回 403——两端唯一差异是调用方 IP，证明区域判定跟调用方走、与 Worker 部署无关。

## 终解：北美 Durable Object

把转发逻辑从 Worker 默认导出挪进 Durable Object，创建 stub 时钉区域，一次通过：

```js
export class Hop extends DurableObject {
  async fetch(request) {
    return fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json',
                 Authorization: request.headers.get('authorization') ?? '' },
      body: request.body,   // 流式 body 直接透传
    })
  }
}
export default {
  async fetch(request, env) {
    // ...门禁：路径白名单 + x-relay-token 对暗号...
    const stub = env.HOP.get(env.HOP.idFromName('us-hop-v1'), { locationHint: 'enam' })
    return stub.fetch(request)
  },
}
```

- `locationHint: 'enam'`（北美东）在 DO **首次创建**时生效；换区域要换 `idFromName` 的名字
- wrangler.toml 需要 `[[durable_objects.bindings]]` + `[[migrations]]` 的 `new_sqlite_classes`（免费版可用 SQLite 型 DO）
- Worker/DO 都不存 OpenAI 密钥，密钥由上游代理经 Authorization 头带过来；Worker 层只对 relay token 暗号

## 同域中转代理的分层安全闸（可复用清单）

公开站零密钥走真 AI 的标准架构：`前端（同源，免 CORS）→ nginx → 本机 Node 代理（密钥注入）→ 区域跳板 → 上游`。闸门各司其职：

| 闸 | 防什么 | 备注 |
|---|---|---|
| Origin 校验 | 别的网站白嫖挂站 | 可伪造，只是礼貌闸 |
| 模型白名单 | 拿你的口子刷贵模型 | 真闸 |
| completion token 上限 | 单请求成本爆炸 | 真闸 |
| 每 IP 滑动窗口限流 | 脚本灌爆 | 真闸；挡不住真人流，后台设用量提醒 |
| Worker 中继令牌 | 跳板被直刷 | 与服务器 env 同值 |

工程三件套（流式接口反代必配）：nginx `proxy_buffering off`（否则打字机变一次性倾倒）+ `proxy_read_timeout` 放宽 + `client_max_body_size` 按最大请求体放宽；Node 端 `res.on('close', () => ctrl.abort())` 联动掐上游，观众关页不空烧 token。

## 顺带踩的坑

- **nginx 的 `sites-enabled/` 是通配 include 的活目录**：备份文件（`.bak.*`）放里面会被当配置加载，`nginx -t` 报 duplicate listen 且报错指向备份文件名——备份挪目录外（如 `/root/nginx-backups/`）
- 多级降级系统给每级输出留肉眼可辨的溯源标记（本案「镜面朦胧·以直觉代读」脚标），线上问题 30 秒定性到具体降级层——为诚实做的设计以诊断价值二次回本

## 迁移判据

任何"服务器所在区域被上游 API 封锁"的场景（不限 OpenAI）：第一步做**双端对照**（同一请求从两个不同区域出口发），10 分钟定性判定跟谁走；确认跟 IP 走再选跳板，跳板必须能**钉死执行区域**——CDN 边缘计算默认"就近执行"的都不行。

代理源码与部署脚本（库外裸路径）：`{mirror-life-rehearsal}/deploy-proxy/`（含运维手册 README_部署.md）；项目视角全记录：`{mirror-life-rehearsal}/进度报告/2026-07-15_线上真AI中转代理_复盘.md`。

## 关联文档

- [[2026-07-14_镜像自我_镜中特写AI读心_迭代复盘]] —— 案例母档/前传：读心板块建设与「安全闸剔除密钥→线上落兜底」问题的由来，本篇是其线上真 AI 收口篇
- [[知识库网站免备案上线_香港轻量服务器方案]] —— 本案的服务器与 CI 底座（同一台香港轻量 + rsync 部署）；那篇解决"国内可达"，本篇解决"从它出网调被封的上游"
- [[CI从Release抓二进制托管自有服务器_桌面应用国内直连下载_v1]] —— 同一台服务器的另一种用法（静态分发）
- [[二维码载荷硬预算与最长真实载荷验证_v1]] —— 同项目前一日的展台侧踩坑
- [[云端定时内容生产连环坑复盘_全绿不等于已发_v1]] —— 同样"云上黑盒先建可观测性再判因"的排查心法
