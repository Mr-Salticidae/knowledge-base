---
tags: [类型/skill存档]
---
# SKILL_INDEX — Skill 使用索引

> 入档：2026-06-04
> 设计原则：**Skill 文件放知识库，调用时 Claude 直接 Read，不依赖动态安装路径**
> 更新规则：新增 / 升级 skill 时先更新本文档，再在 [[07_skill存档索引]] 登记存档版本

---

## 怎么用这份文档

Cowork 的 skill 安装路径每次启动都会变（动态 UUID），无法靠脚本固定安装。
**本索引是替代方案**：把所有 skill 的触发条件、文件路径、使用说明集中在这里，
Claude 读取本文件后即可直接调用对应 SKILL.md，**无需安装到任何目录**。

调用方式：告诉 Claude「查一下 SKILL_INDEX，然后用 `<skill名>` 帮我……」即可。

---

## Skill 总览

| Skill | 类型 | 一句话用途 | 适用工具 |
|---|---|---|---|
| [aigc-prompt-optimizer](#aigc-prompt-optimizer) | 提示词优化 | 口语需求 → 专业 prompt | Claude / Codex |
| [prompt-master](#prompt-master) | 提示词优化（全路由） | 覆盖所有 AI 工具的 prompt 工程 | Claude / Codex |
| [blind-editing-workflow](#blind-editing-workflow) | 视频剪辑 | Python + ffmpeg 蒙眼剪辑工作流 | Claude / Codex |
| [suno-music-brief](#suno-music-brief) | 配乐创作 | Suno 两阶段配乐 brief | Claude / Codex |
| [character-consistency-mj](#character-consistency-mj) | 角色一致性 | MJ 四层金字塔角色一致性 | Claude / Codex |
| [content-publish-sop](#content-publish-sop) | 内容发布 | 入场票审计 + 平台适配 | Claude / Codex |
| [aigc-postmortem](#aigc-postmortem) | 创作复盘 | 事实先行的复盘工作流 | Claude / Codex |
| [ai-short-film-breakdown](#ai-short-film-breakdown) | 短片创作 | AI 短片类型判断与叙事策略 | Claude / Codex |
| [ai-short-film-screenwriting](#ai-short-film-screenwriting) | 短片剧作 | 灵感 → 可制作 AI 短片方案 | Claude / Codex |
| [remotion-explainer-workflow](#remotion-explainer-workflow) | Remotion 视频 | 数据驱动扁平矢量科普解释视频工作流 | Codex |
| [maieutic-skill](#maieutic-skill) | 苏格拉底式共学 | 问题澄清 + 信息收集 + Insight / Beacon | Claude / GPT / Codex |
| [subtask-receipt-writer](#subtask-receipt-writer) | 协作回执 | 子任务完成后判断并书写回执文档 | Claude / Codex |

---

## aigc-prompt-optimizer

**触发词**：「优化 prompt」「写 MJ prompt」「生成 Seedance 提示词」「我想做一张……」「把这个需求改成……」

**用途**：把口语化或模糊的 AIGC 创作需求，翻译成适合具体工具的专业提示词。
支持图片工具（Midjourney、gpt-image、DALL-E、SD、SeaDream）和视频工具（Seedance、Sora、Runway、Kling）。

**文件路径**：`E:\knowledge-base\07_skill存档\aigc-prompt-optimizer\SKILL.md`

**与 prompt-master 的区别**：aigc-prompt-optimizer 专注 AIGC 创作场景（图片/视频），内置知识库的风格方法论；prompt-master 覆盖所有 AI 工具（包括 LLM、代码 Agent 等），适合跨场景使用。

---

## prompt-master

**触发词**：「写一个适合 Cursor 的 prompt」「优化这个 ChatGPT prompt」「给 Claude Code 写指令」「LLM prompt 怎么写」

**用途**：全工具路由的提示词工程 skill，覆盖 Claude / GPT / o3 / Midjourney / Runway / Cursor / Devin 等 20+ 工具的 prompt 规范。

**文件路径**：`E:\knowledge-base\07_skill存档\prompt-master_v1.6.0_SKILL.md`
**引用文件**：
- `E:\knowledge-base\07_skill存档\prompt-master_refs\templates.md`
- `E:\knowledge-base\07_skill存档\prompt-master_refs\patterns.md`

**版本**：v1.6.0 · 存档日期 2026-06-03

---

## blind-editing-workflow

**触发词**：「帮我把这些图做成视频」「按卡点剪辑」「生成剪辑方案」「出剪辑代码」「蒙眼剪辑」

**用途**：让不会专业剪辑软件的创作者用 Python + ffmpeg 完成精确视频剪辑。
AI 生成可审核的剪辑草案 + 可执行代码，创作者负责审美判断和反馈。

**文件路径**：`E:\knowledge-base\07_skill存档\blind-editing-workflow\SKILL.md`

**关联方法论**：[[蒙眼剪辑法_方法论笔记]]

---

## suno-music-brief

**触发词**：「帮我写 Suno prompt」「给这个项目配乐」「用 Suno 做一首歌」「生成 Suno brief」

**用途**：把项目配乐需求转化为 Suno 的 Simple Mode 探索 brief 和 Custom Mode 固化 brief。
核心原则：先 Simple Mode 找 happy accident，再 Custom Mode 锁定。

**文件路径**：`E:\knowledge-base\07_skill存档\suno-music-brief\SKILL.md`

**关联方法论**：[[Suno_v5.5_行为规律]] · [[Suno配乐制作分享]]

---

## character-consistency-mj

**触发词**：「保持角色一致性」「同一个角色不同场景」「sref 怎么用」「oref 锁脸」「角色 IP 设定」

**用途**：用四层金字塔结构（sref / oref-seed-描述词 / personalize-moodboard / 装扮签名）维持 MJ 角色跨图一致性。

**文件路径**：`E:\knowledge-base\07_skill存档\character-consistency-mj\SKILL.md`

**关联方法论**：[[角色一致性金字塔]] · [[sref编号独立律]] · [[装扮签名vs五官精度]]

---

## content-publish-sop

**触发词**：「这个作品要发哪里」「帮我写发布文案」「快手标题怎么写」「网易云怎么填标签」「要不要投流」

**用途**：发布前做入场票审计，判断作品的平台接口，给出快手 / 网易云 / B站等平台的最小适配建议。

**文件路径**：`E:\knowledge-base\07_skill存档\content-publish-sop\SKILL.md`

**关联方法论**：[[入场票框架_v1]] · [[快手分发SOP_v1]] · [[网易云发布Brief_通用模板]] · [[网易云音乐人发布SOP_v1]]

---

## aigc-postmortem

**触发词**：「帮我复盘这次比赛」「写一份获奖图复盘」「整理这个项目的经验」「复盘这次测试」

**用途**：引导创作者先冻结客观事实（结果/数据），再写判断，防止把"我喜欢的方案"误写成"成功的方案"。

**文件路径**：`E:\knowledge-base\07_skill存档\aigc-postmortem\SKILL.md`

**关联方法论**：[[复盘事实先行原则]] · [[好流量是好作品的产物_v3.1反思]]

---

## ai-short-film-breakdown

**触发词**：「我想做一部 AI 短片」「帮我拉片」「分析这部 AI 视频的结构」「怎么讲剧情」「AI 短片怎么选类型」

**用途**：先判断短片类型（概念推演型 / 关系叙事型 / 现实悖论型 / 情绪氛围型），再匹配对应的叙事策略和技术路径。

**文件路径**：`E:\knowledge-base\07_skill存档\ai-short-film-breakdown\SKILL.md`

**关联方法论**：[[概念推演型AI短片_TotalPixelSpace]] · [[现实悖论型AI短片_Jailbird]] · [[多线交叉型AI短片_TheWindshieldWiper]] · [[强对比型AI短片_IceMerchants]] · [[图生视频_ForwardOnly原则]]

---

## ai-short-film-screenwriting

**触发词**：「我想做一部 AI 短片」「这个故事能不能拍」「帮我设计短片结构」「把这个灵感变成短片方案」「诊断这个剧本为什么单薄」

**用途**：把初始灵感、主题、现实素材、人物关系或已有梗概发展成适合 AI 视频制作的短片方案。重点输出观看规则、视觉锚点、核心动作、情绪曲线、剧作结构、分镜方向和 AI 制作可行性评估。

**文件路径**：`E:\knowledge-base\07_skill存档\ai-short-film-screenwriting\SKILL.md`

**与 ai-short-film-breakdown 的区别**：`ai-short-film-breakdown` 偏拉片分析和类型判断；`ai-short-film-screenwriting` 偏从灵感生成方案、诊断故事单薄、设计可制作的短片结构。

**关联方法论**：[[概念推演型AI短片_TotalPixelSpace]] · [[现实悖论型AI短片_Jailbird]] · [[多线交叉型AI短片_TheWindshieldWiper]] · [[强对比型AI短片_IceMerchants]] · [[图生视频_ForwardOnly原则]]

---

## remotion-card-video

**触发词**：「帮我做成视频」「生成 Remotion 脚本」「出 TSX 代码」「做成卡片视频」「把这篇做成 B 站视频」

**用途**：把知识类内容翻译成「极简知识卡片流」风格的 Remotion 视频。内置设计系统（颜色/字号/间距 tokens）、spring 动效规则（克制活泼）、封面/知识卡/代码卡/结尾四类场景组件模板，输出可直接运行的 TSX 代码。

**文件路径**：`E:\knowledge-base\07_skill存档\remotion\SKILL.md`

**关联方法论**：[[AIGC_Skill到Remotion视频闭环]] · [[SKILL入门完全指南]]

---

## remotion-explainer-workflow

**触发词**：「Remotion 科普视频」「sceneSpecs」「sceneAssets」「做 in a nutshell 风格解释动画」「设计 Remotion 视频工作流」「Skill 调用协议」

**用途**：把笔记、脚本、总纲或 sceneSpecs 转成数据驱动的 Remotion 科普解释视频生产计划。主路线是 in a nutshell inspired flat-vector explainer；支持 sceneSpecs / sceneAssets 拆分、dry-run Skill 调用协议、与现有 Skill 的组合规划。

**文件路径**：`E:\knowledge-base\07_skill存档\remotion-skill\SKILL.md`

**引用文件**：
- `E:\knowledge-base\07_skill存档\remotion-skill\references\skill-call-protocol.md`
- `E:\knowledge-base\07_skill存档\remotion-skill\references\scene-assets.md`
- `E:\knowledge-base\07_skill存档\remotion-skill\references\remotion-skill-ts-relationship.md`

**关联方法论**：[[AIGC_Skill到Remotion视频闭环]] · [[蒙眼剪辑法_方法论笔记]] · [[SKILL入门完全指南]]

---

## maieutic-skill

**触发词**：「Maieutic」「苏格拉底式共学」「帮我把问题想清楚」「我很迷茫」「学习路径」「创作构思」「信息收集」「Insight」「Beacon」

**用途**：把 Maieutic 封装成可被 Claude / GPT / 本地 Agent 调用的 Skill。核心能力是根据用户问题切换 Knowledge / Exploration / Reflection / Creation 四种模式，并在需要时启用 Research-Assisted Mode，最后输出 Insight 与 24 小时内可执行的 Beacon。

**文件路径**：`D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\SKILL.md`

**引用文件**：
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\system_prompt.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\mode_classifier.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\knowledge_mode.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\exploration_mode.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\reflection_mode.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\creation_mode.md`
- `D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\prompts\reflection_output.md`

**测试文件**：`D:\AIGC工作站\知识库\07_skill存档\maieutic-skill\tests\test_cases.md`

**关联方法论**：[[对话感_关系产生生命力]] · [[语言形式_思维模式_沟通成本]] · [[SKILL入门完全指南]]

---

## subtask-receipt-writer

**触发词**：「写回执」「回函」「收口简报」「给主会话」「致 GPT 主会话」「子任务完成后回流」「按交接文档规范写」

**用途**：每次执行完工作后，判断是否属于需要回流的子任务；如果是，按 [[交接文档书写规范]] 在 `D:\AIGC工作站\跨会话协作\` 写回执文档。适用于 Codex / Claude / Cowork 与 GPT 主会话之间的工作闭环。

**文件路径**：`E:\knowledge-base\07_skill存档\subtask-receipt-writer\SKILL.md`

**关联方法论**：[[交接文档书写规范]] · [[Cowork协作的接口文件模式]]

---

## 新增 Skill 的登记规范

1. 在 `07_skill存档/` 下新建同名子目录，放入 `SKILL.md`
2. 在 [[07_skill存档索引]] 的表格里登记版本 + 归档日期
3. 在本文档新增一个 `##` 段，填写：触发词、用途、文件路径、关联方法论
4. 在根 README 的「主题脉络十一」补一行 `[[]]` 链接

## 关联文档

- 全库入口：[[README]]
- Skill 存档区：[[07_skill存档索引]]
- Skill 使用入门：[[SKILL入门完全指南]]
