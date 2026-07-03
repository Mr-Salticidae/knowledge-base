---
tags: [类型/方法论, 工具/GPT-Image, 通用/prompt工程, 模板]
---
# GPT Image 2 游戏动作精灵图 · 三段锁定法 v1

> 首次记录:2026-07-03
> 状态:**已验证(首验,单角色两案例)**——机器兔角色(有目标效果图参考)+ 边牧狗狗角色(仅四视图定妆表、无目标效果图)两次均出片,作者确认可用
> 作者:跳蛛先生 + Claude
> 应用去向:独立游戏《Last Stand》怪物动作关键帧(待实战)

---

## 一句话总结

给 GPT Image 2 一张角色定妆图(单图或四视图皆可),用**「参考图硬锁 + 网格排版规范 + 逐行动作分解」三段式 prompt**,能直接产出绿幕、多行多帧、可抠可剪的游戏动作关键帧精灵图——角色一致性靠"特征清单写死 + 易丢配饰逐帧点名"压住。

---

## 适用场景

- 独立游戏角色 / 怪物 / NPC 的动作关键帧(待机、走路循环、攻击、倒地等);
- 需要绿幕背景、后期抠像进引擎或剪辑软件的素材;
- 手上只有一张定妆图或一张四视图 turnaround,没有现成动画参考。

---

## 方法:三段式 prompt 结构

### 第一段 · 参考图硬锁(角色一致性)

开头即声明"Using the attached character reference image / turnaround sheet as the ONLY character reference",然后**把角色特征逐项写死成清单**:体型、配色、五官、材质风格、每一件配饰。

关键手法:
- **特征清单不嫌啰嗦**:白色球形机身、青色半透明兔耳、黑色面罩、双竖条发光眼……一项都别省。模型漂移的就是你没写的那项。
- **易丢配饰显式点名"每帧必须出现"**:小物件(帽子、徽章、围巾、挂饰)是最高频丢失项,单独写一句 "the straw hat, badge and neckerchief MUST appear in every single frame with unchanged colors"。
- 画风也要锁:"same clean cel-shaded anime style with crisp dark outlines as the reference",防止行与行之间画风漂移。

### 第二段 · 网格排版规范(工程可用性)

- **绿幕纯色**:flat solid chroma-key green background (#00FF00),写明 no shadows, no gradients, no text, no labels, no grid lines——阴影和渐变都会毁抠像。
- **严格网格**:N rows × N columns、帧数总数、evenly spaced、every frame the same size、character centered in each cell。
- **基线对齐**:走路类动作加 "feet aligned to the same baseline within each row",否则逐帧播放会上下跳。
- **光照统一**:consistent lighting from the upper left in all frames。

### 第三段 · 逐行动作分解(一行一动作)

每行一个动作,单独一段描述:视角 + 动作过程 + 表情 + 帧间变化逻辑(如 "the 6 frames form one smooth walk loop with alternating legs")。

**四视图定妆表的独特优势——按行锚定视角**:参考图是 front/left/right/back 四视图时,每行动作直接写 "matching the LEFT view of the reference sheet",左走锚左视图、右走锚右视图、正面动作锚正视图。视角一致性瞬间稳定,这是单张定妆图给不了的。

---

## 实操经验(踩坑清单)

| 问题 | 对策 |
|---|---|
| 一次生成 24 帧,帧数不严格、个别帧漂移 | **逐行生成后挑帧重拼**更稳:每次只保留一个 Row 段落,后期拼接。工程交付优先走这条 |
| 走路循环卡顿 | 6 帧是下限,要顺滑改 8 帧(行数×列数与各行帧数同步改) |
| "趴下"类动作播起来怪 | 过渡动画(transition)≠循环动画(loop),进引擎只播一遍、停末帧 |
| 参考图上的中文标注(正视图/左视图)被抄进结果 | 裁掉参考图底部文字再上传 |
| 附了目标效果图,结果被原样照抄 | **只附角色定妆图,不附目标效果图**;目标效果用文字描述,让模型重新演绎 |

---

## 可复用 prompt 骨架

```
Using the attached character [reference image / turnaround sheet (front, left, right, back views)] as the ONLY character reference, generate a game animation sprite sheet of this exact character. The character MUST stay identical to the reference in every frame: [特征清单:体型/配色/五官/材质/每件配饰,逐项写死]. Same proportions, same colors, same [画风描述] as the reference.

Layout: a sprite sheet arranged in a strict grid of [N] rows × [M] columns, [N×M] frames total, evenly spaced, every frame the same size, character centered in each cell, feet aligned to the same baseline within each row. Flat solid chroma-key green background (#00FF00) filling the entire canvas, no shadows, no gradients, no text, no labels, no grid lines.

Row 1 — [动作名]: [视角(可锚定参考表对应视图)] + [动作过程] + [表情] + [帧间变化逻辑,如 the M frames form one smooth loop].
Row 2 — [动作名]: ...
(一行一动作,依此类推)

Consistent lighting from the upper left in all frames. Every frame MUST depict the same character with no design drift: [易丢配饰逐一点名] MUST appear in every single frame with unchanged colors.
```

---

## 举一反三

- **怪物/敌人单位**:同一骨架,把行换成 待机/移动/攻击/受击/死亡 五行,就是标准敌人动作集(《Last Stand》待实战)。
- **表情差分**:行换成不同表情(喜/怒/哀/惊),就是 galgame / 对话立绘差分表。
- **道具/特效帧**:主体换成道具或技能特效,绿幕+网格规范照用。
- 本法与 [[GPT图像一次性生成中文分镜表_v1]] 是同一底层能力(单图内多格协调)的两个应用面:那边是"表格+文字+多图",这边是"角色一致+动作序列";"逐格清单"和"逐行动作"是同一招。

---

## 关联文档

- 同底层能力的姊妹篇:[[GPT图像一次性生成中文分镜表_v1]] —— 单图内多格协调,逐格清单写死布局
- 角色一致性总纲:[[角色一致性金字塔]] —— 本法的"特征清单写死"是其描述锚定层在 GPT Image 2 上的应用
- 工具选择上下文:[[代码生成vsGPT图像_工具选择假说]] —— 本文为其新增数据点:多帧角色动作序列可由 GPT Image 2 单图承载
- GPT Image 2 一致性边界:[[GPTImage2锁脸的脸占比上限_v1]] —— 写实人脸另有占比上限,本法验证于卡通/Q版角色,写实角色套用需留意
- prompt 结构:[[prompt的四段式结构_v1]]
