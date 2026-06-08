export type LayoutType =
  | 'center-focus'
  | 'left-right-contrast'
  | 'vertical-scale'
  | 'circular-system'
  | 'zoom-in-cross-section'
  | 'network-map'
  | 'library-system';

export type BackgroundType =
  | 'space'
  | 'body'
  | 'data'
  | 'city'
  | 'abstract'
  | 'plain'
  | 'library'
  | 'workspace';

export type SubjectType =
  | 'human'
  | 'ai-assistant'
  | 'manual'
  | 'markdown-file'
  | 'index-card'
  | 'prompt-bubble'
  | 'warning-icon'
  | 'library-shelf'
  | 'abstract-shape'
  | 'arrow'
  | 'data-packet';

export type ColorToken =
  | 'navy'
  | 'sky'
  | 'cyan'
  | 'yellow'
  | 'orange'
  | 'red'
  | 'green'
  | 'purple'
  | 'white'
  | 'ink';

export type Position = {
  x: number;
  y: number;
};

export type Size = {
  w: number;
  h: number;
};

export type SubjectSpec = {
  id: string;
  type: SubjectType;
  position: Position;
  size: Size;
  colorToken: ColorToken;
  label?: string;
  rotation?: number;
};

export type TextSpec = {
  id: string;
  text: string;
  position: 'top' | 'bottom' | 'center' | 'left' | 'right';
  emphasis?: boolean;
  delayFrames?: number;
};

export type NarrationBeat = {
  id: string;
  startFrame: number;
  durationInFrames: number;
  text: string;
  emphasis?: boolean;
  linkedSubjectIds?: string[];
};

export type MotionType =
  | 'fade-in'
  | 'pop-in'
  | 'scale-up'
  | 'slide-in'
  | 'pulse'
  | 'shake'
  | 'compress'
  | 'scatter'
  | 'connect'
  | 'zoom'
  | 'wipe';

export type MotionSpec = {
  targetId: string;
  type: MotionType;
  startFrame: number;
  durationFrames: number;
  direction?: 'left' | 'right' | 'up' | 'down';
  intensity?: number;
};

export type SceneSpec = {
  id: string;
  durationInFrames: number;
  goal: string;
  concept: string;
  narration: string;
  narrationBeats?: NarrationBeat[];
  layout: LayoutType;
  background: BackgroundType;
  subjects: SubjectSpec[];
  texts: TextSpec[];
  motion: MotionSpec[];
  transitionOut?: 'zoom-in' | 'zoom-out' | 'wipe' | 'fade' | 'morph';
};

export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export const sceneSpecs: SceneSpec[] = [
  {
    id: 'scene_00_intro_question',
    durationInFrames: 660,
    goal: '用简短问题建立观看动机：为什么观众需要 Skill。',
    concept: '新对话反复归零，散落的流程卡最终聚合成 SKILL。',
    narration:
      '你有没有遇到过这种情况：同一个 AI，昨天刚教会它你的偏好，今天换个新对话，它又像第一次见你一样。你明明已经总结过流程，但每次开工，还是要重新解释一遍。如果 AI 真的能帮我们工作，那它不该只会回答问题。它应该记住流程，调用工具，并且稳定复现一套做事方法。这就是这期视频要讲的东西：Skill。',
    narrationBeats: [
      {
        id: 'beat_01_same_ai_forgets',
        startFrame: 0,
        durationInFrames: 150,
        text: '同一个 AI，昨天刚教会它你的偏好，今天又像第一次见你一样。',
        emphasis: true,
        linkedSubjectIds: ['assistant', 'memory_bar'],
      },
      {
        id: 'beat_02_repeat_process',
        startFrame: 150,
        durationInFrames: 150,
        text: '你明明已经总结过流程，但每次开工，还是要重新解释一遍。',
        linkedSubjectIds: ['process_a', 'process_b', 'process_c'],
      },
      {
        id: 'beat_03_should_remember',
        startFrame: 300,
        durationInFrames: 170,
        text: '如果 AI 真的能帮我们工作，它不该只会回答问题。',
        linkedSubjectIds: ['assistant', 'tool_node'],
      },
      {
        id: 'beat_04_skill_promise',
        startFrame: 470,
        durationInFrames: 160,
        text: '它应该记住流程，调用工具，稳定复现一套做事方法。',
        emphasis: true,
        linkedSubjectIds: ['skill_block', 'process_a', 'tool_node'],
      },
    ],
    layout: 'network-map',
    background: 'workspace',
    subjects: [
      { id: 'assistant', type: 'ai-assistant', position: { x: 26, y: 52 }, size: { w: 280, h: 280 }, colorToken: 'cyan' },
      { id: 'memory_bar', type: 'abstract-shape', position: { x: 50, y: 30 }, size: { w: 420, h: 110 }, colorToken: 'red', label: 'Memory 0%' },
      { id: 'process_a', type: 'index-card', position: { x: 44, y: 58 }, size: { w: 260, h: 140 }, colorToken: 'sky', label: '偏好' },
      { id: 'process_b', type: 'index-card', position: { x: 58, y: 50 }, size: { w: 280, h: 150 }, colorToken: 'green', label: '流程' },
      { id: 'process_c', type: 'index-card', position: { x: 72, y: 58 }, size: { w: 260, h: 140 }, colorToken: 'orange', label: '避坑' },
      { id: 'tool_node', type: 'data-packet', position: { x: 66, y: 30 }, size: { w: 140, h: 120 }, colorToken: 'purple', label: 'Tools' },
      { id: 'skill_block', type: 'manual', position: { x: 50, y: 54 }, size: { w: 360, h: 260 }, colorToken: 'yellow', label: 'SKILL' },
    ],
    texts: [
      { id: 'top', text: 'AI 真的能记住你的流程吗？', position: 'top', emphasis: true },
      { id: 'bottom', text: '从反复解释，到稳定复现', position: 'bottom' },
    ],
    motion: [
      { targetId: 'assistant', type: 'slide-in', startFrame: 0, durationFrames: 36, direction: 'left' },
      { targetId: 'memory_bar', type: 'wipe', startFrame: 30, durationFrames: 58 },
      { targetId: 'process_a', type: 'scatter', startFrame: 132, durationFrames: 110 },
      { targetId: 'process_b', type: 'scatter', startFrame: 150, durationFrames: 110 },
      { targetId: 'process_c', type: 'scatter', startFrame: 168, durationFrames: 110 },
      { targetId: 'tool_node', type: 'pulse', startFrame: 310, durationFrames: 180 },
      { targetId: 'skill_block', type: 'compress', startFrame: 450, durationFrames: 90 },
    ],
    transitionOut: 'zoom-in',
  },
  {
    id: 'scene_01_hook',
    durationInFrames: 240,
    goal: '建立误区：Skill 不是神秘插件。',
    concept: '创作者看着发光的 SKILL 方块。',
    narration: '很多人第一次听到 Skill，会以为它是某种神秘插件。其实不是。',
    narrationBeats: [
      { id: 'beat_01_skill_word', startFrame: 0, durationInFrames: 70, text: '你可能听过一个很酷的词：Skill。', emphasis: true, linkedSubjectIds: ['skill_block'] },
      { id: 'beat_02_plugin_misread', startFrame: 70, durationInFrames: 90, text: '很多人以为它是神秘插件。', linkedSubjectIds: ['creator', 'skill_block'] },
      { id: 'beat_03_not_magic', startFrame: 160, durationInFrames: 80, text: '但真正有用的地方，不在神秘感。', linkedSubjectIds: ['spark'] },
    ],
    layout: 'center-focus',
    background: 'space',
    subjects: [
      { id: 'creator', type: 'human', position: { x: 34, y: 58 }, size: { w: 260, h: 360 }, colorToken: 'sky' },
      { id: 'skill_block', type: 'abstract-shape', position: { x: 58, y: 48 }, size: { w: 360, h: 260 }, colorToken: 'yellow', label: 'SKILL' },
      { id: 'spark', type: 'data-packet', position: { x: 72, y: 34 }, size: { w: 120, h: 120 }, colorToken: 'cyan' },
    ],
    texts: [
      { id: 'title', text: 'Skill is All You Need', position: 'top', emphasis: true },
      { id: 'subtitle', text: '它不是神秘插件', position: 'bottom' },
    ],
    motion: [
      { targetId: 'creator', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'skill_block', type: 'pop-in', startFrame: 12, durationFrames: 32 },
      { targetId: 'spark', type: 'pulse', startFrame: 32, durationFrames: 180 },
    ],
    transitionOut: 'zoom-in',
  },
  {
    id: 'scene_02_forgetful_assistant',
    durationInFrames: 360,
    goal: '说明 AI 聪明但会失忆。',
    concept: 'AI 助理醒来，记忆条归零。',
    narration: 'AI 很聪明，但每次新对话，它都可能忘掉你之前教过的偏好、规则和坑。',
    narrationBeats: [
      { id: 'beat_01_smart_assistant', startFrame: 0, durationInFrames: 90, text: '想象你雇了一位聪明的 AI 助理。', emphasis: true, linkedSubjectIds: ['assistant'] },
      { id: 'beat_02_fast_execution', startFrame: 90, durationInFrames: 100, text: '它理解很快，执行也很快。', linkedSubjectIds: ['assistant', 'packet_a'] },
      { id: 'beat_03_forgets_every_time', startFrame: 190, durationInFrames: 140, text: '但每次新对话前，它都会失忆。', emphasis: true, linkedSubjectIds: ['memory_bar', 'packet_b'] },
    ],
    layout: 'left-right-contrast',
    background: 'data',
    subjects: [
      { id: 'assistant', type: 'ai-assistant', position: { x: 34, y: 52 }, size: { w: 320, h: 320 }, colorToken: 'cyan' },
      { id: 'memory_bar', type: 'abstract-shape', position: { x: 66, y: 48 }, size: { w: 470, h: 120 }, colorToken: 'red', label: 'Memory 0%' },
      { id: 'packet_a', type: 'data-packet', position: { x: 62, y: 66 }, size: { w: 120, h: 90 }, colorToken: 'purple' },
      { id: 'packet_b', type: 'data-packet', position: { x: 77, y: 68 }, size: { w: 120, h: 90 }, colorToken: 'orange' },
    ],
    texts: [
      { id: 'top', text: 'AI 很聪明', position: 'top', emphasis: true },
      { id: 'bottom', text: '但新对话会失忆', position: 'bottom' },
    ],
    motion: [
      { targetId: 'assistant', type: 'slide-in', startFrame: 0, durationFrames: 32, direction: 'left' },
      { targetId: 'memory_bar', type: 'wipe', startFrame: 24, durationFrames: 54 },
      { targetId: 'packet_a', type: 'scatter', startFrame: 52, durationFrames: 120 },
      { targetId: 'packet_b', type: 'scatter', startFrame: 64, durationFrames: 120 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'scene_03_skill_as_manual',
    durationInFrames: 360,
    goal: '把 Skill 定义为岗位手册。',
    concept: '手册打开，出现 Role / Workflow / Rules。',
    narration: 'Skill 更像一本岗位手册，把角色、流程、规则和输出要求写清楚。',
    narrationBeats: [
      { id: 'beat_01_manual_metaphor', startFrame: 0, durationInFrames: 100, text: 'Skill 更像一本岗位手册。', emphasis: true, linkedSubjectIds: ['manual'] },
      { id: 'beat_02_role_workflow_rules', startFrame: 100, durationInFrames: 110, text: '它把角色、流程和规则写清楚。', linkedSubjectIds: ['role', 'workflow', 'rules'] },
      { id: 'beat_03_repeatable_work', startFrame: 210, durationInFrames: 120, text: '下次 AI 接手，就不用从头教。', linkedSubjectIds: ['manual'] },
    ],
    layout: 'center-focus',
    background: 'workspace',
    subjects: [
      { id: 'manual', type: 'manual', position: { x: 50, y: 51 }, size: { w: 520, h: 360 }, colorToken: 'yellow', label: 'Manual' },
      { id: 'role', type: 'index-card', position: { x: 30, y: 38 }, size: { w: 240, h: 140 }, colorToken: 'sky', label: 'Role' },
      { id: 'workflow', type: 'index-card', position: { x: 50, y: 32 }, size: { w: 300, h: 150 }, colorToken: 'green', label: 'Workflow' },
      { id: 'rules', type: 'index-card', position: { x: 70, y: 38 }, size: { w: 240, h: 140 }, colorToken: 'orange', label: 'Rules' },
    ],
    texts: [
      { id: 'top', text: 'Skill 是岗位手册', position: 'top', emphasis: true },
      { id: 'bottom', text: 'Role / Workflow / Rules', position: 'bottom' },
    ],
    motion: [
      { targetId: 'manual', type: 'scale-up', startFrame: 0, durationFrames: 36 },
      { targetId: 'role', type: 'pop-in', startFrame: 28, durationFrames: 24 },
      { targetId: 'workflow', type: 'pop-in', startFrame: 42, durationFrames: 24 },
      { targetId: 'rules', type: 'pop-in', startFrame: 56, durationFrames: 24 },
    ],
    transitionOut: 'morph',
  },
  {
    id: 'scene_04_repeat_to_skill',
    durationInFrames: 360,
    goal: '说明重复教 AI 的内容值得沉淀。',
    concept: 'prompt 气泡堆积并压缩成手册。',
    narration: '当你反复教 AI 同一件事，那件事就值得沉淀成 Skill。',
    narrationBeats: [
      { id: 'beat_01_repeated_instruction', startFrame: 0, durationInFrames: 110, text: '反复教同一件事，先别急着加 prompt。', linkedSubjectIds: ['bubble_1', 'bubble_2'] },
      { id: 'beat_02_patterns_emerge', startFrame: 110, durationInFrames: 100, text: '重复的格式、流程和避坑，就是模式。', linkedSubjectIds: ['bubble_1', 'bubble_2', 'bubble_3'] },
      { id: 'beat_03_compress_to_skill', startFrame: 210, durationInFrames: 120, text: '把模式压缩成手册，它就变成 Skill。', emphasis: true, linkedSubjectIds: ['manual'] },
    ],
    layout: 'vertical-scale',
    background: 'abstract',
    subjects: [
      { id: 'bubble_1', type: 'prompt-bubble', position: { x: 29, y: 60 }, size: { w: 330, h: 130 }, colorToken: 'sky', label: '格式要求' },
      { id: 'bubble_2', type: 'prompt-bubble', position: { x: 43, y: 46 }, size: { w: 320, h: 130 }, colorToken: 'purple', label: '流程步骤' },
      { id: 'bubble_3', type: 'prompt-bubble', position: { x: 57, y: 60 }, size: { w: 330, h: 130 }, colorToken: 'orange', label: '避坑规则' },
      { id: 'manual', type: 'manual', position: { x: 74, y: 48 }, size: { w: 300, h: 240 }, colorToken: 'yellow', label: 'Skill' },
    ],
    texts: [
      { id: 'top', text: '反复教 AI 同一件事', position: 'top', emphasis: true },
      { id: 'bottom', text: '就值得沉淀成 Skill', position: 'bottom' },
    ],
    motion: [
      { targetId: 'bubble_1', type: 'slide-in', startFrame: 0, durationFrames: 28, direction: 'left' },
      { targetId: 'bubble_2', type: 'slide-in', startFrame: 14, durationFrames: 28, direction: 'up' },
      { targetId: 'bubble_3', type: 'slide-in', startFrame: 28, durationFrames: 28, direction: 'right' },
      { targetId: 'manual', type: 'compress', startFrame: 72, durationFrames: 60 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'scene_05_markdown_structure',
    durationInFrames: 360,
    goal: '解释 Skill 的物理形态。',
    concept: 'Markdown 文件拆成 YAML + 工作流正文。',
    narration: '在文件形态上，它通常就是一个 Markdown 文件，前面是触发描述，正文是工作规则。',
    narrationBeats: [
      { id: 'beat_01_markdown_file', startFrame: 0, durationInFrames: 100, text: '它通常就是一个 Markdown 文件。', emphasis: true, linkedSubjectIds: ['md'] },
      { id: 'beat_02_yaml_trigger', startFrame: 100, durationInFrames: 110, text: '前面写触发条件：什么时候调用。', linkedSubjectIds: ['yaml', 'arrow'] },
      { id: 'beat_03_body_rules', startFrame: 210, durationInFrames: 120, text: '正文写工作规则：怎么执行。', linkedSubjectIds: ['body'] },
    ],
    layout: 'zoom-in-cross-section',
    background: 'plain',
    subjects: [
      { id: 'md', type: 'markdown-file', position: { x: 36, y: 52 }, size: { w: 360, h: 480 }, colorToken: 'white', label: 'SKILL.md' },
      { id: 'yaml', type: 'index-card', position: { x: 64, y: 40 }, size: { w: 400, h: 170 }, colorToken: 'cyan', label: 'YAML: 触发条件' },
      { id: 'body', type: 'index-card', position: { x: 64, y: 60 }, size: { w: 440, h: 190 }, colorToken: 'green', label: '正文: 工作流程' },
      { id: 'arrow', type: 'arrow', position: { x: 51, y: 52 }, size: { w: 180, h: 90 }, colorToken: 'ink' },
    ],
    texts: [
      { id: 'top', text: 'Skill 的物理形态', position: 'top', emphasis: true },
      { id: 'bottom', text: '.md = 触发条件 + 工作规则', position: 'bottom' },
    ],
    motion: [
      { targetId: 'md', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'arrow', type: 'connect', startFrame: 28, durationFrames: 44 },
      { targetId: 'yaml', type: 'slide-in', startFrame: 50, durationFrames: 32, direction: 'right' },
      { targetId: 'body', type: 'slide-in', startFrame: 66, durationFrames: 32, direction: 'right' },
    ],
    transitionOut: 'zoom-out',
  },
  {
    id: 'scene_06_skill_index',
    durationInFrames: 420,
    goal: '说明 SKILL_INDEX 是索引。',
    concept: 'AI 进入图书馆查索引并取书。',
    narration: 'SKILL_INDEX 像图书馆索引，告诉 AI 有哪些手册、何时调用、去哪里找。',
    narrationBeats: [
      { id: 'beat_01_index_metaphor', startFrame: 0, durationInFrames: 120, text: 'SKILL_INDEX 像图书馆索引。', emphasis: true, linkedSubjectIds: ['index', 'shelf'] },
      { id: 'beat_02_where_to_find', startFrame: 120, durationInFrames: 130, text: '它告诉 AI：有哪些手册、放在哪里。', linkedSubjectIds: ['assistant', 'shelf', 'index'] },
      { id: 'beat_03_when_to_use', startFrame: 250, durationInFrames: 130, text: '也告诉 AI：什么时候取哪一本。', linkedSubjectIds: ['book', 'assistant'] },
    ],
    layout: 'library-system',
    background: 'library',
    subjects: [
      { id: 'assistant', type: 'ai-assistant', position: { x: 22, y: 57 }, size: { w: 240, h: 260 }, colorToken: 'cyan' },
      { id: 'shelf', type: 'library-shelf', position: { x: 53, y: 52 }, size: { w: 650, h: 420 }, colorToken: 'navy', label: 'Skill Library' },
      { id: 'index', type: 'index-card', position: { x: 78, y: 34 }, size: { w: 330, h: 180 }, colorToken: 'yellow', label: 'SKILL_INDEX' },
      { id: 'book', type: 'manual', position: { x: 74, y: 64 }, size: { w: 220, h: 180 }, colorToken: 'green', label: 'Prompt Skill' },
    ],
    texts: [
      { id: 'top', text: 'SKILL_INDEX 是索引', position: 'top', emphasis: true },
      { id: 'bottom', text: 'AI 先查目录，再取手册', position: 'bottom' },
    ],
    motion: [
      { targetId: 'assistant', type: 'slide-in', startFrame: 0, durationFrames: 36, direction: 'left' },
      { targetId: 'shelf', type: 'fade-in', startFrame: 10, durationFrames: 24 },
      { targetId: 'index', type: 'pulse', startFrame: 48, durationFrames: 160 },
      { targetId: 'book', type: 'pop-in', startFrame: 92, durationFrames: 30 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'scene_07_common_mistakes',
    durationInFrames: 360,
    goal: '列出三个常见误区。',
    concept: 'Not Magic / Missing Files / No Backup。',
    narration: '常见误区有三个：把 Skill 当魔法、漏掉附属文件、没有版本存档。',
    narrationBeats: [
      { id: 'beat_01_not_magic', startFrame: 0, durationInFrames: 100, text: '第一个误区：把 Skill 当魔法。', linkedSubjectIds: ['mistake_1'] },
      { id: 'beat_02_missing_files', startFrame: 100, durationInFrames: 110, text: '第二个误区：漏掉引用文件。', linkedSubjectIds: ['mistake_2'] },
      { id: 'beat_03_no_backup', startFrame: 210, durationInFrames: 110, text: '第三个误区：没有版本存档。', linkedSubjectIds: ['mistake_3'] },
    ],
    layout: 'left-right-contrast',
    background: 'data',
    subjects: [
      { id: 'mistake_1', type: 'warning-icon', position: { x: 28, y: 50 }, size: { w: 260, h: 230 }, colorToken: 'red', label: 'Not Magic' },
      { id: 'mistake_2', type: 'warning-icon', position: { x: 50, y: 50 }, size: { w: 260, h: 230 }, colorToken: 'orange', label: 'Missing Files' },
      { id: 'mistake_3', type: 'warning-icon', position: { x: 72, y: 50 }, size: { w: 260, h: 230 }, colorToken: 'yellow', label: 'No Backup' },
    ],
    texts: [
      { id: 'top', text: '三个常见误区', position: 'top', emphasis: true },
      { id: 'bottom', text: '不是魔法 / 别漏文件 / 要做版本存档', position: 'bottom' },
    ],
    motion: [
      { targetId: 'mistake_1', type: 'shake', startFrame: 20, durationFrames: 80 },
      { targetId: 'mistake_2', type: 'shake', startFrame: 50, durationFrames: 80 },
      { targetId: 'mistake_3', type: 'shake', startFrame: 80, durationFrames: 80 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'scene_08_ending_system',
    durationInFrames: 240,
    goal: '收束：工作流变成个人系统。',
    concept: '多本手册环绕创作者形成能力库。',
    narration: '最后，Skill 不是终点。它是把你的工作流变成个人系统的开始。',
    narrationBeats: [
      { id: 'beat_01_not_the_end', startFrame: 0, durationInFrames: 80, text: '最后，Skill 不是终点。', linkedSubjectIds: ['creator'] },
      { id: 'beat_02_personal_system', startFrame: 80, durationInFrames: 80, text: '它让工作流变成个人系统。', emphasis: true, linkedSubjectIds: ['manual_a', 'manual_b'] },
      { id: 'beat_03_skill_library', startFrame: 160, durationInFrames: 80, text: '手册越多，能力库越完整。', linkedSubjectIds: ['manual_c', 'manual_d'] },
    ],
    layout: 'circular-system',
    background: 'workspace',
    subjects: [
      { id: 'creator', type: 'human', position: { x: 50, y: 55 }, size: { w: 240, h: 320 }, colorToken: 'sky' },
      { id: 'manual_a', type: 'manual', position: { x: 32, y: 38 }, size: { w: 210, h: 170 }, colorToken: 'yellow', label: 'Prompt' },
      { id: 'manual_b', type: 'manual', position: { x: 68, y: 38 }, size: { w: 210, h: 170 }, colorToken: 'green', label: 'Video' },
      { id: 'manual_c', type: 'manual', position: { x: 28, y: 68 }, size: { w: 210, h: 170 }, colorToken: 'purple', label: 'Review' },
      { id: 'manual_d', type: 'manual', position: { x: 72, y: 68 }, size: { w: 210, h: 170 }, colorToken: 'orange', label: 'Archive' },
    ],
    texts: [
      { id: 'top', text: '把工作流变成个人系统', position: 'top', emphasis: true },
      { id: 'bottom', text: 'Skill 不是终点，是系统开始', position: 'bottom' },
    ],
    motion: [
      { targetId: 'creator', type: 'pop-in', startFrame: 0, durationFrames: 30 },
      { targetId: 'manual_a', type: 'zoom', startFrame: 20, durationFrames: 70 },
      { targetId: 'manual_b', type: 'zoom', startFrame: 30, durationFrames: 70 },
      { targetId: 'manual_c', type: 'zoom', startFrame: 40, durationFrames: 70 },
      { targetId: 'manual_d', type: 'zoom', startFrame: 50, durationFrames: 70 },
    ],
    transitionOut: 'fade',
  },
];

export const TOTAL_FRAMES = sceneSpecs.reduce((sum, scene) => sum + scene.durationInFrames, 0);
