---
tags: [类型/方法论, 主题/prompt, 主题/构图, 主题/AIGC]
---
# AIGC 构图意图层 v1

> 触发：2026-06-09 从外部摄影 / 设计基础资料补入 `aigc-prompt-optimizer` 的构图层。
> 定位：不是摄影课，而是把构图原则翻译成 AIGC 可执行 prompt 变量和看图反馈变量。

## 来源判别

本轮只采用三类资料：

- 摄影生产工具 / 相机厂商资料：Adobe、Nikon，用于确认 rule of thirds、leading lines、negative space、景别与视角等摄影构图基础。
- 博物馆教育资料：Getty，用于确认艺术形式分析里的 balance、emphasis、movement、line 等基础概念。
- 设计教育资料：Interaction Design Foundation，用于确认 visual hierarchy、negative space / white space 对注意力、清晰度和层级的作用。

未采用普通营销号、无来源教程、只列“十大构图技巧”但没有解释视觉机制的文章。

## 核心转译

构图在 AIGC 里不是“画面好看”的同义词，而是四个更可控的问题：

1. 观众第一眼看哪里？
2. 主体和环境是什么关系？
3. 画面靠什么产生稳定、压迫、孤独或故事感？
4. 哪些东西应该被排除，避免抢走视觉重心？

因此 `aigc-prompt-optimizer` 的图片公式改为：

```text
[画面类型], [主体 + 姿态], [服装/外观细节], [环境/背景元素],
[构图意图], [光影效果], [调色方案] color grading, [风格关键词],
[镜头语言], [细节/画质关键词]
```

构图意图必须位于主体 / 环境之后、光影 / 风格之前。原因是：先决定观看路径，再决定如何照亮它。

## 5 个优先实验变量

| 变量 | 来源原则 | AIGC prompt 写法 | 看图时判断 |
|---|---|---|---|
| 视觉层级 | visual hierarchy / emphasis | `clear visual hierarchy`, `single focal point`, `dominant subject` | 第一眼是否知道看哪里 |
| 负空间 | negative space / white space | `negative space`, `large empty background`, `title-safe space` | 留白是否强调主体，而不是空 |
| 视觉重量 | balance / visual weight | `balanced composition`, `asymmetrical balance`, `off-center composition` | 画面是否稳，是否一边过重 |
| 引导线 | line / movement / leading lines | `leading lines toward the subject`, `diagonal composition`, `environmental framing` | 视线是否被带向主体 |
| 层次深度 | depth / foreground-midground-background | `foreground framing`, `midground subject`, `atmospheric background depth` | 是否有前中后景，不是平贴背景 |

## 口语需求翻译表

| 用户说法 | 先不要写 | 改写成 |
|---|---|---|
| 高级一点 | high-end, beautiful | `restrained composition, negative space, clear visual hierarchy` |
| 主体突出一点 | make it pop | `single dominant subject, clean silhouette, uncluttered background` |
| 有故事感 | cinematic story | `foreground-midground-background layering, subject looking away, environmental framing` |
| 更震撼 | epic, powerful | `low-angle shot, strong foreground scale, diagonal composition` |
| 像封面 | cover style | `bold readable silhouette, single focal point, clean title-safe space` |
| 画面太满 | simpler | `large negative space, fewer props, one main relationship only` |

## 看图反馈检查表

每次出图反馈不要只说“好看 / 不好看”，先过 6 个问题：

1. 主体是否一眼明确？
2. 视觉重心是否稳定？
3. 留白是否服务情绪或信息层级？
4. 背景是否抢戏？
5. 画面是否有前景 / 中景 / 远景层次？
6. 光影和色彩是否服务构图，而不是单独炫技？

如果 1-3 项失败，优先改构图；不要先加细节、加质感、加风格。

## 适用边界

- 适用：MJ / gpt-image / DALL-E / SD / SeaDream 的静态图 prompt；Seedance 只做轻量镜头迁移。
- 不适用：已经定稿的角色图海报排版，那里应优先保护人脸和原图气质，参考 [[aigc-poster-layout/SKILL.md]]。
- 不适用：需要严格剧情连续性的短片分镜。构图层只能解决单镜头质量，不能替代故事结构。

## 参考资料

- [Adobe · The basics of photography composition](https://www.adobe.com/creativecloud/photography/discover/photo-composition.html)
- [Adobe · Leading lines photography](https://www.adobe.com/creativecloud/photography/technique/leading-lines)
- [Nikon · 5 Easy Composition Guidelines](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/5-easy-composition-guidelines)
- [Getty · Understanding Formal Analysis: Elements of Art](https://www.getty.edu/education/teachers/building_lessons/formal_analysis.html)
- [Getty · Understanding Formal Analysis: Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html)
- [Interaction Design Foundation · Visual Hierarchy](https://www.interaction-design.org/literature/topics/visual-hierarchy)
- [Interaction Design Foundation · Negative Space](https://www.interaction-design.org/literature/topics/negative-space)

## 关联文档

- [[AIGC构图层实验协议_v1]]
- [[aigc-prompt-optimizer/SKILL.md]]
- [[prompt的三段式结构_v1]]
- [[主体不看镜头律]]
- [[光暗作为空间叙事工具]]
