---
tags: [类型/方法论, 工具/MJ, 通用/prompt工程, 模板]
---

# prompt 的四段式结构 · v1

> 入档：2026-05-20
> 触发：2026-05-19 闪电战 R2 海屿你获奖图定稿 prompt 的结构提炼
> 性质：**通用 prompt 工程模板**（简化 prompt 后的排列方式）
> 关联：[[prompt极简化原则_v1]] / [[获奖图复盘方法论合集_活合集]] / [[摄影术语的杠杆效率]]

---

## 一句话

简化 prompt 后，按 **`场景 → 主体 → 关键事件/光线 → 媒介质感`** 四段排列。这个顺序对齐了 MJ 的注意力衰减——把最重要的元素放在前面。

---

## 完整模板

```
[段 1 · 媒介+场景]
hyperrealistic surreal photograph, [核心场景一句话]

[段 2 · 主体动作]
[主体身份 + 动作 + 视角]

[段 3 · 光线+事件]
[光源 + 方向] + [关键事件/物件] + [反讽锚句/情感锚句]

[段 4 · 媒介质感]
[shot on... + film grain + museum quality]
```

四段按这个顺序排列。

---

## 海屿你定稿 prompt 拆解（验证案例）

完整 prompt：
```
hyperrealistic surreal photograph, a small isolated island in the middle of a vast
calm ocean, a single person sitting alone on a simple wooden chair on the island
viewed from behind facing the horizon, dramatic golden hour backlight from the
setting sun directly behind the figure rim lighting the person's silhouette, the
ocean reflecting the warm golden sunset light creating a luminous golden path on
the water leading toward the sun, in the distance on the horizon a single whale
breaching majestically out of the ocean its dark silhouette caught mid-leap against
the golden sunset light water spray catching the light around it, the whale
appearing as a distant magical moment witnessed by the seated figure, sharp focus
shot on medium format film fine grain
--ar 3:4 --style raw --stylize 200
```

按四段拆解：

### 段 1 · 媒介+场景

```
hyperrealistic surreal photograph, a small isolated island in the middle of a
vast calm ocean
```

- 媒介：超写实超现实摄影
- 场景：一座小孤岛在平静海洋中央

### 段 2 · 主体动作

```
a single person sitting alone on a simple wooden chair on the island viewed
from behind facing the horizon
```

- 主体：一个人
- 动作：独自坐在简陋木椅上
- 视角：背对镜头面向地平线

### 段 3 · 光线+事件

```
dramatic golden hour backlight from the setting sun directly behind the figure
rim lighting the person's silhouette, the ocean reflecting the warm golden sunset
light creating a luminous golden path on the water leading toward the sun, in
the distance on the horizon a single whale breaching majestically out of the
ocean its dark silhouette caught mid-leap against the golden sunset light water
spray catching the light around it, the whale appearing as a distant magical
moment witnessed by the seated figure
```

- 光源：黄金时刻夕阳背光
- 光线方式：rim lighting（边缘逆光）
- 关键事件：远方鲸鱼跃出
- 情感锚句："the whale appearing as a distant magical moment witnessed by the seated figure"（给鲸鱼定位+定情绪+定关系）

### 段 4 · 媒介质感

```
sharp focus shot on medium format film fine grain
```

- 锐焦
- 中画幅胶片
- 细腻颗粒

---

## 为什么这个顺序有效

### MJ 注意力衰减规律

MJ 对 prompt 的注意力**随段位下降**——越前面的描述权重越高。

把元素按"重要性" 排：
1. **场景** 最重要（决定整张图的"类型"）—— 段 1
2. **主体** 第二重要（决定整张图的"主角"）—— 段 2
3. **光线+事件** 第三（决定"质感"和"叙事"）—— 段 3
4. **媒介质感** 第四（细腻度调整）—— 段 4

如果倒过来排，最重要的"场景" 被放在最后，权重最低，整张图可能跑偏。

### 每段对应 MJ 内部的不同处理

| 段 | MJ 内部处理 |
|---|---|
| 段 1 | 建立"画面类型"（是摄影？插画？什么场景？）|
| 段 2 | 锁定"主体形态"（人物？物件？姿态？）|
| 段 3 | 补充"细节修饰"（光线、辅助元素）|
| 段 4 | 调用"质感库"（胶片颗粒、画幅感）|

按顺序排 = 让 MJ 的处理顺序也跟着对齐。

---

## 月下煮茶 prompt 同样符合四段式

```
[段 1 · 媒介+场景]
hyperrealistic surreal cinematic selfie photograph

[段 2 · 主体动作]
an astronaut in a full spacesuit with helmet off floating inside a space capsule
taking a selfie with one hand drinking tea from a small chinese tea cup with
the other hand a teapot floating nearby in zero gravity

[段 3 · 光线+事件]
the enormous full moon glowing brightly through a large round porthole window
behind the astronaut providing dramatic cinematic backlight, sharp focus
shallow depth of field cinematic lighting bright moonlight as key light

[段 4 · 媒介质感]
shot on medium format film fine grain high detail museum quality
```

注意月下煮茶的"段 1" 把场景直接合并进了媒介描述里（cinematic selfie 暗示场景）—— 这种合并是 OK 的，**关键是顺序，不是僵化的字数分配**。

---

## 操作规则

### 写第一版

按四段顺序直接起稿，每段一句话。

### 检查

- 段 1 字数最短（10-20 词）
- 段 2 字数中等（20-40 词，主体复杂时可以更长）
- 段 3 字数最长（30-100 词，光线+事件+情感锚句都在这里）
- 段 4 字数最短（5-15 词，质感套语）

### 反向检查

- 如果段 1 太长 → 把场景里的细节移到段 3
- 如果段 2 太复杂 → 砍掉次要主体
- 如果段 3 没有"事件"或"情感锚句" → 加一个
- 如果段 4 没有质感词 → 加 `shot on... + film grain` 等

---

## 跟 [[prompt极简化原则_v1]] 的协作流程

```
1. 用「极简化原则」决定砍多少 → 保留 6 类核心元素
2. 用「四段式结构」决定怎么排 → 按 媒介场景 → 主体 → 光线事件 → 质感 排
3. 跑图 → 反馈 → 微调
```

两个方法论是**正交**的：
- 极简化决定"内容量"
- 四段式决定"排列顺序"

两者一起用 = 极简但结构清晰的 prompt。

---

## 不适用场景

❌ 极端短 prompt（< 30 词）—— 没必要分段
❌ 半人形拟物（[[半人形拟物的部件化描述法]]）—— 需要部件化描述，不是四段式
❌ 视觉欺骗类（如垃圾高尔夫球）—— 需要尺寸+材质双锚定独立成段

---

## 关联资源

- 案例底料：[[../../复盘记录/海屿你获奖图复盘]] + [[../../复盘记录/月下煮茶获奖图复盘]]
- 合集：[[获奖图复盘方法论合集_活合集]]
- 互补方法论：[[prompt极简化原则_v1]] / [[摄影术语的杠杆效率]]

---

## 版本

- v1 - 2026-05-20 - 基于海屿你 + 月下煮茶定稿 prompt 结构提炼

升级触发：
- 多个独立案例验证后升 v2
- 跨工具验证（Suno 等）
