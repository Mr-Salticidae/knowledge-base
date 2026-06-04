# Skill Call Protocol

Use this protocol when `remotion-explainer-workflow` needs another Skill. First version is a planning protocol only: it describes the request and expected return shape but does not execute external SKILL.md files.

## Request Shape

```ts
export type SkillCallStatus = 'dryRun' | 'planned' | 'rendering' | 'done' | 'error';

export type SkillCallRequest = {
  requestId: string;
  skillName: string;
  purpose: string;
  status: 'dryRun';
  inputs: {
    sceneSpecs?: SceneSpec[];
    sceneAssets?: SceneAsset[];
    brief?: string;
    targetSceneIds?: string[];
    targetSubjectIds?: string[];
    style?: RemotionVideoStyle;
    constraints?: string[];
  };
  expectedOutputs: Array<
    | 'sceneSpecPatch'
    | 'sceneAssets'
    | 'promptSet'
    | 'musicBrief'
    | 'editPlan'
    | 'publishBrief'
    | 'postmortem'
  >;
};
```

## Response Shape

```ts
export type SkillCallResult = {
  requestId: string;
  skillName: string;
  status: SkillCallStatus;
  summary: string;
  outputs: {
    sceneSpecPatch?: Partial<SceneSpec>[];
    sceneAssets?: SceneAsset[];
    promptSet?: PromptAsset[];
    musicBrief?: MusicBrief;
    editPlan?: EditPlan;
    publishBrief?: PublishBrief;
    postmortem?: PostmortemNote;
  };
  logs: string[];
  error?: string;
};
```

## What RemotionSkill Requests

| Skill | Request | Expected return |
|---|---|---|
| `ai-short-film-breakdown` | classify video type, narrative strategy, scene logic | `sceneSpecPatch`, strategy notes |
| `aigc-prompt-optimizer` | prompts for visual assets, SVG/image/video references | `promptSet`, optional `sceneAssets` |
| `prompt-master` | cross-tool prompt/agent instructions | `promptSet` |
| `blind-editing-workflow` | edit/cut plan after timing/media exists | `editPlan` |
| `suno-music-brief` | BGM exploration or locked music brief | `musicBrief` |
| `character-consistency-mj` | character identity constraints for repeated subjects | `promptSet`, character asset notes |
| `content-publish-sop` | publishing route, title/copy/platform adaptation | `publishBrief` |
| `aigc-postmortem` | testing/release review | `postmortem` |

## Binding Rules

1. A result that changes story structure returns `sceneSpecPatch`.
2. A result that produces or requests assets returns `sceneAssets`.
3. A result that only gives prompt text returns `promptSet` and may later be converted into `sceneAssets`.
4. Every asset-like output must include `sceneId`.
5. If it targets a subject, include `targetId`; `targetId` must match a `subjects[].id` in that scene.
6. Never mutate sceneSpecs implicitly. Return patches and let the caller apply them.

## Status Rules

- `dryRun`: request shape only; no external Skill executed.
- `planned`: external Skill response is designed and ready to execute later.
- `rendering`: reserved for actual media/render jobs.
- `done`: external Skill completed and outputs are available.
- `error`: include reason and recovery step.

## Current First-Version Constraint

For this v1 design phase, RemotionSkill should return `dryRun` or `planned` Skill calls only. Do not Read or execute external Skill files until 跳蛛先生 explicitly approves the next phase.
