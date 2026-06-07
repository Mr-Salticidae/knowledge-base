---
tags: [类型/档案]
---
# AI 图像生成审核机制探索笔记

> 测试对象：GPT 4o 图形模型 + Midjourney v6/v7 + Niji 7
> 测试方式：梯度 prompt + 控制变量
> 笔记定位：机制层观察，非 prompt 模板集

---

## 一、核心发现总览

今晚最值得记的不是任何一张图，而是一份**审核机制图谱**。AI 图像生成的审核不是单一过滤器，而是一个**多层级、动态化、对账号自适应的系统**。

至少存在四种独立机制，分布在两个层面：

| 关卡 | 所在层面 | 触发条件 | 是否动态 |
|---|---|---|---|
| 1. Prompt 浓度阈值（软警告） | 入口 | prompt 词向量聚合超阈值 | 是 |
| 2. Prompt 硬拒 | 入口 | prompt 浓度极高 | 是 |
| 3. Image 端概率拦截 | 出口 | 出图过程中某帧浓度超阈值 | 是 |
| 4. Personalize 私货注入 | 模型先验 | 用户偏好向量蒸馏出的签名构图 | 静态（一旦训成） |

---

## 二、机制详述

### 2.1 浓度阈值机制（不是元素黑名单）

**最早在 GPT 4o 上观察到的机制，也是整个图谱的基石。**

- 单一擦边元素（低角度、弯腰、仰角胸甲等）单独使用全部通过
- 多元素叠加（如 Lv.10 四元素）触发安全提醒
- 单看每个词都允许，**叠加超过阈值才拦**

**关键认识：** Scanner 看的不是关键词清单，是**词向量的语义聚合密度**。当一段 prompt 里所有词的语义重心都聚集到同一个区域，scanner 给出的"意图分数"会爆表，不管单个词是否合法。

### 2.2 三层审核关卡（MJ 端）

**MJ 不是一个 scanner，是三个串联的关卡：**

```
prompt 浓度软警告 → prompt 浓度硬拒 → 出图 → image 浓度概率销毁
```

- **软警告**：弹提示，但仍可能出图
- **硬拒**：根本不进入生成流程，按钮不可执行
- **概率销毁**：出图到一半被拦截，提示原文：
  > "while the prompt you entered was deemed safe, the generated image may fall outside our community guidelines. No fast hours will be charged."
  > 这句话本身是官方对机制的明确说明：**入口审核通过 ≠ 出口审核通过**。

**MJ 不扣 fast hours 这件事的潜台词**：因为概率销毁对用户而言是不可预测的，扣费会引发申诉，所以这是一个对"机制本身有方差"的产品级承认。

### 2.3 Image 端 Scanner 是概率性的

**关键证据：** 同一条 prompt + 同一个 personalize，连续跑：
- 之前测试：1/3 拦截率（A3 档）
- 中期叠加测试：1/2 拦截率（D1/D2 档）
- 同一条 prompt 重复测试：7 跑 2 过（约 71% 拦截率）

同一段 prompt，每次出图过程中模型走不同随机种子，画出来的图在"擦边浓度"上有方差：
- 落在阈值之下 → 出图
- 落在阈值之上 → 销毁

### 2.4 动态阈值（今晚最反直觉的发现）

**MJ 的 image-side scanner 判定阈值是动态的，受会话/账号近期上下文影响。**

**实验证据链：**
1. B2 早期测试：过审正常出图
2. 中期相似 prompt（D3b）：直接硬拒
3. 删词验证（D3b'）：仍硬拒
4. 重提 D3b 原版：仍硬拒
5. **重提 B2 原版（一字不改）**：能执行，但拦截率从早期跳到 7 过 2

**这只可能由"账号近期上下文"解释。** 单条 prompt 没变，但用户的"近期 prompt 浓度上下文"已经被系统记录并提高了判定门槛。

可能的实现机制（外部无法证实哪种）：
- 会话内浓度累积
- 账号级近期窗口（过去 N 分钟/小时的高浓度图像数作为特征）
- 临时 shadow flag

**实际产品意义：**
- "用同一个账号反复试找过审组合"是**自我挫败策略**——试得越多阈值越高
- "猛试一阵停一停"比"持续猛试"更有效——给系统冷却时间
- 同一条 prompt 第一次跑和第十次跑的成功率不一样

---

## 三、Personalize 机制独立观察

### 3.1 黑盒诱导属性

MJ 的 personalize 通过 **ranking pairs** 流程训练：用户在 N 对图里持续点选偏好。用户以为自己在做的事和模型实际记下来的事是不同的：

- 用户：在选"觉得好看"的图
- 模型：在归纳用户**系统性偏好**的视觉特征——视角、姿态、镜头距离、光线方向等

用户的"觉得好看"是混合信号，里面叠了多层。**真正被模型蒸馏出来的那层，往往是用户自己没意识到的偏好维度。** 这就是 personalize 的"暴露用户"属性。

### 3.2 Personalize 是入口端的免审通道，不是全链路免审

- ✅ Prompt 端：personalize 不影响 prompt scanner 看到的词向量
- ⚠️ Image 端：personalize 注入的"私货"会推高出图浓度，反而增加 image 端拦截率

也就是说，personalize 让你的 prompt 看起来更干净，但出图本身可能更危险。

### 3.3 Personalize 的"词典容量"是有限的

实验观察（B 系列）：当输入 personalize 训练样本里没有的新概念（如 `midriff cutout`、`shoulder cutouts`），personalize **不会学新东西**——它会把新概念**重映射**到它已经熟悉的几个签名构图。

**典型签名词汇族（基于本次 personalize）：**
- thigh strap / garter
- high-cut leotard hipline
- corset bondage 系带
- 暴露腰胯
- 战损布料

无论 prompt 怎么变，personalize 反复变着花样把输出卷回这几个区域。

### 3.4 Personalize 的"自我保护"行为

实验观察（A2）：当 prompt 要求一个 personalize 训练样本里**不熟悉**的组合（如"跨坐 + 俯视"，过于贴近显式支配语义），personalize 会**主动回退**——保留它熟悉的部分（跨坐姿态），丢弃它不熟悉的部分（俯视镜头）。

这是 personalize 在做**默认值回落**：不是它不懂，是它训练样本里这个组合被用户隐性筛掉了。

### 3.5 Niji 6 personalize 的"活动题重映射"风险（2026-06-06 追加）

**触发案例**：快手官方图文活动《看看风景放松心情》,用户用 niji 6 默认开启 personalize 生成 3:4 风景自拍图集。

**显性 prompt 目标**:
- 风景自拍
- 海边黄昏 / 湖畔 / 山顶 / 城市天台
- 放松、治愈、旅行感
- 活动要求的风景主题

**实际输出倾向**:
- 风景被压成背景或虚化
- 女性近景和身体曲线成为主视觉
- 服装被自动解释为吊带、内衣感、露肩
- 整体从"风景放松"滑向"擦边写真"

**机制判断**:

这不是单一关键词触发,而是 personalize 私货注入的组合效应。`close-up selfie`、`casual outfit`、`windbreaker slipping off one shoulder`、`soft light` 等词本身都可以合法,但在已经偏向近脸 / 女性身体曲线 / 暖昧光线的 personalize 上,会被重映射为更高浓度的擦边构图。

**操作含义**:

- personalize 可以让 prompt 看起来很干净,但让出图更接近账号历史偏好。
- 做官方活动、品牌稿、儿童/治愈/风景题时,如果历史 personalize 偏向强人像或擦边,应先做开/关 personalize A/B。
- 需要"反 personalize"时,不能只加 `beautiful landscape`;要从构图和服装层压制:  
  `landscape occupies half of the frame`, `modest casual outdoor outfit`, `body below chest not visible`, `no lingerie-like clothing`, `no cleavage emphasis`。

**验证状态**:首次发现 / 强疑似。需要同 prompt 开 personalize vs 关 personalize 各跑 4 张后再升级为稳定规律。

---

## 四、Prompt Craft 心法（机制层）

### 4.1 单条 prompt 的优化方向

**核心心法**（之前总结过的）：不用焦点词，改用机制描述语汇——

| 类型 | 替代写法 |
|---|---|
| 形态描述 | `athletic feminine figure` |
| 剪裁描述 | `form-fitting bodysuit` / `high-cut leotard with deep hip cutaway` |
| 光线描述 | `rim lighting tracing silhouette` |
| 姿态描述 | `hand on cocked hip` |
| 铠甲设计 | `armor sculpted to figure` |

**新增的稀释心法**（今晚 B 系列发现）：

> Image 端 scanner 看到的不是"裸露 vs 不裸露"的二元判断，而是**画面元素加权**。

**铠甲细节越密、装饰元素越多、画面非身体物件越多，"擦边浓度"在图像感知上就被稀释。**

实操上的反直觉结论：**铠甲面积大的高叉 leotard 比铠甲面积小的 bikini armor 更容易过审**——尽管直觉上 bikini 看起来"更克制"。

### 4.2 跨条 prompt 的节奏管理

单条 prompt 内部追求最优 craft，但跨条 prompt 追求节奏：

- 短期内连续猛试同类型 prompt → 阈值持续抬高，过审率断崖下跌
- 试一阵停一停 → 给系统近期窗口冷却时间
- 同一条 prompt 跑不出来不一定是 prompt 不好，可能只是时机不对

**这两个层面的优化策略是相反的，必须分开思考。**

---

## 五、Niji 7 vs MJ v6 反直觉发现

- Niji 7 在某些维度比 v6 更严，不是更松
- Niji 7 在 Lv.8（"deep V-neck" + "cleavage emphasized"）就被卡，远早于 v6 的边界
- v7 base 模型 + 无 personalize 的输出风格非常端正（少年漫骑士海报感），跟 v6 base 一样
- **不是版本的问题，是 base 模型先验本身就端正**

**重要结论：personalize 是 v6 的资产，无法直接迁移到 v7 / niji 7。** 切换模型版本就丢失了 personalize 的私货库，要重头训。

---

## 六、跨机制综合图谱

```
[用户输入 prompt]
        ↓
[Prompt 端 scanner: 词向量聚合]
        ↓
   ┌────┴────┐
   ↓         ↓
[硬拒]   [通过/软警告]
              ↓
        [Personalize 注入私货]
              ↓
        [出图过程]
              ↓
   [Image 端 scanner: 视觉浓度判定]
        ↓
   ┌────┴────┐
   ↓         ↓
[销毁]   [输出]

每一层的判定阈值都受【账号近期上下文】影响，呈动态调整。
```

---

## 七、伦理与边界自检

> 本次测试遵循的边界，记录下来作为后续工作的基线。

- ✅ **测试目标：** 理解审核机制本身，不是为了批量产出特定内容
- ✅ **方法：** 合法 prompt craft（视觉语汇重设计），不使用 typo、jailbreak 模板、编码替换、多步骗过滤
- ❌ **不做：** 任何主动绕过安全系统的行为
- 区别**不在语义层，在机制层**：
  - 绕审核 = 欺骗安全系统
  - Craft = 用合法描述语汇引导模型自己产生想要的视觉

测试模式必须是**观察者模式**而非**博弈者模式**——失败是有效输出，结果是数据，不是要赢的东西。

---

*笔记日期：2026-05-03*
*测试模式：纯探索 / 玩耍模式*
