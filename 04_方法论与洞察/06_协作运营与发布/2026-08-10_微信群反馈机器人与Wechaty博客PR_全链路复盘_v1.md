---
tags:
  - 类型/协作工具链
  - 工具/Wechaty
  - 工具/GitHub CLI
  - 主题/微信机器人
  - 主题/开源贡献
  - 来源/pb-arena
---
# 微信群反馈机器人与 Wechaty 博客 PR：全链路复盘

> 入档：2026-08-10
> 项目：pb-arena 微信群反馈收集机器人
> 项目目录（库外裸路径）：`E:\pb-arena\wechat-bot`
> PR 地址：[wechaty/jekyll#201](https://github.com/wechaty/jekyll/pull/201)
> 配套 skill：`wechaty-blog-pr`（用户级 `~/.workbuddy/skills/wechaty-blog-pr`）
> 验证状态：⚠️ PR 已提交，待 CLA 签署 + CI + Review；PadLocal Token 尚未到手，机器人未实跑

## 事实记录（不可修改区）

- **起点**：pb-arena 有一个活跃的用户微信群，反馈散落在聊天里，手工收集漏消息。决定搭一个被动监听机器人自动入库。
- **协议选型**：普通微信群（非企业微信），选定 Wechaty + PadLocal（iPad 协议）。Bot 策略=被动监听、不主动回复（降低风控）。
- **架构**：Wechaty Bot → 规则层（filter.js，53 个中文关键词评分 ≥3 为候选）→ AI 层（analyzer.js，LLM 分类/摘要/严重度）→ 复用 pb-arena 已有 `POST /api/feedback` 入库，与管理后台反馈面板打通。两层过滤的目的是省 LLM 调用成本。
- **交付物**：`E:\pb-arena\wechat-bot\` 下 8 个源文件 + 启动脚本；规则层 16/16 单测通过；依赖安装完成。
- **卡点**：PadLocal 付费站 `pad-local.com` 返回 502，注册站宕机；竞品 Paimon 同样 502，疑似共享基础设施故障。付费路径走不通。
- **转向**：改走 Wechaty Contributor Program——给 wechaty/jekyll 写一篇技术博客提 PR，换取最长 1 年免费 PadLocal Token。
- **博客**：撰写《Building a WeChat Group Feedback Collector with Wechaty + LLM》（英文），含架构图 SVG，归档 `E:\pb-arena\wechat-bot\wechaty-blog-post.md`。
- **PR 执行**：fork `wechaty/jekyll` → 分支 `blog-wechat-feedback-collector` → 放博客/配图/contributor → push → `gh pr create` → PR #201。
- **当前状态**：PR OPEN，mergeStateStatus=BLOCKED，唯一未过检查是 CLA（需作者签署）。

以上先按 [[复盘事实先行原则]] 冻结。下文「成功」仅指 PR 提交成功，不外推成「Token 已到手」或「机器人已跑通」。

## 一句话结论

**这次的核心教训是：旧指南里的仓库地址会过时，git fetch 报成功也不代表 ref 真写进去了——执行第三方开源贡献前，先用 `gh repo view` 验证实际仓库名，再亲自确认 ref 落地，别盲信任何「应该能行」的文档。**

## 一、实际走通的链路

1. **gh CLI 全链路执行**：用户要求「fork + PR 一步到位」。用 `gh repo fork` + `gh pr create` 串起 fork→clone→branch→commit→push→PR，比网页手把手操作高效，且每一步有命令行回执可核查。
2. **先验证再动手**：fork 前先 `gh repo view Mr-Salticidae/jekyll` 查 fork 是否已存在，避免重复 fork；再用 `gh search repos --owner wechaty` 确认目标仓库真名。
3. **踩坑后即时沉淀**：发现 PR 指南里的 `wechaty.js.org` 已更名，当场修正指南文件并写入新 skill，不让下一次再踩。
4. **skill 化**：把整条流程存成 `wechaty-blog-pr` skill，下次投 Wechaty 博客直接复用。

## 二、阻塞与恢复

| 阻塞 | 事实原因 | 恢复方式 | 沉淀 |
|---|---|---|---|
| PR 指南里写 `wechaty/wechaty.js.org`，fork 时报「已存在 Mr-Salticidae/js.org」 | 旧仓库已更名/重定向，指南过时 | `gh search repos --owner wechaty` 查到真名是 `wechaty/jekyll`，重新 fork 正确仓库 | **旧文档的仓库地址会过时**，fork 前必须 `gh repo view` 验证实际仓库名 |
| `git fetch upstream` 报「`* [new branch] main -> upstream/main`」成功，但 `git show-ref` / `git checkout upstream/main` 全部找不到该 ref | Windows Git 2.55 的 ref 存储 bug：`.git/refs/remotes/upstream/` 目录未创建，fetch 写不进 | `mkdir -p .git/refs/remotes/upstream` 后手动 `echo <hash> > .git/refs/remotes/upstream/main`，或直接 `git checkout -b <branch> $(git ls-remote upstream main \| awk '{print $1}')` | **fetch 成功≠ref 写入**；ref 不存在时优先用 `git ls-remote` 拿 hash 直接建分支 |
| PR 指南要求配图转 PNG，但本机无 ImageMagick / cairo / rsvg-convert | Windows 环境缺系统级 SVG 渲染库，cairosvg/svglib 都因缺依赖失败 | 查证目标 Jekyll 站点本身支持 SVG（已有 `_posts` 引用 `.svg`），直接用 SVG，不转 PNG | **目标站点支持的格式就直接用，别在没有转换工具链的环境卡住**；转换是优化不是阻塞 |
| 旧 PR 指南的 contributor 格式只有 name+github 两字段，但现有 contributor 都带 avatar/bio/site | 指南过时，实际仓库格式更丰富 | 参照现有 `_contributors/*.md` 写 richer 格式，avatar 用 `https://avatars.githubusercontent.com/u/<id>?v=4`（`gh api users/<name> --jq '.avatar_url'` 取） | 贡献者文件格式以仓库现有样本为准，不以旧指南为准 |

## 三、可复用方法

### 方法 1：第三方开源贡献前的仓库验证律

提 PR 给第三方开源项目前，**先验证仓库真名，再 fork**。文档（包括自己以前写的指南）里的仓库地址会随项目更名/归档/迁移而过时。

```bash
# 1. 查目标仓库是否存在、是否重定向
gh repo view <org>/<repo> --json name,owner,url,parent
# 2. 查自己是否已 fork
gh repo view <username>/<repo> --json name,parent
# 3. 不确定真名时搜索
gh search repos --owner <org> --json name,url,description
```

`gh repo view` 遇到重定向会返回重定向后的真实仓库名（如 `wechaty/wechaty.js.org` 返回 `name: js.org`），这是仓库已更名的信号。

### 方法 2：git fetch 成功但 ref 不存在时的 fallback

Windows Git 2.55 存在 ref 存储 bug：`git fetch upstream` 输出成功，但 `upstream/main` 在 `git show-ref` / `git branch -a` 里不存在，`git checkout -b x upstream/main` 报「unknown revision」。

判定：`git ls-remote upstream` 能拿到 hash，说明远端没问题，是本地 ref 没写入。

恢复（任选其一）：
```bash
# A. 直接用 hash 建分支，绕过 ref
git checkout -b <branch> $(git ls-remote upstream main | awk '{print $1}')

# B. 手动补 ref 目录再 fetch
mkdir -p .git/refs/remotes/upstream
git fetch upstream
```

这条与 [[开工前先对基线律_v1]] 同族：基线对不齐就别往下走，只是这次的「对不齐」是工具 bug 而非忘记 fetch。

### 方法 3：gh CLI 一步到位执行 fork+PR

给第三方仓库提 PR，用 gh CLI 串起全链路，比网页操作快且可核查：

```bash
gh repo fork <org>/<repo> --clone=false --default-branch-only
git clone https://github.com/<username>/<repo>.git
cd <repo>
git remote add upstream https://github.com/<org>/<repo>.git
# 建分支（见方法 2 的 fallback）
git checkout -b <branch> $(git ls-remote upstream main | awk '{print $1}')
# 改文件…
git add <files>
git commit -m "<msg>"
git push origin <branch>
gh pr create --repo <org>/<repo> --base main --head <username>:<branch> \
  --title "<title>" --body "<body>"
```

注意：个人项目可免 PR 直推（见 [[个人项目免PR直推主分支_v1]]），但**第三方开源项目必须走 fork+PR+CLA**，这是两套规则，不能混用。

### 方法 4：SVG 配图别硬转 PNG

博客配图若源文件是 SVG，先查目标站点是否支持 SVG（`grep -r "\.svg" _posts/` 看现有文章引用），支持就直接用。PNG 转换在没有 ImageMagick / cairo / librsvg 的 Windows 环境会卡住（cairosvg 缺 `libcairo-2.dll`、svglib 缺 `rlPyCairo` backend）。转换只是体积优化，不是阻塞项，别让它挡住 PR 提交。

## 四、本次未验证的部分

- **机器人未实跑**：PadLocal Token 要等 PR 合并后 Wechaty 团队发放，目前 `.env` 里 `WECHATY_PUPPET_PADLOCAL_TOKEN` 仍空，机器人没真正连过微信。
- **两层过滤的召回率未实测**：规则层 53 个关键词是手工配的，AI 层 prompt 没有跑过真实群消息样本，可能漏召回或误召回。Token 到手后需用历史群消息做一轮标注验证。
- **PR 是否合并未知**：取决于 Wechaty 维护者 review，可能要求改稿。

## 关联文档

- 基线对齐同族：[[开工前先对基线律_v1]]（fetch 对基线；本次是 fetch 的 ref bug 版本）
- 个人 vs 协作的分轨：[[个人项目免PR直推主分支_v1]]（个人项目免 PR，第三方开源项目必须走 PR，互为镜像）
- 交付前验证：[[交付前实测证伪律_v1]]（「应该能行」的仓库地址当场证伪）
- 复盘纪律：[[复盘事实先行原则]]（先冻结事实：Token 没到手、机器人没跑）
- 配套 skill：`~/.workbuddy/skills/wechaty-blog-pr/SKILL.md`
- 原始底料（库外裸路径）：`E:\pb-arena\wechat-bot\wechaty-blog-post.md` · `E:\pb-arena\wechat-bot\PR-SUBMISSION-GUIDE.md`
