---
tags: [类型/代码]
---
# MV 模板说明

> 入档：2026-05-12(原文件名 README.md → 2026-05-13 改名为 MV模板说明.md,避免与根目录 README 同名)
> 性质：跨项目复用 · 静态图 + 音频 → 1080p MV 的标准生产线
> 起源：2026-05-12「这瓜包熟吗」项目首次跑通 City Pop 风格 MV
> 上级索引:[[代码资产索引]] · 上级地图:[[README]]

---

## 这个模板做什么

输入：一张图 + 一段音频
输出：1080p 30fps mp4，带

- 线性推近运镜（Ken Burns 效果）
- 胶片噪点
- 暗角
- 底部音频波形可视化
- 片头标题文字（淡入淡出）

适合 Suno / Udio 出来的成品歌配静态封面图直接出片，做 City Pop / Lo-fi / Indie / 纪录片配乐 这类「图静、声动、靠氛围」的内容。

---

## 文件清单

```
MV模板/
├── MV模板说明.md               # 本文档(原 README.md,5/13 改名)
├── make_mv.py                 # ① 横版 MV 生成 — 质量优先(单次 ffmpeg, medium preset)
├── make_mv_chunked.py         # ② 横版 MV 生成 — 慢机/沙箱友好(分块渲染+无损拼接)
└── make_vertical_cover.py     # ③ 横版 MV → 9:16 抖音版(黑胶唱片套框式构图)
```

`make_mv.py` 和 `make_mv_chunked.py` 是同一条生产线的两个版本，CONFIG 接口、滤镜链、输出参数完全一致——只是渲染策略不同，**配置可以直接互换**。

`make_vertical_cover.py` 是配套的"转抖音/小红书竖版"工具——拿前两个脚本的输出 + 该项目的 3:4 海报封面，生成 1080×1920 竖版视频，用封面同款的标题条 + 页脚条做边框，中间放视频。**不需要再走"模糊背景填充"那条路**，因为同画面的模糊填充实测会出现"两个图层感"，反不如换一套完全不同的固定边框来得统一。

---

## 怎么用

### 最小流程

把图和音频放到一个工作目录，叫 `input.png` + `input.{mp3,wav,m4a,flac,aac}` 任一格式：

```bash
mkdir my_mv && cd my_mv
cp 你的图.png input.png
cp 你的音频.wav input.wav        # 或 .mp3 / .m4a 都行
cp /path/to/MV模板/make_mv.py .
python make_mv.py
```

出 `output.mp4`。

### 改标题（不用动脚本）

```bash
MV_TITLE="新歌名" python make_mv.py
```

### 调风格（动脚本顶部 CONFIG）

CONFIG 里这些是常改的参数：

| 字段 | 范围 | 用途 |
|---|---|---|
| `title_text` | 字符串 | 片头标题 |
| `zoom_end` | 1.0-1.20 | 镜头推近终止位置，越大越戏剧化 |
| `noise_strength` | 0-100 | 噪点粗细，City Pop 推荐 15-30 |
| `vignette_angle` | 0-1.5 | 暗角强度，0.3 微弱 / 0.5 明显 |
| `waveform_color` | BGR hex | **注意 BGR 不是 RGB**：粉 0xFF6BB5、绿 0x6BFFB5、蓝 0xB56BFF |
| `waveform_opacity` | 0.0-1.0 | 波形透明度 |
| `title_duration` | 秒数 | 片头停留时长 |

### 选哪个脚本

| 场景 | 用哪个 |
|---|---|
| 自己 Mac/Win 桌面机器、≥4 核 | `make_mv.py`（默认 medium preset，画质更干净） |
| 2 核 / 笔记本电池模式 / 沙箱 | `make_mv_chunked.py` |
| 单条 ffmpeg 命令会超时（CI / 远程 SSH 容易断） | `make_mv_chunked.py` |
| 想看进度 / 失败了能从某一片重跑 | `make_mv_chunked.py` |

经验值（参考 2026-05-12 实测）：
- 2 核 i5-12400F 沙箱，135 秒音频，`medium` preset → 跑不完（被 45 秒超时砍断）
- 同一台机器，`ultrafast` preset + 35 秒分块 → 单块 ~32 秒，4 块 + 拼接 + 挂音轨 ≈ 2:30 完成

---

## 设计笔记

### 为什么把图放大到 120% 再 zoompan

zoompan 的推近表达式 `1 + (zoom_end-1) * on / total_frames` 在末尾会把画面放大到 `zoom_end` 倍。如果原图就是 1920×1080，放大后会出现边缘黑边（因为没有图源了）。所以预先 scale 到 120% 留余量，crop 到目标比例，再交给 zoompan。

### 为什么 zoompan 用 d=1

`d=N` 表示一个 zoom 值持续 N 帧。默认是 d=25，会出现明显阶梯感。设 `d=1` 让每一帧都重新计算 zoom，运镜平滑。代价是 zoompan 比简单 scale 慢约 3-5 倍。

### 分块渲染怎么保持镜头连续

朴素分块：每块的 zoompan 都从 zoom=1.0 开始 → 块之间会有明显跳变。
本模板的做法：把 zoompan 表达式从 `(on)/total_frames` 改成 `(start_frame + on)/total_frames`，每块知道自己在全局的什么位置。这样 4 块拼出来的镜头和单次渲染肉眼无差。

### 为什么标题只在 chunk_0

`title_duration` 默认 4 秒，落在 chunk_0 范围内（chunk_0 一般 30+ 秒）。只在那块加 drawtext，其他块跳过，省了 3/4 的 drawtext 开销。如果哪天把 title_duration 设到 40+ 秒，需要改 `chunk_render` 让 chunk_1 也加 drawtext + 用正确的 `t` 偏移。

### 为什么拼接用 concat demuxer + 流复制

`concat demuxer + -c copy` 是无重编码拼接：把每块的 H.264 字节流首尾相接，几乎不耗 CPU，也不损失画质。前提是每块的编码参数（profile / pixel format / 分辨率 / 帧率）一致——所以分块脚本里所有块用同一套参数。

如果用了 `concat` 滤镜（不是 demuxer），ffmpeg 会重新解码 + 重编码，把分块的好处全抵消了。

### 颜色顺序是 BGR 不是 RGB

ffmpeg 的 `showwaves` 和很多旧 filter 用 BGR 顺序的 hex。`0xFF6BB5` 看起来像深红，实际渲染是粉红（B=FF=蓝高、G=6B、R=B5=红中高 = 在 BGR 解释下是粉）。要换色直接去 `https://www.colorhexa.com/` 取 RGB hex，然后把 R 和 B 两个字节交换。

### 噪点为什么用 alls + allf=t

`noise=alls=20:allf=t`：所有通道（YUV 三通道一起加噪），`allf=t` 表示每帧重新生成噪点。如果不加 `t`，所有帧用同一份噪点 → 看起来像玻璃脏了而不是胶片颗粒。

---

## 转 9:16 抖音版 — `make_vertical_cover.py`

### 怎么用

```bash
# 默认假设当前目录下有 input.mp4 + cover_3_4.png
python make_vertical_cover.py

# 或显式指定路径
SRC=路径/到/横版.mp4 COVER=路径/到/cover_3_4.png python make_vertical_cover.py
```

输出 `output_vertical.mp4`：1080×1920 30fps，深底色 + 标题条 + 主视频(1:1 中央方块) + 页脚条。

### 为什么不用模糊背景填充

「这瓜包熟吗」(2026-05-12) 第一次做抖音版试过模糊填充法（背景 = 同画面高斯模糊 + 暗化，主视频居中放）。试了三轮参数：
- v1: sigma=40 + 暗化 0.15 → 边界硬，像两个图层
- v2: sigma=70 + 暗化 0.08 + 软 alpha 蒙版 → 边界软了但内容冲突明显
- v3: sigma=100 + 软蒙版+ 全局暗角 → 已经接近不出戏，但还是能感觉到「同画面两种处理」的违和

最终放弃这条路，改成"完全不同的固定边框 (深底色 + 项目封面切片)"。结论：当主视频和背景共享同一画面时，无论怎么模糊+暗化，都难逃"像两层透明纸叠在一起"的视觉违和。这是个**画面来源的本质冲突**，不是参数能调好的。

### 为什么用项目封面切片，不另画一个

项目通常已经有配套海报（3:4 唱片套样式），里面已经定好了字体、色彩、品牌徽章。直接从那里切标题条 + 页脚条，**自动继承了所有视觉规范**。零额外设计成本，竖版视频和首图天然是一套设计语言。

### 主视频 aspect 选择

| 选项 | 输出尺寸 | 适合场景 | 代价 |
|---|---|---|---|
| `1:1` (默认) | 1080×1080 | 主体居中、想最像海报 | 丢两侧约 40% 的横向内容 |
| `4:3` | 1080×810 | 想保留多一些侧边但不变细条 | 丢两侧约 25% 横向内容 |
| `16:9` | 1080×608 | 保留全部源画面 | 上下大量深色空白，条带感强 |

### 调整封面切片位置

如果你的 3:4 封面的标题条 / 页脚条占的高度跟默认 `230 / 160` 不一样，改 CONFIG 里的 `title_strip_h` 和 `footer_strip_h`。一般规则：

- 标题条 = 顶部第一个有内容（标签/大字）的区域到下一段（主图开始）之前的整个 dark band
- 页脚条 = 从主图结束 到 画布底部 的整个 dark band

封面如果不是 1080 宽，脚本会自动 scale 到 1080 后再裁。

### 加速秘诀:静态帧模板预烤

朴素做法是每帧都做 `crop title + crop footer + 4 个 overlay`。即使是静态的标题条和页脚条，ffmpeg 每帧都重算一遍，浪费 CPU。

`make_vertical_cover.py` 的做法是**先合成一张 `frame_template.png`**(深底色 + 标题条 + 页脚条都嵌进去)，然后每帧只用做 `视频 crop + 一次 overlay`。实测在 2 核 1080p 60fps 源 → 1080×1920 30fps 输出的渲染，从 ~3x 实时变成了 ~0.4x 实时（快 7 倍）。

---

## 风格变体速查

针对不同曲风的 CONFIG 微调建议：

### City Pop / Synthwave（默认）

```python
"zoom_end": 1.12,
"noise_strength": 20,
"vignette_angle": 0.4,
"waveform_color": "0xFF6BB5",     # 粉
"waveform_opacity": 0.6,
```

### Lo-fi / Chillhop

```python
"zoom_end": 1.06,                  # 推近更克制
"noise_strength": 35,              # 噪点更粗
"vignette_angle": 0.55,            # 暗角更重
"waveform_color": "0xCCFFE5",     # 薄荷绿
"waveform_opacity": 0.4,
```

### 纪录片 / 民谣

```python
"zoom_end": 1.04,                  # 几乎不动
"noise_strength": 8,               # 噪点极弱
"vignette_angle": 0.3,
"waveform_color": "0xFFFFFF",     # 白
"waveform_opacity": 0.3,
```

### Indie Rock / Punk

```python
"zoom_end": 1.18,                  # 推得猛
"noise_strength": 40,              # 噪点厚重
"vignette_angle": 0.6,
"waveform_color": "0x0000FF",     # 纯红（BGR）
"waveform_opacity": 0.8,
"title_fontsize": 96,              # 标题大
```

---

## 限制 / 后续可扩展

当前模板的局限：

- **只支持线性推近**，没有摇移（左右平移）、缩放后回到原大、变速。要加摇移可以把 zoompan 的 x/y 表达式从 `iw/2-(iw/zoom/2)` 改成线性表达式。
- **波形是 line 模式**，不带频谱。换 `mode=cline` / `mode=p2p` / 用 `showspectrum` 滤镜可以换 vibe，但显著增加渲染时间。
- **片头标题是单行文字**，没有歌手 / 副标题分行。要做副标题，复制一份 drawtext 块，改 y 表达式。
- **没做片尾**，只有片头。要加片尾签名「@跳蛛先生」，在 `[final]` 之前再加一个 drawtext，alpha 表达式用 `gt(t,duration-3)` 反过来。

下一首跑模板时如果撞到上面任何一条限制，建议在原项目目录改一个变体，跑稳了再镜像回这里成 `make_mv_<风格>.py`。

---

## 引用

- ffmpeg 滤镜文档：<https://ffmpeg.org/ffmpeg-filters.html>
- zoompan 详解：<https://ffmpeg.org/ffmpeg-filters.html#zoompan>
- showwaves 详解：<https://ffmpeg.org/ffmpeg-filters.html#showwaves>

---

## 关联文档

- 上级索引:[[代码资产索引]]
- 上级地图:[[README]](知识库根目录 MOC)
- 配套方法论:[[图生视频_ForwardOnly原则]]
