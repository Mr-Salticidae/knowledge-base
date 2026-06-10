---
tags: [类型/prompt模板, 主题/构图, 主题/实验协议, 主题/AIGC]
---
# AIGC 构图层实验协议 v1

> 目的：验证 [[AIGC构图意图层_v1]] 是否真的提升 AIGC 画面生成质量。
> 原则：不把外部构图知识直接写成铁律；先用同题对照实验确认它对 MJ / gpt-image / Seedance 是否有效。

## 实验设置

每个题目至少跑两组：

| 组别 | 内容 |
|---|---|
| A 组：原始 prompt | 只写主体、环境、风格、光影，不显式写构图意图 |
| B 组：构图层 prompt | 在主体 / 环境之后加入构图意图，如 `negative space`, `single dominant subject`, `foreground-midground-background layering` |

建议每组 4 张图。若工具支持 seed，固定 seed；若不支持，固定同一工具、同一比例、同一版本、同一参考图状态。

## 实验 1：高级角色海报

目标：验证 `negative space / clear visual hierarchy / title-safe space` 是否能提升封面感。

原始需求：

```text
帮我做一张高级的角色海报。
```

A 组 prompt 方向：

```text
cinematic character poster, lone elegant character standing in a quiet urban night, refined outfit, soft dramatic lighting, premium mood, detailed texture --ar 3:4 --v 8.1 --style raw --no text, watermark, logo, blurry, low quality
```

B 组 prompt 方向：

```text
cinematic character poster, lone elegant character standing in a quiet urban night, refined outfit, soft dramatic lighting, restrained composition, large negative space, clear visual hierarchy, single focal point, clean title-safe space, premium mood, detailed texture --ar 3:4 --v 8.1 --style raw --no text, watermark, logo, blurry, low quality
```

观察：

- 主体是否更清楚？
- 留白是否真的能放标题？
- 是否减少背景抢戏？
- 是否仍然有角色气质，而不是变空？

## 实验 2：主体不够突出

目标：验证 `single dominant subject / clean silhouette / uncluttered background` 是否比单纯加光影更有效。

原始需求：

```text
这个图主体不够突出。
```

A 组改法：

```text
stronger rim lighting, brighter subject, more contrast, cinematic lighting
```

B 组改法：

```text
single dominant subject, clean silhouette, uncluttered background, reduced background detail, subtle rim lighting only around the subject
```

观察：

- 第一眼是否更快识别主体？
- 背景复杂度是否下降？
- 主体是否因为轮廓清楚而不是因为“更亮”才突出？
- 是否损失场景氛围？

## 实验 3：有故事感的场景图

目标：验证 `foreground-midground-background layering / subject looking away / environmental framing` 是否能提升叙事感。

原始需求：

```text
我想做一个有故事感的场景图。
```

A 组 prompt 方向：

```text
cinematic scene, a person standing in an old train station at dusk, emotional atmosphere, soft light, realistic details, quiet mood --ar 16:9 --v 8.1 --style raw --no text, watermark, logo, blurry, low quality
```

B 组 prompt 方向：

```text
cinematic scene, a person standing in an old train station at dusk, foreground framing with blurred platform columns, midground subject looking away from the camera, atmospheric background depth, environmental framing, clear visual path toward the subject, soft light, realistic details, quiet mood --ar 16:9 --v 8.1 --style raw --no text, watermark, logo, blurry, low quality
```

观察：

- 是否出现前景 / 中景 / 远景？
- 主体“不看镜头”是否增强故事感？
- 环境是否服务人物，而不是变成空背景？
- 画面是否更像“一个时刻”，而不是角色摆拍？

## 实验 4：二选一判断

目标：验证二选一时能否显式加入构图判断。

记录格式：

```markdown
选第 X 张。

构图原因：
- 主体第一眼更明确 / 更弱
- 视觉重心更稳 / 更散
- 留白更服务情绪 / 只是空
- 前中后景层次更清楚 / 更平

非构图原因：
- 光影：
- 质感：
- 题眼：
```

禁止只用“更高级 / 更有感觉 / 更电影感”做判断。

## 实验 5：Seedance 构图迁移

目标：验证静态构图词能否转成镜头段落。

静态构图：

```text
negative space, single focal point, foreground-midground-background layering
```

Seedance 迁移写法：

```text
0-2s: Start with a wide frame and large negative space on the left side, keeping one clear focal subject on the right third of the frame.
2-5s: Slow push-in toward the subject while foreground objects pass softly across the frame, creating depth without blocking the main silhouette.
5-8s: Hold a stable final composition with foreground framing, midground subject, and atmospheric background depth.
No visible text, no logo, no watermark.
```

观察：

- 静态构图是否在视频里被保留？
- 镜头运动是否破坏留白？
- 前景运动是否增强层次，而不是遮挡主体？
- 末帧是否能作为稳定画面继续接 Remotion / 剪辑？

## 评分表

每张图 / 视频按 1-5 分记录：

| 维度 | 分数 | 备注 |
|---|---:|---|
| 主体明确度 |  |  |
| 视觉重心稳定度 |  |  |
| 留白有效性 |  |  |
| 前中后景层次 |  |  |
| 背景克制度 |  |  |
| 题眼 / 情绪表达 |  |  |

通过标准：B 组在至少 4 个维度上平均高于 A 组，且没有明显牺牲题眼和情绪表达。

## 结论记录模板

```markdown
## 实验结论

- 工具：
- 日期：
- 题目：
- A 组结果：
- B 组结果：
- 哪些构图词有效：
- 哪些构图词无效或副作用明显：
- 是否更新 `aigc-prompt-optimizer`：
```

## 关联文档

- [[AIGC构图意图层_v1]]
- [[aigc-prompt-optimizer/SKILL.md]]
- [[Seedance2.0_素材准备清单]]
