import type { SceneSpec } from '../data/sceneSpecs';

export type RemotionVideoStyle = {
  visualLanguage?: 'in-a-nutshell-inspired' | 'minimal-card' | 'flat-vector';
  palette?: 'vivid-controlled' | 'dark-card' | 'light-workspace';
  motionPreset?: 'calm' | 'snappy' | 'playful';
  assetMode?: 'placeholder' | 'svg' | 'image';
};

export type ExistingSkillName =
  | 'aigc-prompt-optimizer'
  | 'prompt-master'
  | 'blind-editing-workflow'
  | 'suno-music-brief'
  | 'character-consistency-mj'
  | 'content-publish-sop'
  | 'aigc-postmortem'
  | 'ai-short-film-breakdown'
  | 'remotion-card-video'
  | '蒙眼剪辑法'
  | string;

export type SkillRegistryEntry = {
  name: ExistingSkillName;
  purpose: string;
  skillPath: string;
  useInRemotionSkill: string;
  triggerHints: string[];
};

export type ExistingSkillResult = {
  skillName: ExistingSkillName;
  status: 'skipped' | 'done' | 'error';
  assets?: SceneAsset[];
  logs: string[];
  error?: string;
};

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

export type SceneAssetRole =
  | 'subject'
  | 'background'
  | 'text'
  | 'transition'
  | 'narration'
  | 'music'
  | 'sfx'
  | 'caption'
  | 'reference';

export type SceneAsset = {
  id: string;
  sceneId: string;
  targetId?: string;
  kind: SceneAssetKind;
  status: SceneAssetStatus;
  role: SceneAssetRole;
  description: string;
  sourceSkill?: ExistingSkillName;
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

export type CreateVideoParams = {
  sceneSpecs: SceneSpec[];
  style?: RemotionVideoStyle;
  durationInFrames?: number;
  outputPath?: string;
  callExistingSkills?: ExistingSkillName[];
  dryRun?: boolean;
};

export type CreateVideoStatus = 'dryRun' | 'planned' | 'rendering' | 'done' | 'error';

export type RenderResult = {
  status: CreateVideoStatus;
  videoPath?: string;
  sceneCount: number;
  durationInFrames: number;
  style: Required<RemotionVideoStyle>;
  sceneAssets: SceneAsset[];
  skillResults: ExistingSkillResult[];
  logs: string[];
  error?: string;
};

export type CreateVideoResult = RenderResult;

type ExistingSkillAdapter = (params: CreateVideoParams) => Promise<ExistingSkillResult>;

const defaultStyle: Required<RemotionVideoStyle> = {
  visualLanguage: 'in-a-nutshell-inspired',
  palette: 'vivid-controlled',
  motionPreset: 'snappy',
  assetMode: 'placeholder',
};

export const skillRegistry: SkillRegistryEntry[] = [
  {
    name: 'aigc-prompt-optimizer',
    purpose: '口语化 AIGC 创作需求转专业 prompt。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\aigc-prompt-optimizer\\SKILL.md',
    useInRemotionSkill: '用于把视频视觉需求转成图片、视频或分镜提示词。',
    triggerHints: ['优化 prompt', '写 MJ prompt', '生成 Seedance 提示词'],
  },
  {
    name: 'prompt-master',
    purpose: '全工具路由的 prompt 工程规范。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\prompt-master_v1.6.0_SKILL.md',
    useInRemotionSkill: '用于生成跨工具 prompt、Agent 指令或复杂任务 brief。',
    triggerHints: ['LLM prompt', 'Claude Code 指令', 'Cursor prompt'],
  },
  {
    name: 'blind-editing-workflow',
    purpose: 'Python + ffmpeg 蒙眼剪辑工作流。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\blind-editing-workflow\\SKILL.md',
    useInRemotionSkill: '用于后续把 Remotion 输出、素材段落或音频节奏接入剪辑方案。',
    triggerHints: ['蒙眼剪辑', '按卡点剪辑', '生成剪辑方案'],
  },
  {
    name: 'suno-music-brief',
    purpose: 'Suno 两阶段配乐 brief。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\suno-music-brief\\SKILL.md',
    useInRemotionSkill: '用于后续根据视频节奏生成 BGM 探索 brief。',
    triggerHints: ['Suno prompt', '给项目配乐', '生成 Suno brief'],
  },
  {
    name: 'character-consistency-mj',
    purpose: 'Midjourney 角色一致性四层金字塔。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\character-consistency-mj\\SKILL.md',
    useInRemotionSkill: '用于需要固定角色 IP 或同一角色多场景出镜的视频项目。',
    triggerHints: ['角色一致性', 'sref', 'oref 锁脸'],
  },
  {
    name: 'content-publish-sop',
    purpose: '内容发布入场票审计与平台适配。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\content-publish-sop\\SKILL.md',
    useInRemotionSkill: '用于视频产出后判断发布平台、标题、文案和最小适配。',
    triggerHints: ['发布文案', '发哪里', '平台适配'],
  },
  {
    name: 'aigc-postmortem',
    purpose: '事实先行的创作复盘工作流。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\aigc-postmortem\\SKILL.md',
    useInRemotionSkill: '用于视频测试或发布后冻结数据、复盘产出质量和流程问题。',
    triggerHints: ['复盘', '整理经验', '测试结果'],
  },
  {
    name: 'ai-short-film-breakdown',
    purpose: 'AI 短片类型判断与叙事策略。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\ai-short-film-breakdown\\SKILL.md',
    useInRemotionSkill: '用于把视频项目先归类为概念推演、关系叙事、现实悖论或情绪氛围型。',
    triggerHints: ['AI 短片', '拉片', '叙事策略'],
  },
  {
    name: 'remotion-card-video',
    purpose: '知识内容转极简卡片流 Remotion 视频。',
    skillPath: 'E:\\knowledge-base\\07_skill存档\\remotion\\SKILL.md',
    useInRemotionSkill: '作为当前 RemotionSkill 的历史模板和极简卡片视频 fallback。',
    triggerHints: ['Remotion 脚本', 'TSX 代码', '卡片视频'],
  },
];

const findSkill = (skillName: ExistingSkillName) =>
  skillRegistry.find((entry) => entry.name === skillName || (skillName === '蒙眼剪辑法' && entry.name === 'blind-editing-workflow'));

const createIndexedSkillAdapter =
  (skillName: ExistingSkillName): ExistingSkillAdapter =>
  async (params) => {
    const skill = findSkill(skillName);

    if (!skill) {
      return {
        skillName,
        status: 'skipped',
        logs: [`未在 SKILL_INDEX 映射中找到 ${skillName}，已跳过。`],
      };
    }

    return {
      skillName,
      status: 'done',
      assets: createSkillAssets(skill.name, params.sceneSpecs),
      logs: [
        `${skill.name} 已挂载到 RemotionSkill registry。`,
        `Skill 路径：${skill.skillPath}`,
        `dryRun 已生成模拟 sceneAssets，不直接 Read 或执行外部 Skill。`,
        `Remotion 用途：${skill.useInRemotionSkill}`,
      ],
    };
  };

const blindEditingAdapter = createIndexedSkillAdapter('blind-editing-workflow');

const remotionCardAdapter: ExistingSkillAdapter = async () => ({
  skillName: 'remotion-card-video',
  status: 'skipped',
  assets: [],
  logs: [
    'remotion-card-video 是当前工程的历史来源模板。',
    '为避免递归调用当前 Remotion 工程，当前阶段仅作为 fallback 说明保留。',
  ],
});

const createSkillAssets = (skillName: ExistingSkillName, sceneSpecs: SceneSpec[]): SceneAsset[] => {
  if (sceneSpecs.length === 0) {
    return [];
  }

  const firstScene = sceneSpecs[0];

  if (skillName === 'aigc-prompt-optimizer') {
    return [
      {
        id: `asset_${firstScene.id}_visual_prompt`,
        sceneId: firstScene.id,
        kind: 'prompt',
        status: 'planned',
        role: 'subject',
        description: `Flat-vector visual prompt request for ${firstScene.concept}`,
        sourceSkill: skillName,
        prompt: `Create an in-a-nutshell-inspired flat-vector explainer visual for: ${firstScene.concept}`,
        styleTags: ['flat-vector', 'vivid-controlled', 'explainer'],
      },
    ];
  }

  if (skillName === 'blind-editing-workflow' || skillName === '蒙眼剪辑法') {
    return [
      {
        id: 'asset_global_blind_editing_plan',
        sceneId: 'global',
        kind: 'video',
        status: 'planned',
        role: 'transition',
        description: 'Dry-run editing plan placeholder for future ffmpeg or BGM cut workflow.',
        sourceSkill: skillName,
        durationInFrames: getDuration(sceneSpecs),
        constraints: ['dryRun only', 'no render', 'no ffmpeg execution'],
      },
    ];
  }

  if (skillName === 'suno-music-brief') {
    return [
      {
        id: 'asset_global_suno_brief',
        sceneId: 'global',
        kind: 'audio',
        status: 'requested',
        role: 'music',
        description: 'Dry-run BGM brief request reserved for later audio stage.',
        sourceSkill: skillName,
        durationInFrames: getDuration(sceneSpecs),
        constraints: ['do not generate audio in this stage'],
      },
    ];
  }

  return [
    {
      id: `asset_global_${String(skillName).replace(/[^a-zA-Z0-9_-]/g, '_')}`,
      sceneId: 'global',
      kind: 'placeholder',
      status: 'planned',
      role: 'reference',
      description: `Dry-run placeholder showing ${skillName} is callable from RemotionSkill.`,
      sourceSkill: skillName,
    },
  ];
};

const existingSkillAdapters: Record<string, ExistingSkillAdapter> = {
  蒙眼剪辑法: blindEditingAdapter,
  'blind-editing-workflow': blindEditingAdapter,
  'aigc-prompt-optimizer': createIndexedSkillAdapter('aigc-prompt-optimizer'),
  'prompt-master': createIndexedSkillAdapter('prompt-master'),
  'suno-music-brief': createIndexedSkillAdapter('suno-music-brief'),
  'character-consistency-mj': createIndexedSkillAdapter('character-consistency-mj'),
  'content-publish-sop': createIndexedSkillAdapter('content-publish-sop'),
  'aigc-postmortem': createIndexedSkillAdapter('aigc-postmortem'),
  'ai-short-film-breakdown': createIndexedSkillAdapter('ai-short-film-breakdown'),
  'remotion-card-video': remotionCardAdapter,
};

const getDuration = (sceneSpecs: SceneSpec[], override?: number) =>
  override ?? sceneSpecs.reduce((sum, scene) => sum + scene.durationInFrames, 0);

const validateSceneSpecs = (sceneSpecs: SceneSpec[]) => {
  const logs: string[] = [];

  if (sceneSpecs.length === 0) {
    throw new Error('sceneSpecs 不能为空。');
  }

  for (const scene of sceneSpecs) {
    if (scene.durationInFrames <= 0) {
      throw new Error(`${scene.id} 的 durationInFrames 必须大于 0。`);
    }

    const subjectIds = new Set(scene.subjects.map((subject) => subject.id));
    const missingTargets = scene.motion
      .map((motion) => motion.targetId)
      .filter((targetId) => !subjectIds.has(targetId));

    if (missingTargets.length > 0) {
      throw new Error(`${scene.id} 存在未匹配 subject 的 motion target：${missingTargets.join(', ')}`);
    }

    logs.push(`${scene.id}: ${scene.subjects.length} subjects, ${scene.texts.length} texts`);
  }

  return logs;
};

const createBaseSceneAssets = (sceneSpecs: SceneSpec[]): SceneAsset[] =>
  sceneSpecs.flatMap((scene) => [
    {
      id: `asset_${scene.id}_background`,
      sceneId: scene.id,
      kind: 'placeholder',
      status: 'planned',
      role: 'background',
      description: `${scene.background} background placeholder for ${scene.goal}`,
      styleTags: [scene.background, scene.layout],
    },
    ...scene.subjects.map<SceneAsset>((subject) => ({
      id: `asset_${scene.id}_${subject.id}`,
      sceneId: scene.id,
      targetId: subject.id,
      kind: 'placeholder',
      status: 'planned',
      role: 'subject',
      description: `${subject.type} subject placeholder bound to ${scene.id}.${subject.id}`,
      styleTags: [subject.type, subject.colorToken],
      metadata: {
        x: subject.position.x,
        y: subject.position.y,
        w: subject.size.w,
        h: subject.size.h,
      },
    })),
  ]);

const callSkillAdapters = async (params: CreateVideoParams) => {
  const skillNames = params.callExistingSkills ?? [];
  const results: ExistingSkillResult[] = [];

  for (const skillName of skillNames) {
    const adapter = existingSkillAdapters[skillName];

    if (!adapter) {
      results.push({
        skillName,
        status: 'skipped',
        logs: [`未找到 ${skillName} 的本地适配器，已跳过。`],
      });
      continue;
    }

    results.push(await adapter(params));
  }

  return results;
};

export const createVideo = async (params: CreateVideoParams): Promise<RenderResult> => {
  const style = { ...defaultStyle, ...params.style };
  const logs = [
    'RemotionSkill.createVideo 已接收任务。',
    `渲染模式：${params.dryRun === false ? '允许后续渲染' : 'dryRun，仅规划不渲染'}`,
  ];

  try {
    logs.push(...validateSceneSpecs(params.sceneSpecs));

    const skillResults = await callSkillAdapters(params);
    const sceneAssets = [...createBaseSceneAssets(params.sceneSpecs), ...skillResults.flatMap((result) => result.assets ?? [])];
    const durationInFrames = getDuration(params.sceneSpecs, params.durationInFrames);

    logs.push(`sceneSpecs 已绑定：${params.sceneSpecs.length} scenes。`);
    logs.push(`总时长：${durationInFrames} frames。`);
    logs.push(`风格：${style.visualLanguage} / ${style.palette} / ${style.motionPreset} / ${style.assetMode}。`);

    logs.push(`sceneAssets 已生成：${sceneAssets.length} assets。`);

    if (params.dryRun === false) {
      logs.push('实际 Remotion 渲染接口尚未启用，当前返回 planned 状态。');
    }

    return {
      status: params.dryRun === false ? 'planned' : 'dryRun',
      videoPath: params.outputPath,
      sceneCount: params.sceneSpecs.length,
      durationInFrames,
      style,
      sceneAssets,
      skillResults,
      logs,
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);

    return {
      status: 'error',
      sceneCount: params.sceneSpecs.length,
      durationInFrames: 0,
      style,
      sceneAssets: [],
      skillResults: [],
      logs: [...logs, message],
      error: message,
    };
  }
};
