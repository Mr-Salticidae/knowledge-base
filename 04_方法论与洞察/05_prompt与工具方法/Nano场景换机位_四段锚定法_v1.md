---
tags: [类型/方法论, 工具/nano, 通用/prompt工程, 模板, 状态/待验证]
---
# Nano 场景换机位 · 四段锚定法 v1

> 入档:2026-06-15
> 触发:助行器展厅参考图换机位需求(拍场景另一侧)的 prompt 提炼
> 性质:Nano(Gemini 图像模型)基于单张参考图生成"换机位拍另一侧"画面的通用方法
> 关联:[[nano跨场景三变量发现_v1]] / [[prompt的四段式结构_v1]] / [[概念锚定_风格置换迭代法_v1]]

---

## 一句话总结

**让 Nano 给同一场景"换机位",本质是「锚定不变元素 + 指定新机位」的脑补,不是 3D 重建。** Prompt 用四段式:同一场景 → 列清不变元素 → 换到这个角度拍 → 锁定风格;固定段抽成"通用锚定段"复用,机位单列做变量。

---

## 一、原理认知:Nano 在做什么

换机位拍"另一侧",意味着新画面里大部分内容是原图**没拍到**的。这件事的本质:

- **Nano 不是 3D 重建**,做不到几何级精确还原。
- 它是"**理解 + 脑补**":从参考图提取主体特征(产品类型、颜色、材质、空间风格、光线),再想象新角度下一个合理协调的场景。
- 结果:**风格、氛围、产品类别、光影能保持一致;但主体的精确数量、排列、几何位置会有出入。**

| 适合 | 不适合 |
|---|---|
| 概念图、氛围图、提案配图 | 需要精确还原的产品目录图 |
| 多角度展示空间感觉 | 数量/排列必须 100% 一致的场景 |
| 快速出多版机位挑选 | 工程级精度还原 |

> 认清这一点 → 不对结果产生不切实际期待,也知道力气花在哪。

---

## 二、方法论:四段式结构(顺序重要)

**1. 锚定身份 ——「这是同一个场景」**
开头说明"同一个场景 / 同一批物体,保持一致",让模型知道是延续而非新建。

**2. 列清固定元素 ——「哪些不能变」**
逐条写明要保留的:产品(类型、颜色、材质)、空间结构(墙、窗、地面、天花)、光线、整体氛围。**列得越具体,跑偏越少。**

**3. 描述新机位 ——「从哪儿拍」**(换机位核心,用摄影术语)
- 方向:`反打 / 180-degree reverse angle`、`opposite side`、`from the entrance`
- 高度:`平视 eye-level`、`俯拍 high-angle`、`低机位 low-angle`
- 焦段:`24mm 广角`、`35mm 标准`、`85mm 长焦`
- 要露出什么:明确点名"原图没拍到的那部分"

**4. 锁定风格 ——「氛围不变」**
结尾重申光线、色调、整体调性一致,避免换角度时连风格一起改了。

> **口诀:同一个场景(1)+ 这些东西别变(2)+ 换到这个角度拍(3)+ 风格保持(4)。**

**为什么拆成「锚定段 + 机位描述」:** 把固定部分(1/2/4)抽成可复用的锚定段,机位(3)单列。试多个机位时基准一致、变量单一,便于对比择优。与 [[prompt的四段式结构_v1]] 同源——都是"把固定结构沉淀、把变量前置"的思路。

---

## 三、可复用成品(以助行器展厅参考图为例)

### 通用锚定段(每个 prompt 开头加)

**中文:**
> 同一个医疗助行器展厅,保持所有元素一致:白色矩形展台上成排陈列的四轮带座助行器(红色、紫色、银黑色车架,黑色坐垫和黑色实心橡胶轮),右墙浅色木质格子展示柜(内置助行架、轮椅、膝代步车等辅具),左侧整面落地玻璃窗外欧式街景,抛光水泥地面,白色天花配轨道射灯,明亮自然光,高端简洁的商业展厅氛围。机位改为:

**English:**
> The same medical mobility-aid showroom, keep every element consistent: rows of four-wheeled rollators with seats on a white rectangular platform (red, purple, silver-black frames, black seats, black solid rubber wheels); light wooden cubby shelving on the right wall (walkers, wheelchairs, knee scooters inside); full glass window wall on the left showing a European street; polished concrete floor; white ceiling with track spotlights; bright natural daylight; clean high-end commercial-showroom mood. Change the camera to:

### 机位清单(接在锚定段后)

| # | 机位 | 中文 | EN |
|---|---|---|---|
| ① | 入口全景 | 从入口往里拍的广角全景,平视略低机位,24mm,左窗+中台+右柜全收,展现整体格局 | A wide establishing shot from the entrance looking in, slightly low eye-level, 24mm lens, capturing window wall, central platform, and shelving — whole layout |
| ② | 高角俯拍 | 从后角高处俯拍,鸟瞰,展现助行器成排阵列与地面/展台几何关系 | High-angle bird's-eye view from a back corner, revealing the neat grid of rollators and floor/stage geometry |
| ③ | 反打窗边 | 走到木柜端做 180 度反打,朝落地窗回拍,平视 35mm,逆光窗边光晕+剪影氛围 | 180-degree reverse angle from the shelving end, shooting back toward the window wall, eye-level 35mm, backlit window glow and soft silhouette mood |
| ④ | 产品近景 | 贴近最前排红色助行器低机位近景,浅景深背景虚化,突出车架质感与坐垫细节 | Low-angle close-up of the front red rollator, shallow depth of field, showroom softly blurred, highlighting frame texture and seat detail |
| ⑤ | 木柜侧视 | 正对右墙木质格子柜平视中景,稍侧角,展现柜内辅具陈列,展台在前景一角 | Eye-level medium shot facing the wooden cubby shelving, slight angle, showing aids inside, platform in foreground corner |
| ⑥ | 窗外街拍 | 从窗外街道往店内拍,透过玻璃看陈列,临街橱窗视角,带轻微玻璃反光 | Shot from the street outside through the floor-to-ceiling glass, storefront perspective with subtle glass reflections |

---

## 四、调优技巧

1. **机位转得越大,脑补越多。** 尤其 ② 俯拍、⑥ 窗外,助行器数量/颜色排列会与原图有出入,属正常,挑顺眼的留。
2. **一次只改一个变量。** 换机位时别同时改光线/风格,改动越多越易整体跑偏(对照 [[概念锚定_风格置换迭代法_v1]] 的"单层迭代")。
3. **跑偏就追加约束句。** 末尾补锁定:`keep the wooden shelving exactly as in the reference` / `保持机位高度不变` / `do not change the product colors`。
4. **优先英文 prompt。** 多数图像模型对英文摄影术语理解更稳,中文亦可,关键术语可中英混写。
5. **批量生成择优。** 同条 prompt 多跑几张挑最好,再微调逐步逼近。
6. **善用摄影术语。** `reverse angle` / `opposite side` / `180-degree view` / `establishing shot` / `bird's-eye view` 比口语"另一侧"更精确。

---

## 五、举一反三(迁移到任意场景)

替换三处即可复用:
- **锚定段第 2 部分** → 换成你场景的固定元素(主体、背景、材质、光线)。
- **机位描述** → 套用上面六个模板,改方向/高度/焦段。
- **约束句** → 按你最在意、最易跑偏的元素加。

> 永恒模板:**同一个场景 + 列清不变元素 + 指定新机位 + 锁定风格 + 必要时追加约束。**

---

## 关联文档

- [[nano跨场景三变量发现_v1]] —— 同为 Nano 工程规律(跨场景锁脸 vs 同场景换机位)
- [[Nano换屏图像融合_指令式编辑法_v1]] —— 同为 Nano 工程规律(换机位 vs 局部换屏融合),共享"锚定不变 + 指定变化"结构
- [[prompt的四段式结构_v1]] —— 同源的"结构沉淀 + 变量前置"思路
- [[概念锚定_风格置换迭代法_v1]] —— 单层迭代、单变量调优原则
- 索引入口:[[04_方法论与洞察索引]]
