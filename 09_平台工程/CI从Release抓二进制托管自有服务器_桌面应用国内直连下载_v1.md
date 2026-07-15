---
tags: [类型/平台工程]
---
# CI 从 Release 抓二进制托管自有服务器 · 桌面应用国内直连下载

> 入档:2026-06-26
> 来源:把桌面小工具《工位池塘 Desk Pond》v0.5.0 发布到自有站 tiaozhuxiansheng.com,要给国内用户一个「点一下就下」的入口
> 状态:全链路跑通并验证(部署成功 + curl HTTP 200 + Content-Length 与构建字节逐字节一致)

## 一句话总结

要给一个 Windows 应用/游戏做**国内直连、零维护**的下载入口:**别把二进制塞进 git,也别只甩 GitHub 直链(国内慢)**——让 CI 在部署时**从 GitHub Release 抓最新 `.exe`、随静态站产物一起 rsync 到自有(香港)服务器**,主页按钮指向服务器上**固定文件名**的绝对地址。下载走香港服务器(国内直连),二进制不进仓库、不进 Pages 产物,每次部署自动同步到最新版。

## 为什么这么选(决策链)

- **塞进 git**:每发一版就多存一份 ~100MB blob,仓库历史爆炸。❌
- **只给 GitHub Release 直链**:国内下载慢/不稳,等于把「自有站国内直连」的优势丢掉。❌
- **塞进 GitHub Pages 产物**:Pages 单文件 100MB 上限,大包直接超限。❌
- **网盘(夸克等)**:要手动上传、每版手动替换、用户还要转存,维护成本高、体验差。❌
- ✅ **正解**:站点已经在 CI 里 rsync 到香港服务器(见 [[知识库网站免备案上线_香港轻量服务器方案]]);顺手让 CI **额外抓一份 Release 二进制进 dist**,跟着 rsync 上同一台香港服务器。下载和网站同机、同样国内直连;二进制只在 CI 里临时存在,不进任何 git。

## 可照做(CI 步骤)

在「构建 → rsync」之间插一步,从公开仓库的最新 Release 抓 `.exe`:

```yaml
- name: 拉取最新 Release 二进制到 dist
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    mkdir -p dist/<app>/download
    asset_url=$(curl -sL -H "Authorization: Bearer $GH_TOKEN" \
      https://api.github.com/repos/<owner>/<repo>/releases/latest \
      | grep -o '"browser_download_url": *"[^"]*\.exe"' | head -1 \
      | sed -E 's/.*"(https[^"]+)".*/\1/')
    test -n "$asset_url"                       # 取不到 URL 就让 job 显式失败
    curl -fL "$asset_url" -o dist/<app>/download/<App>-Windows.exe   # -f:HTTP 错误即失败
# 之后照常 rsync dist 到服务器
```

主页下载按钮指向**绝对地址**(任何镜像访问都打到香港服务器):

```html
<a href="https://你的域名/<app>/download/<App>-Windows.exe">下载 Windows 版</a>
```

## 关键设计点(都是会咬人的)

- **固定文件名**(如 `App-Windows.exe`,不带版本号):主页链接**永不随版本改**,发新版主页零改动。版本号写在页面文案里,别写进文件名。
- **`rsync --delete` 要求二进制每次都在 dist 里**:所以抓取步骤**每次部署都要跑**(包括定时 cron 部署),否则 dist 里没有这文件 → `--delete` 会把服务器上的旧包**删掉**。不能用「只在 push 时抓」的条件跳过。
- **抓取失败要让 job 显式失败**(`curl -f` + `test -n`):宁可整个部署红掉、服务器保留旧包,也别静默地把空/缺文件 rsync 上去再被 `--delete` 清空。
- **不要放进 Pages 那个 build job**:GitHub Pages 单文件 100MB 上限,大包会超;只在 rsync-to-server 的 job 里抓。
- **绝对地址而非站内相对路径**:这样即使用户在 GitHub Pages 镜像上打开页面,下载按钮也直连香港服务器(Pages 镜像上没有这个大文件)。
- **自动同步**:每发一个新 Release,主页下载会在下次部署(push 或定时 cron)**自动**指到最新包,无需手动替换网盘/资产。

## 配套:刚发布、近零下载时可「补包」不升版本

UI 小修想立刻让下载用户拿到、且该版本刚发布几乎无人下载时:重新构建 → `gh release upload <tag> <file> --clobber` 替换资产 → 触发一次部署(`gh workflow run`)让服务器重抓。**边界:一旦版本有真实下载量,必须升版本保持不可变性,不能再悄悄改旧版内容。**

## 边界

- 仅适合**公开仓库** Release(`browser_download_url` 免鉴权可取)+ **自有服务器**;私有 Release 取资产要带 token。
- 服务器侧 nginx 默认把 `.exe` 当 `application/octet-stream` 下发(浏览器下载而非执行),一般无需额外配置。

## 关联文档

- [[知识库网站免备案上线_香港轻量服务器方案]] —— 本律所依赖的底座:站点免备案上线 + CI rsync 到香港服务器的完整方案
- [[内容子项目构建时同步_独立仓库镜像进public_v1]] —— 同一「CI 在构建时把外部产物拉进 dist 再部署」母题的另一应用(内容仓库 vs 二进制 Release)
- [[OpenAI区域封锁与Worker就近执行陷阱_北美DO跳板_v1]] —— 同一台香港服务器的另一种用法:静态分发之外挂动态 AI 中转代理(nginx location → systemd Node 服务)
- [[桌面应用打磨发布闭环复盘_工位池塘v0.5.0_v1]] —— 本律的来源案例(完整发布闭环复盘)
- 对外讲解版(裸路径,不进图谱):`08_对外分发/给Windows小工具做国内直连下载_学员版.md`
