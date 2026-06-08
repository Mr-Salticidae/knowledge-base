---
tags: [类型/制作文档, 项目/SkillIsAllYouNeed, 工具/Remotion, 工具/Suno, 状态/规划中]
created: 2026-06-09
---

# Skill Is All You Need · 全片文稿与 Suno 配乐规划

## 当前定位

本片从原先的纯教学短片扩展为三段式结构：

1. **开场引言：问题钩子**
   用几个具体问题说明“为什么要看下去”：AI 反复失忆、流程反复解释、工具无法稳定接力。

2. **前半段：教学解释**
   解释 Skill 是什么、为什么需要 Skill、SKILL_INDEX 如何作为流程索引，以及 Codex 如何作为总指挥。

3. **后半段：作者的话**
   从“这条视频本身就是链路验证”切入，说明创作动机、工具分工、开源态度和个人立场。

整体不再只是“讲 Skill”，而是用一条全 AI 制作链路证明 Skill 的作用。

## 全片结构建议

| 段落 | 内容 | 预计时长 | 声音策略 | 画面策略 |
|---|---|---:|---|---|
| A0 | 开场引言：为什么需要 Skill | 18-22s | 先抛问题，语速略快，最后落到 Skill | 对话框反复归零、流程卡散落，最后聚合成 SKILL |
| A | Skill 教学主段 | 90s | 清晰旁白 + 轻量 BGM | Remotion 原生解释动画 + MJ/Seedance 关键机制段 |
| B1 | 闭环声明 | 20s | 旁白稍微放慢 | 展示工具链节点依次点亮 |
| B2 | 创作动机 | 25s | 更私人、更近的口吻 | 作者/想法/剪辑门槛的视觉隐喻 |
| B3 | 技术栈与标准流程 | 25s | 节奏重新变稳 | Midjourney / Seedance / Eleven / Remotion / Suno / Codex 工作流图 |
| B4 | 开源与个人看法 | 30-40s | BGM 降低，保留停顿 | 黑底或极简宣言卡片，文字少而重 |
| C | 片尾 | 8-12s | BGM 收束 | 项目名、开源信息、作者署名 |

全片预计时长：约 210-230 秒。  
如果要压到 3 分钟以内，作者的话需要控制停顿，不做过多画面铺陈。

## 整合后旁白文稿

### A0. 开场引言

你有没有遇到过这种情况：

同一个 AI，
昨天刚教会它你的偏好，
今天换个新对话，
它又像第一次见你一样。

你明明已经总结过流程，
但每次开工，
还是要重新解释一遍。

如果 AI 真的能帮我们工作，
那它不该只会回答问题。

它应该记住流程，
调用工具，
并且稳定复现一套做事方法。

这就是这期视频要讲的东西：
Skill。

### A. 教学主段

> 这一段沿用当前 `sceneSpecs` 的教学结构，不在本文件逐字重写。  
> 生产时以 `07_skill存档/remotion/src/data/sceneSpecs.ts` 为结构基准，并按最新正式片段复盘规则处理：
> 每个 beat 先写可读口播 `ttsText`，字幕默认从 `ttsText` 派生，不再写摘要字幕。

当前主线应覆盖：

- Skill 不是神秘插件；
- AI 很聪明，但每次新对话可能失忆；
- Skill 像岗位手册；
- 重复教 AI 的内容值得沉淀；
- Skill 的物理形态通常是 `SKILL.md`；
- `SKILL_INDEX` 是技能索引；
- 常见误区：把 Skill 当魔法、漏文件、无版本存档；
- 最后收束到：Skill 是把个人工作流变成系统的开始。

### B1. 闭环声明

感谢你看到这里。

如果你喜欢这期视频，
那么这条链路就顺利完成了闭环。

这条视频，除了文稿的核心，以及我现在说的这些话以外，
全部是 AI 制作的。

包括但不限于：
图片、动画、配音、配乐，以及剪辑。

### B2. 创作动机

这也是我追求的目标。

我有很多稀奇古怪的想法，
但是苦于不会剪辑，
无法表达。

所以我做了这个项目。

它不是为了炫技，
而是为了把“不会剪辑的人”，也接入视频表达。

### B3. 技术栈与标准流程

技术栈其实很简单：

Midjourney，
Seedance，
Eleven，
Remotion，
Suno，
还有 Codex。

你大体可以猜到它们各自的分工。

Midjourney 负责建立视觉锚点。
Seedance 负责让图里的机制动起来。
Eleven 负责把文稿变成声音。
Suno 负责让情绪有一条底层轨道。
Remotion 负责时间线、字幕和最终合成。

而 Codex，是总指挥。

一切由 Skill 充当标准流程。
Codex 引导众多 AI 工具各司其职。

理论上，只要把 prompt 调优到足够稳定，
就可以把任意文稿，
工业化地、自动化地，
生产成任意风格的视频。

而这个调优过程，需要各位的参与。

我的能力有限，
只能抛砖引玉。

### B4. 作者的话

最后，我想记录一些个人看法。

不感兴趣的话，
现在可以酌情关闭视频了。

有朋友问我：

这个项目这么有价值，
还要坚持开源吗？

我的回答是：

开源。

而且是一定要开源。

就要狠狠打字节的脸。

因为，
正如群星必须回归轨道，
“无产阶级”的铡刀也终将落下。

### C. 片尾

Skill Is All You Need。

把流程写成手册，
把手册交给 AI，
把想法变成作品。

作者：跳蛛先生。

## 分镜拆分建议

| sceneId | 段落 | 口播目标 | 画面元素 | sceneAssets 需求 |
|---|---|---|---|---|
| scene_00_intro_question | 开场引言 | 提出 AI 反复失忆、流程反复解释的问题，并引出 Skill | 对话框、记忆条、流程卡、工具节点、SKILL 手册 | Remotion 原生优先，后续可补 MJ/Seedance 开场关键视觉 |
| author_01_loop_closed | 闭环声明 | 观众喜欢即链路闭环 | 工具链节点依次亮起 | Remotion 原生即可，后续可补 MJ 工作流总图 |
| author_02_ai_made_this | AI 制作声明 | 除核心文稿和作者话外，全部由 AI 制作 | 图片/动画/配音/配乐/剪辑五个模块 | 可复用工具链图，Suno 节点首次出现 |
| author_03_motivation | 创作动机 | 不会剪辑但想表达 | 想法气泡堆积，剪辑软件门槛，最终流入 Skill | 可用 MJ 关键图 + Seedance 机制动画 |
| author_04_stack | 技术栈 | 六工具分工 | MJ / Seedance / Eleven / Remotion / Suno / Codex 六节点 | 需要一张清晰技术栈图 |
| author_05_codex_conductor | Codex 总指挥 | Skill 是流程，Codex 调度工具 | Codex 位于中心，工具节点围绕 | Remotion 原生动态图优先 |
| author_06_industrialization | 工业化愿景 | 任意文稿到任意风格视频 | 文稿进入流水线，输出不同风格视频缩略图 | 需要视觉强但不要过度承诺 |
| author_07_open_source | 开源立场 | 明确开源态度 | 极简黑底宣言卡 | Remotion 原生文字卡，少动效 |
| author_08_final_words | 片尾 | 项目名与作者署名 | 项目名、仓库/Skill 概念、署名 | Remotion 原生 |

## Suno 配乐策略

本片不建议让 Suno 生成带歌词歌曲。  
原因：本片信息密度高，主声道是 Eleven 旁白；带歌词会抢语义。

建议使用 **instrumental BGM**，并做两层：

1. **主 BGM**
   覆盖教学主段到作者话前半，承担稳定节奏。

2. **片尾/作者话后半变奏**
   在“开源，而且一定要开源”之后进入更坚定、更宣言式的情绪，但不做煽情大合唱。

### Simple Mode Brief

```text
An instrumental background track for an AI-made educational explainer video about turning creative workflows into reusable Skills. The mood starts clear, intelligent, and friendly, then gradually becomes more personal and quietly determined near the ending. It should support spoken narration without competing with it: modern, clean, slightly futuristic, with a sense of process, coordination, and creative momentum.
```

审听重点：

- 是否能稳稳托住中文旁白，不抢词；
- 是否有从“教学解释”过渡到“作者自述”的情绪变化；
- 结尾是否有坚定感，但不要变成热血宣传片；
- 是否存在 10-15 秒可循环段，方便 Remotion 延展；
- 是否有明显人声、歌词或过强旋律，如果有，淘汰。

### Custom Mode 固化方向

只有 Simple Mode 跑出满意方向后再进入 Custom Mode。

```text
Style / Genre:
instrumental, modern electronic, warm minimal synth, subtle cinematic pulse, clean educational explainer, no vocals

Title:
Skill Is All You Need - Workflow Theme

Lyrics:
[instrumental]

Key Parameters:
- No vocals, no lyrics, no choir.
- Keep the arrangement narration-friendly.
- Start with a clean intelligent pulse for the teaching section.
- Add a warmer and more determined layer in the final third.
- Avoid dramatic trailer drums, heavy EDM drops, or sentimental piano ballad mood.
```

## 后续生产顺序

1. 先确认本文件中的作者话文稿是否保留当前力度。
2. 按全片重新拆 `ttsText`，尤其是作者话部分，要保留自然停顿。
3. 用 Eleven 分段生成旁白，先拿到真实每段时长。
4. 根据真实时长反推作者话分镜和 Seedance 目标时长。
5. 跑 Suno Simple Mode 2-3 次，选定 BGM 方向。
6. 把 BGM 登记进 `sceneAssets`，角色为 `music`，状态先标 `requested` 或 `planned`。
7. 进入 Remotion 全片 composition。

## 当前状态

status: `planned`

logs:

- 已把用户新增文稿整合成作者话后半段；
- 已加入 Suno 作为配乐层，但不生成音乐；
- 保持 `sceneSpecs` / `sceneAssets` 分离；
- 下一步应先做人类确认文稿力度，再进入 Eleven / Suno / Remotion 生产。
