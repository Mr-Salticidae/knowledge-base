---
name: report-longimage
version: 1.0
description: 把一篇 Markdown 文档渲染成 PB Arena「简洁低疲劳 V2」版式的报告长图 PNG（暖白/炭黑/珊瑚红，细线分隔，无渐变无阴影），用 headless Chrome 两趟截图出全页图。当用户说「做成 pb-arena 同款图片」「出一张长图」「把这篇做成报告长图」「渲染成图发群」「做张图发朋友圈」，或任何「文档 → 可直接转发的长图」的诉求时触发，即使没提 pb-arena。
---

# 报告长图渲染（PB Arena 同款版式）

把一篇已成稿的 md（复盘、尽调、更新报告、教程）渲染成**一张可直接转发的长图 PNG**。
版式来自 PB Arena 的「简洁低疲劳 V2」视觉规范，产线是 HTML 母版 + headless Chrome 两趟截图。

**边界**：本 skill 只管「已有内容 → 出图」。内容本身怎么写不归它管（尽调类内容见 `opportunity-due-diligence`，对外帖体例见 `insight-public-post`）。

## 资产

| 文件 | 用途 |
|---|---|
| `E:\knowledge-base\07_skill存档\report-longimage\母版.html` | 组件画廊：每种块各一个带占位文案的示例，复制需要的块 |
| `E:\knowledge-base\07_skill存档\report-longimage\render.sh` | 两趟截图脚本，`bash render.sh in.html out.png` |
| `E:\knowledge-base\08_对外分发\海外短剧剪辑拉新副业能不能做_尽调笔记.html` | 真实成品样例（2240×10754），当参考比母版更直观 |
| `E:\pb-arena\docs\更新报告_2026-07-30_*.png` | 版式源头，拿不准时回看这张 |
| `E:\pb-arena\docs\更新报告_2026-08-05_浅色对战V4改稿落地.{md,html,png}` | md / html / png 三件齐全的一次真实产出（2240×7524），要改文案直接改那份 html 重渲染 |

## 第 1 步：套母版

复制 `母版.html` 到 scratchpad，改内容。**版式骨架顺序固定，不要重排**：

```
眉标(珊瑚红字距)  →  大字标题(1-2行)  →  mono 元信息行(日期/署名/域名)
  →  细线  →  导语(交代对象 + 一句话结论,加粗收尾)
  →  四格指标栏  →  01/02/03… 编号章节  →  页脚(圆形mark + 署名 + 胶囊徽章 + 来源行)
```

### 硬规则

- **珊瑚红 `#ff5a52` 全页占比 5%–8%**。它只出现在：眉标、章节编号、列表圆点、`.hl` 红字、callout 竖线、红线框。`.hl` 全页最多 5–8 处，`.redline` 整篇**最多一次**——出现两次就都不重了。
- **不加渐变、光晕、厚阴影、玻璃拟态**。层级只靠字重、对齐、留白、细分隔线（`#e6e5e1`）建立。
- **指标栏固定四格**，全页只出现一次，紧跟导语。每格 = 小标签 + 大数值 + 小注解；最多 1–2 格标红（`.m-value.accent`），全标等于没标。**注解那行放对照值**（「同类行价 $0.22」「已按乐观口径」）——一个数字配一个参照才有信息量。
- **署名固定「跳蛛先生」**（跳蛛 = Salticidae，不是「跳猪」）。
- **称谓**：稿子若是直接转发给当事人读的，正文一律第二人称，不要出现「学员/同学/他」把读者写成第三方。

### 组件选用

| 想表达 | 用 |
|---|---|
| 一句话结论、值得被单独记住的判断 | `.quote` |
| 补充说明，不至于上红框 | `.callout` |
| 全篇最重的一条戒律 | `.redline`（限一次） |
| 层级 / 转包 / 流程，且要指出「你在哪一格」 | `.chain` + `<em>` 标红末端 |
| 两种口径对照（宣传 vs 免责、修复前 vs 修复后） | `.grid2` + `.box` |
| 逐项核查、带判定列 | `<table>` + `td.y`（绿色判定） |
| 分项测算、要有合计 | `<table class="t-narrow">` + `tr.total` |
| 必问清单、编号步骤 | `<ol class="qs">`（序号自动补零成 01/02） |

## 第 2 步：出图

```bash
bash "E:/knowledge-base/07_skill存档/report-longimage/render.sh" <in.html> <out.png>
```

默认逻辑宽度 1120、缩放 2 倍 → 成图 2240 宽，与 PB Arena 既有报告图一致。

脚本做的事就是**两趟**：第一趟 `--dump-dom` 读页面自报的 `scrollHeight`，第二趟按精确高度 `--window-size` 截图。

## 第 3 步：验收（不许跳过）

**渲染完必须裁头 / 中 / 尾三段放大回看**，不能只看整图缩略图：

```bash
python -c "from PIL import Image;im=Image.open(r'out.png');print(im.size);im.crop((0,0,im.size[0],1300)).save('_c1.png');im.crop((0,im.size[1]-900,im.size[0],im.size[1])).save('_c2.png')"
```

缩略图看不出的东西，裁图一眼就能看见：中文字体回退成宋体、页脚漏改的旧文案、指标栏数值溢出。**2026-07-31 那次，署名写错和 CJK 掉宋体两个问题都是靠裁图才发现的，整图缩略图上完全看不出来。**

## 三个已知坑

### 1 · 一趟截图只截视口，长内容被直接切掉

Chrome 的 `--screenshot` 截的是 `--window-size` 那么大的区域，不会自动截全页。所以必须两趟。母版末尾那行 `document.title = "H" + scrollHeight` 是第一趟的读数口，**删了脚本就跑不了**。

比「先截一张超高图再裁」干净——猜高度要么切内容要么留一大片空白。

### 2 · `--mono` 以 generic `monospace` 收尾，中文全掉进宋体

`monospace` 是通配的 generic family，会匹配一切，**排在它后面的字体永远不生效**。所以 CJK 字体必须排在 `monospace` **之前**：

```css
--mono:"DM Mono", Consolas, "Cascadia Mono", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", monospace;
```

否则眉标、元信息行的署名、指标栏里的中文数值（「字节系」「0 元」）会全部渲染成宋体，跟整套无衬线体系打架。拉丁字符仍走 Consolas，不受影响。

同族见 `09_平台工程/导出运行时无系统字体回退律_CJK豆腐块_v1.md`——都是「把兜底固化进产物」。

### 3 · `set -e` 下用 `&&` 链找文件会静默退出

`render.sh` 里定位 Chrome 的循环，写成 `[ -f "$p" ] && CHROME="$p" && break` 时：第一个候选路径不存在 → 循环体最后一条命令返回非 0 → `set -e` 直接终止脚本，**且不打印任何错误**。必须写成 `if [ -f "$p" ]; then …; fi`。

## 第 4 步：归档

- PNG 与 md 同目录同名（`xxx.md` / `xxx.png`），**HTML 源码一并留下**（`xxx.html`）——下次改文案重渲染比从母版重搭快得多；
- 按知识库 CLAUDE.md 惯例 **commit 并 push**。

## 关联

- `opportunity-due-diligence` —— 尽调类内容的写法，写完交给本 skill 出图
- `insight-public-post` —— 对外帖体例；那条链路的产物同样可以过本 skill
- `aigc-poster-layout` —— 区别：那个是作品/角色宣传海报（图为主），本 skill 是文档型报告长图（字为主）
- `09_平台工程/美工改稿全站落地_跨稿重复才是规范_v1.md` —— 视觉规范与两趟截图法的出处
