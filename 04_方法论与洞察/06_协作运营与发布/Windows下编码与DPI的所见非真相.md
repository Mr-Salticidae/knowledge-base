---
tags: [类型/协作工具链]
---
# Windows 下编码与 DPI 的「所见非真相」

> 首次记录：2026-06-16
> 来源：Desk Pond（Godot）项目——GitHub Release 中文说明三连乱码，以及 UI 截图两次误判「按钮被截断 / 池塘溢出」
> 状态：**规律已确立**，凡是在 Windows 上发中文、截图核查 UI 都适用

---

## 核心观察

在 Windows 上，**你「看到」的产出之前，隔着两层会骗你的转换**：

1. **编码层**——文本在进程间传递时被按 GBK（cp936）而非 UTF-8 解码；
2. **DPI 缩放层**——截图工具在 125% 缩放下把窗口尺寸算错。

两层都会让「看起来坏了 / 看起来好了」与**真相**脱节。结论：**跨编码、跨缩放、跨进程的产出，必须用程序化字节级核查，不能靠肉眼看终端或截图。** 这是 [[Claude完成报告核查心法]] 在 Windows 工具链上的具体形态。

---

## 陷阱一：Python 把管道 / stdin 当 GBK 解码

把中文（UTF-8）经管道喂给 `python`，`sys.stdin.read()` 在 Windows 上**默认按 GBK 解码** → 入库即乱码。

| 现象 | 真因 |
|---|---|
| Release 正文 `婼犽����` 全是乱码，但**标题正常** | 标题内联在 python 源码里（按 UTF-8 读源文件），正文走 stdin（按 GBK 解码） |
| 三个 Release（v0.2.0/.1/.2）正文全坏 | 同一套 `NOTES 堆文档 → python stdin` 写法复制了三次 |

**坏写法**（隐式编码，必踩）：

```bash
NOTES=$(cat <<'EOF' ... 中文 ... EOF)
python -c "import json,sys; print(json.dumps({'body':sys.stdin.read()}))" <<EOF
$NOTES
EOF
```

**对写法**（显式 UTF-8 + 纯 ASCII 过线）：

```python
body = open("notes.md", encoding="utf-8").read()      # 显式 UTF-8 读
payload = json.dumps({"body": body}).encode("ascii")  # ensure_ascii=True 默认 → 全部转 \uXXXX
```

要点：**让中文以 `\uXXXX` 转义形态过线**，彻底绕开任何字节编码歧义；源文用文件而非管道，并显式 `encoding="utf-8"`。

---

## 陷阱二：终端显示层也按 GBK（红鲱鱼）

修好之后我 `print` 入库结果做核查，终端又显示 `??λ????`——**差点以为没修好**。其实入库是对的，是 **Bash 控制台按 GBK 渲染 python 的 UTF-8 输出**。

**教训：肉眼看终端里的中文，不能用来判断中文数据对不对。** 显示层和数据层是两回事，一次 bug 里我被同一个 GBK 假象骗了两遍（写入端 + 核查端）。

---

## 陷阱三：DPI-unaware 截图把尺寸算错

同源的「所见非真相」。系统 125% 缩放下，DPI-unaware 的截图进程把 640×520 的窗口抓成 **512×416**（=÷1.25），内容被压 / 裁，于是我**两次误判**「最小化/关闭按钮被挤出窗口」「池塘溢出」——其实布局本身没问题。

- 截图核查 UI 前先 `SetProcessDPIAware()`，否则尺寸全错。
- 更可靠的是**用引擎自身坐标核查**：打印控件 `rect` / `get_combined_minimum_size()`，而不是数截图像素。布局打印显示 `×` 按钮在 602–628（窗口 640 内）才是真相，截图的「截断」是假象。

### 第三、四次验证（2026-08-02 · LiveLink）⭐⭐⭐ —— 这次假象进了对外文案

**形态三：PowerShell DPI-unaware → 误判「布局被撑破」，并写进了已发布的 release notes。**
125% 缩放下 `GetWindowRect` / `CopyFromScreen` 走虚拟坐标，截图右侧被裁。
据此判断「窄窗口下布局溢出、右边按钮被裁掉」，写了 CSS 修复，
**并把这条写进 commit message 和已发布的 GitHub release notes**。
后来用 CDP 量 `document.documentElement.scrollWidth` —— 等于 `innerWidth`；
再做对照实验（900 / 820 / 760px 下加不加那段 CSS 结果完全一致）：**该 bug 从不存在**。
线上 release notes 已编辑删除该虚假声明。

> 前两次假象停在「判断」层，这次**流到了对外文案**。教训升级为：
> **没有第二种手段确认过的现象，不能写进对外文案。**

**形态四：CDP 的 `contentSize` 是物理像素，不是 CSS 像素。**
生成长图时用 `Page.getLayoutMetrics().contentSize` 量高度，它按宿主 DPI 报物理像素
（125% 下多报 25%），当成 CSS 像素套进 `setDeviceMetricsOverride` → 图底部空一大截。
改用 `document.documentElement.scrollHeight`（纯 CSS 像素）即正常。
判据：`contentSize.width ÷ 设定宽度` 正好等于系统缩放比（本次 938/750 = 1.25）就是踩到了。

**补两条规则**：
- 凡量页面尺寸，**一律用 DOM 的 `scrollWidth / scrollHeight`**，
  不要用任何「窗口 / 截图 / 布局指标」类 API —— 前者是 CSS 像素，后者随 DPI 漂移。
- 网页截图改用 CDP `Emulation.setDeviceMetricsOverride` + `captureBeyondViewport` **离屏渲染**：
  既不受 DPI 影响，也不会像整屏捕获那样抓到别的窗口
  （本次整屏截图两次抓到无关前台窗口，含私人聊天内容，只能删掉重来）。

### 第五次验证（2026-08-05 · PB Arena 移动端改稿校对）⚠️ —— 窗口宽度被系统夹住

**形态五：`--window-size` 传的窄宽度截不出来，Windows 会把窗口夹到最小宽度。**

用 `chrome --headless=new --window-size=430,2700 --screenshot` 校对移动端，
截出来的图**到处横向溢出**：卡片右边被切、顶部计数少半截、阶段轴第三格不见了。
据此判断「移动端布局崩了」，改了一轮 CSS。

真相是 **Windows 把浏览器窗口宽度夹到约 500px**：页面按 ~500px 布局，
截图再裁到 430px 输出 —— 页面本身 `scrollWidth === 430`，**从来没有溢出过**。
与形态三 / 四同源：**你传给截图工具的尺寸，不等于页面实际拿到的视口宽度。**

解法是**别让窗口来定宽，让 iframe 定宽**（宿主窗口开 520+ 以避开夹取）：

```html
<iframe id="f" src="/target.html" style="width:430px;height:2700px;border:0"></iframe>
<script>
  var d = f.contentDocument, vw = d.documentElement.clientWidth, bad = [];
  d.querySelectorAll("*").forEach(el => {                    // 页内实测，不看截图
    var r = el.getBoundingClientRect();
    if (r.right > vw + 1 && r.width > 0) bad.push(el.className);
  });
  out.textContent = "scrollW=" + d.documentElement.scrollWidth
                  + "\n" + (bad.join("\n") || "NO OVERFLOW");
</script>
```

媒体查询在 iframe 里按 430 求值，截出来的就是真的；顺带还能在 iframe 里
`.click()` 导航按钮驱动到需要交互才到达的页面，并挂 `window.onerror` 收报错，
一次调用同时拿到目标页截图、溢出清单、控制台报错三样。

> 这是「量页面尺寸一律用 DOM 的 `scrollWidth / scrollHeight`」那条规则的又一次兑现：
> **响应式验证不能信「我给浏览器传了多宽」，要信「页面自己报了多宽」。**
> 出处见 [[美工改稿V4四屏落地_禁止项是待办不是护栏_v1]] insight 5。

### 第六次验证（2026-08-10 · 飞书小桁同步）⚠️ —— Git Bash 把 Unix 路径前缀双写成 Windows 路径

**形态六：Git Bash 调 Node 处理 Windows 路径时,`/e/...` 被解析成 `e:\e\...`。**

调用 pb-arena 的 sync.mjs 同步飞书文档,先用 `ls "/e/pb-arena/.../sync.mjs"` 验证文件存在(成功),再 `node /e/pb-arena/.../sync.mjs --test`——报 `Cannot find module 'e:\e\pb-arena\...sync.mjs'`,路径里凭空多出 `e\` 前缀。原因:Git Bash(MSYS2)的 POSIX 路径转换层会把 `/e/...` 转成 `e:\e\...`(把挂载点字母当前缀拼两次),Node 收到的是被它改过的 Windows 路径,而那条路径根本不存在。

**解法不是关 MSYS,是用 `MSYS_NO_PATHCONV=1` + Windows 反斜杠原路径**:

```bash
MSYS_NO_PATHCONV=1 node 'E:\pb-arena\tools\feishu-doc-sync\sync.mjs' 'E:\vacat-2026\review\xxx.md' --title 'xxx_2026-08-10'
```

- 单引号包裹反斜杠路径防止 Bash 二次转义
- `MSYS_NO_PATHCONV=1` 关掉 POSIX → Windows 路径自动转换,Node 拿到的就是原样
- 或者干脆用 `cd` 进脚本目录后用相对路径 `node sync.mjs`,绕开整层转换(但 cwd 切走后无法同时引用工作区的目标 md,仅适合单文件任务)

**判据**:Node 报 `MODULE_NOT_FOUND` 且错误路径里出现双前缀(如 `e:\e\` / `c:\c\` / `d:\d\`)就是踩到了。`ls` 能列出文件≠ Node 能解析路径——前者是 Bash 自己处理 POSIX 路径(它会做正确转换),后者是 Bash 把路径传给 Node 时被 MSYS 转换层污染。

> 这是「响应式验证不能信『我给浏览器传了多宽』,要信『页面自己报了多宽』」那条规则的姊妹形态:**调用方传给被调方的路径,不等于被调方实际收到的路径。** 同源教训:验证文件存在用 Bash 内建命令的 `ls`/`test` 都做 POSXI 兼容转换,不能用来验证 Node/Python 等非 Bash 程序收到的 Windows 路径。

---

## 陷阱四：脚本文件层也按 GBK（.ps1 读入 + Python 输出）

同一 GBK 根因，还咬在"脚本文件本身"这一层，两个方向各一个：

**读入侧——`.ps1` 含中文必须存 UTF-8 BOM。** Windows PowerShell 5.1 读 `.ps1` 时，**无 BOM 的 UTF-8 会被按系统 ANSI(GBK) 解码**：中文注释/字符串里的全角标点（`（）` `，` `——`）被错读成别的 token，直接**解析失败**（`Unexpected token` / `Missing closing`），脚本根本跑不起来。用 Write 工具生成的 `.ps1` 默认无 BOM，必踩。修：写完转带 BOM 的 UTF-8——

```powershell
$c = Get-Content -Raw -Encoding UTF8 .\x.ps1
Set-Content -Path .\x.ps1 -Value $c -Encoding UTF8   # PS5.1 的 -Encoding UTF8 写出即带 BOM
```

**输出侧——Python `print` 非 GBK 字符直接崩。** 陷阱二是"显示乱码但不报错"；更狠的一档是**硬崩**：Python 的 stdout 编码在 Windows 控制台是 GBK，`print('✓')`（U+2713 不在 GBK 码位）抛 `UnicodeEncodeError: 'gbk' codec can't encode character`，整个脚本中断。修：脚本开头 `sys.stdout.reconfigure(encoding="utf-8")`，或输出只用 ASCII（`[OK]` 别用 `✓`）。

教训：**GBK 不只咬"进程间管道"和"终端显示"，还咬"脚本文件的读入与输出编码"。** 凡 Windows 上跑含中文/符号的 `.ps1`/`.py`，先把两端编码显式钉死。

---

## 附带：Bash 赋值前缀用的是旧值

```bash
TOKEN=$(...) python ... "$TOKEN"   # ✗ 参数里的 $TOKEN 是赋值"之前"的旧值 → 401
```

简单命令的 `VAR=val cmd "$VAR"`：`"$VAR"` 在**赋值生效前**就展开了。要分两句写，或 `export` 后让程序从 `os.environ` 读。

---

## 心法：字节级核查清单

凡在 Windows 上交付中文 / 核查 UI：

1. **发中文到 API**：UTF-8 文件 → `encoding="utf-8"` 读 → `json.dumps(ensure_ascii=True)` → 纯 ASCII 过线。
2. **核查文本**：把数据**拉回来与源文 `==` 比对**，再数 CJK 字符数、查是否含替换符 `�`——**只输出 ASCII 诊断**（`match=True`、`cjk=121`、`has_replacement=False`），不要肉眼看终端里的中文。
3. **核查 UI**：DPI-aware 截图，或直接读引擎布局坐标；别拿可能被缩放的像素截图下结论。
4. **怀疑一切隐式编码 / 隐式缩放**：管道、stdin、控制台、截图——每一层都可能悄悄换编码或换比例。

宁可多写一句显式编码，也不要让产出经过一层「看不见的转换」。

## 关联文档

- [[Claude完成报告核查心法]] —— 本文是它在 Windows 工具链上的具体形态:「所见」≠「真相」,要程序化核查而非肉眼信任
- [[Claude_Opus_4.8行为实测]] —— 4.8 更诚实,但 Windows 编码 / DPI 这类环境假象与模型诚实无关,仍须独立核查
- [[Claude_Code_Worktree隔离的协作陷阱]] —— 同属「视角 / 环境错位导致 self-verify 失真」的一类
- [[UI自动化的固定坐标必须绑前提断言_v1]] —— 同源的「环境隐式转换」在 UI 自动化侧的形态:DPI 缩放悄悄改比例,面板开合 / 窗口状态悄悄改布局,坐标照样执行、只是执行在别的控件上
- [[长期更新展示站_两层结构与无头卡片量产_v1]] —— 该法用 Chrome 无头截图量产卡片,也踩到了中文文件名编码 / MSYS 路径映射这类「环境隐式转换」坑
- [[Mac素材包到Windows的两个坑_zip文件名编码与HEVC解码_v1]] —— 同一 UTF-8 vs GBK 根因的接收侧形态:Mac zip 的文件名在 Windows 解压即乱码
- [[2026-07-14_vpn-guard从工具到宣传片_全链路复盘_v1]] —— 陷阱四(.ps1 需 BOM / Python 输出 ✓ 崩溃)来源;同链踩到 tzutil 切时区后同进程 `[TimeZoneInfo]::Local` 缓存不刷新,须新起进程验证
- [[2026-08-02_LiveLink断线重连重做与视觉系统_迭代复盘_v1]] —— 陷阱三的第三、四次验证来源:DPI-unaware 截图误判成布局 bug 并写进已发布 release notes;CDP `contentSize` 按 DPI 报物理像素
- [[开工前先对基线律_v1]] —— 陷阱六的同源镜像:「搜不到≠不存在」在 Git Bash 路径转换这一层也会发生(Bash 自己 `ls` 能看见 ≠ Node 能解析路径)
