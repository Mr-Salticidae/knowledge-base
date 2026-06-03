---
tags: [类型/skill存档]
---
# Skill 存档索引

> 用途:固定存放测试过的 skill 原文与版本记录。每测一个 skill,就把它的 SKILL.md(及引用文件)原样归档到这里,配上版本号、归档日期和对应的测试复盘链接,方便日后回看与版本对比。

## 存档规则

- 文件名格式:`<skill名>_v<版本号>_SKILL.md`,内容为 **verbatim 原文**,不改动。
- 同一 skill 升级版本后,新建一份带新版本号的文件,旧版保留,便于 diff。
- 引用文件(如 `references/templates.md`)若本地存在,一并归档到 `<skill名>_refs/` 子目录。
- 每条记录在下表登记:skill、版本、归档日期、来源路径、对应测试复盘。

## 已存档 Skill

| Skill | 版本 | 归档日期 | 类型 | 安装目标 | 对应测试复盘 |
|---|---|---|---|---|---|
| prompt-master | v1.6.0 | 2026-06-03 | 提示词优化(图片 + 视频 + LLM + Agent 等全工具路由) | Claude + Codex | [[2026-06-03_口语化需求到专业提示词_图片+视频双skill复盘]] |
| aigc-prompt-optimizer | v1.0 | 2026-06-04 | 口语化需求 → 专业 prompt（MJ / gpt-image / Seedance 等） | Claude + Codex | 待测试 |
| blind-editing-workflow | v1.0 | 2026-06-04 | 蒙眼剪辑法——AI 辅助视频剪辑闭环（Python + ffmpeg） | Claude + Codex | 待测试 |
| suno-music-brief | v1.0 | 2026-06-04 | Suno 两阶段配乐创作（Simple→Custom） | Claude + Codex | 待测试 |
| character-consistency-mj | v1.0 | 2026-06-04 | MJ 角色一致性四层金字塔 | Claude + Codex | 待测试 |
| content-publish-sop | v1.0 | 2026-06-04 | 内容发布入场票审计 + 平台适配（快手/网易云） | Claude + Codex | 待测试 |
| aigc-postmortem | v1.0 | 2026-06-04 | 创作复盘工作流（事实先行，防自我归因偏差） | Claude + Codex | 待测试 |
| ai-short-film-breakdown | v1.0 | 2026-06-04 | AI 短片类型判断与创作策略 | Claude + Codex | 待测试 |

### prompt-master v1.6.0 备注

- 文件:[[prompt-master_v1.6.0_SKILL.md]]
- 来源:`https://github.com/nidhinjs/prompt-master`
- 一份 skill 覆盖图片(Midjourney / DALL-E / SD / SeeDream / gpt-image)与视频(Sora / Runway / Kling / Seedance 等)两类路由。本次「图片 prompt 优化」与「视频 prompt 优化」两组测试实际都由它驱动。
- 已补归档公开仓库引用文件:[[prompt-master_refs/templates.md]]、[[prompt-master_refs/patterns.md]]。
- `templates.md` 已核对包含 Template A-M;`patterns.md` 为公开源原文,保留其末行原样。

### 本次封装的 7 个 Skill（v1.0，2026-06-04）

来源：知识库 `04_方法论与洞察` 全量工作流整理。每个 Skill 的 `SKILL.md` 存放在同名子目录下。

- [[aigc-prompt-optimizer/SKILL.md]] — Claude + Codex 双装
- [[blind-editing-workflow/SKILL.md]] — Codex only（本地 Python + ffmpeg）
- [[suno-music-brief/SKILL.md]] — Claude only
- [[character-consistency-mj/SKILL.md]] — Claude only
- [[content-publish-sop/SKILL.md]] — Claude only
- [[aigc-postmortem/SKILL.md]] — Claude only
- [[ai-short-film-breakdown/SKILL.md]] — Claude only

调用方式：在对话开始时告知 Claude SKILL_INDEX.md 位置，Claude 读取索引后自动判断触发并 Read 对应 SKILL.md 执行，无需安装。

## 关联文档

- 全库入口:[[README]