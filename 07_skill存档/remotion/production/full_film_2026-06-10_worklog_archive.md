---
tags: [类型/制作文档, 项目/SkillIsAllYouNeed, 工具/Remotion, 工具/Midjourney, 工具/Seedance, 状态/阶段存档]
created: 2026-06-10
---

# Skill Is All You Need · 2026-06-10 收工复盘

## 今日结论

`SkillIsAllYouNeedFullFilm` 已从“框架视频验证”推进到“MJ / Seedance 素材替换准备完成”的阶段。

当前主线不是发布收尾，而是继续按既定工作流推进：

1. 先确认全片框架、旁白、BGM、字幕和节奏；
2. 再做 Midjourney 关键图；
3. 再用 Seedance 2.0 做 5 秒机制动效；
4. 最后回接 Remotion，完成最终视觉替换。

## 已完成

### 1. 框架视频验证

- 全片 composition：`SkillIsAllYouNeedFullFilm`
- 当前导出文件：
  - `out/skill-is-all-you-need-full-film.mp4`
- 当前成片参数：
  - 1920x1080
  - 30fps
  - H.264 + AAC
  - 约 216.45 秒
- 验证结果：
  - `npm.cmd run typecheck` 通过；
  - 全片可导出；
  - 作者话目标字幕抽帧确认正常。

### 2. 作者话微调

按用户意见完成两项修改：

- 把作者话中的“字节”改为“所谓大厂”；
- 将全片旁白播放速率设为 `1.05`，并同步重算 full-film timing。

相关提交：

- `b0d3eb6 Polish full film author note`

### 3. MJ / Seedance 生产包

新增全片素材替换生产包：

- `production/full_film_2026-06-10_mj_seedance_replacement_pack.md`

生产包明确：

- A 批次优先替换 6 个 scene；
- B 批次为可选补充；
- C 批次保留 Remotion 原生；
- Seedance 只承担 5 秒机制动效，不承担整段长 scene；
- Remotion 继续负责字幕、时间线、静态持帧、裁切和兜底。

相关提交：

- `a72ac1e Add full film MJ Seedance replacement pack`

### 4. A 批次 Midjourney 关键图归档

已归档 6 张 A 批次 Midjourney 图，统一放入：

`public/assets/full_film_20260610/`

归档映射：

| sceneId | asset |
|---|---|
| `scene_00_intro_question` | `scene_00_intro_question_mj_key_visual.png` |
| `scene_02_forgetful_assistant` | `scene_02_forgetful_assistant_mj_key_visual.png` |
| `scene_06_skill_index` | `scene_06_skill_index_mj_key_visual.png` |
| `author_03_motivation` | `author_03_motivation_mj_key_visual.png` |
| `author_04_stack` | `author_04_stack_mj_key_visual.png` |
| `author_06_industrialization` | `author_06_industrialization_mj_key_visual.png` |

所有图片尺寸均为 `1456x816`。

验证结果：

- `npm.cmd run typecheck` 通过；
- Remotion 抽帧确认 `scene_00_intro_question` 和 `author_04_stack` 能正常加载新图；
- 字幕区未被遮挡；
- `sceneAssets.ts` 已登记 6 张图为 `linked` 状态。

相关提交：

- `6c910be Archive full film MJ key visuals`

### 5. Seedance 2.0 API 探测

已确认 Ark API key 可用于读取火山方舟模型列表。

模型列表中确认存在：

- `doubao-seedance-2-0-260128`
- `doubao-seedance-2-0-fast-260128`

其中 `doubao-seedance-2-0-fast-260128` 标记为：

- domain: `VideoGeneration`
- task type: `MultimodalToVideo`, `VideoExtension`, `VideoEditing`
- input modalities: `text`, `image`, `video`, `audio`
- output modalities: `video`

注意：

- API key 不写入仓库；
- 今日只做了模型列表读取和 endpoint 低风险探测；
- 没有提交真实视频生成任务；
- 没有消耗 A 批次 Seedance 生成额度。

当前阻塞点：

- 火山方舟视频生成任务的真实 endpoint 还未从官方控制台文档中定位；
- 常见猜测路径均返回 `404`；
- 下一步需要从控制台复制「视频生成 API 调用示例 / curl」后再写批量自动生成脚本。

## 下一步

### 优先动作

1. 打开火山方舟视频生成控制台；
2. 找到 Seedance 2.0 / 视频生成的 API 调用示例；
3. 复制 curl 示例或真实请求路径；
4. 写 `scripts/generate-seedance-full-film-assets.ts`；
5. 批量提交 A 批次 6 个 Seedance 任务；
6. 轮询任务状态并下载 MP4；
7. 保存到：

```text
public/assets/full_film_20260610/
  scene_00_intro_question_seedance_motion.mp4
  scene_02_forgetful_assistant_seedance_motion.mp4
  scene_06_skill_index_seedance_motion.mp4
  author_03_motivation_seedance_motion.mp4
  author_04_stack_seedance_motion.mp4
  author_06_industrialization_seedance_motion.mp4
```

### 回接策略

每个 Seedance 视频回收后：

1. 更新 `src/data/sceneAssets.ts`，新增对应 `video-insert` 资产；
2. 设置合理 `timeRange`，只覆盖关键机制动效段；
3. 保留 MJ 静态图作为开头、结尾和失败兜底；
4. 抽帧检查字幕区、裁切和黑帧；
5. 再导出一版全片预览。

## 当前 Git 状态

截至本存档创建前，相关仓库状态：

- `E:\knowledge-base`: 已同步到 `origin/main`
- `E:\AIGC工作站`: 主分支已同步，但存在鲸海拾贝相关未跟踪目录；这些目录属于其他项目，本轮未处理。

