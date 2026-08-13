---
tags: [类型/代码, 主题/vibe-coding, 状态/活跃]
---

# Vibe Coding 视觉特效合集

> 入档:2026-08-13
> 性质:单文件 HTML 交互式视觉特效 demo + 对标教程链接
> 上级索引:[[代码资产索引]]

---

## 为什么有这个目录

Vibe Coding（氛围编程）的核心思路：用自然语言描述感觉，让 AI 生成代码，快速迭代视觉效果。这个目录收录 5 个"简单但视觉震撼"的单文件 demo，每个不到 150 行代码，零依赖，双击即开。

用途：
- 团队内部对接时快速展示某种视觉效果的可能性
- 作为 vibe coding 工作流的参考案例
- 学习 Canvas 2D / 噪声场 / 粒子系统 / shader 数学 的入门素材

---

## Demo 清单

所有文件均为单文件 HTML，纯 Canvas 2D + vanilla JS，零依赖。

| 文件 | 效果 | 代码量 | 交互方式 | 核心技术 |
|------|------|--------|----------|----------|
| `cosmic_flow.html` | 800 粒子沿 Perlin 噪声力场流动，宇宙星云感 | ~100 行 | 鼠标引导粒子方向，点击重新生成 | 噪声场 + 粒子系统 + lighter 混合模式 |
| `plasma.html` | 像素级等离子体，5 层 sin 波叠加，迷幻色彩流动 | ~60 行核心 | 鼠标扭曲空间 | ImageData 像素操作 + sin 波叠加 |
| `neon_waves.html` | 5 条霓虹波浪交织，多层频率叠加 | ~80 行 | 鼠标改变波浪基线，点击切换 4 套配色 | shadowBlur 辉光 + 多频正弦波 |
| `mandala.html` | 鼠标绘制万花筒对称曼陀罗，实时变色 | ~90 行 | 鼠标绘制，滚轮调对称数(3-30)，点击清空 | 极坐标变换 + 镜像对称 + HSL 色环 |
| `matrix_rain.html` | 黑客帝国数字雨，片假名+数字+符号 | ~50 行 | 鼠标附近字符变青色发光 | 字符流 + 距离检测 |
| `index.html` | 展示索引页，含所有 demo 的实时预览动画 | — | 点击卡片进入对应 demo | 卡片悬浮动画 + 缩略图渲染 |

### 运行方式

直接双击 `index.html` 在浏览器打开，从索引页进入各 demo。或直接双击任意 `.html` 文件。

---

## 核心技术速查

### 1. Perlin 噪声流场（cosmic_flow）

粒子沿一个不可见的力场流动，力场方向由噪声函数决定：

```js
// 简化版伪噪声（无需库）
function noise(x, y, t) {
  return Math.sin(x * 0.003 + t * 0.0003) * Math.cos(y * 0.003 - t * 0.0002);
}
// 粒子受力方向 = noise 值映射到角度
const angle = noise(this.x, this.y, t) * Math.PI * 3;
this.vx += Math.cos(angle) * 0.15;
this.vy += Math.sin(angle) * 0.15;
```

关键效果：
- `globalCompositeOperation = 'lighter'` 让粒子叠加发光
- 每帧 `fillRect` 半透明黑色 → 拖尾效果
- 粒子有生命周期，死后重生

### 2. Plasma 等离子体（plasma）

逐像素计算颜色，多层 sin 波叠加产生有机流动感：

```js
const v1 = Math.sin(fx * 4 + time);
const v2 = Math.sin(fy * 4 + time * 0.7);
const v3 = Math.sin(distance * 6 - time * 2 + angle * 2);
const v = (v1 + v2 + v3 + v4 + v5) / 5;
// 映射到 RGB — 三个相位偏移的 sin 产生流动色彩
r = Math.sin(v * Math.PI + 0) * 127 + 128;
g = Math.sin(v * Math.PI + 2.0) * 127 + 128;
b = Math.sin(v * Math.PI + 4.0) * 127 + 128;
```

### 3. 霓虹辉光（neon_waves）

Canvas 2D 的 `shadowBlur` + `shadowColor` 是最简单的辉光方案：

```js
ctx.shadowBlur = 20;
ctx.shadowColor = color;
ctx.strokeStyle = color;
ctx.stroke(); // 第一次细线
ctx.lineWidth = 8;
ctx.globalAlpha = 0.15;
ctx.stroke(); // 第二次粗线叠加 → 更宽的辉光
```

### 4. 对称曼陀罗（mandala）

极坐标旋转 + 镜像翻转 = 万花筒：

```js
for (let i = 0; i < symmetry; i++) {
  const angle = (i / symmetry) * Math.PI * 2;
  const cos = Math.cos(angle), sin = Math.sin(angle);
  // 旋转
  const x1 = cx + dx * cos - dy * sin;
  const y1 = cy + dx * sin + dy * cos;
  // 镜像翻转
  const x1m = cx + dx * cos + dy * sin;
  const y1m = cy - dx * sin + dy * cos;
}
```

---

## 对标教程链接

### 粒子流场 / Perlin Noise

| 教程 | 作者 | 平台 | 说明 |
|------|------|------|------|
| Mesmerizing Particle Flow Field in p5.js | BigCodeNeck | YouTube | p5.js + Perlin Noise 流场粒子，步骤清晰，适合入门 |
| The Beauty of Code: Flow Fields | Chris Courses | YouTube | Canvas 系统课中的流场章节，讲透 Perlin Noise 原理 |
| Flow Fields | Patt Vira | pattvira.com | 从力学原理到粒子类到美化，28 分钟完整流程，带时间戳 |
| Perlin Noise Shader Tutorial (R3F) | canxerian | YouTube + GitHub | React Three Fiber + GLSL shader 实现噪声流场，附完整源码 |

### Plasma / Shader 效果

| 教程 | 作者 | 平台 | 说明 |
|------|------|------|------|
| Shadertoy for absolute beginners | The Art of Code | YouTube | 从零学 GLSL，手绘公式图解，公认最好的 shader 入门系列 |
| GLSL Beginner Tutorials (28 课) | Uğur Güney | Shadertoy | 从空白屏幕到 Plasma 效果，第 25 课就是等离子体 |
| Plasma Effect (在线源码) | — | shadertoy.com/view/Xst3zN | 经典 plasma shader 源码，可直接在线编辑运行 |

### Canvas 粒子 & 视觉特效

| 教程 | 作者 | 平台 | 说明 |
|------|------|------|------|
| Galactic Light Trails | Chris Courses | YouTube | 38 分钟，Canvas 旋转 + 粒子辉光 + 鼠标交互，效果极震撼 |
| Realistic Canvas Fireworks | Chris Courses | YouTube | 29 分钟，物理粒子系统（重力/摩擦/拖尾），烟花爆炸效果 |
| Create STUNNING Particle Effects | Islomiddin | YouTube | 纯 vanilla JS 粒子动画，网站背景/落地页适用 |
| Music Visualizer (Canvas + Audio API) | Makbul | YouTube | Vibe coding 风格，5 步做出音频可视化器，零依赖 |

### Vibe Coding 综合教程（中文）

| 教程 | 作者 | 平台 | 说明 |
|------|------|------|------|
| 鱼皮的免费 Vibe Coding 教程 | 鱼皮 | B站 | 覆盖 Cursor/Claude Code/TRAE 等工具，B站 IT 榜 No.1 |
| 2026 Vibe Coding 实战教程 | — | B站 + 飞书 | 工具+案例+黑客松，附飞书文档 |
| Gemini 3 + Three.js 3D 手势粒子 | — | aiposthub.com | 一段 Prompt 生成 3D 手势交互粒子，附完整 prompt 模板 |
| 零基础 10 分钟搓出粒子特效 | — | f.mffb.com | 从装环境到粒子追踪网页，纯新手向 |

### 最推荐的 3 个入门视频

1. **The Art of Code — Shadertoy for absolute beginners**（YouTube）— shader 界公认最佳入门
2. **Chris Courses — Galactic Light Trails**（YouTube）— Canvas 粒子特效最佳实战
3. **鱼皮 Vibe Coding 教程**（B站）— 中文氛围编程最佳综合课

---

## 技术要点备忘

- **拖尾效果**：每帧 `fillRect` 半透明背景色（alpha 0.03-0.08），而非 `clearRect`，旧帧渐隐产生拖尾
- **发光叠加**：`globalCompositeOperation = 'lighter'` 让粒子颜色叠加变亮，适合宇宙/光效场景
- **shadowBlur 辉光**：Canvas 2D 最简单的发光方案，但性能开销大，大场景需控制粒子数
- **ImageData 像素操作**：plasma 效果需要逐像素计算，用 `createImageData` + `putImageData`，注意性能与分辨率平衡
- **极坐标对称**：曼陀罗的核心是 `(cos, sin)` 旋转矩阵 + 镜像翻转，对称数 = 旋转份数 × 2

---

## 关联文档

- [[代码资产索引]]
- [[代码公开说明]]
