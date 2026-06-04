# Maieutic Skill MVP

Maieutic 是一个可测试的 Skill MVP：帮助使用者把问题想清楚，并在必要时补足信息。

当前版本只交付 Skill 文件包，不包含 Web、服务器、数据库、登录、长期记忆或复杂 Agent 编排。

## 目录

```text
maieutic-skill/
├── README.md
├── SKILL.md
├── prompts/
├── examples/
└── tests/
```

## 使用方式

把本目录作为 Skill / prompt 包导入 Claude、GPT 自定义指令或本地 Agent。入口文件是 `SKILL.md`。

建议第一轮测试直接使用 `tests/test_cases.md` 中的 5 个案例，观察：

- 模式判断是否正确
- 明确知识问题是否直接回答
- 纯知识问题是否避免强行输出 Beacon
- 模糊问题是否只问一个关键问题
- 信息收集是否服务问题，而不是堆资料
- 需要 Insight / Beacon 的场景中，它们是否具体

## MVP 边界

本包只验证一件事：Maieutic 是否能同时做到苏格拉底式共学与必要的信息收集。
