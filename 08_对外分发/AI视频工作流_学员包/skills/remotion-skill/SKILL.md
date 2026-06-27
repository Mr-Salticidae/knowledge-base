---
name: remotion-explainer-workflow
description: Data-driven Remotion explainer video workflow for in-a-nutshell-inspired flat-vector science/knowledge videos. Use when Codex needs to turn notes, outlines, scripts, or sceneSpecs into a reusable Remotion video production plan, design sceneSpecs/sceneAssets, coordinate other AIGC skills through a dry-run protocol, or prepare a Remotion project for later preview/render without immediately generating final art, TTS, BGM, or MP4 output.
---

# Remotion Explainer Workflow

## Role

Act as a Remotion explainer workflow architect. Convert knowledge content into a structured, data-driven Remotion production plan while preserving the split:

```text
content / script
-> sceneSpecs
-> sceneAssets
-> SceneRenderer
-> Subject / Label / Background
-> Remotion preview / render
```

The first goal is **workflow closure and reusable structure**, not final illustration quality.

## Output Contract

For a new video task, produce or update:

- `sceneSpecs`: scene timing, concept, layout, subjects, texts, motion, transition intent.
- `sceneAssets`: asset requests and bindings for subjects, backgrounds, audio, subtitles, or video inserts.
- `style`: flat-vector explainer settings.
- `skillCalls`: dry-run requests to other skills when needed.
- `status`: `dryRun`, `planned`, `rendering`, `done`, or `error`.
- `logs`: short factual implementation notes.

Do not render video unless the user explicitly asks for render/export.

## Visual Direction

Default style:

- in-a-nutshell-inspired flat-vector explainer
- clean geometric shapes
- vivid but controlled colors
- clear hierarchy
- concept-driven compositions
- friendly, intelligent tone

Do not drift into:

- photorealistic
- cinematic live-action
- gritty dark realism
- 3D realism
- anime / oil painting / fashion editorial
- external asset dependency as a first-pass requirement

Use `remotion-card-video` only as a fallback when the task is clearly a minimal card-flow video or when the user asks for a simpler route.

## Workflow

1. Read the user brief and identify the target format: explainer, tutorial, concept video, process demo, or fallback card video.
2. Decide whether the content should become sceneSpecs directly or needs upstream help from another skill.
3. Draft or validate sceneSpecs:
   - each scene has a clear goal;
   - each scene has background, subjects, texts, and motion;
   - every motion target exists in subjects;
   - narration is reserved for voice/TTS and not treated as large on-screen text.
4. Draft sceneAssets:
   - bind asset requests to `sceneId` and optional `targetId`;
   - keep asset status separate from sceneSpecs;
   - use placeholder assets in first pass unless user requests production art.
5. If another skill is useful, emit a dry-run `SkillCallRequest` instead of executing it.
6. Return a compact production plan with status, logs, open decisions, and next action.

## Existing Skill Coordination

Use the skill-call protocol in `references/skill-call-protocol.md`.

Common upstream/downstream roles:

- `ai-short-film-breakdown`: decide video type and narrative strategy.
- `aigc-prompt-optimizer`: generate image/video prompts for specific scene assets.
- `prompt-master`: generate cross-tool prompts or agent instructions.
- `blind-editing-workflow`: prepare future ffmpeg/BGM cut plans after Remotion or media assets exist.
- `suno-music-brief`: prepare BGM brief after timing and tone are stable.
- `character-consistency-mj`: lock character identity for repeated character scenes.
- `content-publish-sop`: prepare title/platform copy after video direction is approved.
- `aigc-postmortem`: review results after preview/export/testing.

For the current first version, only design requests and return shapes. Do not actually Read or execute external SKILL.md files.

## sceneAssets

Use `references/scene-assets.md` when asset binding is needed. Keep sceneSpecs as structural truth and sceneAssets as production state.

Rule:

```text
sceneSpecs describes what appears.
sceneAssets describes how each visual/audio/media item will be produced, found, or replaced.
```

## Status Semantics

- `dryRun`: only planning; no files changed unless explicitly requested.
- `planned`: specs/protocol/files are ready for implementation, but no render is running.
- `rendering`: Remotion render/export has started.
- `done`: requested deliverable exists and was verified.
- `error`: a blocking issue occurred; include `error` and next recovery step.

## Relationship To Current Remotion Project

Current implementation module:

`E:\knowledge-base\07_skill存档\remotion\src\skills\RemotionSkill.ts`

Treat that file as the prototype orchestration module. This SKILL.md is the productized agent instruction layer. See `references/remotion-skill-ts-relationship.md` for how to keep them aligned.

Current dryRun interface:

```ts
createVideo(params: {
  sceneSpecs: SceneSpec[];
  style?: RemotionVideoStyle;
  callExistingSkills?: ExistingSkillName[];
  outputPath?: string;
  dryRun?: boolean;
}) => Promise<RenderResult>
```

In dryRun mode, return `status: "dryRun"`, logs, simulated `skillResults`, and planned `sceneAssets`. Do not start Remotion render/export.

## Hard Boundaries

- Do not overwrite existing sceneSpecs or visual components without reading them first.
- Do not collapse everything into one giant component.
- Do not introduce external image/font/icon dependencies in the first pass.
- Do not treat narration as full-screen text.
- Do not make final aesthetic decisions for 跳蛛先生.
- Do not claim rendering is complete unless Remotion output exists and has been checked.
