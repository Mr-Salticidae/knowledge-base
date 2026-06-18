---
tags: [类型/方法论, 工具/nano, 工具/即梦, 通用/prompt工程, 图像融合, 状态/已验证]
---
# Nano 换屏图像融合 · 指令式编辑法 v1

> 入档:2026-06-18
> 触发:把「英雄联盟失败结算截图」贴进「雨夜书桌场景显示器屏幕」的换屏需求,即梦多次出图不理想,改用 Nano(Gemini 图像模型)一条 prompt 即出。
> 性质:把 A 图内容融合进 B 图指定区域(换屏、换画、换招牌、换海报)的通用方法,以及「即梦 vs Nano」在此类任务上的工具选择。
> 关联:[[Nano场景换机位_四段锚定法_v1]] / [[prompt的三段式结构_v1]] / [[MJ出图绕开抠图陷阱]]

---

## 一句话总结

**把一张图的内容融合进另一张图的指定区域(典型是「换屏」),要用 Nano 这类「指令式编辑模型」,而不是即梦这类「重新生成式」模型;Prompt 不是堆形容词,而是像跟人说话一样把「替换动作 + 透视贴合 + 光线溢出 + 锁定其余」四件事讲清楚。**

---

## 一、先选对工具:即梦 vs Nano

同样是「把图1贴进图2的屏幕」,两类模型的工作方式根本不同,结果天差地别:

| 维度 | 即梦(重新生成式) | Nano Banana(指令式编辑) |
|---|---|---|
| 工作方式 | 倾向**重新画一张**融合图,容易顺手重绘全图 | 倾向**在原图上局部编辑**,默认保留其余像素 |
| 听不听「保持不变」 | 弱,锚点(台灯/窗外/色调)常漂移 | **强**——这正是它的看家本领 |
| 透视贴合 / 光溢出 | 一般,常像平贴的死图 | 自然,屏幕像真的亮着 |
| 吃什么样的 prompt | 关键词 + 形容词堆叠 | **完整句子的编辑指令** |

> **判据:凡是「只改一处、其余 90% 必须原样保留」的任务(换屏、换画、换招牌、换海报、换标签、局部替换),优先用 Nano,不要硬磕即梦。** 即梦更适合从零生成或大幅重构。这与 [[MJ出图绕开抠图陷阱]] 同源——选对"做减法的工具",比在错工具上调参数省力得多。

---

## 二、原理认知:Nano 在做什么

换屏 = 在保持整张照片不动的前提下,**只把屏幕这块矩形区域的像素换成新内容,并让它和环境光照自洽**。Nano 能做好,是因为它本质是「理解指令 + 局部重绘」:

- 它能读懂「替换屏幕里的画面」「其余不变」这种**带动作和范围的指令**;
- 它会自动处理屏幕的**透视、反光、亮度**,以及光往桌面/键盘上的**溢出**;
- 但它需要你**显式说清楚**:替换(不是叠加)、贴合透视、点亮、光溢出、锁住其余。少说一条,就可能翻车。

---

## 三、方法论:四件事讲清楚(顺序即结构)

换屏 prompt 的骨架,就是把下面四件事按顺序说死:

**1. 定义角色 + 下替换指令 ——「图1贴到图2屏幕,完全替换原画面」**
开头先点名「图1是什么、图2是什么」,再说把图1放到图2屏幕上、**completely replacing(完全替换)**当前画面。
> ⚠️ `completely replacing` 这个词**必须有**。不强调替换,Nano 可能把新图叠在旧画面上,或留着旧图。

**2. 透视贴合 ——「按屏幕角度变形,对齐内框」**
屏幕是斜的,直接平贴会穿帮。要求截图按显示器的 perspective and angle 贴合,边缘对齐屏幕内边框(inner bezel)。

**3. 点亮 + 光溢出 ——「像真的亮着,蓝光洒到环境」**
这是「融合」与「PS 抠图」的分水岭:
- 屏幕呈真实点亮态:轻微反光(reflections)、微弱眩光(glare)、真实亮度;
- 屏幕的冷光**自然溢出**(spill)到键盘、桌面、台灯周围,与原场景光照融合。

**4. 锁定其余 ——「除屏幕外,一切不变」**
逐项点名要保留的锚点(台灯、键盘、窗外雨夜、海报、纸张、整体色调),强调 keep everything else unchanged。**列得越具体,漂移越少。**

> **口诀:图1贴图2屏幕并完全替换(1)+ 按屏幕透视贴合(2)+ 点亮并让光溢出(3)+ 其余一切不变(4)。**

这套结构和 [[Nano场景换机位_四段锚定法_v1]] 的「锚定不变 + 指定变化」是同一个底层思路——**把要保留的锁死、把要改的讲精确**,只是这里的「变量」从机位换成了屏幕内容。

---

## 四、可复用成品(以「换屏」为例)

### 英文版(推荐,成功率更高)

> Using the two provided images: Image 1 is a game result screenshot (a red-and-gold ornate banner with the Chinese characters "失败" in the center). Image 2 is a rainy-night desk scene with a green banker's lamp, a mechanical keyboard, and a monitor.
>
> Take the full content of Image 1 and place it onto the monitor screen in Image 2, completely replacing the game image currently displayed on that screen.
>
> - Match the screenshot to the monitor's exact perspective and angle, aligning its edges to the inner bezel of the screen.
> - Make the screen look genuinely powered on: subtle reflections, slight glare, and realistic brightness.
> - Let the screen's cool blue glow spill naturally onto the keyboard, desk surface, and the area around the lamp, blending with the existing lighting.
> - Keep everything else unchanged — the green lamp, keyboard, rainy window, poster, papers, and overall color grading must stay exactly as in Image 2.
>
> Photorealistic, cinematic contrast between the warm green lamp light and the cool blue screen light.

### 中文版(即梦/国内 Nano 接口可用)

> 用提供的两张图:图1是游戏结算截图(红金色花纹边框,中央有「失败」二字);图2是雨夜书桌场景(绿色台灯、机械键盘、显示器)。
>
> 把图1的完整画面放到图2显示器的屏幕上,**完全替换**屏幕里当前显示的游戏画面。
> - 按显示器屏幕的透视和角度贴合,边缘对齐屏幕内框;
> - 屏幕呈真实点亮状态:轻微反光、微弱眩光、真实亮度;
> - 屏幕的冷蓝光自然溢出到键盘、桌面和台灯周围,与原有光照融合;
> - 其余一切保持不变:台灯、键盘、窗外雨夜、海报、纸张、整体色调都与图2完全一致。
>
> 写实质感,暖绿台灯光与冷蓝屏幕光形成电影感冷暖对比。

---

## 五、调优技巧

1. **一次只下一个核心指令。** 就是「换屏」。别在同一句里又改色调、又加雨、又改海报,会互相干扰。不满意再**多轮对话式微调**(Nano 支持续聊编辑)。
2. **字糊了 → 单独锁字。** 补一句:`Keep the "失败" characters sharp and undistorted.`(保持「失败」二字清晰不变形)。
3. **比例被拉伸 → 锁比例,宁留黑边。** `Preserve the screenshot's 16:9 aspect ratio; add black bars on the sides rather than stretching it.`
4. **光不够 / 太亮 → 调溢出措辞。** 屏幕盖住反光就把「亮度提升」改成「适度提亮」;想更融就强调 `glow spill onto the desk`。
5. **优先英文。** 摄影/光影术语(perspective、bezel、glare、spill、color grading)英文理解更稳,中文亦可,关键词可中英混写。
6. **能局部涂抹更稳。** 若工具支持框选/涂抹屏幕区域再配指令,漂移最小——但 Nano 的指令理解力强到很多时候**整图 + 一条指令即可一条出**(本案例即如此)。

---

## 六、举一反三(迁移到任意「局部替换融合」)

把"屏幕"换成任意目标区域即可复用:

- **换画**:把图1放进图2墙上的相框 / 画框,替换原画;
- **换招牌 / 海报**:替换店铺招牌、广告灯箱、墙面海报的内容;
- **换标签 / 包装**:替换瓶身、盒子、书脊上的图案;
- **换手机/电视画面**:同屏幕逻辑。

> 永恒模板:**定义两图角色 + 把 A 放进 B 的某区域并「完全替换」+ 按该区域透视贴合 + 让它与环境光照自洽(点亮/反光/溢出/投影)+ 锁定其余一切不变。**

---

## 关联文档

- [[Nano场景换机位_四段锚定法_v1]] —— 同为 Nano 工程规律(同场景换机位 vs 局部换屏融合),共享"锚定不变 + 指定变化"底层结构
- [[prompt的三段式结构_v1]] —— 同源的"结构沉淀 + 变量前置"思路
- [[MJ出图绕开抠图陷阱]] —— 同为"选对做减法的工具"的工具选择智慧
- 索引入口:[[04_方法论与洞察索引]]
