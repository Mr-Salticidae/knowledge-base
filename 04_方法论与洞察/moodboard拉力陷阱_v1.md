---
tags: [类型/方法论, 工具/MJ, 状态/已验证]
---
# moodboard 拉力陷阱 · v1

> 入档:2026-05-19
> 触发:23 项目《再少年》5/17 晚 MJ「女鬼事件」
> 性质:**moodboard 拉的不只是色调,还会拉走画面内容/姿态/情绪——这是 MJ 用户最容易踩的坑**
> 关联:[[personalize与moodboard分工]] / [[sref纯净性原则]] / [[双工具分工_nano锁脸+MJ摄影质感]]

---

## 一句话总结

**MJ 的 moodboard 不是"颜色滤镜",是"视觉语义场"——它会同时拉走色调 + 构图 + 主体姿态 + 氛围联想**。用 moodboard 救色调时,主体可能被"拉到"奇怪的方向(如女鬼/恐怖/猎奇)。

---

## 现象描述 · 女鬼事件

5/17 晚 23 项目跑 MJ:
- 目标:出 S05(主角念名特写)的氛围版本,锁色调到清冷古风
- 用了 5 张「清冷古风 moodboard」(全是人像 + 雾感 + 苍白肤色)
- prompt:`young woman in pale hanfu, blurred face, looking down, raining, cinematic still`

**输出结果**:
- ✗ 苍白脸+模糊+雨+古风 → 触发 MJ 内部「东方恐怖片」语义关联
- ✗ 输出图主角看起来像「女鬼」(贞子/聊斋式联想)
- ✗ 跳蛛先生原话:「这太恐怖了,不行」

**根因**:moodboard 5 张人像里有 2 张本身就有「神秘/苍白/哀伤」的氛围,加上 prompt 里的 `blurred face + pale hanfu`,**两个语义信号叠加,把 MJ 推到了"恐怖"分支**。

---

## moodboard 拉力的本质

### 它不只拉色调

| 维度 | 你以为 moodboard 拉 | 实际 moodboard 还拉 |
|---|---|---|
| 颜色 | ✅ 主色调 | ✅ 是 |
| 光影 | ✅ 是 | ✅ 是 |
| 构图 | ⚠️ 部分 | ✅✅ 也拉(画面密度、留白比例)|
| 主体姿态 | ❌ 没想到 | ✅✅ **拉**(站姿/坐姿/视线)|
| 主体特征 | ❌ 没想到 | ✅✅ **拉**(年龄/性别/服装)|
| 氛围联想 | ❌ 没想到 | ✅✅✅ **强拉**(神秘/恐怖/欢快/孤独)|

→ **5 张 moodboard 提供的"语义信号"远远不止颜色**。

### 为什么 MJ 这样设计

MJ 的 moodboard 是「reference image」的扩展——MJ 用 CLIP-like embedding 编码每张 moodboard,**embedding 里包含了图片的所有语义维度**,不只是颜色。
这是「设计选择」,不是 bug——MJ 团队认为 moodboard 提供更全面的视觉锚定。
对**色调统一**用户来说,这就是坑。

---

## 救场方案

### 方案 A · moodboard 内部去人像化

只用「无人像的纯环境图」做 moodboard——雨景/光影/材质/留白。
**避免任何"人/脸/眼神"参与进 moodboard**。

| 反例 | 正例 |
|---|---|
| 5 张人像古风图 | 5 张古风环境(雨檐/纸窗/水墨/光斑/古木)|
| 主体清晰的肖像 | 主体被裁掉的环境近景 |

### 方案 B · prompt 里去除"语义雷区词"

| 雷区词 | 触发的联想 |
|---|---|
| `pale + blurred + young woman` | 东方恐怖片 |
| `dark forest + child` | 童话恐怖/失踪 |
| `red liquid + close-up` | 血/暴力 |
| `mask + crowd + night` | 邪教/恐怖事件 |

**操作规则**:写 prompt 后,**反向检查每个形容词的"最坏联想"**——如果联想能跳到恐怖/猎奇/敏感分支,换词。

### 方案 C · 完全切换工具

像 23 项目最终决策——**所有需要主角脸的镜头切到 nano**,MJ 只跑环境/物件镜。
这是双工具分工的最稳健解。

详见 [[双工具分工_nano锁脸+MJ摄影质感]]。

---

## 反向陷阱

### ❌ 陷阱 1 · 「moodboard 多放几张稀释拉力」

直觉:moodboard 5 张人像 → 加到 10 张 → 拉力被稀释?
**错**——MJ 的 moodboard embedding 是**加权平均**,加更多类似图反而**强化**了那个语义场。
正确做法:**换不同类型的图**,不是加更多同类图。

### ❌ 陷阱 2 · 「加 sref 抵消 moodboard」

试图用 `--sref` 去抵消 moodboard 的内容拉力——会导致 sref 编号被污染。
详见 [[sref编号独立律]]——sref 是用于「风格固化」的,不该和 moodboard 内容博弈。

### ❌ 陷阱 3 · 「降低 stylize 让 MJ 不自由发挥」

`--stylize 50` 让 MJ 更听 prompt,但**也让 moodboard 拉力变得更"机械"**——结果是色调对了,但画面变得僵硬。
**stylize 不能消除 moodboard 拉力**,只能调节 MJ 的"自由度"。

---

## 与 [[personalize与moodboard分工]] 的协同

[[personalize与moodboard分工]] 讲的是「**何时用 personalize / 何时用 moodboard**」。
本条讲的是「**当你用 moodboard 时,要警惕它的隐性拉力**」。

两条是同一套 MJ 控制系统的两个面:
- 选哪个工具(personalize vs moodboard)→ 那篇
- 选定 moodboard 后避雷 → 这篇

---

## 元层洞察

**这条陷阱揭示的更深规律**:

> AI 视觉工具的「reference」类参数(moodboard/sref/personalize/cref)**没有一个是"单一维度"的**——它们都是「语义场拉力」,会同时拉多个维度。
> 用户的直觉模型是「我只想拉 X 维度」,实际是「拉了 X 也拉了 Y/Z/W」。

→ **任何 reference 类参数都要做"反向预演"**:这张参考图除了我想要的之外,还会带来什么?

---

## 跨场景适用性

### 已验证适用
- ✅ MJ moodboard
- ✅ 类 MJ 的 reference image 系统

### 推测适用
- 🔄 MJ sref / cref / oref(同源机制)
- 🔄 SD 的 IPAdapter / ControlNet reference
- 🔄 任何「图作为 prompt」的系统

### 验证待补
- 🔄 nano 的参考图机制是否有类似拉力(初步看是有的,但弱很多)

---

## 关联文档

- 配套陷阱:[[sref编号独立律]] / [[sref纯净性原则]]
- 工具选择:[[personalize与moodboard分工]] / [[双工具分工_nano锁脸+MJ摄影质感]]
- 项目复盘:[[2026-05-18_23项目再少年MV完整复盘]]
- 元方法论:[[识别工具天花板的时机]]

---

## 版本

- **v1 - 2026-05-19 - 23 项目女鬼事件首次沉淀**

升级触发:
- 在第二个 MJ 项目验证「moodboard 去人像化」的命中率
- 整理 MJ 雷区词清单(语义触发器列表)
- 找到反向利用 moodboard 拉力的方法(比如**故意**想要某种联想时,用同维度 moodboard 强化它)
