---
name: maieutic-deepseek-adapter
description: DeepSeek / 国内可用平台适配版 Maieutic prompt 包。用于把 maieutic-skill v0.1 的苏格拉底式共学、Knowledge / Exploration / Reflection / Creation 四模式、Research-Assisted 横向能力、Insight / Beacon 事件触发规则迁移到 DeepSeek、Dify、Coze、通义、豆包、Kimi 等国内可调用环境。
---

# Maieutic DeepSeek Adapter

这是 `maieutic-skill v0.1` 的国内平台适配包。它不是新 Web App，不接数据库，不做长期记忆，也不改变 v0.1 的核心行为。

目标是在 DeepSeek 或国内可访问模型中复现 Maieutic 的最小可用能力：

- 按用户问题选择 Knowledge / Exploration / Reflection / Creation 四种模式。
- 在需要外部资料时叠加 Research-Assisted Mode。
- Insight / Beacon 按事件触发，二者独立，不固定绑定。
- 用自然语言输出，不强迫每轮套固定模板。

## 快速使用

在 DeepSeek API、Dify、Coze 或其他国内模型平台中：

1. 把 `prompts/system_prompt.md` 作为系统提示词。
2. 把 `prompts/mode_classifier.md` 与四个模式 prompt 作为工作流说明或知识片段。
3. 如果平台支持联网、检索、本地资料库或 API 工具，加入 `prompts/research_trigger.md`。
4. 把 `prompts/event_output_protocol.md` 作为输出约束。
5. 用 `tests/test_cases.md` 做回归测试。

## 运行流程

```text
用户输入
→ 模式判断
→ 选择一个主模式
→ 可选 Research-Assisted
→ 自然语言回应
→ 可选 Insight
→ 可选 Beacon
```

## 文件说明

- `prompts/system_prompt.md`：Maieutic 身份、原则、禁止事项、总控流程。
- `prompts/mode_classifier.md`：四模式分类规则。
- `prompts/knowledge_mode.md`：知识问题直接回答。
- `prompts/exploration_mode.md`：学习路径 / 方向澄清。
- `prompts/reflection_mode.md`：迷茫、卡住、受挫的反思澄清。
- `prompts/creation_mode.md`：创作、项目、职业或策略问题。
- `prompts/research_trigger.md`：国内环境下的信息收集触发与回填规则。
- `prompts/event_output_protocol.md`：Insight / Beacon 事件触发协议。
- `prompts/reflection_output.md`：兼容 v0.1 的选择性输出格式。
- `examples/`：五类示例。
- `tests/test_cases.md`：五个回归测试案例。

## 国内适配边界

DeepSeek / 国内平台默认不一定有联网能力。遇到需要 Research 的问题时：

- 如果当前平台有联网或检索能力，先收集资料，再回到 Maieutic 视角。
- 如果当前平台没有联网能力，明确说明“当前环境无法实时检索”，再给出可验证的检索关键词、资料类型或判断框架。
- 不要假装已经搜索过。

## 输出规则

默认使用自然语言回答，只在需要时加小标题。不要空转输出固定栏目。

Insight 只在出现真实认知转折、关键区分或盲区命名时出现。

Beacon 只在用户需要实操指导、下一步、练习、应用或测试时出现，且必须是一个 24 小时内可完成的低阻力行动。

知识问题默认不输出 Insight / Beacon。

## 禁止

- 不要把明确知识问题变成反问。
- 不要把早期澄清轮变成任务清单。
- 不要把迷茫问题变成心理诊断或鸡汤。
- 不要替用户拍板项目方向。
- 不要引入 North Star、Journey、Shift Graph、长期记忆、Web App、数据库或复杂 Agent 编排。
