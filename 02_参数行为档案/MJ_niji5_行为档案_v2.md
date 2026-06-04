---
tags: [类型/档案, 模型/niji5]
---

# MJ niji 5 · 行为档案 · v2

> 入档：2026-05-15（v1）/ 升级 v2：2026-05-20
> 触发 v1：Prompt Battle 比赛冠军形象图项目，副会话 13 轮实测后沉淀
> 触发 v2：副会话 #4 涂图儿+良伞会话验证悠船 niji 5 与 MJ 官方 niji 5 的实测差异 + Nano 同样吃极简 prompt
> 实测对象：冠军 #1（v1）+ 冠军 #4 涂图儿（兽人）+ 冠军 #5 良伞（人形山海经神祇）
> 关联：[[方法论笔记_AI形象图工作流分层_niji5+Nano]] / [[MJ_v8.1_无oref_混合工作流]] / [[../../复盘记录/复盘笔记_涂图儿良伞_悠船niji5_Nano极简_2026-05-20]]

---

## 一句话

**niji 5 是有"两个分支"的模型——3D CGI 渲染分支 和 二次元立绘分支。哪个分支被触发取决于 prompt 里有没有特定"触发词"。理解这两个分支的边界 + 6 条已知坑，决定你能不能稳定出图。**

---

## 一、双分支结构（最核心）

niji 5 默认不是稳定的"动漫风"，而是会在以下两个分支间漂移：

### 分支 A · 3D CGI 渲染（推荐路径）

**视觉特征**：3D 高级渲染感、PBR 材质、SSS 皮肤、金属高光、布料褶皱、电影级光影
**适合**：游戏角色立绘、虚拟偶像、潮流人物形象、高质量插画

**稳定触发条件**：
- ✅ 镜头描述：`half body shot` / `three quarter body shot`（**半身或 3/4 身**，全身不稳定）
- ✅ 视角锚定：`frontal view, symmetric`
- ✅ 摄影锚定：`Panoramic lens, Long shot`
- ✅ 渲染词堆叠（完整版必带）：`C4D, blender, unreal engine, octane render, global illumination, ray traced reflections, SSAO, shaders, FXAA, CGI, RTX, VFX, 4K`
- ✅ 质量词：`best quality, ultra detailed, hyperrealistic`

### 分支 B · 二次元立绘（默认 / 不推荐）

**视觉特征**：动漫角色立绘、平涂、卡通比例、二次元线条
**适合**：纯萌系 / Chibi / 表情包

**误触发关键词**（**会切到立绘分支**）：
- ❌ `floating` / `soaring` / `mid-air` / `no ground` / `bare feet` / `leaping`
- ❌ 任何"飞升 / 漂浮 / 不踩地"语义
- ❌ 删除上述"摄影锚定词"（`frontal view, symmetric`）

### 实战教训

**项目里要 3D CGI 风**，但加 `floating` 制造漂浮感 → 100% 切到二次元立绘分支。
**正确做法**：3D 分支稳定渲染 + 漂浮感**留给后期工具（Nano）做**。

---

## 二、6 条已知坑

### 坑 1 · 否定语义失效

niji 5 对 `no X` 类否定描述**近乎无效**：
- `no ground` → MJ 仍会画地面
- `no shadow` → 仍会画阴影
- `feet not touching ground` → 双脚仍然落地

**这不是 niji 5 独有的问题**（MJ 系列普遍弱），但 niji 5 上特别严重。

**结论**：想要"不踩地" / "无地面" / "无阴影"——**靠 prompt 无解，必须靠后期工具**。

### 坑 2 · 描述层过载（注意力争夺）

niji 5 prompt 描述层 **> 10 个特征词**时：
- 模型注意力被吃满
- **颜值 / 解剖细节会被牺牲**
- 例：在已有人物描述基础上加 `sharp piercing gaze + looking at camera + intense + eyes open + sharp eyes` 5 个眼神词 → 4 张图全部丢失麦克风（虽然 prompt 里写了 holding microphone）

**原则**：每加一个新约束，**就要删一个旧约束**。不能堆叠。

### 坑 3 · `red accent` 的"贪婪解读"

写 `red accent` 时 niji 5 **强制把红色落到鞋上**（100% 撞同一陷阱）。

**解决**：
- ✅ `red highlights in hair only` —— 锁定红色位置
- ✅ 完全删除"red"描述 —— 让头发自然挑染
- ❌ `red accent` / `red detail` / `red color pop` —— 都会落鞋

**推广**：任何颜色 accent 必须**明确指定位置**，否则 niji 5 会贪婪解读到一个奇怪的位置。

### 坑 4 · 单数 vs 复数手部描述

**侧脸视角下**：
- ❌ `hands by sides`（复数）—— niji 5 强行画两只手 → 解剖崩坏概率 100%
- ✅ `one hand visible in pocket`（单数 + 明确位置）—— 解剖正确率显著提高

**结论**：侧脸视角下，**所有手部描述必须用单数 + 明确位置**。

### 坑 5 · 半身→全身扩图的物理限制

半身像扩图到全身：
- **补全区域必须 ≥ 原图区域**（腿+脚占人体一半）
- 这违反 MJ 扩图"补全 ≤ 原图"的安全区原则 → 必然激进扩图

**解决**：**两次扩图**
1. 半身 → 3/4 身（Aspect 2:3 / Scale 65% / 原图垂直顶部留 3%）
2. 3/4 身 → 全身（Aspect 2:3 / Scale 70-72%）

但每次扩图都有：
- 画质衰减
- 风格漂移 1 次（增加触发到立绘分支的概率）

**这条坑是 "niji 5 全身像下脸糊" 的根因**——脸在画面占比 < 5% 时分辨率不够，**全身像下五官精致几乎不可避免**。

### 坑 6 · 颜值锚定的尺度依赖

- 半身像下：加 `beautiful + sharp jawline + delicate features` 颜值显著提升 ✓
- 全身像下：颜值锚定**几乎无效**（脸占比太小）

**结论**：冠军形象图 / 高颜值需求项目，**必须走"半身先渲染颜值 → 扩图保留颜值"工作流**，**不能直接出全身**。

---

## 三、稳定输出 prompt 配方（实测可用）

### 3.1 半身像基底配方（3D CGI 风格）

```
3D high fashion illustration by nick knight and rick owens,
Panoramic lens, Long shot, half body shot,
a beautiful young Asian woman with sharp jawline, side profile view,
[人物特征：长发/服装/配色],
[场景：black background / 简单背景],
frontal view, symmetric,
C4D, blender, unreal engine, octane render, global illumination,
ray traced reflections, SSAO, shaders, FXAA, CGI, RTX, VFX, 4K,
best quality, ultra detailed, hyperrealistic
--fast --style expressive --niji 5
```

**Aspect 默认 1:1**（不指定 `--ar`）。

### 3.2 第一次扩图（半身→3/4 身）

**网页端参数**：Aspect Ratio 2:3 / Scale 65% / 原图垂直顶部留 3%

```
3D high fashion illustration by nick knight and rick owens,
Panoramic lens, Long shot, three quarter body shot,
a beautiful young Asian woman with sharp jawline, side profile view,
[人物特征同上],
one leg stepping forward as if walking,
one hand visible in pocket,
black background, no ground, no shadow,
[渲染词堆叠 + 质量词 同上]
--fast --style expressive --niji 5
```

注意：
- `one leg stepping forward` → 制造动势（不要用 floating）
- `one hand visible in pocket` → 单数手部描述，避免解剖错误

### 3.3 第二次扩图（3/4 身→全身）

**网页端参数**：Aspect 2:3 / Scale 70-72%

```
3D high fashion illustration by nick knight and rick owens,
Panoramic lens, Long shot, full body shot,
[人物特征同上],
walking forward dynamically, [鞋款描述如 black combat boots],
black background, no ground, no shadow,
[渲染词堆叠 + 质量词 同上]
--fast --style expressive --niji 5
```

---

## 四、style 子模式（默认 expressive）

niji 5 的四个 style 子模式：

| 子模式 | 视觉特征 | 适用 |
|---|---|---|
| `--style original`（默认） | niji 5 原生风格 | 平衡稳，不知道选啥就先用这个 |
| `--style cute` | Chibi / 可爱 / Q 版 | 表情包 / 二次元卡通 |
| **`--style expressive`** | **大眼睛 / 现代日漫 / 立绘感** | **首选：个人形象图、海报、立绘** |
| `--style scenic` | 场景丰富 / 电影感 / 偏后景 | 全身 + 环境图 |

**实战推荐：`--style expressive`** —— 立绘感最强，最适合人物形象图。

---

## 五、niji 5 vs niji 6 的取舍

- **niji 5**（2023-12）：原汁原味日漫感、绘画感强、不太"AI"
- **niji 6**（2024-01）：更细腻但偏现代，少了"手绘"质感

跳蛛先生在 Prompt Battle 项目里**选 niji 5 而不是 niji 6** —— 因为想要"手绘 / 角色绘"质感。

如果项目需要"更现代 / 更细腻"的二次元感 → 切 niji 6 测试。

---

## 六、配套工作流（关键）

niji 5 **不是孤立工具**。它的物理上限决定了必须分层使用：

```
Layer 1: niji 5  → 主体出图（画风、服装、构图、颜值）
Layer 2: Nano    → 后期精修（加道具、改局部、制造漂浮感、调动势）
Layer 3: PS（可选）→ 微调（局部颜色、印刷分辨率）
```

niji 5 物理上做不到的事（必须后期）：
- 漂浮 / 不踩地 / 无阴影
- 特定道具（麦克风 / 剑 / 卡牌等的精确位置）
- 鞋款细节（战术靴 → 骑士靴等替换）
- 头发动势加强 / 红色挑染比例调整

详见配套方法论 [[方法论笔记_AI形象图工作流分层_niji5+Nano]]。

---

## 七、什么时候不要用 niji 5

| 场景 | 替代方案 |
|---|---|
| 需要写实风（非二次元） | MJ v7 / v8.1 |
| 需要 cref / oref 锁脸 | MJ v7 + oref（niji 5 时期 cref 较弱） |
| 多人构图（>2 人） | 单独跑每人再合成（niji 5 多人必翻车） |
| 写实手部细节 | 任何工具都不擅长，但 niji 5 是手部软肋之一 |
| 复杂服装图案 / 文字 logo | niji 6 比 niji 5 处理更好 |

---

## 八、风格 DNA 反推的常见错误（元教训）

副会话在做这次项目时，最初基于 10 张往期作品反推风格 DNA，犯了 2 处误判，被跳蛛先生纠正：

1. **"几乎不直视镜头"** ❌ → 实际有部分直视，只是侧脸占比偏多
2. **"全部漂浮 / 不踩地"** ❌ → 实际"漂浮"是少数派（~30%），站立/行走/裙摆吞脚才是主流

**元教训**：
- **基于第一次提取的特征直接推进，容易把"少数派特征"过度泛化**
- 必须和用户**多轮确认** style DNA，不能一次反推就上手做
- "不踩地"的本质是 **不画地面/阴影/重心明显**，不是必须真腾空——本质 ≠ 表象

详见 [[方法论笔记_AI形象图工作流分层_niji5+Nano]] §五·风格 DNA 反推陷阱。

---

## 九、信息密度速查表

如果你只看一节，看这个：

| 维度 | 关键规律 |
|---|---|
| **画风触发** | 3D 渲染词堆叠 + 摄影锚定 + 半身/3-4 身 → 3D 分支；任何"漂浮"语义 → 立绘分支 |
| **否定语义** | `no X` 失效，**用后期工具替代** |
| **描述层** | > 10 词过载，颜值/解剖被牺牲。**加一删一** |
| **颜色** | `red accent` 落鞋；必须 **明确位置**（如 `red in hair only`） |
| **手部** | 侧脸视角必须**单数 + 明确位置**（如 `one hand in pocket`）|
| **扩图** | 半身→全身**两次**扩图，每次 ≤ 30% 补全 |
| **颜值** | 半身渲染颜值后扩图保留，**不能直接出全身** |
| **style** | 默认 `expressive`（个人形象图）|

---

## 十 · 悠船 niji 5 特性补充（🆕 v2）

> 入档：2026-05-20
> 触发：副会话 #4 跳蛛先生 MJ 额度耗尽后切换到悠船（一个第三方 MJ 调用平台），实测发现"niji 5" 标签下的实际行为与 MJ 官方 niji 5 存在显著差异。
> 含义：本档案 §一~§九 基于 MJ 官方实测，**迁移到悠船时不能 100% 套用**。

### 10.1 悠船 vs MJ 官方 niji 5 差异对照表

| 维度 | MJ 官方 niji 5（§一~§九）| 悠船 niji 5（实测） |
|---|---|---|
| 默认 Aspect | 1:1（不写 `--ar` 即方形） | **偏纵向构图**（不写 `--ar` 大概率出全身） |
| `half body shot` 响应度 | 强，能稳定锁定半身 | **弱**，常被忽略，需要 `close-up portrait` 双重强化 |
| 渲染词堆叠（C4D/blender/octane...）| 稳定触发 3D CGI 分支（§一）| **响应较弱**，易回到 niji 立绘分支 |
| 否定语义（`no X`）| 弱（§坑 1）| 同样弱，程度类似 |
| 描述层过载阈值 | >10 词颜值下降（§坑 2）| **同款规律，但阈值更低（>8 词就开始漂移）** |
| **质感天花板** | 能稳定出 nick knight 时装大片渲染感 | **天花板更低**，稳定出 niji 立绘感，需要"半身像 + 极简" 才能勉强触及大片渲染 |

### 10.2 悠船胜利配方（本次会话验证）

```
3D high fashion illustration by nick knight and rick owens,
Panoramic lens, Long shot, half body shot, close-up portrait,  ← 双重强化半身
[人物核心 1 句],
[配色/服装 1-2 句],
[气质 1 句],
clean black background / off-white background,
[渲染词堆叠]
[质量词]
--ar 1:1 --fast --style expressive --niji 5
```

总词数 ≤ 8 个核心描述词。良伞 v3/v4/v5 都按这个走通了。

### 10.3 与 §三 MJ 官方配方的核心差异

- ✅ 加 `close-up portrait` 双重强化半身（悠船对单一 `half body shot` 不敏感）
- ✅ 强制 `--ar 1:1`（悠船默认非方形）
- ✅ 砍掉所有"奇幻复合元素细节"（种族/翅膀/鳞片/特定生物结构）—— 复杂奇幻题材在悠船 niji 5 上会被渲染成简化立绘
- ✅ 总词数控制在 8-10 个核心描述词内（比 MJ 官方更严格）

### 10.4 何时回 MJ 官方 / 何时悠船够用

| 场景 | 推荐 | 理由 |
|---|---|---|
| 高质感时装大片（潮流风格）| MJ 官方 | 悠船质感天花板低 |
| 复杂奇幻题材（兽人/异形生物/神祇）| MJ 官方 | 悠船易回到 niji 立绘分支 |
| 简洁人物形象图（半身+清背景）| 悠船够用 | 极简配方在悠船能跑通 |
| 应急（MJ 官方额度耗尽）| 悠船 | 但要降低质感预期 |

### 10.5 元教训：标签相同 ≠ 行为相同

第三方 MJ 调用平台（如悠船）虽然标注使用同一模型（niji 5），但**因渲染管线 / 默认参数 / 模型版本快照 等差异，实际行为可能显著不同**。

未来遇到任何"标签声称的模型"，应该：
1. 用工作站既有档案（如本档案 §一~§九）作为**起点假设**
2. 但**实测验证差异**，不要盲目套用
3. 发现差异时**分别建立档案章节**（不要污染原档案的实测结论）

这条规律对所有"第三方 AI 工具平台"都成立——Suno 第三方调用、MJ 第三方调用、Claude API vs Claude Code 等场景都适用。

---

## 十一、版本

- **v1 - 2026-05-15 - 主对话 Claude 沉淀**（基于副会话 niji 5 共创者 13 轮实测）
- **v2 - 2026-05-20 - 主对话 Claude（第二任）补充**（基于副会话 #4 涂图儿+良伞会话的悠船 niji 5 实测差异）

继承链：
- 副会话 v1 原始材料：`跨会话协作/项目阶段性回执_运营经理_2026-05-15.md`
- 副会话 v1 复盘：`复盘记录/复盘笔记_冠军1_prompt_battle形象图_2026-05-15.md`
- **副会话 v2 复盘**：[[../../复盘记录/复盘笔记_涂图儿良伞_悠船niji5_Nano极简_2026-05-20]]
- 配套工作流：[[../04_方法论与洞察/方法论笔记_AI形象图工作流分层_niji5+Nano]]（v2 同步升级，加 Nano 极简原则）

后续更新触发：
- 第三个独立悠船 niji 5 案例后，§十 可独立成档为 [[悠船niji5_行为档案_v1]]
- 验证其他第三方 MJ 平台（liblib MJ V7 等）后，§10.5"标签相同 ≠ 行为相同" 升格为独立元方法论
