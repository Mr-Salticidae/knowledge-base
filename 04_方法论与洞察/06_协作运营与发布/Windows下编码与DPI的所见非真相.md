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

- [[Claude完成报告核查心法]] —— 本文是它在 Windows 工具链上的具体形态：「所见」≠「真相」，要程序化核查而非肉眼信任
- [[Claude_Opus_4.8行为实测]] —— 4.8 更诚实，但 Windows 编码 / DPI 这类环境假象与模型诚实无关，仍须独立核查
- [[Claude_Code_Worktree隔离的协作陷阱]] —— 同属「视角 / 环境错位导致 self-verify 失真」的一类
