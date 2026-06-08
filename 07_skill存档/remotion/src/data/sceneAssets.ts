import type { SceneAsset } from '../skills/RemotionSkill';

export const SCENE_04_MJ_KEY_VISUAL_PATH = 'assets/scene_04/mj_prompt_to_skill_key_visual.png';
export const SCENE_04_SEEDANCE_MOTION_PATH = 'assets/scene_04/seedance_prompt_to_skill_motion.mp4';

export const sceneAssets: SceneAsset[] = [
  {
    id: 'asset_scene_04_remotion_native_fallback',
    sceneId: 'scene_04_repeat_to_skill',
    kind: 'placeholder',
    status: 'planned',
    role: 'subject',
    description: 'Remotion native fallback: prompt bubbles compress into a Skill manual using existing subject animation.',
    provider: 'remotion-native',
    binding: 'native-subject',
    constraints: ['must remain available when Midjourney or Seedance assets are missing'],
    styleTags: ['flat-vector', 'native-fallback', 'in-a-nutshell-inspired'],
  },
  {
    id: 'asset_scene_04_mj_key_visual',
    sceneId: 'scene_04_repeat_to_skill',
    kind: 'image',
    status: 'linked',
    role: 'subject',
    description: 'Midjourney key visual for the concept of repeated prompt bubbles compressing into a reusable Skill manual.',
    provider: 'midjourney',
    binding: 'foreground-image',
    assetPrompt:
      'flat vector educational explainer illustration, repeated prompt bubbles with labels format requirements, workflow steps, guardrails, compressing into a clean handbook labeled SKILL, bright friendly science explainer style, thick dark outlines, simple geometric shapes, clear cause and effect composition, light warm background, no photorealism, no anime, no cinematic lighting, no 3D realism --ar 16:9 --style raw',
    expectedPath: SCENE_04_MJ_KEY_VISUAL_PATH,
    filePath: SCENE_04_MJ_KEY_VISUAL_PATH,
    styleTags: ['midjourney', 'flat-vector', 'key-visual', 'in-a-nutshell-inspired'],
    constraints: [
      'keep enough empty lower area for Remotion caption',
      'avoid tiny unreadable text except the SKILL label',
      'do not replace Remotion subtitles or timeline',
    ],
  },
  {
    id: 'asset_scene_04_seedance_motion_insert',
    sceneId: 'scene_04_repeat_to_skill',
    kind: 'video',
    status: 'linked',
    role: 'subject',
    description: 'Seedance 2.0 motion insert: prompt bubbles gather, compress, and transform into a Skill manual.',
    provider: 'seedance-2.0',
    binding: 'video-insert',
    assetPrompt:
      '@Image1 as the first frame and visual style reference. Create a 4-second premium flat-vector educational explainer animation based on @Image1. Keep the same off-white paper texture, thick dark ink outlines, simple geometry, compression funnel, prompt bubbles, and blue handbook labeled SKILL. 0-1s: the prompt bubbles on the left gently drift toward the funnel entrance, with small colored particles beginning to flow into the transparent chamber. 1-2.5s: the funnel activates; colored particles swirl downward inside the chamber, then travel through the pipe toward the handbook. The camera stays mostly locked with a very subtle slow push-in. 2.5-4s: the blue handbook on the right receives the compressed particles, the SKILL label gives one subtle clean pulse, then the frame settles into a stable final pose. Leave the bottom area clean for Remotion subtitles. Style: premium editorial flat-vector science explainer, restrained motion, calm intelligent tone, no photorealism, no anime, no 3D realism, no cinematic live action, no realistic human faces, no extra text, no logo, no watermark.',
    expectedPath: SCENE_04_SEEDANCE_MOTION_PATH,
    filePath: SCENE_04_SEEDANCE_MOTION_PATH,
    durationInFrames: 120,
    timeRange: {
      startFrame: 72,
      endFrame: 192,
    },
    styleTags: ['seedance-2.0', 'motion-insert', 'flat-vector', 'in-a-nutshell-inspired'],
    constraints: [
      '3-5 seconds only',
      'central visual insert, not a full-video replacement',
      'leave subtitle area readable',
    ],
    metadata: {
      width: 1280,
      height: 720,
      sourceFps: 60,
      durationSeconds: 4.062993,
      archiveSource: 'C:\\Users\\Administrator\\Downloads\\jimeng-2026-06-08-2329- as the first frame and visual style ref....mp4',
    },
  },
];
