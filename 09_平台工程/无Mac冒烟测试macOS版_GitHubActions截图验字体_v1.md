---
tags: [类型/平台工程, 主题/CI]
---
# 没有 Mac 也能冒烟测试 macOS 版：GitHub Actions 截图验字体

> 入档：2026-09-29
> 来源：desk-pond（工位池塘）v0.6.0 → v0.6.1，`{AIGC工作站}/desk-pond/.github/workflows/mac-smoke.yml`
> 验证状态：✓✓（一个 Godot 项目：v0.6.1 三轮 CI + v0.6.2 发布后一轮）；查出一个真 bug 并修好发布

## 一句话

作者手上没有 Mac，Mac 版只能发出去等用户反馈。

GitHub 的 macOS runner（公开仓库免费）可以替你做三件事：
- **静态检查**：下载 Release 包，解压，查签名、架构、版本号。
- **启动检查**：无界面启动，扫脚本报错。
- **截图**：**Apple 芯片的 runner 有 Metal 虚拟显卡，能录下真实画面**，出来的截图就是 Mac 用户看到的样子。

第一轮就截到了 v0.6.0 Mac 版中文全是方框。

**修复版先挂草稿 Release，给 CI 测，测过再公开。**第二轮修复反而让界面一个字都不显示，就是靠这一步拦住，没发出去。

## 如何使用

### 1. 工作流骨架

- 触发：`workflow_dispatch`（手动，传 tag）+ `release: published`（公开发布时自动再跑一遍）。
- 矩阵：`macos-latest`（arm64）和 `macos-15-intel`（x86_64）各跑一遍，因为安装包是 Universal 2。
- 步骤：
  1. `gh release download <tag> --pattern 'DeskPond-macOS-*.zip'`。
  2. `ditto -x -k` 解压，等同于用户双击“归档实用工具”，能保住权限位。
  3. 静态检查：
     - `codesign --verify --deep --strict` 查 ad-hoc 签名。
     - `lipo -archs` 查双架构。
     - `PlistBuddy` 读 `CFBundleShortVersionString`，对照 tag。
  4. 无界面启动：`--headless --quit-after 300`，grep `SCRIPT ERROR|Parse Error|Failed loading`，再看退出码。带启动参数的路径（例如打开分享码）单独跑一遍。
  5. 有画面地录帧：`--write-movie frames/f.png --fixed-fps 24 --quit-after 96`，只留最后一帧；设 `continue-on-error`，因为 Intel runner 录不出帧。
  6. `actions/upload-artifact` 上传日志和截图，下载下来直接看图。

### 2. 实测到的 runner 差异

| runner | 启动 | 录帧 |
|---|---|---|
| `macos-latest`（arm64） | ✅ | ✅ Metal 虚拟显卡，能出真实画面 |
| `macos-15-intel` | ✅ | ❌ 没有 GPU，录到 0 帧 |

所以 **arm64 负责看图，Intel 只做启动测试。**

### 3. 草稿 Release 先测

- 修复版先建**草稿** Release，上传安装包，手动触发 CI 指向这个 tag。测过再点公开。
- **坑**：草稿 Release 对只有 `contents: read` 的 token 不可见，`gh release download` 找不到它。工作流要给 `permissions: contents: write`。
- 公开以后，`release: published` 触发器会自动再跑一遍，留下一份正式版的验证记录。
- 补（2026-10-07，v0.6.2）：这一版没有 Mac 相关的改动，作者选择直接公开。`release: published` 自动跑的那一轮两个架构全绿，包括 arm64 的截图步骤。这次的取舍：Mac 平台差异相关的修复版仍先挂草稿测，普通版本直接公开、靠发布后这一轮兜底（单次样本，⚠️首次）。见 [[2026-10-06_工位池塘v0.6.2_老issue分诊到三端发版_复盘_v1]]。

### 4. 本次查出的 bug：Mac 版中文方框（三轮）

1. **v0.6.0**：截图里中文全是方框。桌面非 Windows 平台没有给中文配字体，靠引擎自动借系统字体，而导出版在 macOS 上借不到。Windows 上一直正常，所以本地永远测不出来。
2. **第一次修**：用 `SystemFont` 点名苹方、冬青黑体等系统中文字体。结果**截图里一个字都没有，连数字都没了**。
   - 加了 `--font-debug` 启动参数打印字体解析，才看清原因：在 CI 的 macOS 上，点名 “PingFang SC” 解析成一个 FreeType 加载不了的空路径字体集（name 为空、32 个 face），整个默认字体因此失效。
   - 这一轮只挂在草稿上，没发出去。
3. **第二次修**：不碰系统字体。默认字体改成 `FontVariation(base_font = 引擎默认字体, fallbacks = [打包的像素中文字体])`，和 Web / 手机版用同一套中文字形。截图里主界面、逛朋友缸的页面中文都正常，两个架构启动日志 0 报错。发 v0.6.1。

- 调试探针本身也会制造噪音：`--font-debug` 探测苹方时，日志会刷一百多条 FreeType 报错；不带这个参数跑的日志里是 0 条。**先确认报错来自谁，再下结论。**

## 覆盖不到的

- **Gatekeeper 首次放行**：CI 下载的文件没有隔离属性，所以“无法验证开发者”“仍要打开”这一步测不到，仍以用户反馈为准。
- 真机的 Retina 缩放、触控板手势、多显示器。
- 虚拟显卡和真显卡在着色器、性能上的差异。

## 关联文档

- 字体规律本体（本例是第二例）：[[导出运行时无系统字体回退律_CJK豆腐块_v1]]
- 来源复盘：[[2026-09-29_右下角的池塘_游戏宣传微电影_实录混剪到双语字幕发布_复盘_v1]]
- 同一个项目的 CI 与发布：[[CI从Release抓二进制托管自有服务器_桌面应用国内直连下载_v1]] · [[2026-06-26_桌面应用打磨发布闭环复盘_工位池塘v0.5.0_v1]] · [[2026-10-06_工位池塘v0.6.2_老issue分诊到三端发版_复盘_v1]]
- 检测工具先被证伪：[[全站文字截断体检_检测工具本身要先被证伪_v1]]
