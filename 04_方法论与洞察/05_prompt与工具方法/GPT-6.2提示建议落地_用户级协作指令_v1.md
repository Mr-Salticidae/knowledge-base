---
tags: [类型/协作工具链]
---
# 把 GPT-6.2 的提示建议落到用户级协作指令

> 入档:2026-11-23

## 一句话

全局指令优先约定反复发生的协作决策：什么时候自主推进，什么结果算交付，最终答复需要交代哪些信息。

## 来源与采用依据

- OpenAI 观察到 Astra 默认更简短，目标或细节模糊时 GPT-6.2 有时会停在建议阶段。官方给出了写作、任务完成、编码和前端设计的提示示例。[OpenAI GPT-6.2 提示指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra#prompting-best-practices)
- The Decoder 将建议整理为三类常见问题：回答过短、过早追问、代码改动容易引入多余结构。报道还介绍了 Responses API 的会话与参数变化。[The Decoder 原文](https://the-decoder.com/openai-shares-new-prompting-tips-for-gpt-6-2-astra-and-sol-to-fix-brief-answers-and-unnecessary-questions/)

## 如何使用

1. **把常规判断交给助手**。对可逆小事采用合理假设，完成授权范围内的步骤。涉及授权、不可逆后果或用户负责的决策时，停在对应的动作前。共学和分阶段审稿以约定的分工为准。
2. **把验收写进完成条件**。执行型任务照用户的交付目标核对实际产物。代码沿正常入口检查，尽量复用已有逻辑和测试，只有明确要求、仓库规定或具体回归风险才增测。可复用的工作约定见 [[AGENTS#协作与交付]]。
3. **让交付能独立阅读**。先交代结果，按复杂度保留理解和核查所需的细节。对外代写补充读者缺少的背景，编辑保留作者原意。最终答复带上关键假设和验证边界，便于直接转用或复核。
4. **按作用范围落位**。跨项目约定写进 `~/.codex/AGENTS.md`，本库同步四个本地入口的公共条款。视觉与字体要求放在具体项目，Responses API 的参数与会话配置在接入侧管理。[Codex 用户级指令加载规则](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance)

本次记录基于公开指南和本机配置变更。对回答详略、追问频率和任务完成率的影响，仍待用独立任务做前后对照。

## 关联文档

- [[AGENTS]] 保存知识库的工作约定及公共指令的版本存档。
- [[04_方法论与洞察索引#05_prompt与工具方法]] 收录相关方法笔记。
