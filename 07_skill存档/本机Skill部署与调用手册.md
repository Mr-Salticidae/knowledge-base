---
tags: [类型/skill存档, 类型/工具手册]
---

# 本机 Skill 部署与调用手册

> 扫描日期：2026-07-28
> 扫描机器：Windows 10 Pro（`C:\Users\1`）
> 扫描方法：全盘递归 `SKILL.md`（排除 `node_modules`），逐个解析 YAML frontmatter 的 `name` / `description` / `version` / `disable-model-invocation`
> 结果规模：全盘 1867 个 `SKILL.md` → **已装 186 处条目（去重 100 个不同 skill）+ 14 个 Claude Code 内置**，其余约 1640 个是未加载的市场缓存
> 替代：本文档取代根目录旧版 `skills-inventory.md`（2026-07-17，已过期，当时统计 70 个）

---

## 零、先看这一段：怎么调用 Skill

本机的 skill 分布在 **6 个宿主**（Claude Code / Codex / WorkBuddy / OpenClaw / 项目级 / 源仓库），
但**调用方式只有四种**：

| 调用方式 | 怎么用 | 适用于 |
|---|---|---|
| **① 自动触发（主流）** | 什么都不用做，正常说话即可。你的话命中 skill `description` 里的触发词时，宿主自动把 SKILL.md 塞进上下文 | 绝大多数 skill |
| **② 斜杠命令** | 输入 `/<skill名>`，如 `/grill-me`、`/code-review`、`/simplify` | 内置命令 + 标了 `disable-model-invocation: true` 的 skill |
| **③ 显式点名** | 直接说「用 `lark-sheets` 帮我……」「查一下 SKILL_INDEX，用 `insight-public-post`……」 | 触发词没命中、或你想强制指定某个 skill 时 |
| **④ 直接 Read**（不安装） | 告诉 AI「读 `07_skill存档/SKILL_INDEX.md`，然后用 X」 | 本知识库自研 skill 的兜底调用法，见 [[SKILL_INDEX]] |

**三个必须知道的坑：**

1. **目录名 ≠ skill 名**。触发和点名用的是 frontmatter 里的 `name`，不是文件夹名。本机有 3 处不一致：
   - `~/.claude/skills/remotion-skill/` → 真名 `remotion-explainer-workflow`
   - `~/.codex/skills/remotion/` → 真名 `remotion-card-video`
   - `~/Desktop/seedance-2.0/SKILL.md` → 真名 `seedance-20`（总入口，未安装）
2. **`grill-me` 模型叫不动**。它标了 `disable-model-invocation: true`，只能由你手打 `/grill-me`；它内部再委托给 `grilling`（`grilling` 可自动触发）。
3. **Claude 和 Codex 装的不是同一套**。有 12 个 skill 只在 Codex 里，Claude 会话中说破天也调不出来，详见第三节。

---

## 一、Claude Code 内置 Skill（14 个，无本地文件）

由 Claude Code 客户端自带，**磁盘上没有 SKILL.md**，随版本更新而变。

| Skill 名称 | 一句话用途 | 调用方法 |
|---|---|---|
| `dataviz` | 任何图表 / 仪表盘 / 数据可视化的设计规范（配色、图元、无障碍、明暗主题） | 自动：说到「图表」「chart」「可视化」「dashboard」 |
| `artifact-design` | Artifact 网页的设计规范 | 自动：发布 Artifact 前 |
| `artifact-capabilities` | Artifact 的运行时能力（实时数据、共享状态、自更新） | 自动：要做「会动的」网页时 |
| `claude-api` | Claude API / Anthropic SDK 速查：模型 ID、定价、参数、流式、工具调用、缓存 | 自动：提到 Claude / Anthropic / 模型选型 |
| `update-config` | 改 `settings.json`：hooks 自动化、权限、环境变量 | 自动：说「以后每次 X 就 Y」「允许 npm 命令」 |
| `keybindings-help` | 自定义快捷键 `~/.claude/keybindings.json` | 自动 / `/keybindings-help` |
| `fewer-permission-prompts` | 扫历史会话，生成只读命令白名单塞进项目 settings，减少授权弹窗 | `/fewer-permission-prompts` |
| `simplify` | 只做质量清理（复用 / 简化 / 效率），不找 bug | `/simplify` |
| `security-review` | 当前分支待提交改动的安全审查 | `/security-review` |
| `review` | 审查 GitHub PR（本地 diff 请用 `/code-review`） | `/review` |
| `run` | 启动本项目应用、截图，确认改动在真实环境生效 | 自动 / `/run` |
| `init` | 生成项目 `CLAUDE.md` | `/init` |
| `loop` | 按间隔重复跑一个提示或命令，如 `/loop 5m /foo`；不给间隔则模型自己定节奏 | `/loop <间隔> <命令>` |
| `schedule` | 创建 / 管理 cron 定时云端 agent（routines），也支持一次性定时 | 自动 / `/schedule` |

> 另有 `/code-review`（本地 diff 审查，支持 `/code-review ultra` 多 agent 云端审查）属于内置命令。
> **注意**：旧版清单里的 `deep-research`、`verify`、`code-review` 三条已不在当前会话的 skill 列表中，属客户端版本变动。

---

## 二、Claude Code 用户级 Skill（86 个）

**根目录**：`C:\Users\1\.claude\skills\`
**本体文件**：`C:\Users\1\.claude\skills\<目录名>\SKILL.md`
**这是本次会话真正能调用的那一套**，下面 86 个按来源分 5 组。

### 2.1 飞书 lark-* 系列（27 个，OpenClaw 官方源）

全部依赖 `lark-cli` 二进制；认证 / 身份 / 权限统一走 `lark-shared`。
**本体**：`~/.claude/skills/lark-<xx>/SKILL.md`

| Skill | 版本 | 用途 | 触发方式 |
|---|---|---|---|
| `lark-shared` | 1.0.0 | **底座**：`auth login/status/logout`、user vs bot 身份、业务域权限 `--domain`、缺 scope 处理 | 被其他 lark-* 依赖，一般不直接叫 |
| `lark-doc` | 2.0.0 | 云文档 Docx / Wiki 读写、插入下载图片附件；也管思维笔记 | 给出文档 URL 或 token |
| `lark-sheets` | 3.0.0 | 电子表格：建表、行列、单元格值/公式/样式、查找替换、图表、透视表、条件格式、财务建模 | 「电子表格」「Sheets」「公式」 |
| `lark-base` | 1.2.2 | 多维表格：建表、字段、记录、视图、公式 lookup、表单、仪表盘、workflow、角色权限 | 「多维表格」「Base」「bitable」 |
| `lark-im` | 1.0.0 | 收发消息、搜聊天记录、群成员、上传下载文件、表情回复、加急、交互卡片及回调 | 「发消息」「群里」「聊天记录」 |
| `lark-drive` | 1.0.0 | 云空间：上传下载、建文件夹、复制移动删除、权限订阅、版本、导入 Word/Excel/CSV/PPTX | 「云盘」「云空间」「导入文件」 |
| `lark-wiki` | 1.0.2 | 知识空间、空间成员、节点层级、快捷方式 | 「知识库」「Wiki」「知识空间」 |
| `lark-calendar` | 1.0.0 | 日历日程、参会人、忙闲、推荐时段、会议室预定 | 「日程」「安排会议」「订会议室」 |
| `lark-task` | 1.0.0 | 任务清单、子任务、协作成员、附件、任务智能体注册 | 「待办」「任务」「清单」 |
| `lark-mail` | 1.0.0 | 起草/发送/回复/转发/搜索邮件、文件夹标签、收信规则、监听新邮件 | 「写邮件」「查邮件」 |
| `lark-approval` | 1.2.0 | 审批待办/已办/实例，搜索审批定义并发起原生审批 | 「审批」（**注**：审批待办 ≠ 飞书任务） |
| `lark-contact` | 1.0.0 | 通讯录：姓名/邮箱 → open_id，或 open_id 反查部门联系方式 | 提到某人姓名要发消息/排日程 |
| `lark-slides` | 1.0.0 | 幻灯片创建、读取、页面增删改 | 「幻灯片」「PPT」 |
| `lark-whiteboard` | 1.0.0 | 画板导出预览图 / 原始节点结构、编辑画板 | 「画板」「白板」 |
| `lark-minutes` | 1.0.0 | 妙记：搜索、下载上传音视频、读改产物、换说话人；**本地音视频转写优先走它，别用 ffmpeg/whisper** | 「妙记」「转逐字稿」 |
| `lark-note` | 1.0.0 | 已知 `note_id` 时直查会议纪要详情与原始逐字记录 | 手里有 note_id 时 |
| `lark-vc` | 1.0.0 | 搜历史会议、查纪要（总结/待办/章节/逐字稿）、参会人快照 | 「上次那个会」「会议纪要」 |
| `lark-vc-agent` | 1.0.0 | 机器人真实加入/离开进行中的会议，读会中事件、发会中消息表情 | 「现在这个会在说什么」 |
| `lark-okr` | 1.0.0 | OKR 周期、目标、KR、对齐关系、量化指标、进展记录 | 「OKR」「目标管理」 |
| `lark-attendance` | 1.0.0 | 查自己的考勤打卡记录 | 「考勤」「打卡」 |
| `lark-markdown` | 1.2.2 | 飞书侧 Markdown 文件的查看/创建/上传/局部 patch/diff 比较 | 「Markdown 文件」 |
| `lark-event` | 1.0.0 | 实时事件流：`lark-cli event consume <EventKey>` 输出 NDJSON，支持 `--max-events`/`--timeout` | 做机器人、长驻订阅 |
| `lark-apps` | 1.0.0 | 妙搭（Spark/Miaoda）应用开发托管：建应用、HTML 站点发布、云端迭代、日志/Trace/PV/UV、环境变量 | 「妙搭」「做个应用」「拿分享链接」 |
| `lark-openapi-explorer` | 1.0.0 | 现有 skill 覆盖不到时，从官方文档挖原生 OpenAPI 裸调 | 需求超出封装范围时 |
| `lark-skill-maker` | 1.0.0 | 把飞书 API 操作封装成新的可复用 skill | 「做一个飞书 skill」 |
| `lark-workflow-meeting-summary` | 1.0.0 | **工作流**：汇总指定时间范围的会议纪要 → 结构化报告 | 「整理这周会议纪要」「会议周报」 |
| `lark-workflow-standup-report` | 1.0.0 | **工作流**：编排 `calendar +agenda` + `task +get-my-tasks` → 日程待办摘要 | 「今天什么安排」「早报」 |

### 2.2 飞书 feishu-* 系列（10 个，OpenClaw Lark 扩展）

和 lark-* 是**两套并行实现**（feishu-* 走扩展内工具，lark-* 走 lark-cli）。功能重叠，优先用 lark-*。
**本体**：`~/.claude/skills/feishu-<xx>/SKILL.md`

| Skill | 用途 | 触发方式 |
|---|---|---|
| `feishu-channel-rules` | Lark 频道输出规则，**始终激活** | 在飞书对话中自动加载 |
| `feishu-bitable` | 多维表格：27 种字段类型、高级筛选、批量操作、视图管理 | 「多维表格」「bitable」 |
| `feishu-calendar` | 日历日程、参会人、忙闲查询 | 「日历」「日程」 |
| `feishu-create-doc` | 用 Lark-flavored Markdown 新建云文档，可指定文件夹/知识库 | 「创建飞书文档」 |
| `feishu-fetch-doc` | 拉云文档内容为 Markdown，处理图片/文件/画板 | 「读飞书文档」 |
| `feishu-update-doc` | 更新云文档，7 种模式：追加/覆盖/定位替换/全文替换/前后插入/删除 | 「更新飞书文档」 |
| `feishu-im-read` | IM 读取：会话消息、话题回复、跨会话搜索、图片文件下载 | 「群里说了什么」「搜消息」 |
| `feishu-task` | 任务与清单的创建查询更新、负责人截止时间、附件、Agent 注册 | 「飞书任务」 |
| `feishu-troubleshoot` | 飞书插件排障 FAQ + 深度诊断 `/feishu_doctor` | 多次授权仍失败时 |
| `feishu-doc-publish` | **自研**：本地 md → 飞书云文档 + 可分享链接（零依赖 Node CLI `sync.mjs`） | 「发布到飞书」「同步到飞书」 |

### 2.3 Seedance 2.0 视频提示词系列（28 个）

字节 Seedance 2.0 视频生成的完整提示词工程套件，**来自 `~/Desktop/seedance-2.0/` 源仓库**。
**本体**：`~/.claude/skills/seedance-<xx>/SKILL.md`
调用无需点名——描述你要拍什么、或贴出失败的 prompt，对应 skill 自动进场。

| 分组 | Skill | 用途 |
|---|---|---|
| **入口 / 创作** | `seedance-interview` | 导演式访谈，把想法问成可制作的 prompt（从「毫无头绪」到「专业分镜」都适配） |
| | `seedance-interview-short` | 快速版访谈，压缩式需求收集 |
| | `seedance-prompt` | **主力**：写 / 改进 / 翻译 / 压缩 / 调试 Seedance prompt（T2V、I2V、V2V、R2V） |
| | `seedance-prompt-short` | 30–100 词紧凑版 prompt |
| | `seedance-recipes` | 类型模板：产品广告、生活方式、剧情、MV、风景、商业片、动画 |
| | `seedance-sequence` | 长故事 / 多镜头 / 分镜密集 → 拆成有状态的连续片段 |
| | `seedance-continuation` | 续拍、接尾、修补尾帧、重锚漂移 |
| **镜头语言** | `seedance-camera` | 运镜、景别、镜头感、构图、一镜到底、推拉摇移、手持、航拍、微距 |
| | `seedance-lighting` | 布光、氛围、时间、色温、阴影、反射、天气光、实用光源 |
| | `seedance-motion` | 肢体动作、编舞、物理、物体运动、动作连贯、特技 |
| | `seedance-style` | 视觉风格、美术方向、渲染质感、年代美学、写实程度 |
| | `seedance-vfx` | 特效：粒子、能量、破坏、变形、天气、魔法、爆炸、烟火水 |
| | `seedance-characters` | 角色一致性、身份锁定、多角色走位、服装连续性、手部安全 |
| | `seedance-audio` | 对白、口型同步、音乐、音效、环境声、卡点、音画同步排障 |
| **质量 / 合规** | `seedance-antislop` | 清除 AI 套话、空洞形容词、含糊影视黑话，换成精确制作术语 |
| | `seedance-filter` | prompt 被拦截 / 静默降级时的安全改写 |
| | `seedance-copyright` | 涉及知名角色、IP、名人、真人、品牌 logo、版权曲时的合规改写 |
| | `seedance-troubleshoot` | 出片模糊、抖动、跑题、变形、不稳、失同步的根因诊断 |
| **词表** | `seedance-vocab-zh` | 中文运镜/布光/动作/VFX/音频术语表与压缩 |
| | `seedance-vocab-en` | 英文精确制作词汇，去 slop |
| | `seedance-vocab-ja` / `-ko` / `-ru` / `-es` | 日 / 韩 / 俄 / 西 语术语表 |
| **示例** | `seedance-examples-zh` / `-ja` / `-ko` | 中 / 日 / 韩 可用 prompt 样例与改写 |
| **工程** | `seedance-pipeline` | 工作流与 API：BytePlus ModelArk、即梦 Dreamina、国内通道、ComfyUI、后期、批量、拼接 |

### 2.4 AIGC 创作工作流（11 个，自研为主）

**本体**：`~/.claude/skills/<目录名>/SKILL.md`

| Skill | 目录名 | 用途 | 触发词 |
|---|---|---|---|
| `aigc-prompt-optimizer` v1.5 | 同名 | 口语需求 → 专业 prompt；prompt battle 发散、MJ 出图反馈、二选一、视觉诊断、构图意图层 | 「优化 prompt」「改成 MJ prompt」「prompt battle」「这张图哪里不好」「二选一」 |
| `prompt-master-skill` | 同名 | 通用 prompt 生成：视频 / 图片 / 文本，覆盖报告文案 PPT 邮件脚本 | 「写个 prompt」 |
| `character-consistency-mj` | 同名 | MJ 角色一致性「四层金字塔」，sref / oref 锁脸 | 「保持角色一致」「sref 怎么用」「oref 锁脸」 |
| `storydiffusion` | 同名 | StoryDiffusion（NeurIPS 2024）跨帧角色一致漫画 / 视频生成 | 「分镜角色统一」「漫画分镜生成」「图生视频」 |
| `ai-short-film-breakdown` | 同名 | AI 短片类型判断与创作策略，拉片、规避 AI 技术短板 | 「帮我拉片」「分析这部 AI 视频的结构」 |
| `ai-short-film-screenwriting` | 同名 | 灵感 / 主题 / 素材 → 可制作短片方案；诊断故事单薄、情绪闭环 | 「这个故事能不能拍」「诊断这个剧本」 |
| `blind-editing-workflow` | 同名 | 蒙眼剪辑法：Python + ffmpeg 精确剪辑，图片/视频素材合成 MV、角色 PV | 「把这些图做成视频」「按卡点剪辑」 |
| `song-caption-mv-workflow` | 同名 | 歌曲 MV + 字幕自动化：无字版导出、Demucs 人声分离、WhisperX 词级对齐、中英双语 SRT | 「给这首歌做 MV」「生成 SRT」「哼唱太多识别不准」 |
| `suno-music-brief` | 同名 | Suno 两阶段配乐：Simple Mode 探索 brief + Custom Mode 固化 brief | 「用 Suno 做一首歌」「给这个项目配乐」 |
| `remotion-explainer-workflow` | **`remotion-skill`** ⚠️ | Remotion 扁平矢量科普解释视频：sceneSpecs / sceneAssets / 跨 skill 干跑协议 | 「Remotion」「做科普视频」 |
| `content-publish-sop` | 同名 | 发布前入场票审计 + 平台适配（快手 / 网易云 / B站） | 「这个作品发哪里」「快手标题怎么写」 |

### 2.5 通用 / 元工具（10 个）

**本体**：`~/.claude/skills/<目录名>/SKILL.md`

| Skill | 用途 | 调用方法 |
|---|---|---|
| `excalidraw-diagram` | 生成 Excalidraw 流程图 / 架构图，输出 `.excalidraw` + PNG，自带 Playwright 渲染做视觉 QA | 自动：「画个流程图」「架构图」 |
| `maieutic-skill` | 苏格拉底式共学：问题澄清、学习路径、迷茫反思、研究辅助；输出 Insight / Beacon | 自动：「助产术」「苏格拉底式共学」「我很迷茫」 |
| `grilling` | 无情拷问一个计划 / 决策 / 想法，压力测试思维 | 自动：「grill」「拷问我」 |
| `grill-me` | `grilling` 的手动入口（`disable-model-invocation: true`） | **只能 `/grill-me`** |
| `imagegen` | 生成 / 编辑位图：照片、插画、纹理、精灵、样机、透明底抠图 | 自动：「生成一张图」 |
| `openai-docs` | OpenAI 产品 / API / Codex 官方文档带引用查询、模型选型与升级建议 | 自动：提到 OpenAI / Codex |
| `skill-creator` | 创建或升级 skill 的规范指南 | 自动：「做一个 skill」 |
| `skill-installer` | 从精选列表或 GitHub repo 安装 skill 到 `$CODEX_HOME/skills` | 自动：「装个 skill」 |
| `install-skill-from-source` | 从 GitHub / URL / 文件夹手工安装 skill（含安全审计、依赖检查），SkillManage 不可用时的兜底 | 自动：「从这个仓库装 skill」 |
| `plugin-creator` | 脚手架 Codex 插件目录：`.codex-plugin/plugin.json`、清单默认值、个人市场条目 | 自动：「做个 Codex 插件」 |

---

## 三、Codex 用户级 Skill（28 个）

**根目录**：`C:\Users\1\.codex\skills\`
**只在 Codex 里能用**（Claude Code 不读这个目录）。其中 16 个与 `.claude/skills` 重名重复，**下面只列 Codex 独有的 12 个**。

### 3.1 Codex 独有自研 skill（12 个）

**本体**：`C:\Users\1\.codex\skills\<目录名>\SKILL.md`

| Skill | 版本 | 用途 | 触发词 |
|---|---|---|---|
| `prompt-master` | 1.6.0 | 全工具 prompt 路由（LLM / Cursor / MJ / 图片 / 视频 / 代码 Agent）。**仅在明确要求写改 prompt 时激活** | 「帮我写 prompt」 |
| `prompt-master-series` | 1.4.0 | 《目标是成为 Prompt 大师》系列内容生产：破题拆解 + 小红书双卡 + 正文 + 小白笔记 + 系列归档 | 「做成一期 Prompt 大师」「出四层拆解卡」 |
| `knowledge-base-curator` | 1.0 | **本知识库专属**四阶段策展：答疑 → 小白笔记 → 内核存档（双链+索引+MOC）→ 学员版分发 | 「沉淀进知识库」「按知识库规范归档」 |
| `insight-public-post` | 1.1 | 知识库内核档 → B站 AI 开发者小站公开版对外帖，发布后回收终稿保持库内外一致 | 「发小站」「写公开版」「分发出去」 |
| `work-weekly-report` | 1.0 | 跨工作区所有仓库一周 git 活动 → 公司标准三段式周报，写入并推送 work-reports 仓库 | 「写周报」「提交给公司的周报」 |
| `aigc-poster-layout` | 0.4.0 | 作品宣传海报排版（B站/小红书/快手/朋友圈）；封面精修首选选帧 + GPT Image 2 叠排不重绘主体 | 「做张宣传海报」 |
| `aigc-video-cover-gpt` | 1.3 | 人物参考图 + 脚本 → GPT Image 2 一步出 16:9 商单封面（含锁脸 + 中文大字策略） | 「给这个视频做封面」 |
| `aigc-postmortem` | — | 创作复盘工作流，事实先行防自我归因偏差 | 「帮我复盘这次比赛」「整理项目经验」 |
| `subtask-receipt-writer` | — | 子任务完成后写交接回执 / 回函 / 收口简报，回报给 GPT 主会话 / Claude / Cowork | 「写个回执」「回函」 |
| `maieutic-deepseek-adapter` | — | Maieutic 的国内平台适配 prompt 包（DeepSeek / Dify / Coze / 通义 / 豆包 / Kimi） | 要迁到国内模型时 |
| `remotion-card-video` | — | 目录 **`remotion`** ⚠️ · Remotion + React 生成「极简知识卡片流」视频，内置设计系统与场景模板 | 「把这篇文章做成卡片视频」「出 TSX 代码」 |
| `review-agent` | — | 位于 `.system/` · 只读、缺陷优先的代码审查，供其他 agent 委派 | 由 agent 委派，不直接叫 |

### 3.2 Codex 系统 skill（6 个）

**本体**：`C:\Users\1\.codex\skills\.system\<名>\SKILL.md`
含 `imagegen`、`openai-docs`、`plugin-creator`、`skill-creator`、`skill-installer`、`review-agent`。
前 5 个与 `~/.claude/skills/` 同名副本一致，第 6 个 `review-agent` 是 Codex 独有（见上表）。

### 3.3 与 Claude 重复的 16 个

`ai-short-film-breakdown`、`ai-short-film-screenwriting`、`aigc-prompt-optimizer`、`blind-editing-workflow`、
`character-consistency-mj`、`content-publish-sop`、`feishu-doc-publish`、`maieutic-skill`、
`remotion-explainer-workflow`、`song-caption-mv-workflow`、`suno-music-brief` +
系统 5 件套 `imagegen` / `openai-docs` / `plugin-creator` / `skill-creator` / `skill-installer`。

> **版本可能不一致**：两边是独立副本，改一边不会同步另一边。改动后请两边都更新，或以 `07_skill存档/` 为唯一真身。

---

## 四、WorkBuddy Skill（6 个）

**根目录**：`C:\Users\1\.workbuddy\skills\`
**本体**：`C:\Users\1\.workbuddy\skills\<名>\SKILL.md`
6 个全部已复制到 `~/.claude/skills/`，Claude 会话中直接可用：
`excalidraw-diagram`、`feishu-doc-publish`、`grill-me`、`grilling`、`install-skill-from-source`、`maieutic-skill`。

---

## 五、OpenClaw Skill（38 个，飞书宿主）

OpenClaw 是飞书侧的 agent 宿主，skill 分三处：

| 位置 | 数量 | 内容 | 本体路径 |
|---|---|---|---|
| `~/.openclaw/workspace/.agents/skills/` | 27 | lark-* 全家桶（与第 2.1 节同源） | `<该目录>/<名>/SKILL.md` |
| `~/.openclaw/extensions/openclaw-lark/skills/` | 9 | feishu-* 系列（与第 2.2 节同源，不含 feishu-doc-publish） | `<该目录>/<名>/SKILL.md` |
| `~/.openclaw/plugin-skills/` | 11 | **全部是 Junction 链接**，不是实体 | 见下 |

`~/.openclaw/plugin-skills/` 的链接指向：

- `browser-automation` → `%APPDATA%\npm\node_modules\openclaw\dist\extensions\browser\skills\browser-automation`（**浏览器自动化，本机唯一一份**）
- `canvas` → `%APPDATA%\npm\node_modules\openclaw\dist\extensions\canvas\skills\canvas`（**画布，本机唯一一份**）
- 其余 9 个 `feishu-*` → 指回 `~/.openclaw/extensions/openclaw-lark/skills/`

> `browser-automation` 和 `canvas` **只在 OpenClaw（飞书对话）里可用**，Claude Code 和 Codex 都没装。

---

## 六、项目级 Skill（knowledge-base 仓库内）

**本体真身**：`<仓库>/.agents/skills/<名>/SKILL.md`（28 个：27 个 lark-* + `grill-me`）

同一套在仓库里有 **3 个入口**，后两个是 Junction 链接，不占额外空间：

| 路径 | 形态 | 说明 |
|---|---|---|
| `.agents/skills/` | **实体目录** | 唯一真身 |
| `.codebuddy/skills/` | Junction → `.agents/skills/` | CodeBuddy 宿主入口 |
| `skills/` | Junction → `.agents/skills/` | 通用入口 |

`skills-lock.json` 记录每个 skill 的来源与哈希：`lark-*` 来自 `open.feishu.cn`（well-known），`grill-me` 来自 GitHub `mattpocock/skills`。

> ⚠️ **项目级版本比用户级新**：`lark-sheets` 项目级 v3.0.2 vs 用户级 v3.0.0；`lark-wiki` 项目级 v1.0.3 vs 用户级 v1.0.2。在本仓库工作时以项目级为准。

---

## 七、源仓库 / 未安装（作为素材存在）

这些位置有 SKILL.md，但**不是任何宿主的加载目录**，只是源码 / 存档 / 学员分发包：

| 位置 | 数量 | 说明 |
|---|---|---|
| `~/Desktop/seedance-2.0/` | 29 | Seedance 套件源仓库（含总入口 `seedance-20`）。已安装的 28 个是它的副本 |
| `~/Desktop/ai-editing-course/.claude/skills/` | 4 | AI 剪辑课程项目级（课程目录下打开时才生效） |
| `~/Desktop/ai-editing-course/00_学员包_工作流入门/skills/` | 9 | 学员分发包，给学员自己装 |
| `<本仓库>/07_skill存档/` | 23 目录 | **自研 skill 的唯一真身与版本存档**，见 [[07_skill存档索引]]、[[SKILL_INDEX]] |
| `<本仓库>/08_对外分发/AI视频工作流_学员包/` | 9 | 对外学员包副本 |

> `07_skill存档/` 里有 3 个 skill **没装到任何宿主**，只能靠「④ 直接 Read」调用：
> `dingtalk-doc-delivery`（钉钉知识库交付）、`aigc-poster-layout` 的存档版、`insight-public-post_v1.0`（旧版留档）。

---

## 八、未安装的市场缓存（1600+ 个，**不可调用**）

全盘共扫到 **1867 个 SKILL.md**，其中约 1640 个属于市场 / 插件缓存，**没有被任何宿主加载**，仅占磁盘：

| 缓存位置 | 量级 | 内容 |
|---|---|---|
| `~/.workbuddy/plugins/marketplaces/codebuddy-plugins-official/` | ~340 | CodeBuddy 官方插件市场（+ 一份同等大小的 `.tmp` 残留副本，可删） |
| `~/.workbuddy/plugins/marketplaces/cb_teams_marketplace/` | ~90 | 团队市场：金融、投行、私募、股票研究、产品管理等 |
| `~/.workbuddy/connectors-marketplace/connectors/` | ~45 | 连接器：feishu、wecom、cloudbase 等 |
| `~/.codex/.tmp/plugins/plugins/` | ~250 | Codex 插件缓存：vercel、superpowers、supabase、stripe、slack、teams、sentry、render、netlify、expo、cloudflare、hugging-face 等 |
| `~/.codex/plugins/cache/openai-curated-remote/` | ~80 | OpenAI 官方精选远程插件：investment-banking、data-analytics、openai-templates 等 |
| `~/.cache/codex-runtimes/` | ~8 | Codex 运行时自带：documents、pdf、presentations、spreadsheets、template-creator |

**想用其中某个**：走 `skill-installer` 或 `install-skill-from-source` 正式安装到 `~/.claude/skills` 或 `$CODEX_HOME/skills`。

---

## 九、维护待办（扫描中发现的问题）

1. **`~/.codex/skills/` 混入了 12 个空目录**：`.github`、`.obsidian`、`00_仓库维护`、`01_sref档案`、`02_参数行为档案`、`03_prompt模板库`、`04_方法论与洞察`、`05_视觉系统`、`06_代码`、`07_skill存档`、`08_对外分发`、`09_平台工程` —— 是知识库目录骨架被误同步过去的残留，全空，可直接删。
2. **`~/.workbuddy/plugins/marketplaces/codebuddy-plugins-official.1784097135841-hzssgt.tmp/`** 是一份完整的市场副本残留（138+34+28 个 SKILL.md），安装中断留下的，可删。
3. **根目录 `skills-inventory.md` 已过期**（2026-07-17，70 个，路径还写着 `~/.openclaw/workspace/`），已被本文档取代，可删。
4. **Claude / Codex 双装的 16 个 skill 会版本漂移**，建议约定以 `07_skill存档/` 为唯一真身，改完再同步两边。
5. **项目级 lark-sheets / lark-wiki 比用户级新**，可考虑把用户级也升上去。

---

## 关联文档

- 自研 skill 存档与版本记录：[[07_skill存档索引]]
- 自研 skill 触发词与免安装调用法：[[SKILL_INDEX]]
- 全库入口：[[README]]
- 知识库协作规范：`CLAUDE.md`
