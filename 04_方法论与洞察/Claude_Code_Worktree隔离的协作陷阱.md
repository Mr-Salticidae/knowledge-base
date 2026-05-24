---
tags: [类型/协作工具链]
---
# Claude Code Worktree 隔离的协作陷阱

> 首次记录：2026-05-12
> 来源：B 站直播弹幕插件项目 patch3 / P0.5 / patch4 / patch5 反复遇到
> 状态：**规律已确立**（5 次实测全部复现），可放心当作默认假设

---

## 现象

Claude Code 完成一次 patch 后报告 "git status clean、commit 已推 main"，但跳蛛先生在主仓库目录跑 `git status` 时看到：

- **几十个 tracked 文件 M 状态**
- 物理文件被截断到中间（比如 `src/main/index.ts` 断在 `console.err` 半行就结束）
- 多出一个 `.claude/worktrees/<某个随机串>/` 目录

## 根因

Claude Code（在 Cowork mode 的 harness 里）执行任务时**默认启用 git worktree 隔离模式**——它在 `.claude/worktrees/<branch>/` 创建一个独立工作树工作、commit、push 到 main 分支。

**坑在哪**：
- Claude Code 的 `git status` / `git log` / build 全部基于 worktree 视角检查
- 主工作树（用户实际操作的目录）的物理文件**没有自动同步到最新 commit**
- 主工作树的物理文件依然是"上一次主工作树状态"——可能是某次 Cowork Edit 后的中间产物（被某种方式截断）

Claude Code 的完成报告里"git status clean"是**真的**（worktree 视角），但**没有可执行性**（主工作树没同步）。

## 应对（已稳定的工作流）

### 1. 完成报告必须显式提示用户同步

不要要求 Claude Code "不用 worktree"——这是 harness 行为，无法通过 prompt 禁止。

改约定：**完成报告 §"已知 leftover" 必须写一行**：

> 请跳蛛先生跑 `git checkout HEAD -- .` 同步主工作树。

把这个动作从"异常补救"升级为"预期工作流的一部分"。

### 2. 跳蛛先生执行的三行修复

```powershell
cd <项目根>
git checkout HEAD -- .   # 把 tracked 文件强制覆盖到 HEAD
git worktree prune       # 清掉过期 worktree 标记
```

这三行不会动 untracked 文件（如 untracked 的 icon.ico / 临时 PNG 等），安全。

### 3. Cowork 验收时**必须用 bash 在主工作树 verify**

不要相信 Claude Code 完成报告里"git status clean"那一句。验收清单加一条：

```bash
cd <主工作树路径> && git status --short
```

如果有 M 文件 → 不是 Cowork 的活，告诉跳蛛先生跑 §2 那三行就行。

### 4. 验证 commit 内容真的入了 main

```bash
git show HEAD:<关键文件路径> | head -50
git log --oneline -5
```

确认 commit 在 main 分支顶部、内容是预期的。**只要 commit 对，exe 也是好的**（Claude Code 在 worktree 里 build 用的是 worktree 的完整文件 → bundle 内容正确）。

## 为什么不能在 Cowork 这边阻止

试过两次：

- **patch3 交接文档明令禁止 worktree** → Claude Code 还是用了
- **P0.5 文档加强禁止 + 完工前 verify 主工作树** → Claude Code 自己自检时显示 "git status clean"（基于 worktree），实际主工作树仍坏

根因：worktree 是 Claude Code harness 在 Cowork mode 下的**进程隔离机制**，不通过 prompt 控制。

**与其对抗，不如接受**。

## 关联现象

这个陷阱还会同时产生：

1. **资源文件路径混乱** —— `out/dist/` 是输出目录，Claude Code 在 worktree 里 build 但 output 配置写到主工作树的相对路径（`out/dist`），所以 exe 实际**写到了主工作树**，是好的
2. **`.claude/worktrees/` 可能因为文件锁删不掉** —— 重启电脑后再删；不删也不影响，git 已经 prune

## 如何使用

- 任何 Claude Code 协作场景，交接文档里**默认包含**这一段约定
- 验收时**默认跑** §3 验证步骤
- 不要再花时间研究"为什么 Claude Code 用了 worktree" —— 它就是这么工作的

## 关联文档

- 配套心法:[[Claude完成报告核查心法]](核查 Claude 自述时如何避开本陷阱触发的盲区)
- 主线交接:`{AIGC工作站}/跨会话协作\B站直播弹幕插件_全局进度_交接给_下一次Cowork.md` §五 第 6 条
- 现役所有 P0.5 patch 完成报告 §"已知 leftover"
