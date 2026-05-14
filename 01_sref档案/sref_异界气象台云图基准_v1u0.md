---
tags: [类型/档案]
---
# sref 异界气象台云图基准 · v1_u0

> 建档：2026-05-14
> 项目：20_异界气象台_minitest
> 类型：MJ V8.1 Web 端 sref（图片挂载式，无数字 ID）
> 关联：[[MJ_v8.1_无oref_混合工作流]] 中"sref 工作流变化（2026-05-14 实测）"小节

---

## 一句话定位

**伪 90 年代央视气象档案的视觉基准——上下黑边 letterbox + 地球弧线 + 老胶片水平刮痕 + navy 冷色。**

---

## 基准图位置

- 本项目副本：`D:\AIGC工作站\20_异界气象台_minitest\02_视觉\开场云图\sref基准图_v1u0.png`
- 原始候选编号：v1_u0（来自 `MJ_prompt套装_v2.md` 第 v1 路径 4 张抽卡的 0 号）

**重要**：MJ V8.1 web 端不给 sref 数字 ID，使用方式是**每次出图时点击 prompt 框旁的"加图"按钮，把这张图挂为 sref**。

---

## 原始 prompt（产出此 sref 母本的 prompt）

```
cinematic still from a 1990s East Asian state broadcast satellite weather monitoring station, ultra wide establishing shot, deep navy blue background with subtle gradient, upper third of the frame shows pale cloud bands and faint latitude grid, middle third shows the curved horizon of an unknown planet with white cumulus cloud formations drifting across it, lower third is dark navy negative space with subtle CRT scanline texture, archival broadcast footage quality, vintage analog video grain, no continents, no text, no labels, no logos, vertical 9:16 composition --ar 9:16 --v 8 --style raw
```

**纯净性确认**：本 sref 是用纯 prompt 抽卡产物（无 sref 输入），主体形态中性（无具体大陆/具体云形/具体异物），符合 [[sref纯净性原则]] 的要求。

---

## 视觉指纹（这张 sref 注入后续生成的视觉特征）

- **配色**：deep navy + 冷青大气层光带 + 白色云团
- **构图**：上下 letterbox 黑边 + 中间窄云图区 + 地球弧线斜切
- **质感**：1990 年代录像带胶片噪点 + 一道老胶片水平刮痕
- **气氛**：克制、秩序、真实档案感

---

## 适用 / 不适用主体

### ✅ 适用

- 开场卫星云图特写
- 三地区天气云图叠加（深海地图 / 海域地图 / 冰原地图）
- 收尾全球总览图
- 任何"卫星/俯瞰/气象播报"语境的镜头

### ⚠️ 半适用（sw 建议降到 50-70）

- 第二节·克苏鲁海域的双螺旋黑色风暴特写（sref 偏冷蓝，但暴风需要更暗 navy 加鬼火黄 accent，强 sref 会洗掉鬼火黄）
- 第三节·永夜带冰原地表特写（sref 是俯视云图，但永夜带需要近地表，强 sref 会拉回俯视）

### ❌ 不适用

- 任何近景人物/角色镜头（本片无人物，N/A）
- R 系列机体的特写（如果做，应单独抽卡，不挂此 sref）

---

## 使用方式（v8.1 web 端）

1. 进 MJ web → 准备 prompt
2. 点击 prompt 输入框右侧的"加图"图标 → 上传 `sref基准图_v1u0.png`
3. UI 显示图片缩略图已挂载状态
4. 在 prompt 文本里加 `--sw 100`（或视情况降到 50-70）
5. 写主体描述 + 9:16 + v8 + style raw
6. Submit

---

## 跨会话/跨项目复用注意

- ❌ 不能用"sref ID 数字"复用（v8.1 无 ID）
- ✅ 复制本图片到新项目目录，重新挂载
- ✅ 本档案路径稳定，跨会话可引用

---

## 文档版本

- v1 - 2026-05-14 - 异界气象台 minitest 制作期建档
