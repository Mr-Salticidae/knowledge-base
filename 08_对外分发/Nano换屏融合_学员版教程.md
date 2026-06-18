# 把一张图「装进」另一张图的屏幕里:换屏融合保姆级教程

> 一个真实案例:把「英雄联盟·失败」的结算截图,装进「雨夜书桌」场景的显示器屏幕里,
> 让它看起来像那台电脑真的在显示这局败局。下面从选工具到写提示词,一步步拆给你。

---

## 一、先别急着写提示词,先选对工具

很多人换屏失败,不是提示词不好,是**工具选错了**。AI 出图工具分两大类:

| 类型 | 代表 | 它的默认动作 | 擅长 |
|---|---|---|---|
| **重新生成式** | 即梦、Midjourney | 「重新画一张」,哪怕给了参考图也容易整张重画 | 从零创作、大改、风格重绘 |
| **指令式编辑** | Nano Banana(谷歌 Gemini 图像模型) | 「保留原图,只改你点名的那块」 | 局部替换:换屏、换画、换招牌 |

**换屏属于「只改一小块、其余 90% 必须原样保留」的活**——这正是**指令式编辑模型(Nano)的强项**,而**逆着重新生成式工具(即梦)的默认行为**,所以即梦经常把台灯、窗外、色调一起改跑偏。

> 🔑 **一句话口诀:改一处用编辑式(Nano),造全图用生成式(即梦/MJ)。**
> 本案例在即梦上反复出图都不理想,换到 Nano 后一条提示词就出对了。

---

## 二、搞懂 Nano 换屏时在干什么

换屏 = 在**整张照片不动**的前提下,只把「屏幕」这块矩形区域的画面换掉,并让它和环境光自然融为一体。

Nano 能做好,是因为它会:
- 读懂「替换屏幕画面、其余不变」这种**带动作和范围**的人话指令;
- 自动处理屏幕的**透视、反光、亮度**,以及屏幕光往桌面/键盘上的**溢出**。

但前提是:你得把要求**一条条说清楚**。少说一条,它就可能翻车(比如新图叠在旧图上、屏幕像贴上去的死图、或者把台灯也改了)。

---

## 三、提示词的骨架:四件事讲清楚

写换屏提示词,本质就是把下面四件事按顺序说死:

**① 定义两张图 + 下「完全替换」指令**
先说清「图1是什么、图2是什么」,再说把图1放到图2屏幕上、**完全替换**当前画面。
> ⚠️ 「完全替换(completely replacing)」这个词**必须有**!不强调替换,AI 可能把新图叠在旧画面上,或者旧图还留着。

**② 透视贴合**
屏幕是斜的,直接平贴会穿帮。要求截图**按显示器的角度和透视变形**,边缘对齐屏幕内边框。

**③ 点亮 + 让光溢出**
这是「真融合」和「PS 硬贴」的分水岭:
- 屏幕要像**真的开着**:轻微反光、微弱眩光、真实亮度;
- 屏幕的冷光要**自然洒到**键盘、桌面、台灯周围,跟原场景的光融在一起。

**④ 锁定其余一切**
逐项点名要保留的东西(台灯、键盘、窗外雨夜、海报、纸张、整体色调),强调**其余全部不变**。列得越具体,跑偏越少。

> 口诀:**完全替换 → 透视贴合 → 点亮溢光 → 锁住其余。**

---

## 四、可直接套用的提示词(本案例实测一条出)

> 平台:liblib.tv 的 Nano 节点。
> `{{Image 1}}` / `{{Image 2}}` 是平台的**图槽占位符**,分别对应你上传的第 1、2 张图,运行时自动替换。
> 换别的平台时,把它改回普通的 `Image 1` / `Image 2` 即可。

**英文版(推荐,成功率更高):**

```text
Using the two provided images: {{Image 1}} is a game result screenshot (a red-and-gold ornate banner with the Chinese characters "失败" in the center). {{Image 2}} is a rainy-night desk scene with a green banker's lamp, a mechanical keyboard, and a monitor.

Take the full content of {{Image 1}} and place it onto the monitor screen in {{Image 2}} , completely replacing the game image currently displayed on that screen.

Match the screenshot to the monitor's exact perspective and angle, aligning its edges to the inner bezel of the screen.
Make the screen look genuinely powered on: subtle reflections, slight glare, and realistic brightness.
Let the screen's cool blue glow spill naturally onto the keyboard, desk surface, and the area around the lamp, blending with the existing lighting.
Keep everything else unchanged — the green lamp, keyboard, rainy window, poster, papers, and overall color grading must stay exactly as in {{Image 2}} 
Photorealistic, cinematic contrast between the warm green lamp light and the cool blue screen light.
```

**中文版(国内 Nano 接口可用):**

```text
用提供的两张图:图1是游戏结算截图(红金色花纹边框,中央有「失败」二字);图2是雨夜书桌场景(绿色台灯、机械键盘、显示器)。

把图1的完整画面放到图2显示器的屏幕上,完全替换屏幕里当前显示的游戏画面。
- 按显示器屏幕的透视和角度贴合,边缘对齐屏幕内框;
- 屏幕呈真实点亮状态:轻微反光、微弱眩光、真实亮度;
- 屏幕的冷蓝光自然溢出到键盘、桌面和台灯周围,与原有光照融合;
- 其余一切保持不变:台灯、键盘、窗外雨夜、海报、纸张、整体色调都与图2完全一致。

写实质感,暖绿台灯光与冷蓝屏幕光形成电影感冷暖对比。
```

---

## 五、出图不满意?对症追加一句

Nano 支持**多轮对话式微调**,第一版不完美别重写,只追加一句改它:

| 问题 | 追加这句 |
|---|---|
| 屏幕上的字糊了/变形 | `Keep the "失败" characters sharp and undistorted.`(保持「失败」二字清晰不变形) |
| 截图被拉伸变形 | `Preserve the screenshot's 16:9 aspect ratio; add black bars on the sides rather than stretching it.`(保持16:9,宁可两侧留黑边也不拉伸) |
| 屏幕太亮、盖住了反光 | 把「亮度提升」改成「适度提亮」 |
| 屏幕像贴上去的、不够融 | 强调 `glow spill onto the desk`(让屏幕光洒到桌面) |
| 一次改太多、整体跑偏 | **一次只下一个核心指令**,别在同一句里又改色调又加雨又改海报 |

---

## 六、学会这一招,能干一堆事

把「屏幕」换成任意区域,同一套思路通吃:

- **换画**:把图1放进墙上相框/画框
- **换招牌/海报**:替换店铺招牌、灯箱、墙面海报内容
- **换包装/标签**:替换瓶身、盒子、书脊图案
- **换手机/电视画面**:同屏幕逻辑

> **万能模板:** 定义两图角色 → 把 A 放进 B 的某区域并「完全替换」→ 按该区域透视贴合 → 让它与环境光自洽(点亮/反光/溢出/投影)→ 锁定其余一切不变。
