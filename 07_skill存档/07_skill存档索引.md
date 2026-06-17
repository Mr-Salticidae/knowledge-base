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
| aigc-prompt-optimizer | v1.5 | 2026-06-09 | 口语化需求 → 专业 prompt；新增 prompt battle 发散、出图反馈、二选一、冠军图复盘、尺度跃迁、巨物地貌化与构图意图层 | Claude + Codex | 待正式复盘 |
| blind-editing-workflow | v1.0 | 2026-06-04 | 蒙眼剪辑法——AI 辅助视频剪辑闭环（Python + ffmpeg） | Claude + Codex | 待测试 |
| suno-music-brief | v1.0 | 2026-06-04 | Suno 两阶段配乐创作（Simple→Custom） | Claude + Codex | 待测试 |
| character-consistency-mj | v1.0 | 2026-06-04 | MJ 角色一致性四层金字塔 | Claude + Codex | 待测试 |
| content-publish-sop | v1.0 | 2026-06-04 | 内容发布入场票审计 + 平台适配（快手/网易云） | Claude + Codex | 待测试 |
| aigc-postmortem | v1.0 | 2026-06-04 | 创作复盘工作流（事实先行，防自我归因偏差） | Claude + Codex | 待测试 |
| ai-short-film-breakdown | v1.0 | 2026-06-04 | AI 短片类型判断与创作策略 | Claude + Codex | 待测试 |
| ai-short-film-screenwriting | v1.0 | 2026-06-04 | AI 短片剧作辅助（灵感 → 可制作短片方案） | Claude + Codex | 待测试 |
| remotion-explainer-workflow | v0.1 | 2026-06-04 | Remotion 科普解释视频工作流（sceneSpecs / sceneAssets / Skill 调用协议） | Codex | 待测试 |
| subtask-receipt-writer | v1.1 | 2026-06-05 | 子任务完成后的回执 / 回函 / 收口简报书写流程；支持显式免回执 | Claude + Codex | 待测试 |
| maieutic-skill | v0.1 | 2026-06-05 | 苏格拉底式共学 + 信息收集 + Insight / Beacon 输出 | Claude + GPT + Codex | [[测试复盘_MaieuticSkill_v0.1_20260605]] |
| maieutic-deepseek-adapter | v0.2 | 2026-06-05 | Maieutic 国内可用适配 prompt 包（DeepSeek / Dify / Coze / 国内模型） | DeepSeek + 国内平台 | [[maieutic-deepseek-adapter/tests/test_cases.md]] |
| song-caption-mv-workflow | v0.1 | 2026-06-07 | AI 歌曲 MV + Demucs/WhisperX 字幕自动化工作流 | Codex | [[2026-06-07_Stay_alive_AI音乐公益MV复盘]] |
| prompt-master-series | v1.2.0 | 2026-06-17 | 系列内容生产:prompt 作品 → 小红书双卡 + 正文 + 小白笔记 + GitHub Pages 画廊上线 | Claude + Codex | [[2026-06-12_对话甲骨文二进制获奖图复盘]] |

### prompt-master v1.6.0 备注

- 文件:[[prompt-master/SKILL.md]]
- 来源:`https://github.com/nidhinjs/prompt-master`
- 一份 skill 覆盖图片(Midjourney / DALL-E / SD / SeeDream / gpt-image)与视频(Sora / Runway / Kling / Seedance 等)两类路由。本次「图片 prompt 优化」与「视频 prompt 优化」两组测试实际都由它驱动。
- 已补归档公开仓库引用文件:[[prompt-master/references/templates.md]]、[[prompt-master/references/patterns.md]]。
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

### aigc-prompt-optimizer v1.5（2026-06-09）

来源：`请你吃个冰淇淋` Midjourney prompt battle 实测迭代与冠军图复盘。

- [[aigc-prompt-optimizer/SKILL.md]] — Claude + Codex

2026-06-09 升级：补入 AIGC 构图意图层 / 画面生成判断层。图片 prompt 在主体、外观、环境之后必须补构图意图，再进入光影、调色和风格；看图反馈时必须判断主体是否明确、视觉重心是否稳定、留白是否服务情绪、背景是否抢戏、是否有前中后景层次。该升级优先服务 MJ / gpt-image 图片生成；Seedance 只做轻量迁移，将静态构图翻译成镜头段落和画面层次。

本次升级补入 prompt battle 工作流：先做题眼发散，再收束主视觉；看图反馈时先诊断主体关系、题眼清晰度、构图光影与质感，再只改关键 prompt 变量；二选一时必须给明确判断；看到冠军图 / 获奖图时先反向复盘其获胜原因并提炼可迁移规则。

2026-06-05 追加：从"请你吃个冰淇淋"主题下的冰淇淋彗星图提炼"尺度跃迁"规则。日常物件题除了关系叙事，也要发散一条宏观奇观路线：把小物件转译为天体、气象、地貌、海面或城市事件，同时保留原物件轮廓、材质和物理痕迹。

2026-06-05 追加：从《童话镇里的纸飞机》获奖图复盘提炼"巨物地貌化"规则。具体物件题除了作为道具或自然现象,也可以变成微型居民可攀爬、探索、定居或围观的空间地貌;LEGO / 玩具沙盘 / 微缩摄影可把潜在危险的巨物事件转成童年想象和公共冒险。

### remotion-explainer-workflow v0.1（2026-06-04）

来源：`Remotion_Skill_设计总纲领_交接给_Codex.md` 与当前 Remotion MVP 工程。

- [[remotion-skill/SKILL.md]] — Codex
- [[remotion-skill/references/skill-call-protocol.md]] — Skill 调用协议
- [[remotion-skill/references/scene-assets.md]] — sceneAssets 数据结构建议
- [[remotion-skill/references/remotion-skill-ts-relationship.md]] — 与当前 `RemotionSkill.ts` 的关系说明

### subtask-receipt-writer v1.0（2026-06-04）

来源：跳蛛先生本轮规则确认——每次执行完工作后，判断是否是子任务；若是子任务，则按照 [[交接文档书写规范]] 书写回执文档。

- [[subtask-receipt-writer/SKILL.md]] — Claude + Codex

2026-06-05 补充：当跳蛛先生明确说明是子会话临时任务且“不需要写回执”时，当前指令优先，不写回执。

调用方式：在对话开始时告知 Claude `07_skill存档/SKILL_INDEX.md` 位置，Claude 读取索引后自动判断触发并 Read 对应 SKILL.md 执行，无需安装。

### ai-short-film-screenwriting v1.0（2026-06-04）

来源：`AI短片_剧作Skill_交接文档.md` 与四篇 AI 短片 / 动画短片拉片方法论。

- [[ai-short-film-screenwriting/SKILL.md]] — Claude + Codex

定位：从初始灵感、主题、现实素材或已有梗概生成可制作 AI 短片方案；与 [[ai-short-film-breakdown/SKILL.md]] 的区别是前者偏剧作生成与诊断，后者偏拉片分析与类型判断。

### maieutic-skill v0.1（2026-06-05，首轮测试通过）

来源：`D:\AIGC工作站\Maieutic_Skill_MVP\` 与 `Maieutic_Skill_MVP_交接资料包.zip`。当前版本是 Skill 化 MVP，不继续 Web App，不接数据库，不做长期记忆。

- [[maieutic-skill/SKILL.md]] — Claude + GPT + Codex
- [[maieutic-skill/prompts/system_prompt.md]] — Maieutic 身份、灯塔原则、禁止事项
- [[maieutic-skill/prompts/mode_classifier.md]] — Knowledge / Exploration / Reflection / Creation 模式判定
- [[maieutic-skill/prompts/reflection_output.md]] — Insight / Beacon 标准输出模板
- [[maieutic-skill/tests/test_cases.md]] — 5 个 MVP 测试案例
- [[maieutic-skill/测试复盘_MaieuticSkill_v0.1_20260605.md]] — 首轮测试复盘
- [[maieutic-skill/路线图_MaieuticSkill_v0.2_国内适配.md]] — v0.2 国内可用适配路线图

定位：帮助使用者把问题想清楚，并在必要时补足信息。首轮测试后已确认 Insight / Beacon 采用事件触发输出：Insight 只在出现真实认知推进时出现，Beacon 只在需要实操下一步时出现。

### maieutic-deepseek-adapter v0.2（2026-06-05，国内适配 MVP）

来源：`Maieutic_Skill_v0.2国内适配任务包.zip` 与 [[maieutic-skill/路线图_MaieuticSkill_v0.2_国内适配]]。当前版本不改动 v0.1 核心 Skill，只把 v0.1 行为迁移成国内模型 / 工作流平台可复制的 prompt 包。

- [[maieutic-deepseek-adapter/SKILL.md]] — 适配包入口
- [[maieutic-deepseek-adapter/README.md]] — DeepSeek / Dify / Coze / 通义 / 豆包 / Kimi 部署说明
- [[maieutic-deepseek-adapter/prompts/system_prompt.md]] — 国内模型 system prompt
- [[maieutic-deepseek-adapter/prompts/mode_classifier.md]] — 四模式分类规则
- [[maieutic-deepseek-adapter/prompts/research_trigger.md]] — Research-Assisted 国内环境触发与限制说明
- [[maieutic-deepseek-adapter/prompts/event_output_protocol.md]] — Insight / Beacon 事件触发协议
- [[maieutic-deepseek-adapter/tests/test_cases.md]] — 5 个 v0.1 回归测试案例

定位：面向国内可访问环境的最小可执行适配层。重点是可复制、可测试、可迁移，而不是新增产品功能。

### song-caption-mv-workflow v0.1（2026-06-07，Stay alive 实战跑通）

来源：《Stay alive》AI 音乐公益 MV 从 Suno 创作、MJ 抽象视觉、蒙眼剪辑、电影感渲染，到 Demucs + WhisperX GPU 字幕链路的完整实战。

- [[song-caption-mv-workflow/SKILL.md]] — Codex
- [[song-caption-mv-workflow/references/stay-alive-case-notes.md]] — 实战环境与关键经验
- 对应复盘：[[2026-06-07_Stay_alive_AI音乐公益MV复盘]]

### prompt-master-series v1.2.0(2026-06-17,首期《对话》跑通并上线画廊)

来源:本会话把「《对话》获奖图 → 小红书双卡 → 小红书正文 → 小白独立笔记 → 系列归档 → GitHub Pages 画廊」的全流程沉淀为可复用 skill。

- [[prompt-master-series/SKILL.md]] — Claude + Codex
- [[prompt-master-series/assets/make_cards.py]] — 参数化小红书双卡生成器(Pillow,每期只改顶部 CONFIG)
- [[prompt-master-series/templates/episode_note_template.md]] — 小白独立笔记骨架(长 · 存档)
- [[prompt-master-series/templates/xiaohongshu_caption_template.md]] — 小红书正文骨架(短 · 发布,内敛克制)
- [[prompt-master-series/templates/gallery_episode_block.html]] — 画廊新增一期的 article 区块(小红书入口=活帖直链)
- 首期实例:`E:\目标是成为 Prompt 大师\01_对话\`(已独立出库)
- 在线画廊:https://mr-salticidae.github.io/becoming-a-prompt-master/
- 对应原始档:[[2026-06-12_对话甲骨文二进制获奖图复盘]]

v1.1.0 升级:新增「阶段 C2 · 写小红书正文」——区分「存档笔记(长)」与「发布正文(短、钩子前置、内敛克制)」,补正文模板与硬规则(不写名次 / 不署名 / emoji 克制 / 标题前置 / 留看图钩子)。

v1.2.0 升级:发布物独立到 `E:\目标是成为 Prompt 大师\` 并上线 GitHub Pages 画廊;新增「阶段 E · 发布与上线画廊」与画廊区块模板。约定:画廊「小红书」入口**直链已发布的活帖**(xhslink / 帖子 URL),md 仅作内部存档;帖子链接回填到正文顶部。

定位:面向 AIGC 小白的系列内容生产。克制内敛(不写名次 / 不署名),小白第一(去双链 / 降术语 / 名词小抄)。

## 关联文档

- 全库入口:[[README]]
- Prompt 入口:[[03_prompt模板库索引]]
- 方法论入口:[[04_方法论与洞察索引]]

## 2026-06-08 补充入口

- [[aigc-poster-layout/SKILL.md]]：AIGC 作品宣传海报手工排版工作流；对应复盘 [[2026-06-08_晴枝3x4宣传海报复盘]]。
