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
| [maieutic-deepseek-adapter](#maieutic-deepseek-adapter) | 国内适配 | Maieutic v0.2 DeepSeek / 国内平台 prompt 包 | DeepSeek / Dify / Coze / 国内模型 |
| [subtask-receipt-writer](#subtask-receipt-writer) | 协作回执 | 子任务完成后判断并书写回执文档 | Claude / Codex |
| [song-caption-mv-workflow](#song-caption-mv-workflow) | 歌曲 MV 字幕 | AI 歌曲 MV + Demucs/WhisperX 字幕自动化 | Codex |
| [prompt-master-series](#prompt-master-series) | 系列内容生产 | prompt 作品 → 小红书双卡 + 小白笔记 + 归档 | Claude / Codex |
| [knowledge-base-curator](#knowledge-base-curator) | 知识库策展 | 答疑成果 → 内核版存档 + 学员版分发 | Claude |
| [aigc-video-cover-gpt](#aigc-video-cover-gpt) | 视频封面生成 | 人物参考图 + 脚本 → GPT Image 2 一步出 16:9 封面 | Claude / Codex / GPT |
| [work-weekly-report](#work-weekly-report) | 公司工作周报 | 跨工作区所有仓库一周活动 → 公司三段式周报(写入 work-reports 仓库) | Claude |

---

## aigc-prompt-optimizer

**触发词**：「优化 prompt」「写 MJ prompt」「生成 Seedance 提示词」「prompt battle」「比赛主题」「二选一」「这张图哪里不好」「冠军图复盘」「获奖图分析」「我想做一张……」「把这个需求改成……」

**用途**：把口语化或模糊的 AIGC 创作需求，翻译成适合具体工具的专业提示词；支持比赛主题发散、MJ 出图反馈、二选一选图、冠军图反向复盘和迭代改写。
支持图片工具（Midjourney、gpt-image、DALL-E、SD、SeaDream）和视频工具（Seedance、Sora、Runway、Kling）。

**版本状态**：v1.4 · 2026-06-05 · 新增冠军图反向复盘、日常题尺度跃迁与巨物地貌化规则。

**文件路径**：`E:\knowledge-base\07_skill存档\aigc-prompt-optimizer\SKILL.md`

**与 prompt-master 的区别**：aigc-prompt-optimizer 专注 AIGC 创作场景（图片/视频），内置知识库的风格方法论；prompt-master 覆盖所有 AI 工具（包括 LLM、代码 Agent 等），适合跨场景使用。

---

## prompt-master

**触发词**：「写一个适合 Cursor 的 prompt」「优化这个 ChatGPT prompt」「给 Claude Code 写指令」「LLM prompt 怎么写」

**用途**：全工具路由的提示词工程 skill，覆盖 Claude / GPT / o3 / Midjourney / Runway / Cursor / Devin 等 20+ 工具的 prompt 规范。

**文件路径**：`E:\knowledge-base\07_skill存档\prompt-master\SKILL.md`
**引用文件**：
- `E:\knowledge-base\07_skill存档\prompt-master\references\templates.md`
- `E:\knowledge-base\07_skill存档\prompt-master\references\patterns.md`

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

**版本状态**：v0.1 首轮测试通过，待真实用户测试。核心修正：Insight / Beacon 从固定输出改为事件触发输出。

**文件路径**：`E:\knowledge-base\07_skill存档\maieutic-skill\SKILL.md`

**引用文件**：
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\system_prompt.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\mode_classifier.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\knowledge_mode.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\exploration_mode.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\reflection_mode.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\creation_mode.md`
- `E:\knowledge-base\07_skill存档\maieutic-skill\prompts\reflection_output.md`

**测试文件**：`E:\knowledge-base\07_skill存档\maieutic-skill\tests\test_cases.md`

**测试复盘**：[[测试复盘_MaieuticSkill_v0.1_20260605]]

**v0.2 路线图**：[[路线图_MaieuticSkill_v0.2_国内适配]]

**关联方法论**：[[对话感_关系产生生命力]] · [[语言形式_思维模式_沟通成本]] · [[SKILL入门完全指南]]

---

## maieutic-deepseek-adapter

**触发词**：「Maieutic 国内适配」「DeepSeek Adapter」「国内可用 Maieutic」「Dify 版 Maieutic」「Coze 版 Maieutic」「通义 / 豆包 / Kimi prompt pack」

**用途**：把 maieutic-skill v0.1 的四模式、Research-Assisted 横向能力、Insight / Beacon 事件触发规则迁移到国内可调用环境。它是 prompt 包 / adapter，不改 v0.1 核心 Skill，不做 Web App、数据库、长期记忆或公益子 Skill。

**版本状态**：v0.2 MVP · 2026-06-05 · DeepSeek / 国内平台最小可执行适配包。

**文件路径**：`E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\SKILL.md`

**部署说明**：`E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\README.md`

**引用文件**：
- `E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\prompts\system_prompt.md`
- `E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\prompts\mode_classifier.md`
- `E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\prompts\research_trigger.md`
- `E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\prompts\event_output_protocol.md`

**测试文件**：`E:\knowledge-base\07_skill存档\maieutic-deepseek-adapter\tests\test_cases.md`

**上游**：[[maieutic-skill/SKILL.md]] · [[测试复盘_MaieuticSkill_v0.1_20260605]] · [[路线图_MaieuticSkill_v0.2_国内适配]]

---

## song-caption-mv-workflow

**触发词**：「给这首歌做 MV」「歌词卡点不准」「导出无文字版」「生成 SRT」「歌曲字幕识别」「哼唱太多识别不准」「用 Demucs/WhisperX 跑字幕」

**用途**：把 Suno/AI 音乐作品从 MV 画面、无字版导出、Demucs 人声分离、WhisperX 词级对齐，到短语级 SRT 和中文意译字幕整理成可复用流程。

**文件路径**：`D:\AIGC工作站\知识库\07_skill存档\song-caption-mv-workflow\SKILL.md`

**引用文件**：
- `D:\AIGC工作站\知识库\07_skill存档\song-caption-mv-workflow\references\stay-alive-case-notes.md`

**测试复盘**：[[2026-06-07_Stay_alive_AI音乐公益MV复盘]]

---

## subtask-receipt-writer

**触发词**：「写回执」「回函」「收口简报」「给主会话」「致 GPT 主会话」「子任务完成后回流」「按交接文档规范写」

**用途**：每次执行完工作后，判断是否属于需要回流的子任务；如果是，按 [[交接文档书写规范]] 在 `D:\AIGC工作站\跨会话协作\` 写回执文档。适用于 Codex / Claude / Cowork 与 GPT 主会话之间的工作闭环。若跳蛛先生明确说明是临时任务且不需要回执，则不写回执。

**文件路径**：`E:\knowledge-base\07_skill存档\subtask-receipt-writer\SKILL.md`

**关联方法论**：[[交接文档书写规范]] · [[Cowork协作的接口文件模式]]

---

## prompt-master-series

**触发词**:「做成一期 Prompt 大师」「把这个 prompt 拆解成小红书卡片」「写一份小白能看懂的 prompt 笔记」「出 prompt 四层拆解卡」「给这个主题做封面 + 拆解卡」

**用途**:把一个**已有的** prompt battle 主题作品,沉淀成《目标是成为 Prompt 大师》系列的一期可发布内容:抽象主题破题拆解 + 小红书双卡(封面卡 + prompt 四层拆解卡)+ 零前置可独立阅读的小白笔记 + 系列归档封版。硬规则:克制内敛(不写名次 / 不署名)、小白第一(去双链 / 降术语 / 名词小抄)。

**版本状态**:v1.2.2 · 2026-06-17 · 画廊:站内笔记弹窗(marked)、原图内嵌可下载、一键复制 Prompt、**全局真实点赞计数**(Abacus serverless,每浏览器一次);画廊区块模板同步。

**文件路径**:`E:\knowledge-base\07_skill存档\prompt-master-series\SKILL.md`

**引用文件**:
- `E:\knowledge-base\07_skill存档\prompt-master-series\assets\make_cards.py`(参数化双卡生成器,内置「对话」期可运行样例)
- `E:\knowledge-base\07_skill存档\prompt-master-series\templates\episode_note_template.md`(小白独立笔记骨架)
- `E:\knowledge-base\07_skill存档\prompt-master-series\templates\xiaohongshu_caption_template.md`(小红书正文骨架,内敛克制)
- `E:\knowledge-base\07_skill存档\prompt-master-series\templates\gallery_episode_block.html`(画廊新增一期的 article 区块,小红书入口=活帖直链)

**在线画廊**:https://mr-salticidae.github.io/becoming-a-prompt-master/ · 仓库 https://github.com/Mr-Salticidae/becoming-a-prompt-master

**首期实例**:`E:\目标是成为 Prompt 大师\01_对话\`(独立于知识库,保持库内整洁)

**与相邻 skill 的区别**:`aigc-prompt-optimizer` 从零生成 / 优化获奖图 prompt;`aigc-poster-layout` 保护原图视觉资产做宣传海报;本 skill 负责把「已有作品」加工成「系列化、可发布、小白可读」的内容包。

**关联方法论**:[[抽象题面的同构动作对位法_v1]] · [[概念锚定_风格置换迭代法_v1]] · [[2026-06-12_对话甲骨文二进制获奖图复盘]]

---

## knowledge-base-curator

**触发词**:「整理成笔记」「沉淀进知识库」「存档这个经验」「把这次答疑整理一下」「按知识库规范归档」「做一份发给学员的版本」「产出内核版+学员版」「提炼成一句话律」

**用途**:把一次有 insight 的答疑 / 探索,按本库规范(CLAUDE.md + README)沉淀成两类资产——**内核版**(双链 + 索引 + MOC 登记,嵌入图谱)与**学员版**(无双链、冷读自洽,落 `08_对外分发/` 可直接转发)。四阶段:答疑 → 整理成小白笔记 → 存档内核版(含提炼一句话律)→ 分发学员版。内置易漏点核对(回 README MOC、更新优于创建、颜色单标签、双向溯源)。

**版本状态**:v1.0 · 2026-06-18 · 从「Nano 换屏融合」一次答疑的完整沉淀流程提炼。

**文件路径**:`E:\knowledge-base\07_skill存档\knowledge-base-curator\SKILL.md`

**与相邻 skill 的区别**:`aigc-postmortem` 是写复盘(事实先行);`prompt-master-series` 把作品做成可发布系列内容包;本 skill 专管**把答疑成果按本库规范归档 + 产出对外学员版**,是知识库自身的策展流程。

**关联方法论**:[[README]] · [[07_skill存档索引]]

---

## aigc-video-cover-gpt

**触发词**：「给这个视频做封面」「根据脚本出封面」「用 GPT Image 2 做视频封面」「把人物参考图做成封面」「出 3 张封面」「这条片子发 B 站封面帮我搞一下」

**用途**：把「一张人物参考图 + 一份视频脚本」直接变成若干张可发布的 16:9 横版视频封面，由 GPT Image 2 一步出含中文大标题的整张图。内置从模板提炼的商单封面公式（超大主标题 + 高亮字 + 英文幽灵层 + 顶部品牌条 + 主体右置 + 暗角危险氛围）、按题材选配色、标题钩子发散（默认 3 个），以及来自库内实测的 GPT Image 2 锁脸打法（禁美化 + 点名锚点 + 三级补救阶梯）。prompt 是中间产物。

**核心约定**：一步出整图（不做底图+后期两段式）· 接受 ~92% AI 近似（不抠图换脸）· 只出 16:9 · 若干张=多个标题钩子。

**版本状态**：v1.0 · 2026-06-24 · 从同事「03_封面模板」20+ 套商单 PSD 封面提炼公式 + 库内锁脸研究封装。

**文件路径**：`E:\knowledge-base\07_skill存档\aigc-video-cover-gpt\SKILL.md`

**与相邻 skill 的区别**：`aigc-poster-layout` 保护已定稿原图做手工排版海报（不重绘主体）；`aigc-prompt-optimizer` 是通用 prompt 优化；本 skill 专做「脚本 → 封面」一条龙，接受重画人物、内置封面公式与锁脸补救。

**关联方法论**：[[GPTImage2锁脸的脸占比上限_v1]] · [[严格人脸一致性二创的范式阶梯_假说_v1]] · [[角色一致性金字塔]]

---

## work-weekly-report

**触发词**：「写周报」「本周工作周报」「这周的周报」「提交给公司的周报」「生成周报交公司」

**用途**：把一周跨工作区**所有仓库**（公司平台 `taowhale-site` / 个人创作主业 / 知识库沉淀 / 游戏桌面应用 / 维护）的 git 活动与创作产出，聚合成提交给公司的**标准三段式周报**——一、本周工作总结；二、下周工作计划；三、协助·思考·总结·成长。四阶段：跨仓库扫描取数（扫盘发现 git 仓库，对照 `E:\GitHub仓库对应关系.md` 剔除外部上游）→ 归集到工作线 → 写三段 → 写入并推送 work-reports 仓库。

**版本状态**：v1.0 · 2026-06-29 · 从 work-reports 仓库（`E:\工作报告`）3 期真实周报提炼格式；跨仓库取数命令已实跑验证（上周 06-22~28 各仓库提交数与真实周报内容吻合）。

**文件路径**：`E:\knowledge-base\07_skill存档\work-weekly-report\SKILL.md`

**产物去向**：**写到 work-reports 仓库**（`E:\工作报告\2026\周报\YYYY-MM-DD_MM-DD-周报.md`），推送其 SSH 远程，**不进本知识库**。

**与相邻 skill 的区别**：`aigc-postmortem` 是单作品复盘、`knowledge-base-curator` 是知识库策展，两者产物都在知识库内；本 skill 是**对公司的工作汇报**，跨所有仓库聚合，产物落 work-reports 仓库。

**关联文档**：`E:\工作报告`（work-reports 仓库）· `E:\GitHub仓库对应关系.md`（取数源·仓库清单）

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
