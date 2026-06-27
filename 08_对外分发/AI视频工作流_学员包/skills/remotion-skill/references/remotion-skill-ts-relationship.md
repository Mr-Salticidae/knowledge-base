# Relationship To An Optional RemotionSkill.ts

Prototype module (optional, only if the project has one):

`<your-remotion-project>/src/skills/RemotionSkill.ts`

Productized Skill:

this skill's `SKILL.md`

## Relationship

`SKILL.md` is the agent-facing workflow instruction. It tells Codex how to plan and coordinate a Remotion explainer project.

`RemotionSkill.ts` is the engineering prototype. It can later become the runtime/orchestration module that validates sceneSpecs, stores sceneAssets, and calls render or external skill adapters.

## Keep Them Aligned

| SKILL.md concept | RemotionSkill.ts implementation target |
|---|---|
| `createVideo(skillParams)` | exported `createVideo()` function |
| `sceneSpecs` input | `CreateVideoParams.sceneSpecs` |
| `sceneAssets` | add `sceneAssets?: SceneAsset[]` |
| `skillCalls` | add `SkillCallRequest[]` and `SkillCallResult[]` |
| status semantics | keep `dryRun / planned / rendering / done / error` aligned |
| external Skill coordination | keep registry only until execution is approved |

## Suggested Next Patch

When moving from design to implementation, update `RemotionSkill.ts` to:

1. Add `SceneAsset` types from `references/scene-assets.md`.
2. Replace the current loose `ExistingSkillResult` with `SkillCallRequest` and `SkillCallResult`.
3. Return `skillCalls` separately from `skillResults`.
4. Keep all external Skill calls in dry-run mode by default.
5. Add an explicit `allowExternalSkillExecution?: boolean` flag before any real Read/execution is possible.

## Boundary

Do not let the TypeScript module become the source of product rules. Product rules live in SKILL.md and references. The TypeScript module should implement those rules.
