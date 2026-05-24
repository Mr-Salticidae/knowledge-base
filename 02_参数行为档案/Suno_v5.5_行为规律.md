---
tags: [类型/档案]
---
# Suno v5.5 行为规律

> 入档：2026-05-12（D2 晚间）
> 触发：「拾色」Suno BGM 试听时的惊艳发现
> 关联：[[Suno配乐制作分享]]（基础流程 · 仍有效）

---

## 一句话

**Suno v5.5 的自动作词能力 = 跳蛛先生原创草案的能力**。当 prompt 里的"风格描述 + 情境暗示"足够精确，Suno 自己作的词比手写更好。

---

## 如何使用

写新作品 BGM 时：

1. **不要急着写歌词草案**——先把 IP 内核 / 情境 / 调性写进 style prompt
2. **第一轮跑 Suno 不指定 lyrics**（让它自由作词）
3. **如果第一轮歌词命中 IP 内核 ≥ 80% → 直接采纳**（节省"歌词决策日"一整天工作量）
4. 如果命中度 < 80% → 用 Suno 自动作词作为草案，手动修正关键句

---

## v5.5 实测：「拾色」自动作词案例

### Prompt（只写风格 + 情境，无 lyrics 草案）

```
Trip-jazz with Shanghai 1940s old-jazz influence, female lead vocal with restrained nostalgic tone like Zhou Xuan meets Norah Jones, sparse piano, rain ambience, 75 BPM, 3 minutes 10 seconds, Mandarin verses with English chorus phrases "still here, still kept, still folded, still unread", background male humming in outro
```

注意：只给了 4 个英文 hook 关键词（still here / still kept / still folded / still unread），中文部分**完全没给**。

### Suno 自动作词输出（节选 · 与 IP 立项的命中度）

| Suno 写的句 | 命中「拾色」立项的哪个锚点 |
|---|---|
| 雨落在窗沿 / 像旧邮票发蓝 | "她每周去邮局取信" / 旧邮票 |
| 抽屉还留着 / 你没带走的蓝衫 | **题眼 S09 抽屉堆满未拆信** |
| 我没说再见 / 也没把你忘 / 只是把名字 / 轻轻藏进墙 | **"她知道但选择不说"内核** |
| Still folded, still folded / Still unread | **她不拆信的核心动作** |
| 我学会安静 / 像街边那盏栈桥 | **比立项更深的人格隐喻**（神级意象 · 见下方） |

**命中度**：约 95%。**比手写的 brief 草案更好**。

---

## 反直觉发现：Suno 选的意象比立项更深一层

立项书 v1 设计的视觉锚点是**具象空间锚点**：
- 邮局 / 旗袍 / 邮票 / 黄铜邮箱 / 抽屉

Suno 自动作词加入了**抽象人格隐喻**：

> "我学会安静 / 像街边那盏栈桥 / 只把影子留给 / 来往的雨潮"

**栈桥** = 沉默伫立 + 不参与的迎送 + 影子映在水面 + 经历来往雨潮但不被带走。

完美呼应"她知道但选择不说"的内核。

**为什么 Suno 能选出这个意象**：
- prompt 里写了 "restrained nostalgic" + "Zhou Xuan meets Norah Jones"
- v5.5 训练数据里有大量"民国书信体诗歌 / 上海老克勒爵士歌词"
- 它把"克制感"翻译成了"静默物件 + 不参与"的意象组

**立项的视觉层** + **Suno 的人格层** = IP 完整立体起来。

---

## 反直觉发现：Suno 自发完成跨 IP 副歌签名

R-07 Suno V-A_001 副歌（手写）：

```
still here, still near / something soft, something dear
```

「拾色」Suno V-S_001 副歌（仅提示了 4 个 hook 词）：

```
Still here, still here / Still kept, still kept
Still folded, still folded / Still unread
```

**"still here" 在两个 IP 间共享**。Suno 没有跨会话记忆，但因为我们在 prompt 里写了 "still here, still kept, still folded, still unread"，它自然按 R-07 的副歌结构展开了——**形成跨 IP 的副歌签名**。

详见：[[跨IP作者签名_白玉兰与still_here]]

---

## v5.5 vs v3/v4 时代的能力跃升

| 维度 | v3-v4（2024）| v5.5（2026）|
|---|---|---|
| 自动作词质量 | "听起来好听但与画面对不上" | **直接命中 IP 内核 95%+** |
| 中文歌词 | 押韵勉强 / 意象套话 | **押韵自然 + 意象精准 + 文学性强** |
| 中英混 | 衔接生硬 | **自然过渡 + 跨语言 hook 设计** |
| 情境理解 | 只懂"风格描述" | **能从"作者意图"反推具体意象** |
| 演唱表现 | 偶尔出戏 | **女声音色稳定 + 情绪克制** |
| 段落结构 | 偶尔混乱 | **Intro/Verse/Pre-Chorus/Chorus/Bridge/Outro 完整** |

---

## v5.5 的局限（实测发现）

1. **个别字段输出 bug**：歌词文本"街边那盏栈桥"的"盏"作量词不严谨（实际演唱仍是"栈桥"，文本输出小问题，不影响使用）
2. **特定环境音不够明显**：prompt 写了 "rain ambience throughout" → 实际生成的雨声偏弱，需要后期混音叠加
3. **Outro humming 不一定生成**：prompt 写了 "background male humming in outro" → 实际输出可能省略，需要单独跑一段 humming 后期叠加
4. **纯器乐古筝场景时长不稳定**（2026-05-14 异界气象台 minitest 实测）：prompt 写 `approximately 50 seconds instrumental` + 五幕时间锚点（0/3/15/27/37s），实际跑 8 个 take 中 **70%+ 输出 < 20 秒**，少数能跑到 38-72 秒。**Suno 在纯器乐 + Chinese folk 风格下倾向于"短句结束"**，可能是因为这类训练数据本身片段偏短。**应对**：(a) 重跑直到出现一两个达标时长的 take；(b) 接受 30-40 秒输出后用 Suno Extend 续接；(c) 用 Suno Replace Section 把短片段拼成长片段。**最反直觉的发现**：38 秒的 v4_take1 能量曲线竟然天然吻合 0/3/15/27/37s 五幕骨架（27s 后能量缓降，37s 后掉到 0.02 形成自然淡出）——**v5.5 对"段落能量切换"时间锚点的遵循度，远高于对"总时长"的遵循度**
5. **乐器进场时间锚点遵循度低**（同一实测）：prompt 写 `dizi flute joins at 5 seconds with simple counter-line`，实际生成的曲子**全程没有笛声**（仅有古筝独奏）。同一 prompt 里"段落能量切换"锚点（at 15s/27s）却被精确执行。**规律**：v5.5 把"乐器编配"理解为风格描述而非时间指令，**"什么时候加入什么乐器"靠 prompt 控制不稳定**。**应对**：核心乐器写在主风格描述里（如 "guzheng with dizi flute throughout"），不要写"在第 X 秒加入"；如必须特定时点加入，单跑一段独立音轨后期叠加

**应对策略**：主轨 + 后期叠加补救

```
主轨：Suno 自动作词 + 主旋律（保留 95% 内容）
   ↓ 后期混音叠加：
   ├─ 男声 humming 独立生成（30 秒，简短 prompt 单跑）
   ├─ 雨声采样（Freesound 免费源，-15dB 底层叠加）
   └─ 其他 SFX（如有）
```

---

## 工作流时间节省

**v3-v4 时代**：
- 写歌词草案：0.5-1 天
- Suno 多版试听：0.5-1 天
- 微调歌词 + 重跑：0.5 天
- **总计 1.5-2.5 天**

**v5.5 时代**（拾色 D2 实测）：
- Suno 不写 lyrics 直接跑：30 分钟（2 版）
- 试听 + 决策：30 分钟
- 单跑男声 humming + 找雨声：30 分钟
- **总计 1.5 小时**

**节省了 80%+ 的 Suno 工作时间**。「拾色」的 D3 "歌词决策日"被压缩进 D2 当晚完成。

---

## Custom Mode 工程经验（5 条 · v5.5 实测）

> 入档：2026-05-17
> 触发：23《再少年》音乐共创副会话 5 轮 Custom Mode 迭代后的实测经验
> 适用：所有 Suno Custom Mode 操作

### 经验 1 · 字符 1000 上限是硬天花板

**实测**：第一版 1300+ 字符的 Style of Music 直接被 Suno 拒绝。

**应对**：
- 把所有 negative tags（如 no auto-tune / no trap hi-hats / no EDM 等）**全部移到 Exclude Styles 框**
- 正向 Style of Music 框就能腾出空间放结构指令（如段落音色变化）

**Bad**：
```
Mandarin pop-folk, ... no auto-tune, no trap hi-hats, no EDM drops, no plastic synth ...
```

**Good**：
```
Style of Music: Mandarin pop-folk, ... [所有正向描述]
Exclude Styles: autotune, trap hi-hats, EDM, plastic synth
```

### 经验 2 · 段落标签用英文 `[Male] [Female] [Both]` > 中文 `男 / 女 / 合`

**实测**：
- Simple Mode 用中文标签 OK（Suno 自发结构化）
- **Custom Mode 必须用英文标签强制锁定**，中文标签 Suno 可能忽略

**Lyrics 字段示例（正确）**：
```
[Verse 1]
[Male]
我把旧照片一张张摊开
[Female]
雨落在瓦上，很轻
```

### 经验 3 · Vocal Gender 在男女对唱场景必须**留空**

**实测**：男女对唱时强选任何一个 Vocal Gender（Male / Female / Both）都会导致**另一声部被弱化或删除**。

**应对**：让 Lyrics 框的段落标签去控制声部，**More Options 的 Vocal Gender 不选**。

### 经验 4 · Weirdness 与 Style Influence 最优组合

**实测最优组合**：

```
Weirdness:       30-35%
Style Influence: 75%
```

**为什么**：
- Weirdness 低于 25% → Suno 机械执行 → 失去意外发现
- Weirdness 高于 50% → 结构指令失控 → prompt 写的反 Suno 本能指令（如 chorus descends）被无视
- Style Influence 低于 70% → 反 Suno 本能指令（如 chorus 不上扬）被无视

### 经验 5 · "反 Suno 本能"指令需要**重复 + 具象化**

Suno 有强烈的本能默认（如 chorus 默认上扬 / 男女默认 duet / 结尾默认大团圆）。要反这些本能，prompt 必须**重复 + 具象化**。

**Bad**（抽象 + 单点）：
```
keep chorus restrained
```

**Good**（具象 + 重复）：
```
[Style of Music 框]
... chorus descends not ascends ...

[Lyrics 框段落规划里再说]
[Chorus] female voice on final "再少年" makes a small descending slide
```

**口诀**：**反本能指令在 Style 框 + 段落规划 + 具体动作描述 三处说，比说一次精确句更有效**。

### 经验 6 · Vocal Gender 不只是声部开关，更是隐藏的"风格 prior" ⭐⭐⭐

> 入档：2026-05-19
> 触发：29《扔掉》音乐共创副会话 Custom Mode 跑歌时跳蛛先生的反直觉操作
> 详细方法论：[[Vocal_Gender反选_风格prior_v1]]

**实测**：在 Style 框 + Lyrics 标签明确锁定声部的前提下，反向选择 Vocal Gender 会激活"对侧"的风格分布，但声部不会变（被 Style 框 + Lyrics 标签压倒）。

**实测案例**（《扔掉》）：纯男声 indie folk + country
- Vocal Gender: Male → 编曲偏向"乡村硬汉"气质
- Vocal Gender: Female + Lyrics 锁 [Male] → 编曲偏向"现代华语 indie pop" 气质（命中庄东茹《又活了一天》目标参考）
- 结果：男声没变，气质对了

**Vocal Gender 反选 · 气质调味矩阵**：

| 需求 | 配方 |
|---|---|
| 男声 + 厚重传统 | Vocal Gender: Male + Lyrics [Male] |
| 男声 + 现代轻盈 | Vocal Gender: Female + Lyrics [Male] |
| 女声 + 厚重深沉 | Vocal Gender: Male + Lyrics [Female] |
| 女声 + 明亮轻盈 | Vocal Gender: Female + Lyrics [Female] |
| 男女对唱 | Vocal Gender: 不选 |

**口诀**：**Style 框管"是什么"，Vocal Gender 管"什么味"**。

**风险**：
- 这是 v5.5 上的实测发现，可能未来版本变化
- 建议每次跑都对照测试，不要假设它一直有效
- **该经验仅适用于纯男声 / 纯女声场景**（男女对唱时 Vocal Gender 必须留空——见经验 3）

**反向校验**：
- 《再少年》是男女对唱，Vocal Gender 留空 → 此现象未浮现
- 《扔掉》是纯男声 → 此现象浮现

**意义**：
- 之前所有 Suno 经验都是"如何更精确地告诉 Suno"
- 这一条是"如何用 Suno 自己也没明说的参数路径，跨界调味"
- 这是**用户控制层未明示的隐藏维度**——Suno 团队自己可能都没把这个当作设计意图来文档化

---

## 段落差异化设计方法（解决"太平 / 没差异点"）

> 入档：2026-05-17
> 触发：23《再少年》v3 跑出"整体对但太平"，副会话用此方法解决

### 核心思路

**贯穿动机 + 段落差异化**

### 贯穿动机

选一个**有限出现次数（3-4 次）**的"标志音色"，在关键段落复现，制造**"声音指纹"**。

23《再少年》的贯穿动机：**口琴**（同时与跳蛛先生独游"小白"IP 形成隐秘呼应 → IP 内部 callback）。

### 段落差异化

给每个段落注入一个**独特的"声音事件"**，避免段落同质化：

| 段落 | 差异化设计 |
|---|---|
| V1 vs V2 | 器乐厚度差异（V2 加入 bass drone）|
| Pre-Chorus 1 vs 2 | 有吉他 vs 无吉他 |
| Chorus 1 vs 2 | 无口琴 vs 口琴和声 |
| Bridge | **所有器乐坍缩到真空**（反向爆发）|

**关键**：差异化不是为了变化，是为了让**每个段落都有"事件感"**——观众听到这个段落会想"哦这里不一样了"。

---

## 关联文档

- 基础流程:[[Suno配乐制作分享]](仍有效)
- 跨 IP 签名:[[跨IP作者签名_白玉兰与still_here]](still here 跨 IP 副歌签名)
- **两阶段工作流**:[[方法论笔记_Suno两阶段工作流_v1]] ⭐
- **Vocal Gender 反选风格 prior**:[[Vocal_Gender反选_风格prior_v1]] ⭐⭐⭐（经验 6 的独立深入文档）
- **版权过滤器规避**:[[Suno版权过滤器规避_v1]] ⭐
- 上位元方法论:[[识别工具天花板的时机]]
- 主线作品:
  - `D:\AIGC工作站\17_拾色\03_歌词与Suno_prompt\拾色_Suno_brief_v1.md`(拾色 Suno brief)
  - `D:\AIGC工作站\23_檐下再少年_叙事MV\01_音频\` (23《再少年》Custom Mode 实测)
  - `D:\AIGC工作站\29_扔掉_叙事MV\01_音频\` (29《扔掉》Custom Mode 实测 + Vocal Gender 反选发现)
- 案例回执:
  - [[跨会话协作/23_再少年_音乐共创回执_2026-05-17]]
  - [[跨会话协作/24_扔掉_音乐共创回执_2026-05-19]]
