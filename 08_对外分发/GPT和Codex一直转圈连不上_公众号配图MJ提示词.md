# 《你的梯子没坏，是你一直在看假信号》· 公众号配图 MJ 提示词

> 配套正文：`08_对外分发/GPT和Codex一直转圈连不上_公众号版.md`
> 出图工具：Midjourney v8.2 · 8 张（封面 2 + 正文 6）
> 视觉方向：沿用库内已建档的 **sref 5692463053（Navy 现代极简）**

## 为什么选这个 sref

档案里写着它的极端舒适区是「凌晨三点的世界」——深夜加油站、便利店、空荡机场跑道、灯塔，DNA 是 Hopper 的 Nighthawks 加北欧荒诞剧。而这篇文章讲的正是一个人在凌晨对着一块转圈的屏幕。题材和它的舒适区是同一个宇宙。

它的另外两条脾气也刚好对路：**反密度、单数本能**（1 人完美、群体妥协），我们每张图都是单一主体加大留白；**色彩独裁**是 navy 加米白加一抹猩红，正好给这组图一个统一的冷调底子，不用每张单独调色。

要避开的是它三条硬边界：大面积暖色会被吞（所以全组不写 sunset / fire / golden，需要「暖」的地方一律走档案里的**白热化替代**，把暖色换成高对比白）、群体欢腾题材它拒绝、以及它跟「檐下」不同台——这组图是现代极简分支，别和古风线混用。

## 通用参数与共用骨架

v8.2 档案第 7 条实测过：**四张图共用同一句长骨架、各换一句变量从句，可以在完全不挂 sref 的条件下锁住装置一致性，零重跑**。这组沿用同一手法——一段骨架管住气质，每张只换主体那一句，出来才像一套图而不是八张散图。

**共用骨架（每条 prompt 开头都是它，不要改）**

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain
```

**共用参数尾**

```
--sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

四个参数各自的理由：

**`--sw 400`**——档案里只实测过 `sw=800`，结论是那个强度下它会**完全反吃 prompt 的颜色**（写 dark gray with gold patterns，出来还是 navy），而且会把人物推成欧裔。400 是我按「既要它的色彩独裁、又要主体活着」折中给的起点，**不是实测值**。第一轮建议 400 和 700 各跑一次对比，选完之后八张统一用同一个数，别一张一个。

**`--no text, letters, words, numerals`**——这是 v8.2 档案第 6 条的四词法。MJ 画不出可识别的真文字，只会给融化的伪字形，那是公众号封面上最扣分的元素（一眼「AI 做的」）。这个 sref 还有个已记录的癖好：会偷偷漏出对话框气泡、字幕条这类训练池伴生元素——四词法必须一直挂着。**注意 `logo` 绝对不能加进 `--no`**，档案里写明了它会把画面里该保留的图形标记一起压掉。

**`--style raw`**——v8.2 官方审美取向明确偏「抢眼」，而这组图要的是克制冷调近单色，属于档案里点名需要反向压制的类型。raw 加上骨架里那几个词（restrained、unsensational、matte）是压制手段。如果出图还是太戏剧化，往骨架里再加 `deadpan, documentary flatness`。

**`--v 8.2`**——2026-07-24 正式发布之后走这个，`--preview` 通道已经完成使命。

**尺寸**：封面首图 `--ar 235:100`，分享方图 `--ar 1:1`，正文配图 `--ar 16:9`。

公众号首图是 2.35:1，但**不能写成 `--ar 2.35:1`**——MJ 只接受整数比，带小数点会直接报 `Aspect ratio should be of the format width:height` 并拒跑。写成等价的 `--ar 235:100` 即可（约分成 `--ar 47:20` 也一样）。

**一条通用提醒**：MJ 对 `narrow / small / lower third` 这类相对尺寸和位置词执行得很松（档案实测：意图 ≤7% 的窄条，四张全出到 17%，且偏差方向一致）。所以下面所有 prompt 我都没写「在右三分之一」这种，出图后靠公众号排版去裁，不为构图位置重 roll。

## 图 01 · 封面首图

**用途**：公众号首图（2.35:1）
**意象**：凌晨三点的空房间，一块亮着的屏幕，屏上只有一道断开的光环在转。一个人的背影坐在前面，没有脸。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, an east asian man seen only from behind as a dark silhouette sitting alone before a single glowing rectangular screen in an otherwise empty dark room, on the screen nothing but one thin incomplete ring of pale light with a short crimson segment, the room dissolving into flat navy shadow around him --ar 235:100 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：`east asian` 必须留着——档案记录这个 sref 在高 sw 下会把人物推成欧裔，不显式指定就会被它主导。那道光环别写成 loading spinner 之类的 UI 词，一写就长伪字形，`thin incomplete ring of light` 是安全说法。屏幕上如果冒出气泡框或字幕条，就是 sref 的伴生元素漏出，把 sw 降到 250 重跑。

## 图 02 · 封面方图

**用途**：分享缩略图、朋友圈卡片（1:1）
**意象**：同一块屏、同一道断环，人退出画面，只剩物件。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, a single glowing rectangular screen floating in an empty dark room shot straight on, on it one thin incomplete ring of pale light with a short crimson segment, no furniture no people, the surrounding darkness perfectly flat --ar 1:1 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：也可以直接从图 01 裁一张方图省一次抽卡，但单独跑构图会更完整——方图里屏幕居中、四边留白匀，缩略图缩到很小时那道断环还认得出。

## 图 03 · 开场配图

**放在**：正文开头，「那天的现象很具体」那段之后
**意象**：深夜无人的便利店。这是这个 sref 的天才区，几乎不会失手。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, an empty all-night convenience store seen from outside across a wet empty street at three in the morning, cold white interior light spilling onto the pavement, nobody inside, a single crimson object on the counter as the only warm-adjacent note --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：店招上极容易长伪字形，四词法挡掉大部分，仍有漏网就换一个更远的机位重跑。写的是 `cold white interior light` 而不是暖黄灯光，这是档案里的白热化替代——直接写暖光会被它吞掉或改剧本。

## 图 04 · 双重路由

**放在**：第一节，代码块「你实际走的 / 本该走的」附近
**意象**：两条并行的地下管道，一条笔直通到底，另一条在中途被逼着绕进一个多余的接线盒再出来。这是全文最核心的那张图。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, two parallel industrial conduits running left to right across a bare off-white wall, the upper one perfectly straight and continuous, the lower one forced to detour through one extra bulky junction box before rejoining its path, the junction box marked by a single crimson seal, cross-section clarity, diagrammatic stillness --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：这张对「两条路径的差别一眼可见」有要求，抽卡时优先选**那个多余接线盒最突出**的一版——它是整篇文章的论点。如果 MJ 把两条管子画得差不多，把 `one extra bulky junction box` 改成 `one absurdly oversized junction box`，它会照做（这个 sref 有二次创作癖，给它一个夸张的形容词比给它位置词管用）。

**可选变体**：v8.1 档案实测过 inset frame 双层结构 4/4 稳定召出，想做「主图加右上角剖面小窗」的技术档案感，在主体从句后面接一句 `a smaller inset square frame in the upper right corner showing a cross-section diagram of the same two conduits`。但档案同时记录了子图内容会偏离 prompt，属于加分项不是必需项，别为它重 roll 太多次。

## 图 05 · 三个假信号

**放在**：第二节开头
**意象**：一整排一模一样的指示灯，全部亮着同一种冷光，看起来一切正常——而队尾那一盏是暗的，没人注意。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, a long row of identical small indicator lamps mounted on a bare navy panel, every lamp glowing the same flat cold white, one single lamp at the far end dark and dead, shot straight on with clinical symmetry --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：本来想写「一排绿灯」，但档案里这个 sref 会**无视用户的色彩描述**（鹦鹉绿会被改成蓝、泥土褐也被改成蓝），写绿必然翻车。改成冷白反而更贴题——假信号的本质不是绿，是「全都一样、全都看起来没问题」。选片挑那种**排得最整齐、暗掉那盏最不起眼**的一版，那种「你根本不会去看它」的感觉就是文章要的。

## 图 06 · 延迟不等于带宽

**放在**：第二节，「第二个假信号」那段
**意象**：两根并排的管子剖面，一根细如发丝，一根很粗——而它们的开口在同一个平面上，从正面看一样整齐。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, two vertical pipes standing side by side against an empty off-white ground, one hair-thin and one many times wider, both cut cleanly at the same height so their open mouths align on one plane, a thin crimson line marking the water level inside the thin one, austere product-photography lighting --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：粗细对比是这张的全部意义，而 MJ 对 `hair-thin` 这类相对尺寸词执行得松（档案实测偏差方向稳定地偏大）。如果出来两根差不多粗，别改形容词，**给参照物**——把 `one hair-thin` 改成 `one no thicker than a pencil`，实体参照比程度副词硬。

## 图 07 · DNS 从侧门溜走

**放在**：第三节，DNS 那段
**意象**：一道正门，旁边有一条谁也没留意的缝，一根红线正从缝里溜出去。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, one heavy sealed doorway set in a vast bare navy wall, beside it an unnoticed narrow gap at floor level, a single crimson thread slipping out through that gap and trailing away across the pale floor, everything else absolutely still and empty --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：这张是全组最抽象的一张，也最容易被 sref 改剧本（它对极简概念有主动改剧本的癖好，档案里的例子是「红蜡封 on 白纸」被它改成折成三角形的纸加一滴红蜡）。改得好就留着，那通常比原意象更耐看；改得看不懂主题就重跑。红线是这张唯一的信息载体，红线丢了直接弃。

## 图 08 · 结尾 · 不可替代

**放在**：最后一节，「你的账号不是抗封的，是不可替代的」那句附近
**意象**：一把用了很多年的旧钥匙，独自躺在米白台面上，系着一根红绳。磨损是它唯一的价值证明，而磨损无法伪造。

```
minimalist modern editorial image in deep navy and off-white with a single small crimson accent, one lone subject in a vast empty frame, three-in-the-morning stillness, matte even lighting with no warm glow, restrained low-saturation palette, generous negative space, quiet and unsensational, clean geometric composition, fine film grain, a single old key lying alone at the centre of a wide empty off-white surface, its metal worn to cold pewter grey with years of handling, one thin crimson cord tied through its bow, deep navy shadow pooling around it, macro stillness --ar 16:9 --sref 5692463053 --sw 400 --v 8.2 --style raw --no text, letters, words, numerals
```

**抽卡提示**：写的是 `cold pewter grey` 不是黄铜——黄铜是暖色，档案明确写着大面积暖色会被这个 sref 吞掉或改写。磨损感是这张的全部重量，选片挑**磨得最厉害、最不像新钥匙**的那一版，别挑最漂亮的。

## 如果不想要 navy 这个方向

八条 prompt 把 `--sref 5692463053 --sw 400` 整段删掉即可，骨架里的 `deep navy and off-white with a single small crimson accent` 会接管配色，效果会弱一档、跨图统一性下降，但仍然成立——v8.2 档案第 7 条实测过纯骨架也能锁住一致性，只是那次锁的是装置不是景观。

想换个完全不同的气质，库里另外两个已建档的 sref 都在水墨线上（少女水墨摄影、沉郁成熟水墨摄影），和这篇技术文的调性不搭，不建议硬配；真要换方向，按 sref 编号独立律的做法是**换编号重新探脾气**，不是在这个编号上硬调参数。

## 出图后

八张出齐之后，值得把这次的实测结果回填两处：`--sw 400` 到底是不是比 800 更听话（档案里这一格目前是空的），以及这个 sref 在「工业装置 / 剖面示意」这类题材上的表现——档案里的适合题材清单目前只列到「极简符号化」，工业管道属于未验证区。
