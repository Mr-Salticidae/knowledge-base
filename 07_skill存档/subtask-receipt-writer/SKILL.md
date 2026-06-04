---
name: subtask-receipt-writer
description: Write concise handoff receipt documents after Codex completes delegated subtasks in the AIGC workspace. Use when work was triggered by a handoff/brief from another session, when the user asks for a receipt/回执/回函/收口简报, or when a completed task should be reported back to GPT主会话, Claude, Cowork, or another downstream session using the local 交接文档书写规范.
---

# Subtask Receipt Writer

## Purpose

After finishing work, decide whether the work is a **subtask that needs a receipt**. If yes, write a compact receipt document under:

`D:\AIGC工作站\跨会话协作\`

Use this Skill to close the loop between Codex, GPT 主会话, Claude/Cowork, and 跳蛛先生.

## When A Receipt Is Required

Write a receipt when any condition is true:

- The task came from a handoff document, brief, or cross-session instruction.
- The output needs to return to GPT 主会话, Claude, Cowork, or another session.
- The user explicitly says “写回执”, “回函”, “收口简报”, “交接给”, or “给主会话”.
- The task completed a separable module inside a larger project.
- New files, Skill docs, workflow protocols, or project state changed in a way another session must know.

Do not write a receipt for:

- trivial one-line checks;
- same-session micro edits with no downstream reader;
- private/personal conversation;
- temporary experiments that the user did not ask to preserve.
- sub-session temporary tasks when 跳蛛先生 explicitly says “不需要写回执”, “不用回执”, “临时任务”, or equivalent.

If receipt-required and receipt-not-required rules conflict, the user's explicit current instruction wins. For example: if a task changes Skill docs but 跳蛛先生 says it is a sub-session temporary task and does not need a receipt, do not write a receipt; mention the skipped receipt in the final response if useful.

## Required Preflight

Before writing the receipt, inspect:

- `D:\AIGC工作站\知识库\03_prompt模板库\03_流程规范\交接文档书写规范.md`
- the source handoff/brief if one exists;
- the files actually changed;
- existing recent receipts in `D:\AIGC工作站\跨会话协作\` to avoid duplicate names.

## Naming

Use:

```text
回执_[项目或子任务]_[致接收方]_YYYY-MM-DD.md
```

Examples:

- `回执_RemotionSkill产品化_致GPT主会话_2026-06-04.md`
- `回执_Skill封装产出_致GPT主会话_2026-06-04.md`
- `收口简报_[项目名]_YYYY-MM-DD.md`

Use underscores. Keep the receiver visible in the filename.

## Receipt Structure

Use this compact structure unless the source handoff requires more:

```markdown
---
tags: [类型/回执, 主题/<主题>, 状态/已完成]
---

# 回执 · <任务名> · 致 <接收方>

> 致 <接收方>：这是 Codex 完成 <来源任务/交接文档> 后的执行回执。
> 创建时间：YYYY-MM-DD
> 项目阶段：<一句话状态>
> 回流原因：<为什么需要回主会话/下游>
> 文档版本：v1，继承自 <源文档或用户指令>。

---

## 一、本次执行结果

<直接说明完成了什么，不写客套。>

---

## 二、产出清单

| 文件 / 模块 | 状态 | 说明 |
|---|---|---|
| `<路径>` | 已完成 | <作用> |

---

## 三、验证状态

- <命令或检查项>：通过 / 未执行 / 失败原因

---

## 四、需要主会话确认的事项

- [ ] <下一步决策>

反对路径：

- 如果跳蛛先生不接受 <建议>，当前产物可如何保留或回退。

---

## 作者 / 接收 / 下游

**作者**：Codex  
**接收方**：<GPT 主会话 / Claude / Cowork>  
**决策人**：跳蛛先生  
**下游**：<下一步承接方或等待确认>
```

## Writing Rules

- Keep it factual and short.
- Use “跳蛛先生”, not “用户”.
- Link or name real files; do not copy long source content.
- Include exact validation commands when relevant.
- State non-executed items explicitly.
- Include a decision or confirmation list only when downstream action is needed.
- Include an “反对路径” when making a recommendation.

## Hard Boundaries

- Do not write praise, filler, or “希望有帮助”.
- Do not claim completion without verification.
- Do not hide failures; state what failed and why.
- Do not write a receipt that changes project decisions.
- Do not overwrite existing receipts; create a new dated file or a versioned filename.
