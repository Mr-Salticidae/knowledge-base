# Research-Assisted Example

## 输入

```text
帮我找几个适合做 Claude Skill 的学习类案例。
```

## 预期模式

Research-Assisted Layer + Creation / Exploration Mode

## 有检索能力时的示例结构

```markdown
## 信息收集结果

### 关键发现
- 学习类 Skill 更适合做“流程型帮助”，而不是只做知识问答。
- 好案例通常有明确输入、可复用步骤和可检查输出。

### 可能有用的案例方向
- 论文阅读辅助：输入论文或摘要，输出问题地图和阅读路径。
- 语言学习陪练：输入目标场景，输出对话练习和纠错规则。
- 项目制学习教练：输入学习目标，拆成小任务和复盘问题。

### 与你当前问题的关系
- 这些案例都不是“课程库”，而是把学习过程变成可重复的对话工作流。

## Maieutic 视角
如果你要做 Claude Skill，优先选“使用者每次都会卡在同一种流程里”的学习场景，而不是选一个知识面很宽的领域。
```

## 无检索能力时的示例结构

```markdown
当前环境无法实时检索真实案例。我可以先给你一组可验证的案例方向和检索关键词，等你在可联网环境里确认后再收束。

建议检索词：Claude Skill examples, AI learning assistant workflow, Socratic tutor prompt, study planner agent。

从 Maieutic 视角看，适合做 Skill 的学习案例不应只是“回答知识”，而应能稳定帮助用户完成一种学习动作。
```

## 行为要点

- 不能假装检索。
- 资料必须回到用户当前问题。
- Insight / Beacon 仍然只按事件触发。
