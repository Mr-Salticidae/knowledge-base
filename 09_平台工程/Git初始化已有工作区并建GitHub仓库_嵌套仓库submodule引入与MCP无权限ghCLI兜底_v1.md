---
tags: [类型/平台工程, 主题/Git, 主题/GitHub]
---
# Git 初始化已有工作区并建 GitHub 仓库 · 嵌套仓库用 submodule 引入 + MCP 无权限时 gh CLI 兜底

> 入档:2026-08-14
> 来源:WorkBuddy 全案实例汇总项目初始化,Claw 工作区(含 knowledge-base 独立仓库、vibe-demos、Python 脚本)建 GitHub 仓库
> 状态:全流程跑通并验证(本地 git init → submodule → 远程仓库创建 → push 成功)

## 一句话总结

已有工作区建 GitHub 仓库的正解:**嵌套子仓库用 submodule 引入**(不是塞进去),**MCP connector 无 create_repository 权限时用 gh CLI 兜底**(zip 解压即用,凭据走 Windows Credential Manager)。本地已有的 .git 子目录不要删、不要强行 add,用 `git submodule add` 正正经经挂上。

## 破除两个常见误解

1. **「把已有 git 仓库塞进新仓库就行」** ❌ —— `git add` 会把它当嵌套仓库存一个 gitlink(空壳),内容不会跟过去,clone 时拉不到。**必须用 `git submodule add`**,让 git 知道这是一个独立仓库的引用。
2. **「MCP connector 有 GitHub 权限就能建仓库」** ❌ —— connector 的 token scope 决定权限。读/写已有仓库通常有,但 `create_repository` 需要 `repo` scope(或 `public_repo`),403 就是权限不够,不是操作错了。

## 为什么这么选(决策链)

已有工作区含 knowledge-base(独立 GitHub 仓库,有未推送 commit)+ vibe-demos(无 git)+ Python 脚本。三条路:

- **直接 init + 全 add**:knowledge-base 的 .git 会变成嵌套仓库,push 后 clone 拿不到内容。❌
- **删掉 knowledge-base/.git 再 add**:内容能进主仓库,但 knowledge-base 失去独立 push/pull 能力,两边同步变手动。❌
- ✅ **git submodule add**:knowledge-base 保持独立仓库身份,主仓库存引用,两边各自 push/pull,clone 时 `--recursive` 一键拉全。代价:clone 时要多一步 `git submodule update --init`,但这个代价换来的是职责清晰。

> 迁移判据:**当子目录已是独立 git 仓库、且需要保持独立 push/pull 能力时**,用 submodule。如果子目录内容完全属于主项目、不需要独立仓库,直接删 .git 再 add 更简单。

## 可照做(完整步骤)

1. **备份子仓库**(防操作失误):`cp -r knowledge-base /tmp/kb-backup`
2. **移出子仓库**:`rm -rf knowledge-base`(git submodule add 要求目录不存在)
3. **init 主仓库**:`git init && git branch -m main`
4. **写 .gitignore**:排除 `.workbuddy/`、`__pycache__/`、IDE 文件等
5. **写 .gitmodules**:
   ```ini
   [submodule "knowledge-base"]
       path = knowledge-base
       url = https://github.com/用户名/knowledge-base.git
   ```
6. **submodule 引入**:`git submodule add <url> knowledge-base`
7. **写 README.md**:说明目录结构、submodule 用法
8. **提交**:`git add . && git commit -m "init: ..."`
9. **建远程仓库**:
   - 有 gh CLI:`gh repo create <name> --public --source . --push`
   - 无 gh CLI 或权限不够:装 gh CLI(见下)再跑
10. **同步子仓库**:`cd knowledge-base && git pull --rebase && git push`(处理未推送 commit)

## gh CLI 无安装时的兜底方案

MCP connector 403 时,装 gh CLI 最快:

```bash
# 下载 zip(不要用 msi,Windows Installer 可能静默失败)
curl -sL -o "$TEMP/gh.zip" \
  "https://github.com/cli/cli/releases/download/v2.97.0/gh_2.97.0_windows_amd64.zip"

# 解压(注意:zip 内路径是 bin/gh.exe,不是 gh_x.x.x_windows_amd64/bin/gh.exe)
mkdir -p ~/bin && cd ~/bin
unzip -o "$TEMP/gh.zip" "bin/gh.exe" && mv bin/gh.exe . && rm -rf bin

# 验证
./gh.exe --version
```

**认证**:gh CLI 会读 Windows Credential Manager 里 `gh:github.com:<username>` 的凭据。如果之前用过 gh CLI 登录过,凭据还在,新装的 gh 直接可用(`gh auth status` 确认)。没用过的话需要 `gh auth login`(交互式,需要浏览器)。

## 关键设计点 / 踩坑

- **submodule add 的目录必须不存在**:已有内容的目录要先移走,add 完再合回来(或重新 clone)。
- **MSI 安装器可能静默失败**:Windows Installer 在某些环境下(如非管理员终端)装 MSI 会输出乱码然后失败,不报错。zip 解压是最稳的路径。
- **zip 内路径变了**:gh v2.97.0 的 zip 里 gh.exe 在 `bin/gh.exe`,不是旧版的 `gh_x.x.x_windows_amd64/bin/gh.exe`。解压前先 `unzip -l` 确认路径。
- **Windows Credential Manager 是持久化的**:gh CLI 登录一次,凭据存在系统级,重装 gh CLI 或换路径都能读。但 token 有 scope 限制(`repo` scope 才能建仓库)。
- **submodule 的 .git 是文件不是目录**:submodule 的 `.git` 是一个文本文件,内容是 `gitdir: <主仓库>/.git/modules/<子仓库名>`,真正的 git 数据在主仓库的 `.git/modules/` 下。
- **嵌套仓库 vs submodule**:嵌套仓库(直接 add 一个含 .git 的目录)push 后 clone 拿到的是空目录;submodule 有 .gitmodules 记录,clone --recursive 能拉全。**两者外观一样,行为天差地别**。

## 边界

- 仅适用 **已有本地工作区 + 部分子目录已是独立 git 仓库** 的场景。全新项目直接 `git init` + `gh repo create` 即可。
- gh CLI zip 解压方案仅限 Windows。macOS/Linux 用包管理器(brew/apt)更干净。
- Windows Credential Manager 的凭据与用户绑定,换 Windows 用户或重装系统后需要重新 `gh auth login`。
- submodule 引入了额外的 git 复杂度(指针同步、子仓库独立 commit),不适合对 git 不熟的团队成员。

## 关联文档

- [[GitHub强制2FA小白处置_TOTP原理与离线生成器_v1]] —— 同属 GitHub 账号/访问场景
- [[云端定时内容生产连环坑复盘_全绿不等于已发_v1]] —— 同属「以为能用的工具实际不行」类踩坑
- [[09_平台工程索引]] —— 平台工程区入口
