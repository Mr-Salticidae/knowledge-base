# Maieutic DeepSeek Adapter

> 版本：v0.2 MVP  
> 来源：[[maieutic-skill/SKILL.md]] v0.1 首轮测试通过版本  
> 目标：让 Maieutic 能在 DeepSeek / 国内可调用模型或工作流平台中最小可用。

## 这是什么

`maieutic-deepseek-adapter` 是一组可复制到国内模型平台的 prompt 包。

它保留 Maieutic v0.1 的核心行为：

- Knowledge / Exploration / Reflection / Creation 四种模式。
- Research-Assisted Mode 横向叠加。
- Insight / Beacon 事件触发输出。
- 自然语言对话，不强迫固定模板。

## 适用环境

- DeepSeek API：把 `prompts/system_prompt.md` 放入 system message，其余 prompt 作为开发者说明或本地模板拼接。
- Dify：把模式判断、Research 触发和输出协议拆成工作流节点或知识片段。
- Coze：把系统提示词与模式规则放入 Bot 指令，Research 依赖平台插件或外部知识库。
- 通义 / 豆包 / Kimi：作为 Prompt Pack 手动测试，重点观察模式判断与 Insight / Beacon 是否回退。

## 最小部署方式

1. 复制 `prompts/system_prompt.md` 到系统提示词。
2. 追加 `prompts/mode_classifier.md`。
3. 按平台能力追加四个模式 prompt。
4. 如有联网 / 检索 / 本地资料能力，追加 `prompts/research_trigger.md`。
5. 追加 `prompts/event_output_protocol.md`。
6. 用 `tests/test_cases.md` 做回归测试。

## Research 配置

Research-Assisted Mode 不是必须联网才能使用，但不能伪装联网。

有检索能力时：

- 先给“信息收集结果”。
- 再给“Maieutic 视角”。
- 最后只在真正需要时输出 Insight / Beacon。

无检索能力时：

- 说明无法实时检索。
- 给出建议检索词、资料来源类型和筛选标准。
- 回到用户当前问题，说明这些资料为什么相关。

## 验收标准

通过 `tests/test_cases.md` 五个案例：

- “什么是蒙太奇？”直接解释，不追问，不输出 Insight / Beacon。
- “我想学习剪辑，但不知道从哪里开始。”先澄清目标，不强给任务。
- “我最近什么都想学，但什么都开始不了。”不变成时间管理方案。
- “我想做一个 AI 公益项目，但不知道选什么方向。”先挑战触达问题，不替用户决定。
- “帮我找几个适合做 Claude Skill 的学习类案例。”启用 Research 或明确检索限制，再回到 Maieutic 视角。

## 关联文档

- [[maieutic-skill/SKILL.md]]
- [[maieutic-skill/tests/test_cases.md]]
- [[测试复盘_MaieuticSkill_v0.1_20260605]]
- [[路线图_MaieuticSkill_v0.2_国内适配]]
