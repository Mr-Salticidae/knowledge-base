---
tags: [类型/协作工具链]
---
# Memorax Code:AI 编程记忆层的架构与数据边界

> 首次记录:2026-08-25
> 来源:把 [[https://code.memorax.net]] 这个「AI 编程记忆层」工具本地部署 + 端到端实测一遍的结论
> 状态:**规律已确立**(工具认知 + 数据边界),凡给 coding agent 加重「云记忆 / 云外发数据」类插件前都适用

---

## 一句话判断

**带云记忆的 AI 协作工具,「默认值 ≠ 最优值」:装上就能用的那些默认开关(自动写回、内容级本地 trace、明文存 key),往往不是你想要的;用前先把「什么会上云、本地留了什么、凭据存哪」搞清楚。** 这在 [[浏览器插件自动化的能力边界_v1]] 之后,是给 Agent 接入第三方能力时要过的第二道「边界关」。

---

## 它是什么

Memorax Code([github.com/memorax-ai/memorax-code](https://github.com/memorax-ai/memorax-code),v0.1.8,MIT)是一个给 **AI 编码 Agent 加「跨会话记忆层」**的插件 + 平台:让 Codex、Claude Code、DeepSeek Harness、OpenCode 共享一套**能持续积累的记忆**,新会话不再从零开始。

- 四类记忆:**Coding**(工程经验)/ **Repo**(仓库架构地图 + commit/PR/Issue 证据)/ **Personal**(沟通偏好)/ **Procedure**(可复用流程)。
- 结构:**本地一个 Backend**(模块化单体,默认监听 `127.0.0.1:8787`)+ **每客户端一个适配器**(Hook/Plugin 注入)+ **云端记忆 API**(`platform.memorax.net`)。

## 架构与协作的「分家」要点

- **客户端保留模型与凭据**,记忆只归 Backend 管;客户端通过「版本化、限定客户端」的本地 HTTP 命令与 Backend 通信。
- **Repo Memory 完全本地**(仓库根的 `.repo_memory/`),Coding/Personal/Procedure 的记忆检索、结构化、写回在云端。
- 本地 Backend 默认 **loopback-only**,无鉴权(本地信任模型);**要到外部绑定才需要 token**。

## 用前必须懂的数据边界(核心)

| 面 | 实测结论 | 要不要管 |
|---|---|---|
| **检索在哪** | 语义 + BM25 + 召回,在云端 | 云端命中 → 查询词会外发 |
| **自动写回** | 默认**开**:任务后把「选中的 prompt + 最终回复」发云端提记忆 | ⚠️ 敏感对话建议关或只信工作区 |
| **自动召回** | 默认**关**(只有你主动问才查) | 想让它主动喂记忆要显式开 |
| **本地 trace** | 默认 `capture_content=true`,本地 JSONL 记**完整**对话 | ⚠️ 长时间累积占磁盘、含隐私;可配成仅元数据 |
| **凭据存储** | api_key **明文**存 `~/.memorax-code/config.toml`,且本机(含 Codex 沙箱组)可读 | ⚠️ 别在共享/多人机器随便装 |
| **作用域隔离** | git 仓库→`repository-name.v1`;非 git→`local-directory`;不同 checkout 目录 = 不同命名空间 | ✅ 天然隔离,好 |
| **云端额度** | 免费档有配额(实测 write 100 次/周期) | 用多了会提醒,可能影响 |

> 一句话:它把「记忆」放云端,把「凭据 + trace」放本地明文。**对创作者是方便(跨会话记忆不丢),对敏感项目是风险(写回上云、本地留痕)。**

## 设计上值得借鉴的三处(可迁移到自己的 agent 工具)

1. **Repo Memory「机械收集 + agent 撰写 + validate」**:脚本只收集机械证据(commit/PR/Issue),**不代写理解**;理解由 agent 读代码后手工写成 wiki(纯引擎是 `resources/*.md`),最后 `validate_memory.py` 把关。**机器管数据、人管叙事**,比「全部自动生成」靠谱。
2. **记忆云端自动结构化**:写入后云端把一条记忆**拆成多条事实**,检索按「语义 + 稀疏(BM25)+ RRF 融合」打分,可解释。
3. **生命周期编排**:npm 升级时「退役旧 Backend → 替换 → 验证启动」;启动失败不会替换当前生效的 Hook 代际。**失败不破坏已生效状态**,这个原则通用。

## 实测发现的坑(Windows 中文环境)

排查本身又啃到两个 **UTF-8 vs GBK** 的坑——和 [[Windows下编码与DPI的所见非真相]] 母题同根,已补进那篇:

- **`.ps1` 无 BOM 被 PS5.1 按 GBK 读** → 官方 bootstrap 脚本直接 `Unexpected token` 崩;转带 BOM UTF-8 后通过。
- **Python `subprocess.run(text=True)` 按 locale(GBK)解码子进程输出** → Memorax 的 Repo Memory provider 收集崩溃降级;设 `PYTHONUTF8=1` 后正常。

## 关联文档

- [[Windows下编码与DPI的所见非真相]] —— 本次两个排错发现已补进其陷阱一/四(母题同根)
- [[浏览器插件自动化的能力边界_v1]] —— 「接入第三方能力的边界」母题:插件是操作边界,本篇是数据边界
- [[Claude_Code_Worktree隔离的协作陷阱]] —— 同属「环境/视角错位导致 self-verify 失真」的 Agent 协作陷阱族
- [[本机Skill部署与调用手册]] —— DSH/agent skill 部署;Memorax 也是以「skill + 插件」形态集成进 Agent
- [[模型排名科学性律_五层评估框架与AA拆解_v1]] —— 若要对这类「记忆层工具」横向评测,套那套评估框架
