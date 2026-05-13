# 知识库 → GitHub 同步使用说明

这个文件夹（`D:\AIGC工作站\知识库`）已经配好了一套**自动同步到 GitHub 私有仓库**的流程。共 3 个脚本 + 1 个忽略规则文件。

## 文件清单

| 文件 | 作用 | 运行频率 |
|------|------|----------|
| `.gitignore` | 排除不需要入库的临时文件 | 自动 |
| `_setup_git.ps1` | **一次性**初始化 Git + 首次 commit | 跑 1 次 |
| `_register_schedule.ps1` | **一次性**注册 Windows 定时任务 | 跑 1 次（管理员） |
| `_auto_sync.ps1` | 检测变更 → commit → push | 定时自动跑 |

## 三步走（按顺序）

### 第 1 步：初始化本地仓库

打开 **PowerShell**（不需要管理员）：

```powershell
cd D:\AIGC工作站\知识库
.\_setup_git.ps1
```

若提示"无法加载脚本因为禁用了执行"，先执行：
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

脚本会：检查 Git → 设置身份 → `git init` → 首次 `commit`。

### 第 2 步：在 GitHub 创建私有仓库并关联

1. 浏览器打开 https://github.com/new
2. 创建一个 **Private** 仓库（建议名字：`knowledge-base`）
3. **不要勾选** "Add a README"、".gitignore"、"license"
4. 创建后复制 HTTPS 地址（形如 `https://github.com/你的用户名/knowledge-base.git`）
5. 回到 PowerShell 执行（替换成你自己的地址）：

```powershell
git remote add origin https://github.com/你的用户名/knowledge-base.git
git push -u origin main
```

首次 push 会弹出 GitHub 登录授权窗口，授权一次后会记住凭据。

### 第 3 步：注册定时任务

**以管理员身份**重新打开 PowerShell：

```powershell
cd D:\AIGC工作站\知识库
.\_register_schedule.ps1
```

默认每天 **22:00** 自动同步。要改时间，编辑 `_register_schedule.ps1` 第 7 行的 `$triggerTime`。

## 日常使用

设好之后**你什么都不用管**——每天 22:00 自动 commit + push。

需要手动触发：

```powershell
.\_auto_sync.ps1
```

查看日志：`D:\AIGC工作站\知识库\.sync-log\sync.log`

## 以后想给别人开放权限

去 GitHub 仓库页面：

- **Settings → Collaborators** 加单个协作者（仍保持仓库私有，只对加的人可见）
- **Settings → General → Change visibility → Public** 一键转公开

## 常见问题

**Q: 第一次 push 提示要密码？**
A: GitHub 早已不接受密码登录。需要：① 装 [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager)（新版 Git for Windows 自带），它会弹出网页让你授权；或 ② 在 GitHub 生成 [Personal Access Token](https://github.com/settings/tokens) 当密码用。

**Q: 不小心把敏感文件 commit 了怎么办？**
A: 加进 `.gitignore` 后还要执行 `git rm --cached 文件名` 把它从仓库历史移除，然后 commit + push。如果是真敏感（API Key 之类），建议在 GitHub 上直接 revoke 那个 key。

**Q: Obsidian 的 workspace.json 一直在变，commit 提示太烦怎么办？**
A: 已在 `.gitignore` 里排除了它，不会被追踪。

**Q: 想换电脑继续用？**
A: 新电脑装 Git → `git clone https://github.com/你的用户名/knowledge-base.git D:\AIGC工作站\知识库` → 跑 `_register_schedule.ps1` 注册定时任务即可。
