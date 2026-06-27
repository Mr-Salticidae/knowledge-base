# sceneAssets Data Structure

Use `sceneAssets` to separate production assets from scene structure.

## Core Rule

```text
sceneSpecs = what should appear
sceneAssets = how the thing is produced, found, generated, replaced, or verified
```

This keeps sceneSpecs stable and lets visual assets, prompts, audio, subtitles, and generated files evolve without rewriting the scene plan.

## Suggested Types

```ts
export type SceneAssetKind =
  | 'placeholder'
  | 'svg'
  | 'image'
  | 'video'
  | 'audio'
  | 'subtitle'
  | 'prompt'
  | 'style-reference';

export type SceneAssetStatus =
  | 'requested'
  | 'planned'
  | 'generated'
  | 'linked'
  | 'verified'
  | 'rejected'
  | 'error';

export type SceneAsset = {
  id: string;
  sceneId: string;
  targetId?: string;
  kind: SceneAssetKind;
  status: SceneAssetStatus;
  role:
    | 'subject'
    | 'background'
    | 'text'
    | 'transition'
    | 'narration'
    | 'music'
    | 'sfx'
    | 'caption'
    | 'reference';
  description: string;
  sourceSkill?: string;
  prompt?: string;
  filePath?: string;
  durationInFrames?: number;
  timeRange?: {
    startFrame: number;
    endFrame: number;
  };
  styleTags?: string[];
  constraints?: string[];
  metadata?: Record<string, string | number | boolean>;
  error?: string;
};
```

## Example

```ts
const sceneAssets: SceneAsset[] = [
  {
    id: 'asset_scene_06_index_card_prompt',
    sceneId: 'scene_06_skill_index',
    targetId: 'index',
    kind: 'prompt',
    status: 'planned',
    role: 'subject',
    description: 'SKILL_INDEX card visual prompt for flat-vector library metaphor.',
    sourceSkill: 'aigc-prompt-optimizer',
    prompt: 'flat-vector index card labeled SKILL_INDEX, clean educational explainer style',
    styleTags: ['flat-vector', 'library', 'vivid-controlled'],
  },
  {
    id: 'asset_global_bgm_brief',
    sceneId: 'global',
    kind: 'audio',
    status: 'requested',
    role: 'music',
    description: '90-second friendly intelligent explainer BGM brief.',
    sourceSkill: 'suno-music-brief',
  },
];
```

## Binding To sceneSpecs

- `sceneId` must match a scene id in `sceneSpecs`, except `global` for whole-video assets.
- `targetId` must match `subjects[].id` when role is `subject`.
- Audio and subtitle assets may omit `targetId`.
- `filePath` appears only after an asset is linked/generated.
- `prompt` can exist before any file exists.

## RemotionSkill DryRun Binding

If the project has an orchestration module (e.g. `src/skills/RemotionSkill.ts`), in dryRun it creates planned placeholder assets for:

- each scene background;
- each `subjects[].id` as a subject-bound asset;
- simulated outputs from requested existing Skills, such as prompt assets from `aigc-prompt-optimizer` or a global editing-plan asset from `blind-editing-workflow`.

DryRun binding confirms structure only. It does not render video, execute ffmpeg, generate audio, or link production files.

## Production States

Use the smallest honest status:

- `requested`: the need is known, but no plan exists.
- `planned`: prompt or production method exists.
- `generated`: a file or concrete output exists.
- `linked`: Remotion project references the file.
- `verified`: preview/render check passed.
- `rejected`: human review rejected it.
- `error`: generation/linking/verification failed.
