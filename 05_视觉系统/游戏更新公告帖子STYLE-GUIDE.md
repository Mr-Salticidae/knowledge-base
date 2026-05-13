---
tags: [类型/IP视觉]
---
# Last Stand 小红书图文 · 制作经验与风格手册

> 用途：下次再做 Last Stand 的版本公告 / 小红书图文卡片时直接照抄这套规范，避免重复踩坑。

---

## 一、视觉系统（必须遵守）

### 1.1 尺寸 & 数量
- **单张：1080 × 1440**（小红书 3:4 竖屏）
- 一组 8 张（封面 + 3 修复 + 1 新增 + 1 NOT A BUG + 1 预告 + 1 反馈）
- 每张图至少 60% 留白

### 1.2 配色（CSS 变量）
```css
--paper:    #f4ede0;   /* 奶油纸主底色（默认） */
--paper-2:  #ece4d4;   /* 二级纸色 */
--ink:      #1a1412;   /* 主墨色（不是纯黑） */
--ink-faint:#7a6f63;   /* 注释、二级文字 */
--red:      #d92e33;   /* 强调红 */
--orange:   #e8843a;   /* 警示橙（仅极限难度行用） */
```
- **暗色变体**：`--paper:#0d0807; --ink:#f1ead9;`（可通过 Tweaks 切换）
- 红色强度三档：`#b8262b`（收敛）/ `#d92e33`（中）/ `#e8181e`（响亮）
- 默认走"中" + 奶油纸；用户最终选择就是这个

### 1.3 字体
| 用途 | 字体 |
|---|---|
| 标题（独立游戏文学感） | **Noto Serif SC**（思源宋体）·700 |
| 正文 | **Noto Sans SC**（思源黑体）·400/500/700 |
| 代码注释 / 版本号 / 数字 | **JetBrains Mono**·400/500/700 |

- 中文衬线字体的"独立游戏书桌感"是这套设计的灵魂，不要换成 PingFang
- 所有 `// FIX 0X` `// NEW 0X` `// COMING NEXT` 等代码注释风标签 → JetBrains Mono · 22px · 字距 0.06em

### 1.4 排版基线
- 标题字号 64–96px（封面 v0.2.1 用 92px，FIX 02 重磅用 88px）
- 正文 22–26px、line-height 1.6–1.7
- 数字 / 时间 / 关键词标红 + 加粗，其他保持 ink 色
- 每张卡左右内边距 64px、上 64px、下 56px（页脚水印）
- 角标位置固定：左上 `// TAG`、右上 副信息（页码 / 张数）、左下 LAST STAND 水印、右下 页码

### 1.5 手绘元素
- **只用最简单的笔画形状**（矩形、椭圆、单笔曲线、火柴人）
- **绝对不要画复杂 SVG**——人体解剖会翻车（这次封面填充版人体被退回，最终回到火柴人）
- 火柴人原则：单根脊柱 + 单点髋部 / 肩部，不要让躯干和背包、腿在同一坐标重叠
- 红色框只用作强调（指向、圈选），保持和主体黑线对齐（路径坐标要严格匹配父矩形坐标）
- SVG viewBox 高度要给文字留空间——文字 y 坐标 + 字号 ≤ viewBox 高度（卡 2 翻车原因）
- 给每个手绘配 mono 小字注释（"// sketch · placeholder" / "焦点丢失 · capture 释放" 等）

### 1.6 反对清单
✗ 深色科技 PPT 风  
✗ FINAL VERDICT 类 badge  
✗ 数据柱状图 / 流程框图  
✗ 渐变光效 / glow  
✗ 商务风分块卡片 + 圆角左竖条 accent  
✗ Inter / Roboto / 系统字体  
✗ 复杂 SVG 角色 / 武器写实

---

## 二、八张卡的内容模板

| # | 标签 | 标题模式 | 视觉 | 备注 |
|---|---|---|---|---|
| 1 | `// PATCH NOTES · YYYY.MM` | 衬线大字 · 版本号标红 | 火柴人士兵 + 鸟 | 留 hook 引第 3 张 |
| 2 | `// FIX 01` | 衬线 + 红色下划线 | 两个窗口框 + 鼠标飞出/飞回 | 标准 FixCard 模板 |
| 3 | `// FIX 02 · 真·惊喜` | 88px 衬线 · `2 波`标红 | 单行高亮 git 代码 | 主 hook，最戏剧化 |
| 4 | `// FIX 03` | 衬线 | 文件柜 + 红色抽屉 + 钥匙 | 标准 FixCard |
| 5 | `// NEW 01 · 战场清理` | 衬线 | 三难度行表格 + 三帧消失分镜 | 表格用 dashed 分隔 |
| 6 | `// NOT A BUG` + 红色 stamp | 衬线大字 · "反而涨弹药"超大 | 霰弹枪 + AMMO ↑ 框 | 旋转 8° 的红框印章 |
| 7 | `// COMING NEXT` | 衬线 + 大数字 01/02 | 无主图，纯排版 | 列两条 v0.3 方向 |
| 8 | `// FEEDBACK` | 衬线 | QR + 手绘括号角 + 注解箭头 | QR 不要用大白卡 |

### 2.1 复用组件（cards.jsx 里）
- `<Card n={N}>`：通用框，带水印 + 页码 + 纸质径向噪点
- `<Tag tone="red|ink|orange">`：mono 标签
- `<InkUnderline width={N}>`：手绘波浪下划线（只有红色版本）
- `<FixCard n tag title body sketch bottomNote>`：标准修复卡（卡 2/4 用）

---

## 三、关键经验教训

### 3.1 工具/技术坑
1. **中文文件名 run_script 拒收** → 任何要进 `run_script`/`readFile` 的文件先 `copy_files` 重命名为 ASCII
2. **useTweaks 是 tuple 不是 object**：`const [tweaks, setTweak] = useTweaks(defaults)`，不是 `{ tweaks, setTweak }`
3. **html-to-image 在沙箱内不稳定**：捕获 1080×1440 大图会随机 hang（CORS 字体 / 复杂 SVG），别用脚本批量截图——直接给用户离线 HTML 自己截
4. **save_screenshot 只截 viewport** (924×540)：不能截 1080×1440 的元素全图
5. **iframe 渲染 React 有竞态**：第一次 `eval_js` 看到 `#root` 是空的属于正常，reload 一次或加 sleep
6. **离线打包必须有 `__bundler_thumbnail` template**：在 `<head>` 加 `<template id="__bundler_thumbnail"><svg>...</svg></template>`，否则 super_inline_html 不工作
7. **JSX 共享组件**：每个 `<script type="text/babel">` 是独立作用域，组件文件结尾必须 `Object.assign(window, {Card1, Card2, ...})`
8. **`const styles = {}`** 全局命名冲突：用 `cardStyles`、`terminalStyles` 等命名空间
9. **super_inline_html 不会追踪 JSX 字符串里的 `<img src="...">`**：bundler 只解析 HTML 静态属性，对 babel 转译后的 JSX 里的资源路径无能为力。**所有要随离线 HTML 一起交付的图片资源（QR、logo 等），必须直接以 base64 data URL 写进 jsx**：先 `readFileBinary` + `btoa` 转成 `data:image/png;base64,...`，再 `<img src={"data:..."}/>`

### 3.2 设计/沟通坑
1. **手绘人体不要用 fill 写实**——用户会说"不如火柴人"。火柴人 + 不重叠是底线
2. **红色框和黑色主体一定要坐标对齐**（卡 4 文件柜抽屉路径 x 错位 10px 被抓出）
3. **QR 码不要做"大白卡 + 红色阴影"**——会被说"突兀"。改用：
   - 小一点（260px 不是 320）
   - 手绘括号四角（替代实线边框）
   - QR 背景用 `var(--paper-2)` 不要纯白
   - 加一支虚线箭头 + "扫这边 →" 注解
4. **代码块**：用户嫌 `git diff` 双色块太"工具感"，最终选了"单行高亮 + 左红条"
5. **文字别越界**：SVG 内 `<text>` 的 y 坐标 + 字号必须留 viewBox 余量，否则被裁
6. **导出**：用户最后只要"能打开的离线 HTML"，不要再尝试在沙箱里批量生成 PNG，浪费时间

### 3.3 流程经验
- **questions_v2 一上来就问 10 题**——背景色、字体、手绘风格、accent 强度、特殊待遇、git diff、QR 处理、变体数量、导出方式、其它备注
- **Tweaks 默认值留成 EDITMODE-BEGIN/END 块**：用户在页面上切换会自动持久化
- **inline 评论会指到具体 element**：`react: Card8 → image-slot#feedback-qr` 这类信号要会读，定位到具体 jsx 节点
- **每次重大改动后**：调用 `done` 让用户看到，再 `fork_verifier_agent`，再继续

---

## 四、文件结构（推荐）

```
/
├── Last Stand vX.Y.Z Patch Notes.html        ← 主预览（design canvas + tweaks）
├── Last Stand vX.Y.Z · Export.html           ← 8 张纵列导出预览
├── Last Stand vX.Y.Z · Export (offline).html ← 单文件离线版（交付）
├── cards.jsx                                  ← 8 张卡 + 共享组件
├── design-canvas.jsx                          ← starter
├── tweaks-panel.jsx                           ← starter
├── image-slot.js                              ← starter（如用 QR slot）
└── assets/
    ├── qr.png                                 ← 用户上传的 QR
    └── feedback-poster.png                    ← 原始素材
```

## 五、文案风格

- **第一人称偶尔用"我"，更多用"你"和"这版"**
- **代码注释口吻**：`// 这版恢复 30 波`、`// 不修。享用这个小爽点`、`// 想听到 ——`
- **承认错误自嘲**：FIX 02 必须明说"不是设计，是 bug"
- **谢谢玩家**写在卡 1 副标题、卡 2 底部、卡 8 sign-off，但每次换措辞，不要重复
- **避免**："为您带来"、"全新升级"、"用户体验提升"等市场话术
- **保留**：emoji 极少用，最多封面 😅 一个

## 六、下次开工 checklist

- [ ] 读这份文档
- [ ] 用 questions_v2 问 10 题，问清新增 / 修复条目内容
- [ ] 确认是否复用 cards.jsx 里的 FixCard 模板
- [ ] 复制 design-canvas / tweaks-panel / image-slot starter
- [ ] 写 cards.jsx，逐张做完一张 done 一张
- [ ] 输出 Export.html + super_inline_html → 离线 HTML 给用户
- [ ] 不要尝试自己批量截 PNG，浪费时间

---

_最后更新：2026-05 · v0.2.1 制作完成后总结_
