---
tags: [类型/制作文档, 项目/SkillIsAllYouNeed, 工具/Remotion, 状态/阶段存档]
created: 2026-06-09
---

# Skill Is All You Need · 2026-06-09 早间阶段存档

## 本阶段完成

- 全片旁白已按 53 个 beat 生成并接入 Remotion；
- Suno 两首 BGM 已转为 MP3 并接入全片：
  - `Open Bench`：开场与教学段；
  - `Night Workshop Manifesto`：作者的话与片尾；
- BGM 已从完整版中截取更合适的使用片段，而不是直接从 0 秒播放；
- `SKILL_INDEX` 朗读异常按已验证方向修正：
  - 口播与字幕统一为“技能索引像图书馆索引。”；
  - 画面中的卡片标签仍可显示 `SKILL_INDEX`，作为视觉技术名词；
- 移除了全片口播源中的 `[curious]`、`[calm]` 等情绪标签，保证字幕和实际口播文本同源同文。

## 当前工程状态

- 主 composition：`SkillIsAllYouNeedFullFilm`
- 当前总时长：6765 帧，30fps，约 225.50 秒
- 全片旁白 manifest：`public/audio/full_film_20260609/voiceover.manifest.json`
- BGM 组件：`src/components/FullFilmBgmAudio.tsx`
- BGM 剪辑记录：`production/full_film_2026-06-09_bgm_edit_notes.md`

## 已知问题

当前动画节奏仍有历史遗留问题：早期制作顺序是先估算动画时长，再后做口播音频，所以部分场景的动画动作与真实旁白时长不完全贴合。

本轮没有强行重做全部动画时长，只修正了音频、字幕和 BGM 进入点。原因是如果在当前旧结构上局部硬调动画，容易制造新的错位。

## 下一轮制作原则

后续从头制作正式版时，应按以下顺序：

1. 先定稿文稿；
2. 生成 Eleven 分句音频；
3. 读取真实音频时长；
4. 用真实时长反推 scene duration、beat duration 和 motion timing；
5. 再做 MJ / Seedance / Remotion 动画；
6. 最后接入 Suno BGM 并按成片节奏剪辑。

这条顺序可以解决“动画时长靠估算、口播后置导致观感不好”的问题。

## 暂不处理

- 不在本阶段重做所有 scene motion timing；
- 不在本阶段重新生成全部 Seedance 动画；
- 不在本阶段导出最终发布版，只保留可审听的草稿与工程状态。
