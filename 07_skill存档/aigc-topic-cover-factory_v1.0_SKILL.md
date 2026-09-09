---
name: aigc-topic-cover-factory
version: 1.0
description: AI 爆款选题批产 + 小红书真实场景图采集 + 代码合成 960×600 大字封面的一条龙流水线。产出「N 个选题 × M 张背景变体」的封面矩阵供 A/B 挑选。当用户说"给我出 20 个 AI 爆款主题"、"爬小红书图片做封面"、"批量生成视频封面"、"选题+封面一起搞"、"做一批大字封面"时触发。
---

# AIGC Topic Cover Factory

## 适用场景

一次性把「**想选题 → 找素材 → 出封面**」三步跑完，产出一个可以直接拿去 A/B 的封面矩阵。

典型触发语：

- "给我出 20 个 AI 相关的爆款主题，然后做成封面"
- "爬点小红书的图，批量做封面"
- "按这个对标做一批封面"
- "选题和封面一起搞，我要能挑的"

**与相邻 skill 的区别**：

- `aigc-video-cover-gpt` 是**单条视频**出 3 张精修封面，GPT Image 2 一步生成整图，追求质感。
- `aigc-poster-layout` 是**保护已定稿原图**做排版，不重绘主体。
- 本 skill 是**批量流水线**：几十条选题 × 几张背景，追求吞吐和可 A/B，单张质感不是目标。
  要精修封面别用这个。

---

## 核心约定

1. **输出恒为 960×600（16:10）**，B 站视频封面比例。不是小红书 3:4——小红书只是**素材来源**。
2. **不做人物抠像**。对标正片那层抠像人物本 skill 不覆盖，只做「场景照 + 大字」。
3. **版式参数是量出来的，不是调出来的**。所有数字见 `references/对标版式解析.md`，
   改之前先看那份文档，尤其"整块共用一个字号"和"单行 ≤ 10 字"两条。
4. **选题必须覆盖多个钩子公式**。同公式灌 N 条等于只有 1 条选题，A/B 测不出东西。
5. **人工挑图是流程的一部分**，不是失败兜底。脚本产出矩阵，最后一步永远是人选。

---

## 环境准备（首次）

```bash
pip install pillow numpy httpx playwright
python -m playwright install chromium
```

字体：脚本按 `NotoSansSC-VF`（切 Black 字重）→ `msyhbd.ttc` → `simhei.ttf` 顺序找。
Windows 一般自带前两个。都没有就报错，去 `make_covers.py` 的 `FONT_CANDIDATES` 加路径。

---

## 工作流程

### 第一步：产选题（这一步是你做，不是脚本做）

读 `references/选题钩子公式.md`，按用户要的数量产选题。**至少覆盖 6 个不同公式**。

每条选题写成 `topics.json` 的一项：

```json
{
  "id": "01",
  "hook": "身份围观式",
  "title": "让大家感受下大厂 Agent 工程师的工作状态",
  "lines": [
    { "text": "让大家感受下",       "role": "sub"  },
    { "text": "大厂Agent工程师的", "role": "hero" },
    { "text": "工作状态",           "role": "sub"  }
  ],
  "style": "yellow",
  "deco": "block",
  "keywords": ["互联网大厂工位", "程序员桌搭", "写字楼加班"]
}
```

完整字段表见 `scripts/topics.example.json`。三条最容易写错的：

- **`role`**：`hero` 走霓虹色，`sub` 走白色。**结论/冲突/身份放 hero，铺垫/语气放 sub**。搞反就没钩子。
- **单行 ≤ 10 个汉字宽**（"AI" 算 1.1 字）。超了字号会掉到 80 以下，缩略图糊掉。这是几何约束。
- **`keywords` 要能搜到真实生活照**。搜"人工智能"只出概念插画；要搜"程序员工位""出租屋书桌"这种。

写完把选题列表给用户过目再往下走——采集和合成都不贵，但选题错了后面全白做。

### 第二步：采集背景素材

首次要登录一次（扫码，登录态存本地 profile，之后无头跑）：

```bash
python scripts/xhs_fetch.py login
```

然后按 topics 批量拉，每个选题一个目录：

```bash
python scripts/xhs_fetch.py fetch --topics topics.json --out 01_素材 -n 12
```

单个关键词补图：

```bash
python scripts/xhs_fetch.py fetch --keyword "出租屋书桌" --out 01_素材/03 -n 8
```

**兜底**：登录态失效、接口改版、或者选题太偏搜不到图时，别在脚本上死磕——
直接把关键词给用户，让 ta 手动存图进 `01_素材/<id>/`，或者贴一份直链清单：

```bash
python scripts/xhs_fetch.py from-urls urls.txt --out 01_素材/03
```

脚本已经做了：

- **只收笔记正文图**。页面里混着大量同域的前端静态资源（`fe-static` / `fe-video` 下的
  `.js` `.css` `.ico`），不滤会全抓回来——只认 `sns-` 图片域名，并排掉头像/表情。
- 读渲染后 `img` 元素的 `currentSrc`，不拿正则扫 HTML（扫 HTML 会捞到内联脚本里的链接）。
- 滤掉宽高比 < 0.6 的竖图（裁到 16:10 会废）、按内容 MD5 去重、缩略图直链自动升到 1280 宽。
- 登录态失效的判据是搜索页出现 `.login-container` 遮罩，**不是**匹配「扫码登录」文案——
  实测页面写的是「手机号登录」，按文案判会漏判成已登录，然后抓回来一堆静态资源。

> **素材权属**：抓回来的是他人拍摄的照片，脚本只负责取，不处理授权。
> 商业项目里这一项由项目方/甲方负责，采集前确认清楚责任归属。

### 第三步：合成封面矩阵

```bash
python scripts/make_covers.py --topics topics.json --material 01_素材 --out 02_封面 --variants 5
```

产出 `02_封面/<id>/<id>.<n>.jpg`，即「每条选题 × 5 张背景」。

单图快速试排（调文案时用，不用等整批）：

```bash
python scripts/make_covers.py --topics topics.json --only 03 --bg 某张图.jpg --out /tmp/试排
```

### 第四步：拼审图大图，交人工挑

```bash
python scripts/contact_sheet.py --covers 02_封面 --out 03_审图 --cols 5 --rows 4
```

产出带编号的 contact sheet。**把审图大图给用户看，让 ta 报编号**，别自己替 ta 挑。

---

## 出了问题往哪儿看

| 症状 | 原因 | 怎么办 |
|---|---|---|
| 字溢出画布 / 大小不一 | 某行太长，或 `role` 全给了 `hero` | 拆行，或把铺垫行改成 `sub` |
| 字号明显偏小、缩略图糊 | 单行超过 10 个汉字宽 | 改写文案，别指望排版救 |
| 字压在杂物上看不清 | 自动选位没找到干净带 | 加 `"pos": "top"` 指定，或 `"deco": "scrim"` |
| 出现硬边灰块 | scrim 没羽化（老版本 bug） | 确认用的是 `soft_scrim`，不是 `rounded_rectangle` |
| 一批封面长得都一样 | 选题挤在同一个公式里 | 回第一步，按公式覆盖度重出 |
| `fetch` 报登录态失效 | profile 过期 | 重跑 `xhs_fetch.py login` |
| 取到 0 张笔记图 | 登录态刚失效，或关键词太偏 | 先重登；还是 0 就换关键词 |
| 搜不到合适的图 | keywords 太抽象 | 换成具体场景词；实在不行走手动兜底 |

---

## 文件

```
scripts/
  make_covers.py        封面合成（核心）。改版式参数前先读 references/对标版式解析.md
  xhs_fetch.py          小红书采集，Playwright 持久化登录态
  contact_sheet.py      拼审图大图
  topics.example.json   topics.json 完整字段示例
references/
  对标版式解析.md        65 张对标图的像素级量化结果 + 为什么这么设
  选题钩子公式.md        10 个句式公式 + 文案硬规矩 + 一批选题的健康度自检
```
