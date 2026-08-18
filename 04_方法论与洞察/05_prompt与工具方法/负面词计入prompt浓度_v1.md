---
tags: [类型/方法论]
---
# 负面词计入 prompt 浓度（--no 反噬律）

> 首次沉淀:2026-06-17(冷艳女侠定妆照连撞 3 次审核,删掉 --no 后一次过)
> 验证状态:⭐ 首次发现 / 强疑似——单案例验证,需背靠背 A/B 升级为稳定规律
> 关联机制:[[AI图像生成审核机制探索笔记]] 的「浓度阈值机制」

---

## 一句话总结

**`--no` 里的词照样被 prompt 端 scanner 当 token 读入,计入语义聚合浓度。** 对写实真人/擦边这种本就贴近审核线的题,一长串带 `skin / body / face / fingers` 的 `--no` 不会帮你"排除",反而把整条 prompt 的语义重心进一步推向"真人身体/脸",亲手顶过阈值触发审核。

---

## 案例

冷艳孤傲女侠定妆照(古典武侠写实 · 月白 · 高马尾 · 额间朱砂),连续被拦 3 次:

```
... --no text, watermark, logo, blurry, low quality,
        cosplay, plastic skin, oversaturated, extra fingers,
        modern clothing, harsh facial shadows
```

报错:`Sorry! The AI Moderator is unsure about this prompt.`

**删掉整段 `--no` 后,同骨架 prompt 正常出图。**

触发嫌疑词(全在 `--no` 里):`plastic skin` / `harsh facial shadows` / `cosplay` / `extra fingers`——`skin / facial / fingers / cosplay` 全是人体与真人脸语义,叠加推高了"写实真人"浓度。

---

## 机制解释

承接 [[AI图像生成审核机制探索笔记]]:prompt 端 scanner 判的是**词向量语义聚合密度**,不是黑名单。它**不解析 `--no` 的"排除"语义**——在它眼里 `--no` 后面的词和正文的词一样,都是推高浓度的 token。

所以:
- 正文写 `realism + close-up + skin` 已经接近阈值;
- `--no` 再补 `plastic skin / harsh facial shadows / fingers`,等于又往同一语义区域加了一把火;
- 浓度越线 → 入口软警告/硬拒。

这跟知识库另一条规律同源:**「删词比加词更容易过审」**(见 [[prompt极简化原则_v1]])。`--no` 是最容易被忽略的"隐形加词"。

---

## 操作规则

| `--no` 里的词 | 处理 |
|---|---|
| 纯画质项:`text, watermark, logo, blurry, low quality` | ✅ 安全,保留 |
| 人体/皮肤/脸/手相关:`plastic skin, bare skin, harsh facial shadows, extra fingers, cosplay` | ⚠️ 对写实真人题,删掉比留着安全 |
| 防穿帮项:`modern clothing` 等 | 视情况,担心浓度就移到正文正向描述(如 `period-accurate hanfu`) |

**心法**:写实人像题被拦时,先清 `--no`,再清正文里的高浓度真人信号——而不是往 `--no` 里加更多负面词。负面词不是免费的。

---

## 应用记录 · 非验证(2026-08-18)

《目标是成为 Prompt 大师》第 13 期《月白》按本律**预防式**清了 `--no`——把原始 prompt 里的 `plastic skin / AI generated face / distorted features / blurry eyes / extra fingers` 全部拿掉,只留 `text, watermark, logo, low quality, out of focus face`,随后正常出图、未被拦。

⚠️ **这一条不构成第二个验证样本,本档验证状态仍为 ⭐ 强疑似。** 原因:**原始 prompt 从未被实际跑过**,不知道它会不会被拦;"清了 `--no` 之后没被拦"无法反推"不清就会被拦"。这是典型的**幸存者式归因**,按 [[复盘事实先行原则]] 不能记为证据。

真正的升级路径仍是本档「待验证」段写的那个:同一条 prompt 背靠背带 / 不带 `--no` 各跑 4 张。

**本条的价值不在证据,在用法**:本律此前只在"被拦之后救火"的场景下被调用过;第 13 期是**第一次在没被拦的情况下当默认写法用**——即把"负面词不是免费的"当成写 prompt 时的常规纪律,而不是排障手段。这个用法已编进 [[已有prompt的七步体检律_v1]] 第 6 步。

---

## 待验证

- 单案例 + 中间隔了时间,**动态阈值冷却**可能也有贡献。需同一条 prompt 背靠背带/不带 `--no` 各跑 4 张,排除时机干扰,才能从「强疑似」升级「稳定」。
- 是否所有 `--no` 词等权,还是只有人体/脸语义词显著推高浓度,待梯度测试。

---

## 关联文档

- 上位机制:[[AI图像生成审核机制探索笔记]](浓度阈值 / 动态阈值 / 三层关卡)
- 同源规律:[[prompt极简化原则_v1]](删词比加词更容易过审)
- 配套避雷:[[MJ审核避雷词表]](7 大类雷词 + 过审神器)
- 编排位置:[[已有prompt的七步体检律_v1]] —— 本律是七步体检的第 6 步「清 `--no`」
