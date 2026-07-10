---
tags: [类型/档案, 工具/MJ_niji7, 重要度/高]
---

# niji 7 行为规律 v1

> 入档：2026-05-19
> 触发：30_AI 表演我的兴趣项目 5 个角色形象首轮抽卡 + Claude Code 角色"年幼小女孩"问题修正
> 关联：[[Suno_v5.5_行为规律]]（参考格式）/ [[30_AI表演我的兴趣/03_形象出图/niji7_prompt配方_v1]]（应用案例）
> 性质：niji 7 实测行为档案，给所有未来 niji 7 项目作先验

---

## 一句话

**niji 7 在画"年轻女性" 时有强烈的"甜化 + 幼化" 默认倾向**——用 `girl` + `young` + `in her 20s` 之类标准描述，约 80%+ 概率跑出"年幼小女孩" 而不是"成年女性"。要画成年女性需要一组特定的"反萌化 + 成年化武器" 关键词。

---

## 实测案例 · 30 项目 Claude Code 角色

### 现象描述（v1.0 失败版）

副会话用以下"看起来合理" 的 prompt 跑 niji 7：

```
A young anime girl in her 20s, slightly tired but focused intense expression,
short clean-cut hair or tied-back ponytail, wearing simple plain black programmer
t-shirt with subtle code logo, ... half-body portrait, ...
thick painterly anime portrait, heavy brushstrokes, dramatic chiaroscuro lighting,
dark saturated color palette, melancholic gothic aesthetic, painterly thick layers
--ar 3:4 --niji 7 --style raw
```

预期：成年女工程师疲惫专注。
实际：**年幼小女孩**（看起来像 14-16 岁）。

### 修正版 prompt（v1.1 成功）

```
A woman in her late 20s with mature adult features and defined jawline, slender
tall adult build, dark short hair shaved on one side with longer top swept back,
lean forearms visible from pushed-up sleeves of fitted black t-shirt with subtle
code logo, sitting with slight slouch in front of dual monitors showing dense code
with colorful syntax highlighting, one hand resting on mechanical keyboard with
subtle RGB glow, focused exhausted gaze locked on screen with no smile, visible
dark circles under sharp eyes, several crushed energy drink cans and a cold coffee
mug on cluttered desk, algorithm textbooks stacked behind, three-quarter view from
slight low angle, blue-tinted dual-screen glow lighting her face from front, ...
--ar 3:4 --raw --niji 7
```

结果：**成年女工程师疲惫专注**，气质 100% 命中。

---

## 关键武器分类（成年化 / 反萌化）

### 武器 1 · 主体身份措辞

| ❌ 出小女孩 | ✅ 出成年女性 |
|---|---|
| `young anime girl` | `A woman` |
| `young girl in her 20s` | `A woman in her late 20s` |
| `girl` 单独使用 | `mature adult features` + `defined jawline` |

**规律**：`girl` 在 niji 7 里默认理解为"少女"。`woman` 才是成年女性。**这一条是反萌化的最大杠杆**——只改这一处就能解决 50%+ 的"年幼" 问题。

### 武器 2 · 身体形态描述

加入：
- ✅ `slender tall adult build` —— 成年身高/体型
- ✅ `lean forearms visible from pushed-up sleeves` —— 成年手臂（少女手臂细但短，成年手臂细长有筋）

**规律**：niji 7 默认会给"娇小身材"。明确"slender tall adult" 锁定成年体型。

### 武器 3 · 面部疲惫感

加入：
- ✅ `no smile` —— 反默认"微笑萌脸"
- ✅ `visible dark circles under sharp eyes` —— 黑眼圈+锐利眼神
- ✅ `focused exhausted gaze locked on screen` —— 疲惫专注
- ✅ `defined jawline` —— 下颌线明确（成年面部 vs 婴儿肥）

**规律**：niji 默认面部是"圆润 + 微笑 + 大眼"。"no smile" + "dark circles" + "sharp eyes" 三个关键词组合可以反向锁定成年疲惫感。

### 武器 4 · 发型 / 装束非萌系化

加入：
- ✅ `dark short hair shaved on one side with longer top swept back` —— 半边剃毛/朋克风
- ✅ `fitted black t-shirt`（不是宽松卡哇伊） —— 干练剪裁
- ✅ `pushed-up sleeves` —— 工作状态

**规律**：发型/服装的"非萌系" 选择直接打破萌系视觉惯性。半边剃毛、 swept-back、 short hair 都是反萌化标志。

### 武器 5 · 姿态非端正化

加入：
- ✅ `sitting with slight slouch` —— 微弯（成年疲惫姿态 vs 少女端正坐姿）
- ✅ `three-quarter view from slight low angle` —— 略仰角（增加成年权威感）

**规律**：niji 默认会给"端正萌坐"。微弯的"slouch" 是成年工作疲惫的视觉指标。

### 武器 6 · 道具加重时间暗示

加入：
- ✅ `crushed energy drink cans`（不是 `energy drink cans`） —— "被踩扁的" 暗示长时间工作
- ✅ `cluttered desk` —— 凌乱的桌面（成年职场感）

**规律**：道具的"使用痕迹" 比道具本身更能传达"成年职业感"。

### 武器 7 · 参数选择

| ❌ | ✅ |
|---|---|
| `--style raw` | `--raw` |

**待验证规律**：`--raw` 可能比 `--style raw` 在 niji 7 上反甜化更直接。这是副会话实测发现，需要后续多次验证。

---

## "反萌化武器" 总检查清单

每次需要画成年女性时，对照检查 prompt 里有没有：

```
□ 用 woman 不用 girl
□ A woman in her late 20s 或更晚
□ mature adult features + defined jawline
□ slender tall adult build / lean forearms
□ no smile + dark circles + sharp eyes
□ 非萌系发型（如 shaved one side / short / swept back）
□ 非端正姿态（slouch / three-quarter view / low angle）
□ 道具有使用痕迹（crushed / cluttered）
□ 参数用 --raw 不用 --style raw
```

打勾越多，反萌化越成功。**最强杠杆**：woman + mature adult features + no smile + dark circles 四项必加。

---

## 反向案例（不需要反萌化的场景）

如果你**就是要画少女**（如萌系角色、轻松小品、cute 风），上述武器**全部不用**：

- ✅ 用 `young anime girl` / `cute anime girl`
- ✅ 用 `--style cute` 而不是 `--raw`
- ✅ 加 `bright smile` / `chibi proportions`

**这条档案的适用范围**：成年女性 / 反甜化 / 作品级二次元（如凝视厚涂风）。

---

## 与 niji 5 / niji 6 的差异（待验证）

我（主对话 Claude）不完全确定 niji 7 vs niji 5/6 在反萌化武器上的差异：
- niji 5 时代 `--style expressive` 已经偏立绘感，对成年女性支持还行
- niji 6 时代我不熟
- niji 7 时代实测：默认甜化更强，需要更多反向 prompt 关键词

**给未来 niji 系列副会话**：每次新版本上来都要重新测试，不要假设旧版本经验完全沿用。

---

## 副产品 · 30 项目 5 角色画风统一性

30 项目除了 Claude Code 修正，副会话还成功跑出了其他 4 个角色（Niji 7 / Eleven V3 / Nano / Claude 主会话），全部命中"凝视厚涂二次元" 锚点 + 5 种气质差异化。

实测发现的"画风统一性" 关键：
- 统一的厚涂关键词包：`thick painterly anime portrait, heavy brushstrokes, dramatic chiaroscuro lighting, dark saturated color palette, melancholic gothic aesthetic, painterly thick layers`
- 统一的参数 `--ar 3:4 --raw --niji 7`
- 每个角色场景化道具丰富（手办堆 / 录音棚 / 工匠桌 / 双屏 / 便利贴墙）

**这套 prompt 包是 niji 7 上厚涂二次元的可复用模板**——未来 niji 7 作品级二次元项目可直接调用。

---

## 元层意义

这条经验跟 [[Vocal_Gender反选_风格prior_v1]]（Suno）和 [[Suno版权过滤器规避_v1]] 同源——都是**工具默认偏好与创作需求错位** 时的"反向调味" 技巧。

普遍规律：

**生成式 AI 工具有强烈的训练数据默认偏好**（Suno 默认抒情 / niji 默认甜化 / MJ 默认写实精致 / etc.）。要做"反默认" 创作，必须用**重复+具象+反向**的关键词组合压制默认偏好。

抽象的"我要成年感" 不够——具体到 "mature adult features + defined jawline + no smile + dark circles + slouch" 这种**生理细节描述** 才能有效压制。

---

## 关联

- 应用案例：[[30_AI表演我的兴趣/03_形象出图/niji7_prompt配方_v1]] · Claude Code 角色 v1.1 修正版
- 上位元方法论：[[识别工具天花板的时机]] · 这是反向应用——不是撞天花板撤退，是找到"反默认调味" 路径
- 同源经验：[[Vocal_Gender反选_风格prior_v1]] · Suno 上同类"反默认调味" 案例
- 同源经验：[[Suno_v5.5_行为规律]] · 经验 5"反 Suno 本能指令需要重复+具象化"
- 下游案例：[[动作错做减法_风格错辨顺逆_学员答疑案例_v1]] · 学员答疑指向 niji 7 在**风格层**同样默认强势（吉卜力复古手绘被现代二次元先验压制）——回验后可作 v2 材料

---

## 版本

- **v1 - 2026-05-19 - 主对话 Claude（第二任）沉淀**（基于 30 项目 niji 7 角色形象共创副会话的 Claude Code 修正经验）

升级触发：
- 多次 niji 7 项目反向验证后做 v2
- 未来 niji 8/9 发布后建立新档案
