# niji 6 动作对不上、niji 7 出不了吉卜力?一条提示词的两堂课

> 一位同学的真实提问:"为什么 niji 6 做出来的人物,动作完全对不上提示词?换 niji 7,又做不出吉卜力风格?"
> 两个问题看起来是两回事,其实是**同一条提示词踩了两类坑**。下面把诊断和修法完整拆给你,所有提示词都实测过、可直接抄。

---

## 〇、先看这条出问题的提示词

```
Studio Ghibli style, a little boy sitting alone on a stool in front of a wooden
house, lonely and sad facial expression, holding an old photo in his hand,
facing left, gazing at distant mountains, bathed in sunset light lonely yet
warm atmosphere, hand-drawn anime texture.
```

想要的画面:吉卜力风,小男孩坐在木屋前的凳子上,手里拿着旧照片,朝左望着远山,夕阳,孤独又温暖。

结果:niji 6 上动作乱套,niji 7 上没有吉卜力味。**先说结论:这不是玄学,也不是"模型不行"。**

---

## 一、第一堂课:动作对不上 = 提示词自己在打架

### 数一数,主角身上挂了几个指令

坐凳子、手拿照片、朝左、望远山、悲伤表情——**5 个动作/姿态指令同时压在一个小男孩身上**。其中有两个硬伤:

**硬伤 ①:两个指令互相矛盾。**
"手里拿着旧照片"在 AI 的经验里,强烈关联"低头看照片";而"凝望远山"要求抬头看远方。**一个人不能同时看照片又看山**。模型不知道听哪句,于是每次随机选一个——你就会看到"看照片版""看山版""照片干脆消失版"轮流出现,感觉就是"动作完全对不上"。

**硬伤 ②:"facing left" 是个没用的方向词。**
MJ 系模型对"朝左/朝右"这种抽象方向词的执行一直很差,它是**弱信号**——写了约等于没写。方向要靠**画面里的实物**来锁:不写 facing left,改写"侧面像(in side profile)",再把山放进画面一侧,人自然就朝那边看了。

**还有一个隐性失分:情绪词太多,挤掉了动作词的注意力。**
`lonely` 出现了两次,还有一整句"lonely yet warm atmosphere"。提示词的总注意力是有限的,形容词越堆,关键动作分到的注意力越少。**情绪不要用形容词硬说,交给光线和构图去表达**——"暖色夕阳逆光"本身就是孤独又温暖。

### 修正版(niji 6 实测一次命中)

先做一个选择:到底让他看照片,还是看山?我们选看山,照片改成"搁在腿上"——两个动作从打架变成共存:

```
Studio Ghibli style anime film still, a little boy sitting alone on a small
wooden stool in front of an old wooden house, seen in side profile, gazing at
distant mountains, an old photograph resting loosely in his hands on his lap,
warm sunset backlight, hand-painted watercolor background
--niji 6 --ar 4:3
```

实测结果:**一次出图全中**——侧面朝向、望着远山、照片在手、坐姿正确、吉卜力味十足。没有调任何参数,就是把打架的指令拆开了。

> 🔑 **口诀:一个主体,一条视线。方向不写 facing left,写侧面像 + 画面参照物。情绪交给光线,别堆形容词。**

### 一个小插曲:凳子变成了廊沿,要返工吗?

第一次出图时,"小凳子"被画成了"坐在木屋廊沿上"。**不用返工。**这里有个重要的判断标准:

- **关键属性漂移**(错了画面就不成立,比如人物年龄、朝向、核心道具)→ 返工;
- **次要属性漂移**(错了也不影响画面表达,比如凳子还是廊沿)→ 放行。

提示词的约束名额有限,全都锁死反而挤掉重要指令的权重。**只锁"错了就返工"的东西。**

---

## 二、第二堂课:风格出不来 = 你在逆着模型的"默认审美"硬掰

### 每个模型都有自己的"默认审美"

这是理解一切"风格出不来"的钥匙:**每个生图模型都有训练数据带来的默认偏好**。niji 7 的默认审美是**现代高精度二次元**——锐利的线条、精致的光效、高饱和的色彩。

而吉卜力的视觉特征是什么?**复古手绘、水彩背景、平涂赛璐璐、低饱和柔色**——和 niji 7 的默认审美**逐项相反**。

这时你只写一个 `Studio Ghibli style`,就像在急流里插一根小旗子——一个词的权重根本压不过整个模型的先验。出来的必然是"niji 7 味的精致二次元里有个小男孩",而不是吉卜力。

### 遇到这种情况,两条路

**路线 A(省力):顺着默认走,换工具。**
吉卜力这种复古手绘风在 niji 6 的舒适区里,上面那条修正版提示词在 niji 6 上顺水推舟就出片。**能顺默认就别逆默认,这是第一选择。**

**路线 B(可行但费力):逆着默认走,把风格词堆够。**
如果因为其他原因必须用 niji 7(比如它的构图/细节你更喜欢),就不能只写一个风格词——要把"吉卜力"**拆成一串具体的视觉特征**,再把参数压低:

```
1980s Ghibli anime film still, retro cel animation, a little boy sitting alone
on a small wooden stool in front of an old wooden house, seen in side profile,
gazing at distant mountains, an old photograph resting loosely in his hands on
his lap, warm sunset backlight, hand-painted watercolor background, flat cel
shading, soft muted earthy colors, subtle film grain --niji 7 --raw --stylize 50 --ar 4:3
```

实测结果:**四项判定全部命中**——平涂赛璐璐线条(不是 niji 7 的锐利现代线)、水彩手绘背景、低饱和土色、柔和夕照,复古质感完整出片,动作也全对。

拆解一下这条 prompt 的三件武器:

| 武器 | 内容 | 作用 |
|---|---|---|
| **风格特征词堆** | `1980s ... film still` / `retro cel animation` / `hand-painted watercolor background` / `flat cel shading` / `soft muted earthy colors` / `subtle film grain` | 用 6 个具体特征词替代 1 个笼统的"Ghibli style",合力压过默认审美 |
| **低 stylize** | `--stylize 50` | 调低模型"自由发挥"的力度,更听文字的 |
| **--raw** | `--raw` | 进一步关掉美化倾向 |

**一个实测冷知识**:我们还对比测了加不加 `--no glossy, modern digital anime...`(负面排除)的版本——风格层几乎没差别。**真正起作用的是特征词堆 + 低 stylize**,负面词在这个场景里不是关键。所以别迷信 `--no`,先把正面描述写具体。

> 🔑 **口诀:风格出不来,先问自己——我是在顺这个模型的默认,还是在逆它的默认?顺默认,极简提示词就够;逆默认,要么换工具,要么把风格拆成一串具体特征词 + 压低 stylize。**

---

## 三、总结:出图不对,按这个顺序排查

**第一步:动作/姿态错了?→ 做减法。**
- 检查有没有互相矛盾的动作(看照片 vs 望山);
- 检查关键属性是不是只靠一个弱信号词在扛(方向、年龄、数量都是重灾区);
- 砍掉重复的情绪形容词,情绪交给光线和构图。

**第二步:风格错了?→ 辨顺逆。**
- 顺默认:换到擅长这个风格的模型/版本,提示词反而要极简;
- 逆默认:风格拆成具体特征词堆上去,`--stylize` 压低,加 `--raw`。

**第三步:还有小偏差?→ 分级处理。**
- 关键属性漂移 → 针对性补锚点重跑;
- 次要属性漂移 → 放行,别为一个凳子牺牲整体。

**最后才轮到"是不是这个工具不行"。**这次的案例里,连第三步都没走到,问题就全解决了——大多数时候,锅在提示词,不在模型。

---

*本文两条修正版提示词均为 2026-07 实测,niji 6 版一次命中,niji 7 版四项风格判定全中。测试参数如文中所示,重跑存在正常的抽卡波动,漂移时按第三步分级处理即可。*
