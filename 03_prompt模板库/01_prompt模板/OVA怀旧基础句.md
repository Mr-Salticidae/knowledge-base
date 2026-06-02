---
tags: [类型/prompt模板]
---
# OVA 怀旧基础句

> 首次沉淀:2026-05-12(「告白」获奖图复盘方法论 D)
> 三次验证 ✓✓✓:「告白」·「告白」迭代版 ·「秘密基地」(2026-05-14)
> 主线作品来源:`03_prompt模板库/02_案例复盘/告白获奖图复盘.md` + `03_prompt模板库/02_案例复盘/秘密基地获奖图复盘.md`

---

## 一句话总结

**一组可复用的关键词组合**,能稳定锁定"80 年代末 90 年代初日本 OVA 动画"那条线的怀旧手绘动画感,绕开新海诚 / 京アニ 的当代日漫和宫崎骏 / 吉卜力的撞车池。

---

## 如何使用

✅ **适用主题**:**情绪向 / 青春记忆 / 私密时刻**类的人像
- "告白前夜的崩溃"
- "秘密基地里的小女孩"
- "毕业前最后一天"
- "等一个不会来的人"
- "暑假最后一个下午"

✅ **不适用**
- 写实摄影、现代时尚大片
- 动作戏强、需要清晰复杂场景叙事
- 需要"明亮当代日漫感"——那是 [[MUJI极简插画基础句]] 也不对,要走新海诚 / 京アニ 那一条,本基础句反而拉旧

⚠️ **配合**
- [[极简插画删表情律]]——表情词主动删干净,情绪靠姿态承担
- [[主体不看镜头律]]——OVA 风格里"主体看镜头"会失去复古感

---

## 基础句模板

```
1990s anime cel animation style, 
[主体描述],
[姿态:头朝下 / 侧身 / 倚靠 等闭合姿态],
[道具列表:5-6 件,单独 a/an 起头],
[光线时段:late afternoon golden backlight / pale dawn light / dusk blue light],
hand-drawn cel shading with thick line art, 
[色调锚:具体色系,见下],
visible film grain and scratches, 
vintage anime aesthetic reminiscent of late 80s to early 90s OVA, 
[情绪锚:intimate quiet [defeated/tender/lonely] mood]
```

### 后缀(参数)

```
--ar 4:5 --style raw --v 8.1 --profile mb1wwgy dsdxtdr
```

---

## 四层风格关键词(必须全上)

| 层 | 关键词 | 作用 |
|---|---|---|
| 时代锚 | `1990s` / `late 80s to early 90s` | 锁住时代,避开当代日漫 |
| 媒介锚 | `cel animation` / `OVA` / `hand-drawn` | 锁住手绘赛璐珞,避开 CG 风 |
| 工艺锚 | `thick line art` / `cel shading` / `film grain` / `scratches` | 物理痕迹,锁住"母带翻录感" |
| 色调锚 | 具体色系名(见下) | 锁住褪色调,避免出"鲜亮当代风" |

**四层缺一层都会被 MJ 拉回主流**——只写 `anime` 出当代日漫,只写 `OVA` 没有工艺锚则出干净版,只写工艺锚没色调锚则出现代复古风(像 instagram 滤镜)。

---

## 色调锚词库

| 情绪 | 色调写法 |
|---|---|
| 告白 / 心事 | `muted yellow-green nostalgic color palette` |
| 秘密基地 / 童年 | `muted summer afternoon palette of warm ochre faded teal dusty pink and pale gold` |
| 离别 / 毕业 | `washed out blue-purple dusk palette with warm window light` |
| 暑假 / 午后 | `pale sun-bleached palette of cream warm sand and faded green` |
| 凌晨 / 失眠 | `cold violet-grey dawn palette with one warm lamp glow` |

---

## 必须删的词

OVA 风格里这些词会把画面"现代化",拉回新海诚 / 京アニ 的当代风,损失复古独特性:

- ❌ `cinematic` —— 把画面拉向电影感,失了 TV 动画质感
- ❌ `fashion editorial` —— 拉向时尚摄影
- ❌ `detailed rendering` / `highly detailed` —— 把粗线条拉成精细 CG
- ❌ `4k` / `8k` / `ultra realistic` —— 同上
- ❌ `studio ghibli` —— 撞车率最高,出来全是吉卜力面孔
- ❌ 任何表情词 —— 见 [[极简插画删表情律]]
- ❌ `child` / `kid` —— 见 [[儿童主题避雷词替换法]]

---

## 验证案例

### ✓ 第一次「告白」(2026-05-11)

```
1990s anime cel animation style, east asian woman slumped at a wooden desk in her small bedroom at dawn, head down on her arms, dozens of crumpled paper balls scattered around her, an unfinished handwritten letter under her cheek, pen dropped beside her hand, oversized t-shirt and shorts, soft pale dawn light through the window, warm desk lamp still on, hand-drawn cel shading with thick line art, muted yellow-green nostalgic color palette, visible film grain and scratches, vintage anime aesthetic reminiscent of late 80s to early 90s OVA, intimate quiet defeated mood
```

### ✓ 第三次「秘密基地」(2026-05-14)

```
1990s anime cel animation style, a small east asian schoolgirl in a faded blue school uniform crouching alone in a narrow hidden space behind a rusted electrical transformer box by a quiet residential alley after school, her schoolbag set down beside her, the secret hideout decorated with her personal treasures a small notebook a pile of colorful pebbles candy wrappers a half drunk bottle of marble soda and a tiny tin box, late afternoon golden backlight streaming through the gap and catching the dust in the air, her face lit warmly from the side eyes lowered to her notebook, hand-drawn cel shading with thick line art, muted summer afternoon palette of warm ochre faded teal dusty pink and pale gold, visible film grain and scratches, vintage anime aesthetic reminiscent of late 80s to early 90s OVA, intimate quiet private mood, the tender solitude of a child's secret world
```

---

## 关联文档

- 姐妹模板:[[MUJI极简插画基础句]] (日系极简插画版本,适用静默 / 意境 / 抽象触觉类主题)
- 验证案例:[[告白获奖图复盘]] · [[秘密基地获奖图复盘]]
- 配套方法论:[[极简插画删表情律]] · [[主体不看镜头律]] · [[光暗作为空间叙事工具]] · [[私人空间道具密度公式]] · [[儿童主题避雷词替换法]]
- 风格选择:[[AI甜妹脸vs复古东方美人]] · [[跨IP作者签名_白玉兰与still_here]]

