---
tags: [类型/IP视觉]
---
# 用 Suno 给视频做定制 BGM —《凝视》配乐制作分享

> 给对Suno感兴趣的同好们 — 跳蛛先生

很多人听完《凝视》的 BGM 觉得很合,问我怎么做的。这篇就把整个流程分享出来,顺便把我踩过的坑也写下来。

希望对你有用。

---

## 一、写在前面 — 这套方法不是"教程",是"思路"

**Suno 不是按按钮就能出好音乐的工具**。它的核心是:你能用语言精确地描述你想要什么。所以这份文档与其说是"Suno 操作教程",不如说是"如何把自己脑子里的音乐说出来"。

会写 prompt 的人和不会写 prompt 的人,用同一个 Suno,出来的东西天差地别。差别不在 Suno,在你。

---

## 二、起点不是 Suno,是先想清楚视频要什么

我这次最深的教训是:**不要打开 Suno 就开始写 prompt**。

我一开始就是这样做的。结果出来一堆"听起来好听但和视频对不上"的曲子,试了七八首都不对,折磨自己也折磨 Suno。

正确的起点是先回答几个问题:

**1. 视频是什么调性?**
- 暗黑 / 治愈 / 紧张 / 浪漫 / 神秘 / 史诗 ...
- 我是"暗黑+克制+冷感"

**2. 视频时长多少?用什么节奏?**
- 抖音 15s 还是 B站 60s?
- 快节奏(切换频繁)还是慢节奏(每个镜头都长)?
- 我是 15s 快切

**3. 视频的"能量曲线"是什么样?**
- 一直高?一直低?先低后高?有几个高潮?
- 我是"中等→高潮→收束"

**4. 有没有需要"卡点"的关键瞬间?**
- 比如某个角色出现、某个动作完成、某个字幕浮现
- 我有 6 个角色入场点 + 1 个收尾爆点

**这四个问题想清楚,Suno prompt 几乎就写出来了。**

如果你跳过这一步,Suno 会给你一首"通用好听"但永远不能精确卡到你视频上的曲子。

---

## 三、我的 prompt 全文 + 逐段拆解

这是我最终用的完整 prompt:

```
Dark cinematic instrumental at 90 BPM, blending tense orchestral 
suspense with phonk-weighted low-end and a half-time pulse; intro 
starts with mechanical clockwork ticks, deep cello drones, and low 
brass swells, then tribal drums enter at 8 seconds and the bass 
drops hard at 11 seconds for a massive impact before the reverb 
tail fades out. Sparse opening builds into a sudden удар of drums 
and sub, with reversed swells and metallic ticks bridging each hit. 
Wide, ominous, and pressure-filled mix with huge low-end weight 
and crisp transient detail, low, deep cello.
```

看起来很复杂,其实是 4 个层次拼起来的。

### 第 1 层:基础参数(1 行)

```
Dark cinematic instrumental at 90 BPM
```

`Dark cinematic` 调性,`instrumental` 强制纯音乐,`90 BPM` 锁节奏。

**关于 BPM 的关键认知**:这是整个 prompt 里最重要的一个数字。BPM 直接决定后面剪辑节奏。

我怎么定 90 BPM 的:
- 视频 15 秒,要切换 7 次(6 张图 + 收尾)
- 平均每张图 ~2 秒
- 90 BPM 一拍 = 0.667 秒,4 拍 = 2.67 秒 ≈ 一张图的时长
- **完美匹配**

如果你视频每张图想要 1 秒,那 BPM 应该是 120-140;如果每张图 4 秒,BPM 应该选 60-70。
**先有视频节奏,再决定 BGM 的 BPM**。

### 第 2 层:风格融合(2 行)

```
blending tense orchestral suspense with phonk-weighted low-end 
and a half-time pulse
```

这是整个 prompt 的"灵魂",描述了我想要的两种风格的混合:

- `tense orchestral suspense`:紧张感的管弦乐 — 给"高级感、电影感、戏剧张力"
- `phonk-weighted low-end`:phonk 风格的低音处理 — 给"现代感、抖音流量友好的鼓点"
- `half-time pulse`:半拍脉冲(每两拍才打一下鼓的强拍)— 让节奏既稳定又有压迫感

**为什么要混合两种风格?**

纯古典管弦乐 → 太"高雅",和抖音流量调性不符
纯 phonk → 太"街头",和我"作品集"的调性不符
**两个混合 → 高级感 + 流量友好**

这种"风格 A meets 风格 B"是 Suno prompt 的进阶写法,比单一风格描述效果好得多。

### 第 3 层:时间线结构(3-4 行)

```
intro starts with mechanical clockwork ticks, deep cello drones, 
and low brass swells, then tribal drums enter at 8 seconds and 
the bass drops hard at 11 seconds for a massive impact before 
the reverb tail fades out
```

这是最关键的一段——**告诉 Suno 这首曲子的"时间结构"**。

逐段拆:

1. `intro starts with mechanical clockwork ticks` — 开头是机械时钟咔嗒声
2. `deep cello drones, and low brass swells` — 加入大提琴持续音和低音管乐渐进
3. `tribal drums enter at 8 seconds` — **第 8 秒鼓点进入**
4. `bass drops hard at 11 seconds` — **第 11 秒贝斯重击落下**
5. `reverb tail fades out` — 余韵淡出

**为什么要写得这么具体?**

如果只写 "build up and drop",Suno 会瞎编一个时间结构,可能 build up 到 5 秒就 drop 了,可能 12 秒还没 drop。
**写明 "at 8 seconds" 和 "at 11 seconds",Suno 会尽力按这个时间生成**。

这是 Suno 的一个重要能力(很多人不知道)——**它能理解时间锚点**。利用好这点,你能控制曲子的整体结构。

### 第 4 层:质感细节(2 行)

```
Sparse opening builds into a sudden удар of drums and sub, with 
reversed swells and metallic ticks bridging each hit. Wide, 
ominous, and pressure-filled mix with huge low-end weight and 
crisp transient detail, low, deep cello.
```

这一层在补"质感关键词":

- `Sparse opening` — 开头要稀疏(留呼吸感)
- `sudden удар of drums and sub` — 突然的鼓点击中(удар 是俄语"打击",我特意用这个词,因为 Suno 训练数据里这种**非英语词**反而能触发更狂野的效果)
- `reversed swells` — 反向音浪(那种"嘶——嗒!"的电影感前缀音)
- `metallic ticks bridging each hit` — 金属咔嗒声连接每次鼓点
- `Wide, ominous, and pressure-filled mix` — 宽阔、压迫、不祥的混音
- `crisp transient detail` — 清晰的瞬态细节(让鼓点"打"得脆)

**质感词汇是 prompt 的"味精"** — 没有不致命,有了风味更足。

---

## 四、我用了多少次才出这首曲子?

诚实地说:**约 8-10 次生成**。

但**前 5 次都是错误方向**(我一开始没遵守"先想清楚视频要什么"这条),后面 3-5 次才是基于本文这套思路的精修。

如果你按本文的思路从头开始,**3-5 次基本能出满意的**。

迭代的具体路径:

1. **第 1 版**:风格大致对,但 BPM 不对(出来是 120 BPM)
   → 修改:在 prompt 开头明确 `at 90 BPM`
2. **第 2 版**:BPM 对了,但太"古典",缺少 phonk 的现代感
   → 修改:加入 `phonk-weighted low-end and a half-time pulse`
3. **第 3 版**:风格对了,但开头太满,没有"留白感"
   → 修改:加入 `Sparse opening`
4. **第 4 版**:开头有留白了,但 drop 不够狠
   → 修改:加入 `the bass drops hard at 11 seconds for a massive impact`
5. **第 5 版**:基本满意,只差细节
   → 加入 `metallic ticks bridging each hit` 和 `reverb tail fades out` 等微调

**每次迭代只改 1-2 个地方,不要大动**。这样你能精确知道是哪个改动起了作用。

---

## 五、Suno 操作具体步骤

### Step 1:打开 Custom 模式

不要用默认的 "Description" 模式。点进 "Custom" 才能精确控制。

### Step 2:填三个字段

| 字段 | 填什么 |
|---|---|
| **Style of Music** | 我上面那段完整 prompt |
| **Title** | 随意 — 比如 "The Gaze - Soundtrack"(只是文件名,不影响生成) |
| **Lyrics** | **留空** |

### Step 3:勾选 "Instrumental"

**这是最容易漏的一步**。如果不勾,Suno 会自动加歌词演唱,完全毁掉你的纯音乐。

### Step 4:点 Create

Suno 一次会生成 2 首(Suno v4 的设定)。两首都听完。

### Step 5:挑+延长

如果有一首基本对,但只有 1 分多钟,可以用 "Extend" 功能延长——但**对于 15 秒视频用,通常 1 分钟就足够选段了**(我后面会讲选段)。

如果两首都不对,改 prompt 里的某 1-2 个词,重新 generate。**不要从零重写整个 prompt**。

---

## 六、得到 BGM 之后:选段才是真正的工作

我的 BGM 总长 70 秒,但视频只用 15 秒。怎么选?

### 用波形软件看能量曲线

Suno 给你的是一个完整的曲子,有起承转合。**你要做的是从中"剪"出最适合视频的 15 秒**。

我推荐用免费的 Audacity 看波形(任何能显示音频波形的软件都行)。波形高的地方是"高能量段",低的地方是"安静段"。

### 选段原则

1. **开头要"安静→爆发"**:你的视频开头有字幕铺垫,需要 BGM 也"留白",所以选段开头最好是低能量
2. **中段要"持续高能"**:你的视频中段是图片轮播,BGM 要稳住情绪
3. **关键卡点要对齐**:你视频里"最重要的瞬间"应该对齐 BGM 的"最强爆发"

我最终选的是 BGM 的 9.5-24.5 秒段:开头有 2 秒左右安静,然后建立到爆发,正好覆盖 15 秒。

### 具体怎么"剪"?

如果你会 PR/AU,直接剪就行。
如果不会,用 ffmpeg 一行命令:

```bash
ffmpeg -i 原始BGM.wav -ss 9.5 -t 15 输出.mp3
```

`-ss 9.5` 是从 9.5 秒开始,`-t 15` 是截 15 秒长度。

最后建议加 0.3 秒淡出,避免突然结束的"啪"声:

```bash
ffmpeg -i 原始BGM.wav -ss 9.5 -t 15 -af "afade=t=out:st=14.7:d=0.3" 输出.mp3
```

---

## 七、几个我踩过的坑

### 坑 1:在 prompt 里写中文

不行。Suno 对中文 prompt 的理解远不如英文。即使你描述的是"东方风格音乐",也用英文写,比如 `oriental fantasy with guzheng and erhu`。

### 坑 2:堆砌一大堆形容词

❌ `dark, sad, melancholy, gloomy, depressing, eerie, haunting, mysterious...`

太多形容词会互相矛盾,Suno 反而不知道你想要什么。

✅ 选 2-3 个最核心的就够,把空间留给"风格融合"和"时间结构"。

### 坑 3:只描述风格,不描述结构

只写 "dark cinematic instrumental" 出来的曲子,**结构是 Suno 瞎编的**。可能开头就高潮、中间没起伏、结尾突然停。

加上 `intro starts with X, then Y enters at 8 seconds, drops at 11 seconds` 这种**时间锚点**,才能控制结构。

### 坑 4:对生成结果"凑合"

最大的诱惑是:出来一首"听着还行但不是完全对"的,你说服自己"差不多了"。

**别凑合**。每次重新生成只要 30 秒,重新写 prompt 也只要 1 分钟。多迭代 3-5 次就能精确得多。

我一开始就因为"凑合"用了第 4 版 BGM 配视频,结果出来的视频音画不和,差点放弃整个项目。

### 坑 5:在 Suno 里调整,不在视频里调整

如果某段 BGM 不太对,**不要去改视频去适应它**。回 Suno 重新生成。

视频已经是你心里那个"作品",改它会越改越散。BGM 是你能完全控制的变量。

---

## 八、一个进阶技巧:Replace Section

Suno 有个被严重低估的功能叫 **Replace Section**(替换片段)。

如果你出了一首"基本对但某一段不对"的曲子,不需要全部重做。可以:

1. 选中那段不对的(比如 8-15 秒)
2. 写新的 prompt 描述你想替换成什么
3. Suno 会保留前后,只重新生成你选的这段

这个功能让"精修"成为可能。我后期就是用这个把 drop 那段改了 2 次才到位的。

---

## 九、如果你想做和《凝视》类似的暗调系作品

直接抄我这个 prompt,只改一个词:

```
Dark cinematic instrumental at __90__ BPM, blending tense 
orchestral suspense with phonk-weighted low-end and a half-time 
pulse; intro starts with __mechanical clockwork ticks__, deep 
cello drones, and low brass swells, then tribal drums enter at 
8 seconds and the bass drops hard at 11 seconds for a massive 
impact before the reverb tail fades out.
```

**只改两个地方就能变出不同感觉**:

- `mechanical clockwork ticks` → 换成你的"开场氛围"(比如 `rain and distant thunder` / `whispered prayers` / `glitching radio static`)
- `90 BPM` → 改成适合你视频节奏的(慢:60-75 / 快:120-140)

风格框架保留,氛围细节定制。这样你不会出和我一样的曲子,但有相似的"质感",同时是属于你的作品。

---

## 十、最后:为什么这件事值得做

很多人会觉得"BGM 用现成的就行了,何必自己生成?"

但用现成 BGM 你会发现:
- 永远找不到时长完美匹配的(都是 3 分钟,你只要 15 秒)
- 永远找不到鼓点完美对齐你视觉切换的
- 永远会有版权风险
- 永远会和别人撞曲

**Suno 让 BGM 制作变成了"为单个项目量身定制"**,这是几年前完全做不到的事。

而且最妙的是:**Suno 把"音乐人"这个职业的某些部分降低了门槛**。我不是音乐人,但我能用文字精确描述"我想要什么音乐",于是我就拥有了我想要的音乐。

这种"用语言换世界"的能力,是 AI 时代真正给创作者的礼物。

希望这份分享对你有用。

如果做出什么作品,欢迎来找我聊聊。

— 跳蛛先生
