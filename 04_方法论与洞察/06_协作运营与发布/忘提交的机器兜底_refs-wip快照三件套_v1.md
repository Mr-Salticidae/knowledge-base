---
tags: [类型/协作工具链]
---
# 忘提交的机器兜底 · refs/wip 快照三件套

> 首次记录：2026-08-15
> 来源：aigc-creative-archive 双机协作——公司机器的工作没提交推送，家里机器看不到；作者自评"我总是忘记提交"
> 状态：✅ 当场验证（家机三层全链路跑通：快照推到远程可见、计划任务首跑 LastResult=0、hook 实测可执行）

---

## 一句话

**靠记性执行的流程必然漏，修法不是"下次记得"，是把每种忘法各配一个机器兜底。**
"忘记提交"不是一个失败模式，是三个——每层自动化只对付其中一种。

---

## 三种忘法 → 三层兜底

| 忘法 | 兜底 | 机制 |
|---|---|---|
| 压根没想起 git 这回事 | WIP 快照 | 计划任务每小时把工作区快照推到 `refs/wip/<机器名>` |
| commit 了但忘了 push | post-commit hook | 提交即自动推送，离线静默降级不阻塞 |
| 开工在旧基线上 | 会话启动检查 | Claude Code SessionStart 用 `ls-remote` 比对本地/远程（[[开工前先对基线律_v1]] 的机器化） |

只做一层的话做第一层——它是唯一能覆盖"根本没打开 git"这个真实失败模式的。

---

## 核心技法：refs/wip 隐藏引用快照

四个 git 底层命令拼出"备份但不打扰"：

```powershell
$env:GIT_INDEX_FILE = ".git\wip-index"   # 临时索引:不碰用户正在进行的暂存
git read-tree HEAD; git add -A            # 含未跟踪文件,但仍遵守 .gitignore
$tree = git write-tree
$commit = git commit-tree $tree -p (git rev-parse HEAD) -m "wip @机器名"
git update-ref refs/wip/机器名 $commit    # 隐藏引用:不进分支列表,不污染历史
git push --force origin refs/wip/机器名   # force 同名引用:只保留最新,旧的被 gc 回收
```

设计要点：

- **不碰 HEAD、不碰分支、不碰暂存区**——用户毫无感知，master 依然只有亲手写的策展式提交。
- **快照提交以 HEAD 为父**：就算工作区是干净的，只要本地有未推送提交，推快照也会把它们一并带上云端。
- **恢复**：`git fetch origin "refs/wip/*:refs/wip/*"` 后从 `refs/wip/<机器名>` 里 `git checkout ... -- 文件` 捞。
- 双机各推各的引用，永不冲突；双机配不同 `user.name`，看提交作者名即知来自哪台机器。

---

## 工程判断（踩过才知道）

1. **同步"检查"用 `ls-remote`，同步"动作"才用 `fetch`。** 素材型大仓库（工作区 1.3GB）fetch 要 2 分钟起步，塞进 SessionStart hook 会把会话启动卡死；`ls-remote` 只取引用哈希不下载对象，实测秒回。
2. **中断的 fetch 会在 `.git/objects/pack/` 留下 `tmp_pack_*` 垃圾**（本次两个共 380MB），`git gc` 不会删它们，要确认无 git 进程后手动删。`git count-objects -vH` 的 `size-garbage` 一栏能看到。
3. **autocrlf=true 环境下，hook 脚本必须在 `.gitattributes` 锁 `text eol=lf`**——checkout 成 CRLF 的 shell 脚本在 Git Bash 下直接跑不了。
4. **含中文的 `.ps1` 必须存 UTF-8 BOM**，否则 PS 5.1 按 GBK 误读、解析错乱——见 [[Windows下编码与DPI的所见非真相]] 陷阱四（本次为二次验证，且乱码值一路写进了 `git config`）。
5. **hook 要进版本库就用 `core.hooksPath` 指向仓库内目录**（`.git/hooks` 不入库，多机不同步）；部署收敛成一条 `deploy.ps1`，新机器跑一次即完成 hooksPath + 计划任务注册。

---

## 与 AI 协作的分工边界

Claude Code 的安全分类器会拦截**持久化/自扩权类动作**：`git config core.hooksPath`、`Register-ScheduledTask`、推送含 hooks 配置的提交、执行含 force-push 的脚本。这不是障碍，是合理的分工线：

> **AI 负责写好脚本 + 拆步实测 + 只读验收；"启用自动化"这一下由人亲手跑。**

实操上把所有需要人跑的动作收敛成一条命令（deploy.ps1），把验收拆成只读命令（`git config core.hooksPath` / `Get-ScheduledTaskInfo` / `git ls-remote origin "refs/wip/*"`），AI 在人跑完后逐项核对。

---

## 关联文档

- [[开工前先对基线律_v1]] —— 第三层是这条律的自动化形态：把"开工先对基线"从自律动作变成 SessionStart 机器动作
- [[Windows下编码与DPI的所见非真相]] —— 陷阱四（.ps1 无 BOM 按 GBK 误读）在本次部署中二次现形
- [[生成物不入git_v1]] —— 同仓库的体积治理侧：快照会放大二进制推送频率，未压缩 WAV 等大件更该先治理
- [[交付前实测证伪律_v1]] —— 三层各自实测到"远程可见 / LastResult=0"才算交付，不交付"应该能行"
