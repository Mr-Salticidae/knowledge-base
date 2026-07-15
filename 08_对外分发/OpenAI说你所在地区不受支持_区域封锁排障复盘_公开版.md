# 【踩坑记录】OpenAI 说"你所在的地区不受支持"：服务器、Worker、跳板一路排过去，最后一行配置解决

> 适用：你有一个网页应用想接 OpenAI（或任何按地区封锁的 API），但——①前端是公开的，API key 不能打包进去；②你的服务器在香港/大陆，直连被拒 `unsupported_country_region_territory`。这两个问题我在同一个下午连着撞完，中间还被 Cloudflare "就近执行"的特性摆了一道。全程实测，结论可直接抄。

## 先交代背景

我做了个线下展台互动项目：观众在镜子前拍照，AI 读脸生成五段"读心"文案，再织进一份个性化人生报告。展台机走本地模型，但还有个线上版给观众用手机玩——问题就出在线上版。

有天用户反馈："线上的 AI 读心怎么全是固定的片汤话？"

排查发现根因很干净：**发布脚本的安全闸把 API key 从公开产物里剔除了**（这是对的，key 上公网等于送钱包），前端没 key 调不了云端，降级到本地模型又够不着（那在观众自己手机上哪有 LM Studio），最后落到写死的模板兜底——片汤话实锤。

所以要让公开站有真 AI，标准答案只有一个：**自建中转代理**。前端不带 key，请求发给自己的服务器，服务器把 key 加上再转给 OpenAI。

**名词小抄**

- **中转代理**：架在"你的网页"和"OpenAI"之间的一层小服务，负责替前端保管并注入 API key。
- **Cloudflare Worker**：Cloudflare 的免费边缘函数，代码部署一次，全球几百个节点（PoP）都能跑。
- **就近执行**：Worker 的默认行为——请求从哪来，就在离它最近的节点上跑。这是优点，也是本文的坑眼。
- **Durable Object（DO）**：Worker 家族里"有固定住址"的成员，创建时可以指定它住在哪个大区。
- **SSE 流式**：AI 打字机效果的传输方式，服务器一小块一小块地吐字。

## 第一步：中转代理本身，一次写通

代理是个 100 来行的零依赖 Node 脚本，挂在我自己的香港服务器上（nginx 转发到本机端口）。前端同域调用，连跨域问题都没有。

但公开的 AI 入口等于把钱包口子开在马路上，安全闸必须一起上。我的清单，每层防的东西不一样：

| 闸 | 防什么 | 真话 |
|---|---|---|
| Origin 校验 | 别的网站白嫖挂站 | 可伪造，只是礼貌闸 |
| 模型白名单 | 有人拿你的口子刷更贵的模型 | 真闸 |
| 单次生成 token 上限 | 一条请求刷爆账单 | 真闸 |
| 每 IP 限流（30 次/5 分钟） | 脚本灌爆 | 真闸，但挡不住真实人流——后台务必设用量提醒 |

另外三个工程细节，做流式 AI 反代的都会用到：

1. nginx 必须 `proxy_buffering off`，否则打字机效果变成"憋 15 秒一次性倾倒"；
2. 用户关掉页面时要联动掐断上游请求（Node 里 `res.on('close', () => ctrl.abort())`），不然 OpenAI 那头还在替空气生成，token 照烧；
3. 带图请求的 body 很大（照片转 base64 轻松几百 KB），nginx 的 `client_max_body_size` 记得放宽。

本机全链路测通，部署上服务器，愉快地发起第一个请求——

## 坑一：403，`unsupported_country_region_territory`

OpenAI 按 IP 判定地区，香港不在支持列表（大陆同理）。服务器网络是通的，请求能到 OpenAI 门口，人家看了眼你的 IP 直接闭门。

我的服务器在香港是有原因的（大陆用户免备案直连），搬家不可能。那就在受支持的地区加一跳。

## 坑二：加了 Cloudflare Worker，还是同一个 403

思路很自然：部署一个免费 Worker 当跳板，服务器 → Worker → OpenAI，Worker 又不在香港——

等等，Worker 在哪，还真说不准。

部署完一测：**还是 403，一字不差**。

原因是那个被当优点宣传的特性：**Worker 就近执行**。谁调用它，它就在离调用者最近的节点上跑。我的香港服务器调用它，它就在 Cloudflare 的香港节点执行，出网 IP 还是香港——等于原地转了个圈。

这里有个我觉得最值钱的实验，10 分钟定性问题到底跟谁走：

**双端对照**：同一个 Worker，我用本地电脑调（梯子出口在受支持地区）——200 成功；用香港服务器调——403。两次请求唯一的差别是"调用方从哪出网"。**结论坐实：封锁判定跟着调用方 IP 走，跟你把代码部署在哪无关。**

以后遇到任何"地区不受支持"类问题，建议第一步就做这个实验，比翻文档快。

## 坑三：Smart Placement，等了 20 分钟等了个寂寞

Cloudflare 有个听起来正对症的功能叫 Smart Placement：分析你的 Worker 主要在跟哪个后端通信，自动把执行位置挪过去。一行配置的事，先试它。

开启后我灌了 18 个预热请求（它需要观察真实流量才做决策），然后挂了个每分钟自动重测的监控。

20 分钟，403 从头绿到尾（不对，是红到尾）。

事后复盘这 20 分钟本可以省掉：Smart Placement 优化的是**延迟**，不承诺**区域**；而且它的决策机制对"后端也在 Cloudflare 上"的场景（api.openai.com 正是）本来就暧昧。教训：**功能名字听起来对症 ≠ 机制上对症，看清楚它优化的目标是什么。**

## 终解：Durable Object，一行 locationHint

Cloudflare 免费产品线里，唯一能**钉死执行位置**的原语是 Durable Object——创建它的时候可以给一个"住址提示"：

```js
export class Hop extends DurableObject {
  async fetch(request) {
    // 真正的出网发生在这里——DO 住哪，就从哪出网
    return fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: request.headers.get('authorization') ?? '',
      },
      body: request.body,   // 流式 body 直接透传，打字机效果无损
    })
  }
}

export default {
  async fetch(request, env) {
    // ……这里做门禁：路径白名单 + 自定义 header 对暗号，防止跳板被陌生人白嫖……
    const stub = env.HOP.get(env.HOP.idFromName('us-hop-v1'), { locationHint: 'enam' })
    return stub.fetch(request)
  },
}
```

`locationHint: 'enam'` = 北美东部。配置文件（wrangler.toml）里要给 DO 补两段声明：

```toml
[[durable_objects.bindings]]
name = "HOP"
class_name = "Hop"

[[migrations]]
tag = "v1"
new_sqlite_classes = ["Hop"]   # 免费版用 SQLite 型 DO
```

两个细节：**住址提示只在 DO 首次创建时生效**，想换大区要换 `idFromName` 里的名字重建一个；DO 本身不存 OpenAI key，key 由我的服务器经请求头带过来，Worker 层只核对一个自定义暗号头。

部署，重测——**200。一次通过。**

最终链路：网页（无 key）→ 我的香港服务器（注入 key + 全部安全闸）→ Worker（对暗号）→ 北美 DO（出网）→ OpenAI。听着绕，实测带图流式读心：**首字 3 秒，全文 13 秒**，用户端无感知。

## 顺带的一个 nginx 冷坑

部署时改 nginx 配置，习惯性先备份：`cp 配置文件 配置文件.bak.日期`——然后 `nginx -t` 直接报错 duplicate listen。

因为备份是在 `sites-enabled/` 目录里原地做的，而这个目录是**通配 include 的活目录**：里面放什么都会被当配置加载，备份文件也不例外。备份请放到目录外面去（比如 `/root/nginx-backups/`）。

## 五条心得（可以直接抄走）

1. **公开前端 + AI = 必须中转代理。** key 永远只住在服务器上；安全闸分层配（白名单、token 上限、限流是真闸，Origin 校验只是礼貌），后台设用量提醒。
2. **"地区不受支持"先做双端对照。** 同一请求从两个不同地区的出口各发一次，10 分钟定性封锁跟谁走，再决定怎么修。
3. **CDN 边缘函数默认"就近执行"，被封地区调用它等于没挂。** 选跳板的硬指标是"能不能钉死执行位置"。
4. **Cloudflare 系钉位置用 Durable Object 的 locationHint**，免费版可用；Smart Placement 优化延迟不管区域，别指望。
5. **多级降级系统给每一级留肉眼可辨的标记。** 我们的兜底文案自带"镜面朦胧·以直觉代读"字样——用户一句"全是片汤话"，30 秒就定位到了具体是哪一级在输出。为诚实做的设计，最后以诊断效率回本。

从"片汤话"到线上真 AI，一个下午，三堵墙。每堵墙上其实都贴着字条，只是要撞上去才看得清——希望这篇让你少撞两堵。
