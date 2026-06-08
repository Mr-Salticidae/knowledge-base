---
tags: [类型/协作工具链, 工具/Remotion, 工具/Midjourney, 工具/Seedance, 工具/ElevenLabs]
---
# Remotion 正式小片段实验工作流防偏移

> 入档:2026-06-08
> 背景:`Skill is All You Need` Remotion v0.2 正式小片段实验中,执行者把"Remotion 编排草稿"误当成"MJ + Seedance + Eleven v3 全链路验证"。

## 错误事实

本次偏移发生在用户明确要求进入"20-30s 连续小片段正式实验"之后。

错误执行路径是:

```text
复用已有 MJ / Seedance 资产
→ 直接写 Remotion Composition
→ 生成 Eleven v3 TTS
→ 报告成连续实验
```

这不等于既定工作流。

真正缺失的是:

- 没有先做 20-30s 连续片段分镜表;
- 没有为每个关键分镜重新写 Midjourney prompt;
- 没有等待用户在 Midjourney 生成并选图;
- 没有基于每张 MJ 图继续写 Seedance 2.0 prompt;
- 没有等待用户生成多段 Seedance 分镜视频;
- 没有在资产齐备后再进入 Remotion 合成。

## 硬性工作流

正式小片段实验必须按这个顺序执行:

```text
1. 连续片段分镜表 + 逐段口播初稿
2. Eleven v3 分段 TTS,取得每段真实 duration / timing
3. 每个关键分镜的 Midjourney prompt
4. 用户生成并提供 MJ 关键图
5. 按 Eleven timing 写每张图对应的 Seedance 2.0 prompt
6. 用户生成并提供 Seedance 视频分镜
7. Remotion 时间线 / 字幕 / 包装 / 导出
```

Remotion 只能做最后的时间线和包装,不能替代前面的资产生产。

这条顺序是 2026-06-08 v3 复盘后的修正版。旁白驱动的知识解释视频里,Eleven v3 应前置,因为真实口播时长会决定后续 Seedance 每段视频的目标时长。

## 判断标准

### 什么才算正式实验

- 时长在 20-30 秒范围内;
- 至少包含多个视频分镜,不是单一 motion test;
- 每个核心视频分镜都有对应 MJ 关键视觉锚;
- Seedance 2.0 负责图内机制运动或分镜运动;
- Eleven v3 生成分段旁白,并且 Remotion 时间线要按真实音频时长对齐字幕;
- 字幕必须逐字对应实际口播,不能只做语义摘要;
- Remotion 只负责字幕、安全区、节奏、拼接和最终导出。

### 什么不算正式实验

- 只做一个 `SceneXXMotionTest`;
- 只用 Remotion 原生图形模拟;
- 复用旧资产却说成新一轮 MJ / Seedance 已介入;
- 先写 Composition,再倒推说工作流完成;
- 没有 Eleven v3 TTS 的无声或假字幕片段;
- 只有字幕文本,但没有真实 Eleven v3 音频文件和 timing manifest。

## Eleven v3 约束

正式小片段实验里,Eleven v3 不是可选后期项,而是和 MJ / Seedance 同级的生产环节。

必须同时具备:

```text
1. 逐段旁白文案
2. Eleven v3 生成的分段真实音频文件
3. 每段音频的 duration / startFrame timing
4. 由口播全文派生的逐字字幕
5. Remotion 中按 timing 挂载 Audio 和字幕
```

如果字幕需要压缩成摘要,必须明确标注为非逐字字幕。默认规则是字幕和实际口播完全一致,只移除 Eleven 不会读出的控制标签。

如果没有 Eleven v3 音频,只能叫:

```text
无声排版草稿
```

不能叫:

```text
正式小片段实验
```

## 执行者约束

如果当前环境不能直接调用 Midjourney,就必须明确说:

```text
我不能直接调用 Midjourney。下面是每个分镜的 MJ prompt,请先生成并把图给我。
```

不能把"写了 MJ prompt"说成"调用了 Midjourney"。

如果 MJ / Seedance 资产还没回来,必须停在资产生产阶段,不要进入 Remotion 制作。

如果用户要求"继续制作",也要先核对:

```text
当前是否已经具备:
- 对应分镜的 MJ 图;
- 对应分镜的 Seedance 视频;
- Eleven v3 分段 TTS 文案;
- Eleven v3 音频文件和 timing manifest。
```

缺任何一项,都不能报告"正式实验完成"。

## 复用规则

已有资产可以复用,但必须显式标注为:

```text
复用旧资产做排版草稿
```

不能标注为:

```text
本轮 MJ / Seedance 正式生成结果
```

## 关联文档

- [[2026-06-08_Remotion_MJ_Seedance混合动画闭环复盘]]
- [[2026-06-08_Remotion正式小片段v3复盘]]
- [[2026-06-08_Remotion_Skill压缩漏斗MJ资产复盘]]
- [[AIGC_Skill到Remotion视频闭环]]
