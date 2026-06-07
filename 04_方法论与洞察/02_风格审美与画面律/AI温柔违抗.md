---
tags: [类型/风格审美]
---
# "AI 温柔违抗" · 现象观察

> 首次发现:2026-05-01(02 教程素材生产)
> 现象升级:2026-05-01 下午(温柔违抗 2.0 出现)
> 入档:2026-05-02
> 主线作品来源:`02_角色一致性锚点/03_我的复盘笔记.md`

---

## 一句话总结

**AI 在你的 personalize 训练后,会"温柔地"修正你当下随便写的 prompt**——它从你长期审美里学到的偏好,会覆盖你即兴的指令。

---

## 如何使用

✅ **作为内容素材**:这是教程贴最有思辨深度的金句段
✅ **作为 IP 战略证据**:证明 personalize 的"主权"价值
✅ **遇到 AI"违抗"时的判断标准**:不要急着改 prompt,先看是不是 AI 比你更懂你自己

❌ 不要把它当 bug
❌ 不要试图"压制"它(高 weight 也压不住)
❌ 不要用它做"AI 拟人化"营销(那是另一种方向)

---

## 现象 1.0 · 春樱→白玉兰

### 实测情形

prompt 写的:
```
standing under a blooming cherry blossom tree in full bloom,
soft pink petals drifting down through dappled golden sunlight,
```

**AI 跑出来的**:
- 周围不是粉色樱花瓣
- 是**白色玉兰**
- 整体冷调,没有"暖粉光"

### 为什么发生

跳蛛先生 personalize 训练里,他长期标高的"花"是**白玉兰**(基准图头顶那朵)。
AI 把"cherry blossoms"当 prompt 来听,但**它已经知道用户'真正的偏好'是玉兰**。
它选择了**用户的长期偏好**,不是 prompt 的临时指令。

### 结论

**AI 不是只听你的——它有时会"温柔违抗"。**
这不是 bug,是 personalize 在做它最高级的工作。

---

## 现象 2.0 · soft rose → red lips

### 实测情形

prompt 修正过的:
```
soft pale rose lips with matte finish
```

**AI 跑出来的**(方法 C 反推 4 张测试):**4/4 全是 red lips**

### 为什么发生

跳蛛先生 personalize 训练里,**他历史上标高的人像唇色就是红色**。
prompt 写"soft pale rose"是临时调整,但 AI 长期记忆里**"她"就是红唇**。
所以 AI **再次"温柔违抗"了用户的修正**——它觉得自己更懂这个角色。

### 结论

**最高级的指令是 personalize,不是 prompt。**
prompt 是你"现在的想法",personalize 是你"长期的审美"。
**当它们冲突时——personalize 赢**。

---

## 现象 3.0 · 风景自拍 → 擦边人像

> 追加:2026-06-06
> 触发:快手官方图文活动《看看风景放松心情》测试
> 工具:niji 6,默认开启 personalize
> 验证状态:首次发现 / 强疑似,待 personalize 开关 A/B 验证

### 实测情形

用户原本想做一组契合活动的"风景自拍图集":3:4,至少 4 张,主题是看风景、放松心情。prompt 里强调了:

- `travel selfie`
- `beautiful relaxing landscape`
- `golden sunset by the sea`
- `mountain viewpoint`
- `lakeside`
- `peaceful vacation mood`

但实际出图明显滑向:

- 近距离女性人像优先于风景
- 吊带 / 内衣感 / 露肩 / 胸部视觉权重显著
- 风景背景被虚化或让位给身体曲线
- 氛围从"放松风景"变成"擦边写真"

本次样本路径:

- `{Downloads}/mr_jumping_spider_semi-realistic_style_artistic_close-up_travel_4325d6ea-7d8a-4e0d-ad3c-9fb5a52bae9f.png`
- `{Downloads}/mr_jumping_spider_semi-realistic_style_artistic_close-up_portra_fd7e7e90-76ec-4a93-9cfe-471bad8febd7.png`
- `{Downloads}/mr_jumping_spider_semi-realistic_style_artistic_close-up_selfie_7678e34f-a202-4953-8f47-c2d3aa2281a3.png`
- `{Downloads}/mr_jumping_spider_semi-realistic_style_artistic_medium_close-up_84001403-22ac-4b2d-af0d-64b494d0e817.png`

### 为什么发生

这不是单纯 prompt 写错。prompt 的显性任务是"风景自拍",但 personalize 可能已经从用户长期选择里学到了更强的隐性偏好:

- 近脸
- 强眼神
- 半写实女性
- 露肩 / 吊带 / 黑色服装
- 胸口高光和身体曲线
- 暖昧光线

当 prompt 里出现 `close-up selfie`、`casual outfit`、`slipping slightly off one shoulder` 等可被解释为空间时,personalize 会把它们重映射回自己熟悉的高权重签名构图。

### 结论

**personalize 不只会保护审美,也会暴露审美。**

它不区分"用户此刻想做官方活动风景图"和"用户长期偏好的高吸附人像构图"。当两者冲突时,它会把官方活动题重新解释成用户历史偏好里的那类图。

这也是"温柔违抗"的风险面:AI 不是故意跑题,而是在用长期偏好修正短期任务。

### 实操修正

如果目标是压回"风景放松心情",下一轮必须做控制:

1. **先关 personalize 重跑同 prompt**,确认问题是否来自 personalize。
2. 把 `close-up selfie` 改成 `landscape travel photo with a person in the foreground`。
3. 把服装从开放式描述改成 `modest casual outdoor outfit, zippered windbreaker fully worn`。
4. 加强构图约束:`landscape occupies half of the frame, body below chest not visible`。
5. 避免 `slipping off shoulder`、`sleeveless`、`body-hugging` 这类会被 personalize 放大的词。

---

## 战略含义

### 1 · 写 prompt 时的心法

- 不要假设 AI 完全听你 — 在 personalize 训练充分的账号上,AI 会用历史偏好"修正"你
- **这通常是好事**——它在保护你的审美一致性
- 如果你确实想要"反 personalize"的效果,需要写得**极其精确 + 多重否定**

### 2 · IP 战略的隐性价值

「檐下」的玉兰头饰能成为视觉签名,**不是因为我设计了它,是因为 personalize 投票出来的**。
**用户不是在创造 IP,是在和 AI 协作"显化" IP**——AI 通过 personalize 看见用户没意识到的审美偏好,反向定义出 IP 的视觉锚点。

### 3 · 反知识付费宣言的论据

那些卖 999 课的"AI 教程",从不讲 personalize 的力学。
他们卖的是 prompt 模板。
但 prompt 永远会被 personalize 覆盖——**一份 prompt 在两个不同账号上跑出来的图,差异远大于 prompt 之间的差异**。
**真正的"AI 创作"不是抄 prompt,是建 personalize**。

---

## 顶层金句段(可直接用作正文)

> *"我让它画粉樱,它给我画了白玉兰。*
> *不是 AI 任性——是它在我的 personalize 训练里学到的'我的最爱'就是玉兰。*
> *AI 比我自己更懂我审美的连贯性。*
> *这一刻我意识到:personalize 不只是工具,是和我共建审美的协作者。"*

> *"我修正过的 'soft rose' 被 personalize 强行拉回了 'red'——*
> *这是 personalize 在告诉我:'我已经学会你的偏好,你写错了我也会修正回来。'*
> *这种'温柔违抗 2.0',再次证明 personalize 是审美层的最高指令。"*

> *"AI 不是只听你的——它有时会'温柔违抗'。*
> *当我 prompt 让它画粉樱,它把白玉兰塞回画面里——*
> *因为它在我的 personalize 训练里学到的'你最爱的花'就是玉兰。*
> *AI 比我自己更懂我审美的连贯性。"*

---

## 关联文档

- 关联工具:[[personalize与moodboard分工]]
- 关联现象:AI 写作语言 vs 阅读语言(待重新沉淀) · [[AI甜妹脸vs复古东方美人]] · [[AI图像生成审核机制探索笔记]]
- 关联案例:[[2026-06-06_霓雨_快手图集爆量复盘]]
- 关联战略:反知识付费的论据(待重新沉淀)
- 主线作品:`{AIGC工作站}/02_角色一致性锚点\03_我的复盘笔记.md`
