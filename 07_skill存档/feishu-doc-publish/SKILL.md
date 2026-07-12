---
name: feishu-doc-publish
description: 把本地 Markdown 一键发布为飞书云文档并拿回可分享链接（复用 pb-arena 仓库随附的 feishu-doc-sync CLI，即自建应用"飞书助理小桁"）。当用户说「发布到飞书」「导出一份飞书文档」「让小桁发布」「同步到飞书」「给团队发个文档链接」「跟之前一样发飞书」，或任何「本地 md → 飞书云文档」的诉求时使用本 skill，即使没提到小桁、CLI 或 pb-arena。
---

# feishu-doc-publish — 发布 Markdown 到飞书云文档

把一篇本地 Markdown 变成飞书云文档（docx），默认开启组织内可阅读，输出链接交付给用户。工具是 pb-arena 仓库随附的零依赖 Node CLI，API 走"飞书助理小桁"这个自建应用（租户域 `ncnnb044q88x.feishu.cn`）。

**交付标准**：给用户一条可直接粘到群里的 `https://ncnnb044q88x.feishu.cn/docx/...` 链接，且用户账号对文档有编辑权。

## 第 1 步：定位工具

CLI 在 pb-arena 仓库里：`<pb-arena>/tools/feishu-doc-sync/sync.mjs`（零 npm 依赖，Node ≥18 即可）。已知位置：

- 网吧机：`B:\临时\pb-arena`
- 主力机：E 盘工作区（用 Glob 找 `**/tools/feishu-doc-sync/sync.mjs`）

细节与故障速查以同目录 `README.md` 为准，动手前值得扫一眼。

## 第 2 步：环境检查（Node）

`node --version` 能出 ≥18 就跳过本步。网吧机没有全局 Node（winget 安装会崩 0xC0000005），用便携版：

1. 先找现成的：`Get-ChildItem "$env:LOCALAPPDATA\Temp\claude" -Recurse -Filter node.exe` —— 旧会话 scratchpad 里往往留着一份（node v22 便携版，验证过可直接用）；
2. 找不到再准备新的：从 nodejs.org 下载 win-x64 便携 zip 解压到本会话 scratchpad（下载前按平台规则征得用户同意）。

后续命令统一用找到的 node.exe 全路径调用，不依赖 PATH。

## 第 3 步：凭证检查（最常缺的一环）

凭证按此顺序查找：环境变量 `FEISHU_APP_ID`/`FEISHU_APP_SECRET` → CLI 同目录 `feishu_config.json` → `~/.feishu/config.json`（推荐）。

**网吧机陷阱：C 盘每次还原都会清掉 `~/.feishu/config.json`，缺凭证是常态，不是异常。** 凭据本身永远不变——直接向用户要 App ID 和 App Secret（飞书开放平台 open.feishu.cn → 开发者后台 → 应用 → 凭证与基础信息），同时要 `owner_mobile`（用户飞书绑定手机号）。拿到后写入 `~/.feishu/config.json`：

```json
{
  "app_id": "cli_...",
  "app_secret": "...",
  "tenant_domain": "ncnnb044q88x.feishu.cn",
  "owner_mobile": "..."
}
```

`owner_mobile` 不是可选项的原因：导入 API 生成的文档归应用所有，不授权的话**用户自己打开自己的文档只有只读权**（2026-07-09 实际踩坑）。填了它，每次发布完会自动把用户账号加为协作者（full_access）。

## 第 4 步：连通性测试

```powershell
<node> <pb-arena>\tools\feishu-doc-sync\sync.mjs --test
```

期望输出「连通性 OK + 凭据来源 + owner 解析 OK」。凭证错误在这一步暴露，别带着坏凭证进发布流程。

## 第 5 步：准备文档

- 文档须**独立成篇**：不含 Obsidian 双链 `[[...]]`、不依赖库内其他文档。若源文件来自知识库内核档，先按 08_对外分发体例改写；
- **本 CLI 不上传本地图片**——`![](./xxx.png)` 这类引用导入后会失效。纯文字+表格的文档没问题；含本地图片的要么先把图删改成文字，要么改用 knowledge-base `06_代码/feishu_sync`（Python 版，支持嵌图）；
- 标准 Markdown 表格、加粗、代码块都能正确转换；
- 标题约定 `<标题>_<YYYY-MM-DD>`，与历史文档保持一致。

## 第 6 步：发布

```powershell
<node> <pb-arena>\tools\feishu-doc-sync\sync.mjs "<md文件路径>" --title "<标题_YYYY-MM-DD>"
```

成功输出五步进度和最终链接。默认开启「组织内获得链接可阅读」（加 `--no-share` 可关）；配置里有 owner 时自动授权，日志会体现。

## 第 7 步：授权兜底

如果发布时配置里还没填 owner（比如用户后补手机号），单独补授权：

```powershell
<node> <pb-arena>\tools\feishu-doc-sync\sync.mjs --grant <doc_token>
```

`doc_token` 是链接里 `/docx/` 后面那串。补完把 `owner_mobile` 写回配置，下次自动带上。

## 故障速查

- `缺少飞书应用凭据` → 第 3 步，向用户要凭据重建配置；
- `获取 tenant_access_token 失败` → app_id/app_secret 抄错或应用被停用；
- `1061004 / forbidden` → 应用云文档权限问题（正常不会遇到，应用权限跟应用走、早已配好）;
- 开分享失败但文档已生成 → 脚本只警告不中断，让用户在文档右上角手动开「组织内可阅读」；
- 更多见 CLI 同目录 `README.md`。

## 交付

把链接给用户，一并说明：文档已开组织内可阅读、账号已授权可编辑。若本次是在还原盘机器上重建过凭证，提醒一句「下次还原后需要再提供一次 App ID/Secret」。
