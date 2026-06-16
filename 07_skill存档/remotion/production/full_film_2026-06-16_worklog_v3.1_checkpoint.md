# 全片 v3.1 封版存档 · 工作日志（2026-06-16）

> 性质：口播稿大改 + 视觉重写的封版 checkpoint。明日继续调优。
> 当前状态：**provisional（估算 timing）预览态，未生成真实 Eleven 音频。**

## 今天完成

1. **P0（motion 重锚）**：以 `fullFilmVoiceoverTiming` 为时间真相，build 时把 motion 重锚到真实 beat。修复"动画时长靠估算"错位。已单独提交（`413815c`）+ 旧版全片重渲染验证通过。
2. **诊断旧版节奏问题**：作者独白占 49%（107s/216s）喧宾夺主；53 个等长卡片=节拍器；比喻接力无落地。结合 Kurzgesagt / 知识科普脚本规律。
3. **v3.1 口播稿锁定**（`full_film_2026-06-16_script_v3.1_locked.md`）：
   - 母题：**助产(maieutic) ↔ 尸检(postmortem)**，《流浪地球2》"完整的一生"串联。
   - 贯穿案例：**真实双题复盘翻车**（票数靠前未获奖，却被记成"获奖图复盘"，AI 放大成 11 条假经验）。
   - 砍掉技术栈点名 / Codex 总指挥 / 工业化愿景 / "无产阶级铡刀"。作者独白 107s → ~18s。
4. **代码重写**：
   - `fullFilmVoiceover.ts`：23 beat（旧 53），新音频目录 `audio/full_film_20260616`。
   - `sceneSpecs.ts`：9 个新场景（生死框架→法医铁律→真实翻车→冻结事实→.md形态→三误区→一生收束→作者话），复用现有 subject/layout/motion，无新组件。
   - 静音预览管线：`scripts/estimate-full-film-timing.ts`（字数估算 timing，hasGeneratedAudio=false）+ `FullFilmVoiceoverAudio` 静音守卫 + `FullFilmBgmAudio` 作者段锚点改 `author_01_cant_edit` + `generate-full-film-voiceover.ts` 改用 `fullFilmVoiceover.audioPublicDir`。
   - typecheck 通过；6 张预览抽帧确认新结构 on-message（est 总长 ~154s / 2:34）。

## 明日接续（resume）

**第一步：生成真实 Eleven 音频（用户付费步骤）**
```
# 确认 .env 有 ELEVENLABS_API_KEY 与 ELEVENLABS_VOICE_ID
cd "E:\knowledge-base\07_skill存档\remotion"
npm.cmd run generate:full-film-voiceover
```
- 会把 23 段 mp3 写入 `public/audio/full_film_20260616/`，并用**真实时长**覆盖 `fullFilmVoiceoverTiming.ts`（hasGeneratedAudio=true）。
- motion 自动重锚（P0），无需手调动画。

**第二步：渲染真片审节奏**
```
npx.cmd remotion render src/index.ts SkillIsAllYouNeedFullFilm out/full-film-20260616-v3.1.mp4
```
真实节奏只有这一步能 faithful 判定（估算 timing 不算数）。

## 待办 / 开放项

- [ ] 真实音频生成后，审听节奏，按"长短碎交替"继续微调 beat 切分。
- [ ] 旧 6 张 MJ 图是给旧脚本的，新场景需重做 MJ/Seedance（P1，节奏定稿后）。
- [ ] 小瑕疵：warning-icon 三角下方白色标签在浅底偏淡，可改深色描边。
- [ ] BGM：双曲拼接仍在，新片更短，取段点/音量待随新节奏微调。

## 关联
- 文稿：`production/full_film_2026-06-16_script_v3.1_locked.md`
- 旧版工作日志：`production/full_film_2026-06-10_worklog_archive.md`
- 案例真身：`{知识库}/03_prompt模板库/02_案例复盘/灵光一现+风花雪月双题复盘.md`
- 两个 Skill：`aigc-postmortem/SKILL.md`（尸检）、`maieutic-skill/SKILL.md`（助产）
