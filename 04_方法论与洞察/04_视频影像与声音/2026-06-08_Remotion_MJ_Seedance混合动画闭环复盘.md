---
tags: [类型/IP视觉, 工具/Remotion, 工具/Midjourney, 工具/Seedance]
---
# 2026-06-08 Remotion × MJ × Seedance 混合动画闭环复盘

> 入档:2026-06-08
> 项目:Skill is All You Need / Remotion v0.2 单场景验证
> 关联 Skill:[[remotion-skill/SKILL.md]]、[[aigc-prompt-optimizer]]、[[seedance-prompt-en]]

## 事实记录（不可修改区）

- 验证场景:`scene_04_repeat_to_skill`
- 目标命题:反复教 AI 的内容,值得压缩成可复用 Skill。
- Midjourney 主图:`07_skill存档/remotion/public/assets/scene_04/mj_prompt_to_skill_key_visual.png`
- Seedance 视频:`07_skill存档/remotion/public/assets/scene_04/seedance_prompt_to_skill_motion.mp4`
- Seedance 参数:约 `4.06s`、`1280x720`、`60fps`、H.264。
- Remotion 合成输出:`07_skill存档/remotion/out/scene04-seedance-remotion-composite.mp4`
- 验证结果:Remotion 类型检查通过,单帧检查通过,短视频导出成功。

## 本轮结论

这次验证证明了一个可用链路:

```text
Remotion sceneSpecs
→ Midjourney 生成关键视觉锚
→ Seedance 让图内机制动起来
→ Remotion 叠字幕、背景、边框和最终时间线
```

这不是简单的"拿 AI 视频做素材",而是三种工具分工清楚:

- **MJ** 负责概念关系和高端静态图解。
- **Seedance** 负责图内机制运动,把 PPT 式推拉变成真实动画。
- **Remotion** 负责信息秩序,包括字幕、安全区、包装和可重复渲染。

## 为什么这次成立

### 1. 先有视觉锚,Seedance 才没有乱跑

Seedance 直接从文字生成,很容易把漏斗、气泡、手册重画成另一套风格。用 MJ 主图作为 `@Image1` 后,它保留了纸面颗粒、厚描边、漏斗结构和蓝色 Skill 手册。

这说明视频生成前最好先有一张高质量关键帧。关键帧不是装饰图,而是后续动画的视觉边界。

### 2. 动的是机制,不是镜头炫技

这段视频最有效的运动不是推镜,而是图内机制:

- 气泡靠近漏斗;
- 彩色粒子进入透明腔体;
- 粒子沿管道流向手册;
- `SKILL` 手册形成稳定输出。

这类运动直接服务概念。相比 Remotion 只做轻微缩放,Seedance 把"压缩成 Skill"这件事变成了可看见的过程。

### 3. Remotion 保留了信息层控制权

Seedance 视频本身不负责讲完整道理。Remotion 仍然叠加三段字幕:

```text
重复输入,不是经验
经过压缩,才变成流程
Skill 是可复用的工作手册
```

这让画面和论点分工清楚。Seedance 提供直觉,Remotion 提供语言和节奏。

## 可迁移方法论

### AI 视频不要直接全权接管叙事

**核心**:Seedance 适合做局部机制动画,不适合在第一轮就接管整条叙事线。

**来源**:本案例只让 Seedance 处理一个 4 秒机制段,再由 Remotion 统一包装。

**操作规则**:

1. 先用 Remotion 定 scene goal 和字幕逻辑。
2. 用 MJ 生成该 scene 的关键视觉锚。
3. 用 Seedance 只动图内最关键的机制。
4. 回到 Remotion 做字幕、外框、节奏和导出。

### 静态图变视频前要问"动哪里"

**核心**:不是所有静态图都需要动。只有当运动能解释概念关系时,才值得接 Seedance。

**来源**:本案例的运动点非常明确:输入进入漏斗,被压缩,输出到手册。

**操作规则**:

1. 先列出画面中的输入、处理器、输出。
2. 只让这三者之间的关系动起来。
3. 限制镜头运动为 very subtle push-in 或 locked camera。
4. 不要求额外转场、人物、光效或背景变化。

### Remotion 是总控台,不是普通剪辑器

**核心**:Remotion 的价值不是把素材拼起来,而是把所有 AI 资产纳入可复用的结构。

**来源**:本案例通过 `sceneAssets` 管理 MJ 图和 Seedance 视频状态,通过 composition 控制字幕、时长和包装。

**操作规则**:

1. `sceneSpecs` 只管"这一段讲什么"。
2. `sceneAssets` 记录"素材从哪里来、状态是什么、如何绑定"。
3. MJ / Seedance 文件进入 `public/assets` 后再标记 `linked`。
4. 最终输出仍由 Remotion render 生成,不要把时间线交给外部工具。

## 后续方向

1. 把 `scene_04` 的视频插入逻辑推广到其它概念 scene。
2. 每个 scene 先判断是否需要 Seedance:只有机制运动明确的才接。
3. 为 Seedance 输出建立"主视频 / 失败版 / 风格参考"归档规则。
4. 后续全片制作时,每 20-30 秒只放 1-2 个 Seedance 强动画段,其余保留 Remotion 原生解释节奏。

## 关联文档

- [[AIGC_Skill到Remotion视频闭环]]
- [[2026-06-08_Remotion_Skill压缩漏斗MJ资产复盘]]
- [[图片占位到视频替换的工作流_v1]]
- [[图生视频_ForwardOnly原则]]
- [[语言形式_思维模式_沟通成本]]
