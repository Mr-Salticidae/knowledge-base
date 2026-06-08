---
tags: [类型/制作文档, 项目/SkillIsAllYouNeed, 工具/Suno, 状态/待执行]
created: 2026-06-09
---

# Skill Is All You Need · Suno BGM Brief

## 目标

为 224.87 秒全片生成一条不抢中文旁白的纯配乐。

视频结构：

- 开场引言：AI 失忆、流程反复解释、引出 Skill；
- 教学主段：解释 Skill / SKILL.md / SKILL_INDEX / Codex 调度；
- 作者的话：闭环声明、创作动机、AI 工具链、开源态度；
- 片尾：项目名与作者署名。

配乐应服务旁白，不承担歌词叙事。

## 第一阶段：Simple Mode

直接把下面文本放入 Suno Simple Mode，建议连续生成 2-3 次。

```text
An instrumental background track for an AI-made educational explainer video about turning creative workflows into reusable Skills.
The mood starts clear, intelligent, and friendly, with a clean sense of process and coordination.
In the final third, it becomes warmer, more personal, and quietly determined, like a creator explaining why open workflows matter.
It must support spoken narration without competing with it: modern, clean, slightly futuristic, calm, focused, and emotionally steady.
```

审听标准：

- 必须是纯配乐，不能有人声、歌词、合唱或明显哼唱；
- 中文旁白能清楚压在音乐上方，旋律不能抢词；
- 前 90 秒适合教学解释，有清晰但克制的推进感；
- 后三分之一有更私人、更坚定的情绪，但不能变成热血宣传片；
- 最好存在 10-15 秒可循环片段，方便 Remotion 延展；
- 不要重鼓点、EDM drop、煽情钢琴 ballad、电影预告片大鼓。

## 第二阶段：Custom Mode 固化模板

只有 Simple Mode 出现满意方向后，再用这个模板固化。

```text
Style / Genre:
instrumental, modern electronic, warm minimal synth, subtle cinematic pulse, clean educational explainer, narration-friendly, no vocals

Title:
Skill Is All You Need - Workflow Theme

Lyrics:
[instrumental]

Key Parameters:
- No vocals, no lyrics, no choir, no humming.
- Keep the arrangement narration-friendly and leave space for Chinese voiceover.
- Start with a clean intelligent pulse for the teaching section.
- Add a warmer and more determined layer in the final third.
- Avoid dramatic trailer drums, heavy EDM drops, sentimental piano ballad mood, and overly catchy lead melodies.
- A loopable 10-15 second section is useful for Remotion extension.
```

## 导入 Remotion 的目标路径

生成并选定最终版本后，保存为：

```text
public/audio/suno/skill-is-all-you-need-workflow-theme.mp3
```

随后把 `sceneAssets` 中 `asset_global_suno_workflow_theme` 的状态从 `planned` 改为 `linked` 或 `verified`，并接入全片 composition 的 BGM 音轨。

## 当前状态

status: `brief_ready`

notes:

- 旁白已由 Eleven 生成并接入 `SkillIsAllYouNeedFullFilm`；
- 全片真实时长为 6746 帧，30fps，约 224.87 秒；
- 本阶段只执行 Suno 探索 brief，不直接锁死 Custom Mode。
