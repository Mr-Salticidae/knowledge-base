---
tags: [类型/协作工具链, 主题/skill调用, 主题/视频脚本]
入档: 2026-06-04
视频标题: Skill Is All You Need
风格: 极简知识卡片流 · 克制而不僵硬 · 活泼而不轻浮
时长目标: 约 90 秒（2700 帧 @ 30fps）
平台: B站横版 1920×1080
---

# Skill Is All You Need · 视频脚本

---

## 场景总览

| # | 场景 | 帧数 | 时长 | 组件 | accent |
|---|---|---|---|---|---|
| 0 | 封面 | 0–60 | 2s | CoverScene | — |
| 1 | 钩子：AI 每天失忆 | 61–210 | 5s | KnowledgeCard | cold |
| 2 | 比喻：岗位手册 | 211–360 | 5s | KnowledgeCard | cold |
| 3 | Skill 是什么 | 361–510 | 5s | KnowledgeCard | cold |
| 4 | 什么时候该用 | 511–660 | 5s | KnowledgeCard | warm |
| 5 | 旧方法的问题 | 661–810 | 5s | KnowledgeCard | cold |
| 6 | 新方案：SKILL_INDEX | 811–1020 | 7s | KnowledgeCard | warm |
| 7 | 三步上手（代码） | 1021–1230 | 7s | CodeCard | — |
| 8 | 实测结果 | 1231–1380 | 5s | KnowledgeCard | warm |
| 9 | 结尾 | 1381–1500 | 4s | OutroScene | — |

**总帧数：1500 帧 = 50 秒**

> 注：如需 B 站最佳时长（90秒），在第 6-8 场景之间可插入「避坑提示」和「好 Skill 的标准」两张卡片，各 5 秒。

---

## 逐场文案

### Scene 0 · 封面（0–60f · 2s）

```
主标题：Skill Is All You Need
副标题：让 AI 记住你的规则，而不是每次重新教
标签：AI工具 · Cowork · SKILL_INDEX
```

动效备注：标题从下淡入，副标题延迟 12f，标签延迟 24f 逐个出现。

---

### Scene 1 · 钩子（61–210f · 5s）

```
label：问题
title：你的 AI 每天都在失忆
body：每次开新对话，它就忘了你喜欢的格式、
      你反复强调的规则、上次踩过的坑。
      你得从头教。
```

动效备注：body 第二行延迟 8f，第三行延迟 16f——营造逐行揭示感。  
accent：cold（冷色 = 问题/严肃）

---

### Scene 2 · 比喻（211–360f · 5s）

```
label：比喻
title：Skill 就是它的岗位手册
body：你雇了一位助理，很聪明，但每次上班前都失忆了。
      Skill 就是你给它的那本手册——
      角色、规则、禁忌、输出格式，全部写死在里面。
```

动效备注：「手册」二字用 warm 色高亮（`<span>` 包裹，加 accent color）。  
accent：cold

---

### Scene 3 · Skill 是什么（361–510f · 5s）

```
label：概念
title：一个 .md 文件，三件事
body：① 角色说明——它在这个任务里是什么专家
      ② 流程规则——遇到不同输入怎么处理
      ③ 输出约束——交付什么格式，哪些话不能乱说
```

动效备注：三条用 `fadeLeftStyle` 逐条入场，每条间隔 10f。  
accent：cold

---

### Scene 4 · 什么时候该用（511–660f · 5s）

```
label：判断
title：当你反复在教 AI 同一件事
body：Prompt 优化类 → 每次都要重新说规则
      工作流辅助类 → 固定步骤每次都一样
      工具语法类   → 不想每次查文档
```

动效备注：每行用 warm 色「→」箭头，增加节奏感。  
accent：warm（暖色 = 行动/解法）

---

### Scene 5 · 旧方法的问题（661–810f · 5s）

```
label：问题
title：装上去的 Skill 下次可能找不到
body：Cowork 每次启动都会生成一串随机编号（UUID）。
      安装路径跟着变，Skill 就失联了。
      就像把手册锁进每天换地址的保险柜。
```

动效备注：「每天换地址的保险柜」用 secondary 色斜体，强化比喻记忆点。  
accent：cold

---

### Scene 6 · 新方案（811–1020f · 7s）

```
label：解法
title：把手册放在固定的地方
body：知识库的路径不会变。
      SKILL_INDEX.md 是所有 Skill 的目录——
      告诉 Claude 一次，它就知道去哪找、什么时候用哪本手册。
      
      只需要一句开场白，全部自动搞定。
```

动效备注：「SKILL_INDEX.md」用 `FONT.mono` + accent 色显示，像代码。  
accent：warm

---

### Scene 7 · 三步上手（1021–1230f · 7s）

```
caption：每次新对话只需要这一句话
code：
你好，我的知识库在 D:\AIGC工作站\知识库，
请先读取 SKILL_INDEX.md，
后续对话中自动判断何时调用哪个 skill。
```

动效备注：代码块整体 fadeUp 入场，caption 延迟 20f 出现。  
用 CodeCard 组件，背景用 `COLORS.surfaceHover`。

---

### Scene 8 · 实测结果（1231–1380f · 5s）

```
label：实测
title：两次触发，两次成功
body：2026-06-04，设计虚拟形象的对话中，
      aigc-prompt-optimizer 和 aigc-postmortem
      均被自动识别并完整执行，无一遗漏。⭐⭐
```

动效备注：「⭐⭐」用 warm 色，比正文略大（TYPE.h3）。  
accent：warm

---

### Scene 9 · 结尾（1381–1500f · 4s）

```
主标题：Skill Is All You Need
副标题：把你的流程固化成手册，让 AI 每次都能立刻上手
署名：@跳蛛先生 · D:\AIGC工作站\知识库
```

动效备注：与封面呼应，主标题字号和位置完全相同，形成闭环感。

---

## Remotion 实现备注

### 主文件结构

```
src/
├── Root.tsx              # 注册 Composition
├── SkillIsAllYouNeed.tsx # 主合成，用 <Sequence> 拼接所有场景
├── design-tokens.ts      # 颜色/字号/间距变量
└── scenes/
    ├── CoverScene.tsx
    ├── KnowledgeCard.tsx
    ├── CodeCard.tsx
    └── OutroScene.tsx
```

### Sequence 拼接示例

```tsx
export const SkillIsAllYouNeed: React.FC = () => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={61}>
        <CoverScene frame={frame} fps={fps} />
      </Sequence>
      <Sequence from={61} durationInFrames={150}>
        <KnowledgeCard
          frame={frame - 61} fps={fps}
          label="问题"
          title="你的 AI 每天都在失忆"
          body="每次开新对话，它就忘了..."
          accentColor="cold"
        />
      </Sequence>
      {/* 依此类推... */}
    </AbsoluteFill>
  );
};
```

---

## 关联文档

- Skill 内容来源：[[SKILL入门完全指南]]
- Remotion Skill：`D:\AIGC工作站\知识库\07_skill存档\remotion\SKILL.md`
- 生产闭环参考：[[AIGC_Skill到Remotion视频闭环]]
