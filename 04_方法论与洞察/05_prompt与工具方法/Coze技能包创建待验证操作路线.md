---
tags: [类型/协作工具链, 主题/工具方法, 主题/skill迁移, 工具/Coze]
入档: 2026-06-11
来源: "{Downloads}/Coze技能包创建小白操作手册.md"
验证状态: GPT整理，尚未完成真实 Coze 实操验证
---

# Coze 技能包创建待验证操作路线

> 这是一份从 GPT 整理文档中提炼出来的 Coze 技能包搭建路线。当前价值是“操作假设 + 测试清单”，不是已验证 SOP。真正用于教学或交付前，需要在 Coze 里按步骤跑通并补充截图、入口名称和失败案例。

## 一句话

**Coze 里的“技能包”不是 Claude / Codex 那种文件夹式 Skill，而是用 Agent / Bot、Prompt、Knowledge、Workflow、Plugin 组合出来的可视化智能体。**

可以先这样理解：

```text
Claude / Codex Skill = SKILL.md + scripts + assets + templates
Coze 技能包 = Agent / Bot + Prompt + Knowledge + Workflow + Plugin
```

所以，迁移 Skill 思路到 Coze 时，不要问“怎么上传一个 Skill 文件夹”，而要问：

```text
这个 Skill 的角色说明放哪？
方法论文档放哪？
固定步骤是否需要 Workflow？
哪些外部能力必须交给 Plugin？
```

## 适用场景

这条路线适合把已有 AIGC 方法论做成一个可对话、可发布、可给小白使用的 Coze Agent，例如：

- 短片创作助手；
- Midjourney Prompt 优化助手；
- AI 视频创作流程助手；
- Codex / Claude 交接文档生成器；
- 内部培训用的工作流问答助手。

不适合一开始就做复杂插件、数据库、自动调用图片 / 视频 API 的产品化工具。那些属于后续扩展，不是最小可用验证。

## 最小可用顺序

新手不要一开始就搭 Workflow 和 Plugin。先用最小结构验证这个“技能包”是否真的有用：

```text
1. 创建 Agent / Bot
2. 写核心 Prompt
3. 上传 Knowledge
4. 测试基础输出
5. 再拆 Workflow
6. 最后考虑 Plugin
```

对应三档版本：

| 版本 | 组成 | 用途 |
|---|---|---|
| 最小可用版 | Agent + Prompt + Knowledge | 个人测试、快速验证 |
| 标准技能包版 | Agent + Prompt + Knowledge + Workflow | 稳定复用、给别人用 |
| 产品化版 | Agent + Prompt + Knowledge + Workflow + Plugin + 发布渠道 | 团队工具或外部服务 |

## Prompt 层：先写“技能包说明书”

Agent 的 Prompt / Persona / Instructions 区域，对应 Skill 里的 `SKILL.md` 主说明。它至少要说清楚：

1. 这个 Agent 是谁；
2. 它解决什么任务；
3. 默认输出哪些模块；
4. 信息不足时怎么处理；
5. 哪些情况不要闲聊，要直接进入流程。

短片创作类 Agent 的基础结构可以这样写：

```md
# 角色定位

你是一个短片创作技能包 Agent，负责帮助用户把一个模糊想法转化为可执行的短片创作方案。

# 工作目标

当用户输入一个想法、主题、情绪、故事方向或参考作品时，你需要完成：

1. 创意诊断
2. 核心表达提炼
3. 故事大纲
4. 短片脚本
5. 分镜设计
6. Midjourney 画面提示词
7. Seedance / 即梦视频提示词
8. 交接给 Claude / Codex 的执行文档

# 输出要求

- 使用中文
- 优先给可执行结果
- 不要空泛鼓励
- 不要问太多问题
- 信息不足时，先基于合理假设给出第一版方案
```

如果测试时 Agent 仍然闲聊，就在 Prompt 末尾加硬约束：

```md
无论用户输入多短，都必须优先按照默认流程输出，不要只进行闲聊。
如果用户没有明确要求某一步，也请先给出完整第一版方案。
```

## Knowledge 层：只上传结构化资料

Knowledge 对应 Skill 里的方法论、模板、规范和案例底料。第一次只建议上传 3 到 5 份高质量文档，不要把聊天记录整包丢进去。

适合上传：

```text
01_短片创作方法论.md
02_拉片笔记精选.md
03_MJ视觉风格规范.md
04_视频生成提示词规范.md
05_Codex交接文档模板.md
```

每份文档最好有明确结构：

```md
# 文档用途

# 核心原则

# 输出规范

# 示例
```

关键判断：

> Knowledge 不是资料越多越好，而是越清楚、越可检索、越能支撑输出越好。

## Workflow 层：只在流程需要稳定时再拆

如果只是自己用，Prompt + Knowledge 可能已经够。只有当输出要稳定复用、给别人用、或必须按固定步骤推进时，才需要 Workflow。

短片创作 Workflow 可以拆成：

```text
开始节点：接收用户输入
↓
LLM 节点 1：判断创意类型
↓
LLM 节点 2：提炼核心句
↓
LLM 节点 3：生成故事大纲
↓
LLM 节点 4：生成 15 秒分镜
↓
LLM 节点 5：生成 MJ Prompt
↓
LLM 节点 6：生成视频动态提示词
↓
LLM 节点 7：生成交接文档
↓
结束节点：输出完整结果
```

每个节点只做一件事，输入变量来自前一步。不要把所有任务塞进一个超长节点，否则 Workflow 只是换皮 Prompt。

## Plugin 层：最后再碰

Plugin 只在需要外部能力时才必要，例如：

- 联网搜索；
- 读取飞书 / Notion；
- 调用图片生成 API；
- 调用视频生成 API；
- 保存结果到数据库；
- 接入自己的服务器接口。

新手阶段不要把 Plugin 当作“高级必选项”。插件会引入 API、鉴权、参数、返回值、错误处理和调试成本。更稳的路线是：

```text
纯文本技能包跑通
→ 用 10 个案例测试
→ 让真实用户试用
→ 确认有复用价值
→ 再接插件
```

## 首轮验证清单

这份文档目前未经过真实 Coze 操作验证，实操时至少要检查下面这些点：

- Coze 当前版本里入口到底叫 Agent 还是 Bot；
- Prompt / Persona / Instructions 的真实位置和字段限制；
- Knowledge 上传支持的文件格式、大小和分段方式；
- Agent 是否默认启用 Knowledge 检索，是否需要额外开关；
- Workflow 节点变量写法是否真是 `{{input}}` 这类形式；
- Workflow 能否被 Agent 稳定调用；
- 中文输出是否会被平台默认模型风格稀释；
- 发布渠道是否影响功能可用性；
- 免费 / 付费额度是否限制测试。

推荐第一个测试问题：

```text
我想做一个 15 秒短片，主题是：人长大以后，终于学会照顾小时候的自己。
```

理想输出至少包含：

```text
创意判断
核心句
情绪路径
15 秒分镜
画面风格
MJ Prompt
视频 Prompt
交接文档
```

如果这 8 个模块不能稳定出现，说明基础 Prompt 还没锁住，不要急着搭 Workflow。

## 待验证风险

当前原始文档来自 GPT 整理总结，不是实操复盘。最大的风险有三类：

1. **入口名称漂移**：Coze 版本变化后，Agent / Bot / Workflow / Knowledge 的界面名称可能不同。
2. **变量语法不确定**：Workflow 节点里的变量写法需要以 Coze 当前文档和实测为准。
3. **调用稳定性未知**：Agent 是否能稳定调用 Workflow、Knowledge 是否能稳定参与回答，都需要案例测试。

因此，这篇文档暂时只能作为“搭建路线草稿”。完成真实测试后，应该补一篇 Coze 实操复盘，记录：

- 实际入口路径；
- 截图或字段名；
- 成功案例；
- 失败案例；
- 修改后的可复制 Prompt；
- 是否值得做成正式 SOP。

## 如何使用

当你要把一个已有 Skill 或方法论迁移到 Coze 时，先按这个顺序拆：

1. 把 `SKILL.md` 的身份、目标、输出格式迁移到 Agent Prompt；
2. 把方法论文档、模板、案例迁移到 Knowledge；
3. 把稳定流程拆成 Workflow 节点；
4. 只有外部能力不可缺时才接 Plugin；
5. 用 10 个真实输入验证，再决定是否发布给别人。

## 关联文档

- Skill 基础说明：[[SKILL入门完全指南]]
- Skill 到视频工作流：[[AIGC_Skill到Remotion视频闭环]]
- 国内平台适配案例：[[maieutic-deepseek-adapter/README.md]]
- 工作流规划参考：[[方法论笔记_LLM-plan卡点工作流_v1]]
- 原始底料：`{Downloads}/Coze技能包创建小白操作手册.md`
