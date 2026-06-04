---
tags: [类型/skill存档, 状态/路线图]
---

# Maieutic Skill v0.2 路线图：国内可用适配

> 创建时间：2026-06-05  
> 上游版本：[[测试复盘_MaieuticSkill_v0.1_20260605]]  
> 当前定位：方向说明，不进入编码。  
> 优先路线：DeepSeek Adapter。

---

## 一、背景

`maieutic-skill v0.1` 已完成首轮测试，但 Claude / GPT Skill 形态对国内普通用户存在可访问性限制。

如果 Maieutic 要真正触达国内用户，下一步应优先解决“可用入口”，而不是直接开发更垂直的公益子 Skill。

---

## 二、目标

将 Maieutic 的核心方法论迁移到国内可用模型或平台：

- 问题类型判断。
- Knowledge / Exploration / Reflection / Creation 四种模式。
- Research-Assisted 横向能力。
- Insight / Beacon 事件触发输出协议。
- 五个 MVP 测试案例。

v0.2 的目标不是复刻 Claude Skill 文件夹格式，而是做一个能在国内模型 / 工作流平台上运行的最小适配版本。

---

## 三、候选方向

| 方向 | 优点 | 风险 | 初步判断 |
|---|---|---|---|
| DeepSeek API Adapter | 模型可用性高，适合直接迁移 system prompt 与模式判断 | 需要自行处理封装、调用与可能的 Research 能力 | 优先 |
| Dify 工作流 | 适合低代码搭建和可视化工作流 | 可能过早平台化，调试成本不一定低 | 候选 |
| Coze Bot | 国内用户触达较直接，适合 Bot 化测试 | 平台约束会影响 Maieutic 的对话节奏 | 候选 |
| 通义 / 豆包 / Kimi Prompt Pack | 迁移成本低，可快速测试不同模型行为 | 缺少统一 Skill 结构，版本管理容易散 | 辅助测试 |

---

## 四、DeepSeek Adapter 最小版本

第一版只做最小可运行适配：

- `system_prompt`：迁移 Maieutic 身份、灯塔原则、禁止事项。
- `mode_classifier`：保留四模式判断。
- `research_trigger`：定义何时需要外部资料。
- `event_output_protocol`：保留 Insight / Beacon 独立事件触发规则。
- `test_cases`：沿用 v0.1 五个测试用例。

最小输入输出：

```text
输入：用户问题
处理：模式判断 → 可选 Research → Maieutic 视角回应 → 可选 Insight / Beacon
输出：自然语言回答
```

---

## 五、暂不做

- 不做 Web App。
- 不做长期记忆。
- 不做多平台同时适配。
- 不做复杂 Agent 编排。
- 不做乡村老师低资源教案共创子 Skill。
- 不把 Maieutic 改造成课程生成器或资料检索机器人。

---

## 六、测试用例沿用策略

v0.2 仍使用 v0.1 的五个测试用例作为回归测试：

1. 什么是蒙太奇？
2. 我想学习剪辑，但不知道从哪里开始。
3. 我最近什么都想学，但什么都开始不了。
4. 我想做一个 AI 公益项目，但不知道选什么方向。
5. 帮我找几个适合做 Claude Skill 的学习类案例。

通过标准：

- 知识问题不强行 Insight / Beacon。
- 早期澄清轮不强行给任务。
- 反思问题不变成鸡汤或心理诊断。
- 创作 / 公益问题不替使用者拍板。
- Research 后必须回到“这和当前问题有什么关系”。

---

## 七、下一步任务包

等跳蛛先生确认 v0.2 方向后，再新建 `maieutic-deepseek-adapter` 最小任务包。

任务包应包含：

- 适配目标和运行环境。
- Prompt 迁移清单。
- DeepSeek 调用边界。
- Research 能力是否外接。
- 五个回归测试输入与预期。

## 关联文档

- [[测试复盘_MaieuticSkill_v0.1_20260605]]
- [[maieutic-skill/SKILL.md]]
- [[maieutic-skill/tests/test_cases.md]]
