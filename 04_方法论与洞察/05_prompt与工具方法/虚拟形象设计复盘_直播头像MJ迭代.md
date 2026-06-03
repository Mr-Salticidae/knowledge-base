---
tags: [类型/复盘, 工具/Midjourney, 主题/虚拟形象, 主题/人像prompt]
入档: 2026-06-04
---

# 虚拟形象设计复盘 · 直播头像 MJ 迭代

## 事实记录（不可修改区）

- 作品类型：直播用虚拟形象头像
- 工具：Midjourney v8.1
- 迭代轮次：8+ 轮
- 最终结果：找到可用基础版本（港风背头 + 双面材质 + 无恐怖感）
- 未解决问题：MJ 无法精确理解"龙须背头"等中文语境发型概念
- 最优 prompt 版本：见下方 D 区

---

## B. 创作思路与执行过程

**目标**：设计一个有记忆点、适合 AI 应用研究员身份的直播虚拟形象，兼具研究员严谨性和艺术家创意感。

**核心设计概念**：双面材质脸——左侧冷青色电路纹（严谨），右侧暖金橙水彩晕散（创意），两侧在鼻梁交融。

**迭代路径**：
1. 初版 2.5D 插画风 → 太平面，缺质感
2. 引入图2（Surreal 3D collectible）风格语言 → 质感提升但太欧美
3. 加 `East Asian male` → 仍偏欧美 + 多数光头
4. 加发型描述 + `--no bald` → 解决光头，但发型跑偏
5. 加年龄 `25-year-old` + 去胡渣 → 解决年龄感和恐怖感
6. 改发型为"港风凌乱背头"→ 方向对，但"龙须背头"MJ 无法识别
7. 用参考图锁定发型（层次感纹理背头）→ 接近目标
8. 加个人 personalize 全局参数 → 最终可用版本确定

---

## C. 结果分析

### 哪些决策有效

| 决策 | 效果 |
|---|---|
| 引入 `Surreal studio portrait` 开头 | 激活电影感和超现实氛围，比"portrait of"更强 |
| `octane render + cinematic detail` | 解决插画感，拉向写实质感 |
| `25-year-old + clean-shaven smooth skin` | 同时解决年龄和胡渣两个问题 |
| `circuit stops at jawline` | 电路不蔓延到脖子，消除恐怖感 |
| `normal natural human eyes + soft reflection only` | 解决机器人眼/僵尸感 |
| `--no` 补负向词（zombie, horror, aged, western features） | 从反向锁定，效果显著 |
| 加个人 personalize | 风格一致性最强杠杆，胜过单条 prompt 调整 |

### 哪些决策失效

| 决策 | 失效原因 |
|---|---|
| "龙须背头"直译英文 | MJ 不理解中文语境发型概念，需换成视觉描述语言 |
| 早期过度堆砌风格词 | 关键词互相干扰，输出混乱 |
| `--v 6.1` | 已过时，升级到 `--v 8.1` 效果明显提升 |

---

## D. 最优 Prompt 存档

```
Surreal studio portrait of a 25-year-old East Asian male AI researcher, youthful face, sharp clean jawline, clean shaven, bright natural eyes, warm friendly confident expression with subtle smile, dark hair in messy Hong Kong style slicked back look with loose strands falling forward, wet look texture with natural flyaways. Asymmetric dual material face: left half has subtle cold cyan circuit trace patterns softly embedded under skin like tattoos stopping at jawline; right half dissolves into warm golden orange watercolor ink floating into air; both sides blend naturally at nose bridge. Thin round wire frame glasses, natural human eyes with soft cyan and amber reflections. Minimalist matte black turtleneck, three quarter upward gaze, indigo background, soft ambient fill light, faint data particle bokeh. Hyperrealistic mixed with stylized aesthetics, approachable human warmth, centered composition, sharp focus, soft studio key light, cyan left and gold right rim lights, octane render, cinematic detail, premium character design. --no text, watermark, logo, blurry, glowing eyes, robotic eyes, zombie, horror, dark mood, aggressive, stubble, beard, wrinkles, aged, western features --ar 3:4 --raw
```

**附加条件**：配合个人 personalize 全局参数使用效果最佳。

---

## E. 方法论沉淀

### [人像 prompt 的"恐怖谷"排查清单]

**核心**：写实人像容易触发恐怖感，需从眼睛、皮肤侵入感、光源三点排查。

**来源**：电路纹蔓延至脖子 + 发光瞳孔导致多次出图恐怖。

**验证状态**：⚠️ 首次发现

**操作规则**：
1. 眼睛：特效只做镜片反光，不改变瞳孔本身（`natural human eyes with soft reflection only`）
2. 皮肤侵入元素：加边界锁定（`circuit stops at jawline`）
3. 表情：主动写入温度（`warm friendly expression with subtle smile`）
4. 负向词：`zombie, horror, dark mood, glowing eyes` 必加

**反例/边界**：如果本来就要做恐怖/赛博风，则反向利用这些元素。

---

### [中文语境发型需转译为视觉描述]

**核心**：MJ 无法理解"龙须背头""港风背头"等中文造型术语，需翻译成可渲染的视觉语言。

**来源**："dragon-whisker slicked-back style"无效，改用参考图后解决。

**验证状态**：⚠️ 首次发现

**操作规则**：
1. 不用中文造型名直译
2. 描述发型的**结构**（顶部/侧面/刘海的形态）+ **质感**（wet-look / layered / flyaways）
3. 最可靠方法：上传参考图用 `--cref` 或在 prompt 末尾描述"similar to [明星名] hairstyle"

**反例/边界**：部分通用发型（bob cut / buzz cut / undercut）MJ 能直接识别。

---

### [种族锁定需正负双向]

**核心**：仅加 `East Asian` 不够，需同时在 `--no` 里排除 `western features`。

**来源**：加了种族词仍多次出欧美脸，补 `--no western features` 后改善。

**验证状态**：⚠️ 首次发现

**操作规则**：
1. 正向：`25-year-old East Asian male, youthful face, sharp clean jawline`
2. 负向：`--no western features, aged, wrinkles`
3. 如仍跑偏：加 `Chinese / Korean / Japanese facial features` 进一步收紧

---

## F. 下次改进

- [ ] 用 `--cref` 锁定已出的优质脸型，做角色一致性延伸（不同场景/服装）
- [ ] 尝试 personalize 之外的 `--sref` 风格参考，看能否进一步稳定双面材质效果
- [ ] 验证"层次感纹理背头"描述词是否可复用于其他人像项目
