---
tags: [类型/工作流方法论, 工具/音乐卡点, 工具/Whisper, 工具/MoviePy]
---

# AI 辅助音乐 MV 卡点 · LLM-plan 工作流 · v1

> 入档：2026-05-15
> 触发：《即时雨》MV 项目从 v1 到 v7 的工具迭代（约 3 小时算法天花板探索）
> 性质：工作流方法论 + 工具架构 + 协作模式
> 关联：[[Cowork协作的接口文件模式]] / 《即时雨》项目复盘空占位已清理
> 工具：`99_工具/mv_kadian_tool/`（已实现 v2）

---

## 一句话

**音乐 MV 卡点工作流的核心瓶颈不在算法、不在 Whisper 精度、不在 librosa 节拍检测，而在"shot 编号 ↔ 歌词意图"的语义映射——这一层只有 LLM 能做。LLM-plan 工作流让工具的价值从"自动算法"转移到"读 plan JSON + 渲染"。**

---

## 二、背景：纯算法卡点为什么有天花板

### 2.1 中文 MV 卡点要解决的三层问题

| 层 | 解决什么 | 已知工具 | 能力 |
|---|---|---|---|
| **时序层** | 每句歌词在音频里什么时间出现 | Whisper（faster-whisper）| 中文字准 95%（medium 模型）|
| **特征层** | 音乐节拍 / onset / segmentation / RMS | librosa | 拍点检测 ~80% 准 |
| **语义层** | **哪张图配哪句歌词** | ？？？ | **算法无解** |

前两层算法可以做得很好。瓶颈是第三层——**纯语义判断**。

### 2.2 算法天花板实测（《即时雨》项目）

工具迭代历程：

| 版本 | 策略 | LYRIC 锚点命中 | 题眼准确度 |
|---|---|---|---|
| v1 | base 模型 + librosa 9 段强制对齐 | ~7/14 | 题眼错位 |
| v2-v4 | medium 模型 + storyboard 时间区间 | ~9/15 | 题眼错位 |
| v5-v6 | medium + whisper raw segment + ±2.5s snap | **11/15（触顶）** | **题眼仍错位** |

**关键诊断**：S05"饭碗筷子"应该对应"终于吃上公粮了"（56.42s C1 首句），但算法只知道"56.42s 有一句歌词"，不知道哪张图配哪句意图。

工具不"懂"分镜大纲（"S05 是题眼，对应饭碗 + 公粮"），不"懂"歌词的结构（"56.42s 是 C1 首句，整个 chorus 的情绪点在这"）。

**算法解决了"时间对齐"，没解决"语义匹配"。**

### 2.3 关键 quote

跳蛛先生在工具迭代到 v6 后，否决 interactive 模式：

> "如果用 interactive 的话我们的工作就是无效的，因为这与我去剪映等软件直接剪辑无二。"

—— 这是工作流认知转折点。继续在算法层迭代 = 看起来勤奋实际无效。

---

## 三、LLM-plan 工作流（终版）

### 3.1 三步架构

```
[第一步：工具跑 Whisper 转录]
  ↓
  工具 --mode auto --model-path <medium 本地路径>
  目的：生成 transcript JSON（每句歌词的精确时间戳）
  耗时：CPU medium ~3-5 分钟

[第二步：LLM 出 plan JSON]
  ↓
  Claude（任意会话）读取三份文件：
    - 分镜大纲（理解每张图的"段落标签 + 视觉意图"）
    - 歌词原文（识别 Verse / Chorus / Bridge / Outro 段落结构）
    - transcript JSON（拿每句歌词的精确秒级时间戳）
  输出：plan JSON [{shot, start, end, note}, ...]
  关键能力：处理复用段（同 shot 在 Chorus 多次重现）
  耗时：10-20 分钟（LLM 协作）

[第三步：工具按 plan 渲染]
  ↓
  工具 --plan path.json
  完全跳过算法，按 plan 一次性渲染
  耗时：~20 秒（540p 粗剪）/ ~30 分钟（1080p final 含特效）
```

### 3.2 工具的价值转移

| 旧工具价值 | 新工具价值 |
|---|---|
| 自动算法卡点 | **读 plan JSON + 渲染** |
| Whisper / librosa / shot_aligner 算法层 | Whisper 转录 + MoviePy 渲染（**管道工作**）|

工具仍然有价值，但**核心从"自动算法"转到"工程管道"**——
- Whisper 转录（含本地模型加载）
- plan JSON 解析 + 1:N 复用段处理
- MoviePy 渲染（字幕烧录 / Ken Burns / 暗角颗粒）
- UTF-8 编码处理（Windows）
- audio_codec 坑（Windows 权限）

这些不是"算法"，是工程基础设施。但**不可省**——没有这些工具底层，LLM 出的 plan JSON 落不了地。

### 3.3 plan JSON 数据结构

**v1 版（最简）**：

```json
[
  {"shot": 0, "start": 0.00, "end": 15.10, "note": "前奏"},
  {"shot": 1, "start": 15.10, "end": 28.38, "note": "V1 上半"},
  ...
  {"shot": 5, "start": 56.42, "end": 63.84, "note": "C1 首句 ★ 题眼"},
  {"shot": 5, "start": 126.86, "end": 135.00, "note": "[C2 复用] 题眼"},
  ...
]
```

**v2 版（含字幕 + 特效）**：

```json
{
  "clips": [
    {"shot": 5, "start": 56.42, "end": 63.84, "note": "C1 首句"}
  ],
  "subtitles": [
    {"text": "终于吃上公粮了", "start": 56.42, "end": 60.10, "emphasis": true}
  ],
  "effects": {
    "global": {
      "vignette": {"enabled": true, "intensity": 0.15},
      "paper_tint": {"enabled": true, "color": [248, 245, 238], "alpha": 0.06}
    },
    "per_shot": {
      "S05": {"ken_burns": {"type": "zoom_in", "amount": 0.030}}
    },
    "transitions": {"default": "crossfade", "duration": 0.4}
  }
}
```

`emphasis: true` 给副歌字幕加重（字号 +20% + 字色加深 + Weight Regular）。
`per_shot.ken_burns` 给每镜单独的 Ken Burns 微动（zoom_in / zoom_out / pan_x / pan_y）。

---

## 四、工作流的关键能力

### 4.1 1:N shot 复用（Chorus 多次重现）

中文 MV 常见结构：Verse → PreChorus → Chorus → Verse → PreChorus → Chorus → Bridge → Final Chorus。

Chorus 多次重现时，**同一个 shot 编号可以在 plan JSON 里出现多次**：

```json
{"shot": 5, "start": 56.42, "end": 63.84, "note": "C1 首句"},
{"shot": 5, "start": 126.86, "end": 135.00, "note": "[C2 复用]"},
{"shot": 5, "start": 179.76, "end": 187.14, "note": "[FC 复用]"}
```

工具按 plan 渲染时，自动从同一 shot 目录读图，渲染到对应时间段。**14 张图 + 21 个 clip = 自然实现 1:N 复用**。

### 4.2 plan JSON 是新的产物形态

`plan JSON 不是中间态，是最终交付物之一`。

跳蛛先生未来：
- 可以反复用同一份 plan JSON 改图重渲（视觉迭代）
- 可以微调字幕时间 / Ken Burns 类型 / 特效强度（不影响卡点）
- 可以把这份 plan 作为"分镜系列"的复用模板（下一首 MV 借用结构）

**plan JSON = 项目的可执行规格说明**。

### 4.3 LLM 读三份文件的工作

LLM 在第二步要做的核心判断：

| 输入 | LLM 读出什么 |
|---|---|
| 分镜大纲 | "S05 是题眼镜，对应 C1 首句的'终于吃上公粮了'" |
| 歌词原文 | "C1 首句在 [Chorus] 标签下第一行" |
| transcript JSON | "'终于吃上公粮了' 在 56.42s 出现" |
| **三个交叉** | **shot 5 的 start = 56.42** |

这是**纯语义任务**——任何能读懂中文 + 理解音乐结构的 LLM 都能做。不需要 fine-tune，不需要专门训练。

---

## 五、应用边界

### 5.1 适用场景

- ✅ **中文 MV 卡点**（含歌词的视频，14-20 镜）
- ✅ **视频字幕段落分段**（基于歌词或台词的镜头切换）
- ✅ **任何"语义映射 + 时间轴排版"任务**（如 PPT 自动配音 / 朗诵视频）

### 5.2 不适用场景

- ❌ **纯音乐 MV（无歌词）**——LLM 没法读出"哪一拍配哪个镜头"，回到 librosa beat detection
- ❌ **超长视频（>5 分钟）**——LLM 出 plan 的 token 量级会过大，不稳定
- ❌ **极复杂分镜（>50 shot）**——LLM 出错率上升，需要分段做 plan

### 5.3 关键判断

**判断你是否需要 LLM-plan 工作流**：

```
□ 是中文（或其他自然语言）有歌词/台词的视频？
□ 需要 shot 和歌词意图的精确匹配？（不是"任意配图"）
□ 有现成的"分镜大纲 + 歌词文本"作为人类语义输入？

三个都是 → 用 LLM-plan 工作流
任一不是 → 评估其他工具
```

---

## 六、不要做的（已验证失败）

### 6.1 不要用 interactive 模式

工具的 interactive 模式（人类手动调整每个 clip 时间）= 等于剪映手动剪。

`已验证不实用`。原因：
- 不可复用（每次都重做）
- 不可版本控制（没有 plan JSON 作为锚点）
- 跳蛛先生原话："这与我去剪映等软件直接剪辑无二"

工具应该保留 interactive 模式作为应急 fallback，但**不推荐为主工作流**。

### 6.2 不要靠 storyboard 软锚点

工具支持 `--storyboard path.md` 用分镜表估算时间区间。

`已验证效果差`。原因：
- 分镜大纲的"估算时间"和实际歌词时间戳偏差 ±5-10s
- 算法对软锚点的吸附逻辑不够智能，仍会把 S01 放到 0s（前奏没歌词）

软锚点 = 纸上谈兵。**LLM-plan 才是硬锚点**（每个 clip 都有 LLM 校准过的精确时间）。

### 6.3 不要依赖 base 模型

faster-whisper base 模型字准 ~65%，medium 模型 ~95%。

`base 模型不可用`。原因：
- 65% 字准在 LLM 读 transcript 时会引入大量歧义
- "终于吃上公粮了" 可能被识别成 "种鱼吃上工量了"——LLM 没法识别意图
- 必须用 **medium**（CPU 5 分钟可跑）

---

## 七、和现有 AI 视频卡点教程的差别

主流教程会教你：
- "用 Whisper 自动转录，再用算法对齐时间"
- "用 librosa 检测节拍，让画面切换跟着节拍走"
- "调整 sensitivity 让算法更准"

这些教程**停留在算法层**，没意识到瓶颈在语义层。

而**LLM-plan 工作流**的核心洞察：
- 算法解决前两层（时序 + 特征）
- 语义层让 LLM 做（中文 MV 唯一可行解）
- 工具退到工程管道，做好"读 plan JSON + 渲染"即可

---

## 八、工具状态（《即时雨》项目最终版）

工具路径：`{AIGC工作站}/99_工具\mv_kadian_tool\`

### 8.1 关键参数

```
--plan path.json           完整 clip 时间表，跳过所有算法，支持 1:N 复用
--model-path path/         本地下载的 whisper 模型（避免 HF 下载问题）
--transcript path.json     复用上次的 transcript（跳过 Whisper 节省 ~3 分钟）
--storyboard path.md       分镜表软锚点（保留但效果差，不推荐）
--mode auto / interactive  interactive 不推荐
--aspect 9:16 / 16:9 / 1:1 / 4:5
--resolution 540 / 1080
--fps 12 / 24
```

### 8.2 推荐工作流命令

```powershell
$tool = "{AIGC工作站}/99_工具\mv_kadian_tool"
$env:PYTHONIOENCODING = "utf-8"

# 第一步：跑 medium 转录（只为生成 transcript）
& "$tool\.venv\Scripts\python.exe" "$tool\mv_kadian_tool.py" `
  --audio "音频.wav" --images "图片目录\" `
  --model-path "$tool\models\medium" `
  --mode auto `
  --output "临时.mp4"
# 关心的产出：临时_whisper转录.json

# 第二步：LLM 出 plan JSON（人类 + Claude 协作，10-20 分钟）

# 第三步：渲染 final（含字幕 + 特效）
& "$tool\.venv\Scripts\python.exe" "$tool\mv_kadian_tool.py" `
  --audio "音频.wav" --images "图片目录\" `
  --plan "02_分镜\卡点方案_v2_full.json" `
  --transcript "临时_whisper转录.json" `
  --aspect 9:16 --resolution 1080 --fps 24 --mode auto `
  --output "07_输出\final.mp4"
```

---

## 九、协作模式

LLM-plan 工作流是**三方协作**：

| 角色 | 职责 |
|---|---|
| **跳蛛先生（人类）** | 提供分镜大纲 + 歌词原文 + 跑命令 + 审美阈值守门 |
| **Claude（运营经理 / 任意会话）** | 读三份文件 → 出 plan JSON → 解释决策点 |
| **工具（mv_kadian_tool）** | Whisper 转录 + 按 plan JSON 渲染 |

### 9.1 接口文件

- **input**：分镜大纲 .md + 歌词 .md + transcript .json
- **output**：plan JSON

接口文件清晰 = 协作低成本。任何 Claude 会话拿到这三份文件都能出 plan，不依赖某次对话的上下文。

### 9.2 给"运营经理"角色的 prompt 提示词框架

```
读取：
  - 分镜大纲：理解每个 Sxx 的"段落标签"和"视觉意图"
  - 歌词原文：识别 [Verse]/[Chorus]/[Bridge]/[Outro] 段落顺序
  - whisper SRT/JSON：拿到每行歌词的精确秒级时间戳

输出：plan JSON
  [{shot: int, start: float, end: float, note: str}, ...]

复用规则：
  - Chorus 复用（出现多次）：把 Chorus 1 的 shots 在 Chorus 2/Final Chorus 处再列一次
  - 前奏/间奏：如果有 S00 / S15 / 其他过渡图就用，没有就让首镜延伸到首句歌词

输出后跳蛛先生审一遍，确认大方向对再交工具渲染。
```

---

## 十、元学习 · 这条方法论的来源

这条工作流不是先有理论再实践——是 v1-v6 算法迭代 3 小时后被实战逼出来的。

**关键失败 → 关键洞察 的转折点**：
- v5-v6 LYRIC 命中 11/15 后无法再提升
- 跳蛛先生否决 interactive：识别 "算法天花板已到"
- 跳蛛先生说"这与我去剪映直接剪无二"：识别**工具内部努力 = 看起来勤奋实际无效**
- 转 LLM 协作：30 秒内出精确 plan（vs 3 小时算法迭代仍触顶）

**这是 AI 协作中最有价值的元能力之一**：识别工具天花板的时机。

同期《即时雨》项目复盘空占位已清理;相关结论已沉淀在本文 §二·修正 1。

---

## 十一、版本

- **v1 - 2026-05-15 - 主对话 Claude 沉淀**（基于《即时雨》MV 项目实战）

继承链：
- 实战案例：《即时雨》MV 项目（21_即时雨/）
- 工具实现：`99_工具/mv_kadian_tool/`
- 项目复盘：原空占位已清理;核心内容已沉淀在本文
- Code 端交付：`跨会话协作/音乐卡点剪辑工具_收口简报_v2.md`

---

> 落款：
> 这条方法论的真正价值不在"音乐 MV 卡点"这个具体应用——
> 而在揭示了一个普遍规律：**AI 协作中，当工具的"自动算法"在某一层触顶时，让 LLM 接管该层的语义判断，工具退到工程管道，往往是唯一可行的解**。
>
> 跳蛛先生 5/15 这天，两个项目（音乐卡点 + niji 5 形象图）同时撞到同一种元层失败——继续在工具内努力不如换工具/换协作分层。
> 把"识别工具天花板的时机"作为元能力沉淀，价值会跨越远比单个项目大得多。
