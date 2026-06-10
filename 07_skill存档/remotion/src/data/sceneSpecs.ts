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
      { targetId: 'memory_bar', type: 'fade-in', startFrame: 30, durationFrames: 36 },
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
    goal: '说明技能索引是索引层。',
    concept: 'AI 进入图书馆查索引并取书。',
    narration: '技能索引像图书馆索引，告诉 AI 有哪些手册、何时调用、去哪里找。',
    narrationBeats: [
      { id: 'beat_01_index_metaphor', startFrame: 0, durationInFrames: 120, text: '技能索引像图书馆索引。', emphasis: true, linkedSubjectIds: ['index', 'shelf'] },
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
      { id: 'top', text: '技能索引是索引', position: 'top', emphasis: true },
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
  {
    id: 'author_01_loop_closed',
    durationInFrames: 360,
    goal: '把观看行为定义为本片制作链路的闭环验证。',
    concept: '工具链节点依次点亮，最后形成闭环。',
    narration: '感谢你看到这里。如果你喜欢这期视频，那么这条链路就顺利完成了闭环。',
    narrationBeats: [
      { id: 'beat_01_thanks', startFrame: 0, durationInFrames: 120, text: '感谢你看到这里。', linkedSubjectIds: ['viewer'] },
      { id: 'beat_02_like_video', startFrame: 120, durationInFrames: 120, text: '如果你喜欢这期视频，', linkedSubjectIds: ['loop_a', 'loop_b'] },
      { id: 'beat_03_loop_closed', startFrame: 240, durationInFrames: 100, text: '那么这条链路就顺利完成了闭环。', emphasis: true, linkedSubjectIds: ['loop_c', 'loop_d'] },
    ],
    layout: 'circular-system',
    background: 'workspace',
    subjects: [
      { id: 'viewer', type: 'human', position: { x: 50, y: 54 }, size: { w: 220, h: 280 }, colorToken: 'sky', label: 'Viewer' },
      { id: 'loop_a', type: 'index-card', position: { x: 34, y: 36 }, size: { w: 220, h: 130 }, colorToken: 'yellow', label: 'Script' },
      { id: 'loop_b', type: 'index-card', position: { x: 66, y: 36 }, size: { w: 220, h: 130 }, colorToken: 'purple', label: 'Assets' },
      { id: 'loop_c', type: 'index-card', position: { x: 34, y: 70 }, size: { w: 220, h: 130 }, colorToken: 'green', label: 'Render' },
      { id: 'loop_d', type: 'index-card', position: { x: 66, y: 70 }, size: { w: 220, h: 130 }, colorToken: 'orange', label: 'Feedback' },
    ],
    texts: [
      { id: 'top', text: '如果你看到这里', position: 'top', emphasis: true },
      { id: 'bottom', text: '这条链路已经接近闭环', position: 'bottom' },
    ],
    motion: [
      { targetId: 'viewer', type: 'pop-in', startFrame: 0, durationFrames: 30 },
      { targetId: 'loop_a', type: 'pulse', startFrame: 80, durationFrames: 120 },
      { targetId: 'loop_b', type: 'pulse', startFrame: 120, durationFrames: 120 },
      { targetId: 'loop_c', type: 'pulse', startFrame: 180, durationFrames: 120 },
      { targetId: 'loop_d', type: 'pulse', startFrame: 240, durationFrames: 100 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'author_02_ai_made_this',
    durationInFrames: 360,
    goal: '声明本片除核心文稿和作者话以外均由 AI 制作。',
    concept: '图片、动画、配音、配乐、剪辑五个模块并列出现。',
    narration: '这条视频，除了文稿的核心，以及我现在说的这些话以外，全部是 AI 制作的。包括但不限于：图片、动画、配音、配乐，以及剪辑。',
    narrationBeats: [
      { id: 'beat_01_ai_made_this', startFrame: 0, durationInFrames: 170, text: '除了文稿的核心，以及我现在说的这些话以外，全部是 AI 制作的。', emphasis: true, linkedSubjectIds: ['ai_core'] },
      { id: 'beat_02_images_animation', startFrame: 170, durationInFrames: 80, text: '包括图片、动画、配音、配乐，', linkedSubjectIds: ['image', 'motion', 'voice', 'music'] },
      { id: 'beat_03_editing', startFrame: 250, durationInFrames: 80, text: '以及剪辑。', emphasis: true, linkedSubjectIds: ['editing'] },
    ],
    layout: 'network-map',
    background: 'data',
    subjects: [
      { id: 'ai_core', type: 'ai-assistant', position: { x: 50, y: 48 }, size: { w: 260, h: 260 }, colorToken: 'cyan', label: 'AI' },
      { id: 'image', type: 'index-card', position: { x: 28, y: 38 }, size: { w: 220, h: 130 }, colorToken: 'yellow', label: 'Image' },
      { id: 'motion', type: 'index-card', position: { x: 72, y: 38 }, size: { w: 220, h: 130 }, colorToken: 'purple', label: 'Motion' },
      { id: 'voice', type: 'index-card', position: { x: 28, y: 66 }, size: { w: 220, h: 130 }, colorToken: 'green', label: 'Voice' },
      { id: 'music', type: 'index-card', position: { x: 50, y: 72 }, size: { w: 220, h: 130 }, colorToken: 'orange', label: 'Suno' },
      { id: 'editing', type: 'index-card', position: { x: 72, y: 66 }, size: { w: 220, h: 130 }, colorToken: 'sky', label: 'Edit' },
    ],
    texts: [
      { id: 'top', text: '除了核心文稿，几乎全部由 AI 制作', position: 'top', emphasis: true },
      { id: 'bottom', text: '图片 / 动画 / 配音 / 配乐 / 剪辑', position: 'bottom' },
    ],
    motion: [
      { targetId: 'ai_core', type: 'scale-up', startFrame: 0, durationFrames: 36 },
      { targetId: 'image', type: 'pop-in', startFrame: 80, durationFrames: 24 },
      { targetId: 'motion', type: 'pop-in', startFrame: 100, durationFrames: 24 },
      { targetId: 'voice', type: 'pop-in', startFrame: 120, durationFrames: 24 },
      { targetId: 'music', type: 'pop-in', startFrame: 140, durationFrames: 24 },
      { targetId: 'editing', type: 'pop-in', startFrame: 230, durationFrames: 30 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'author_03_motivation',
    durationInFrames: 420,
    goal: '说明个人动机：不会剪辑但想表达。',
    concept: '想法气泡遇到剪辑门槛，最后流向 Skill 流程。',
    narration: '这也是我追求的目标。我有很多稀奇古怪的想法，但是苦于不会剪辑，无法表达。所以我做了这个项目。它不是为了炫技，而是为了把不会剪辑的人，也接入视频表达。',
    narrationBeats: [
      { id: 'beat_01_goal', startFrame: 0, durationInFrames: 80, text: '这也是我追求的目标。', linkedSubjectIds: ['creator'] },
      { id: 'beat_02_many_ideas', startFrame: 80, durationInFrames: 120, text: '我有很多稀奇古怪的想法。', linkedSubjectIds: ['idea_a', 'idea_b', 'idea_c'] },
      { id: 'beat_03_cant_edit', startFrame: 200, durationInFrames: 90, text: '但是苦于不会剪辑，无法表达。', emphasis: true, linkedSubjectIds: ['editing_wall'] },
      { id: 'beat_04_project_reason', startFrame: 290, durationInFrames: 100, text: '所以我做了这个项目。', linkedSubjectIds: ['skill_bridge'] },
    ],
    layout: 'left-right-contrast',
    background: 'workspace',
    subjects: [
      { id: 'creator', type: 'human', position: { x: 26, y: 56 }, size: { w: 260, h: 330 }, colorToken: 'sky' },
      { id: 'idea_a', type: 'prompt-bubble', position: { x: 40, y: 34 }, size: { w: 240, h: 120 }, colorToken: 'yellow', label: 'Idea' },
      { id: 'idea_b', type: 'prompt-bubble', position: { x: 52, y: 46 }, size: { w: 250, h: 120 }, colorToken: 'purple', label: 'Weird' },
      { id: 'idea_c', type: 'prompt-bubble', position: { x: 42, y: 68 }, size: { w: 250, h: 120 }, colorToken: 'green', label: 'Story' },
      { id: 'editing_wall', type: 'warning-icon', position: { x: 66, y: 54 }, size: { w: 300, h: 270 }, colorToken: 'red', label: 'Editing' },
      { id: 'skill_bridge', type: 'manual', position: { x: 78, y: 54 }, size: { w: 220, h: 180 }, colorToken: 'yellow', label: 'Skill' },
    ],
    texts: [
      { id: 'top', text: '想法很多，但不会剪辑', position: 'top', emphasis: true },
      { id: 'bottom', text: '这个项目是表达入口', position: 'bottom' },
    ],
    motion: [
      { targetId: 'creator', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'idea_a', type: 'scatter', startFrame: 70, durationFrames: 90 },
      { targetId: 'idea_b', type: 'scatter', startFrame: 90, durationFrames: 90 },
      { targetId: 'idea_c', type: 'scatter', startFrame: 110, durationFrames: 90 },
      { targetId: 'editing_wall', type: 'shake', startFrame: 190, durationFrames: 90 },
      { targetId: 'skill_bridge', type: 'pop-in', startFrame: 282, durationFrames: 36 },
    ],
    transitionOut: 'morph',
  },
  {
    id: 'author_04_stack',
    durationInFrames: 480,
    goal: '交代六工具技术栈和基础分工。',
    concept: '六个工具节点组成工作流图。',
    narration: '技术栈其实很简单：Midjourney，Seedance，Eleven，Remotion，Suno，还有 Codex。你大体可以猜到它们各自的分工。Midjourney 负责建立视觉锚点。Seedance 负责让图里的机制动起来。Eleven 负责把文稿变成声音。Suno 负责让情绪有一条底层轨道。Remotion 负责时间线、字幕和最终合成。',
    narrationBeats: [
      { id: 'beat_01_stack_names', startFrame: 0, durationInFrames: 130, text: '技术栈其实很简单：Midjourney，Seedance，Eleven，Remotion，Suno，还有 Codex。', linkedSubjectIds: ['mj', 'seedance', 'eleven', 'remotion', 'suno', 'codex'] },
      { id: 'beat_02_roles_hint', startFrame: 130, durationInFrames: 80, text: '你大体可以猜到它们各自的分工。', linkedSubjectIds: ['codex'] },
      { id: 'beat_03_roles', startFrame: 210, durationInFrames: 220, text: '视觉、动画、声音、配乐、时间线，分别交给最适合的工具。', emphasis: true, linkedSubjectIds: ['mj', 'seedance', 'eleven', 'suno', 'remotion'] },
    ],
    layout: 'network-map',
    background: 'data',
    subjects: [
      { id: 'codex', type: 'ai-assistant', position: { x: 50, y: 52 }, size: { w: 260, h: 260 }, colorToken: 'cyan', label: 'Codex' },
      { id: 'mj', type: 'index-card', position: { x: 28, y: 34 }, size: { w: 230, h: 120 }, colorToken: 'yellow', label: 'MJ' },
      { id: 'seedance', type: 'index-card', position: { x: 50, y: 28 }, size: { w: 250, h: 120 }, colorToken: 'purple', label: 'Seedance' },
      { id: 'eleven', type: 'index-card', position: { x: 72, y: 34 }, size: { w: 230, h: 120 }, colorToken: 'green', label: 'Eleven' },
      { id: 'remotion', type: 'index-card', position: { x: 34, y: 72 }, size: { w: 250, h: 120 }, colorToken: 'sky', label: 'Remotion' },
      { id: 'suno', type: 'index-card', position: { x: 66, y: 72 }, size: { w: 230, h: 120 }, colorToken: 'orange', label: 'Suno' },
    ],
    texts: [
      { id: 'top', text: '六个工具，各司其职', position: 'top', emphasis: true },
      { id: 'bottom', text: 'MJ / Seedance / Eleven / Remotion / Suno / Codex', position: 'bottom' },
    ],
    motion: [
      { targetId: 'codex', type: 'pop-in', startFrame: 0, durationFrames: 34 },
      { targetId: 'mj', type: 'pop-in', startFrame: 42, durationFrames: 24 },
      { targetId: 'seedance', type: 'pop-in', startFrame: 62, durationFrames: 24 },
      { targetId: 'eleven', type: 'pop-in', startFrame: 82, durationFrames: 24 },
      { targetId: 'remotion', type: 'pop-in', startFrame: 102, durationFrames: 24 },
      { targetId: 'suno', type: 'pop-in', startFrame: 122, durationFrames: 24 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'author_05_codex_conductor',
    durationInFrames: 300,
    goal: '明确 Codex 是总指挥，Skill 是标准流程。',
    concept: 'Codex 位于中心，手册与工具节点围绕。',
    narration: '而 Codex，是总指挥。一切由 Skill 充当标准流程。Codex 引导众多 AI 工具各司其职。',
    narrationBeats: [
      { id: 'beat_01_codex_conductor', startFrame: 0, durationInFrames: 100, text: '而 Codex，是总指挥。', emphasis: true, linkedSubjectIds: ['codex'] },
      { id: 'beat_02_skill_process', startFrame: 100, durationInFrames: 120, text: '一切由 Skill 充当标准流程。', linkedSubjectIds: ['manual_a', 'manual_b'] },
      { id: 'beat_03_tools_work', startFrame: 220, durationInFrames: 70, text: '众多 AI 工具各司其职。', linkedSubjectIds: ['tool_a', 'tool_b'] },
    ],
    layout: 'circular-system',
    background: 'library',
    subjects: [
      { id: 'codex', type: 'ai-assistant', position: { x: 50, y: 50 }, size: { w: 280, h: 280 }, colorToken: 'cyan', label: 'Codex' },
      { id: 'manual_a', type: 'manual', position: { x: 32, y: 42 }, size: { w: 210, h: 160 }, colorToken: 'yellow', label: 'Skill' },
      { id: 'manual_b', type: 'manual', position: { x: 68, y: 42 }, size: { w: 210, h: 160 }, colorToken: 'green', label: 'Process' },
      { id: 'tool_a', type: 'data-packet', position: { x: 34, y: 70 }, size: { w: 150, h: 110 }, colorToken: 'purple', label: 'AI Tool' },
      { id: 'tool_b', type: 'data-packet', position: { x: 66, y: 70 }, size: { w: 150, h: 110 }, colorToken: 'orange', label: 'AI Tool' },
    ],
    texts: [
      { id: 'top', text: 'Codex 是总指挥', position: 'top', emphasis: true },
      { id: 'bottom', text: 'Skill 是标准流程', position: 'bottom' },
    ],
    motion: [
      { targetId: 'codex', type: 'pulse', startFrame: 0, durationFrames: 180 },
      { targetId: 'manual_a', type: 'zoom', startFrame: 60, durationFrames: 80 },
      { targetId: 'manual_b', type: 'zoom', startFrame: 80, durationFrames: 80 },
      { targetId: 'tool_a', type: 'connect', startFrame: 160, durationFrames: 80 },
      { targetId: 'tool_b', type: 'connect', startFrame: 180, durationFrames: 80 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'author_06_industrialization',
    durationInFrames: 450,
    goal: '提出任意文稿工业化生成任意风格视频的愿景，并邀请参与调优。',
    concept: '文稿进入生产流水线，输出多种风格视频卡片。',
    narration: '理论上，只要把 prompt 调优到足够稳定，就可以把任意文稿，工业化地、自动化地，生产成任意风格的视频。而这个调优过程，需要各位的参与。我的能力有限，只能抛砖引玉。',
    narrationBeats: [
      { id: 'beat_01_industrialize', startFrame: 0, durationInFrames: 170, text: '只要把 prompt 调优到足够稳定，就可以把任意文稿工业化地生产成视频。', emphasis: true, linkedSubjectIds: ['document', 'pipeline'] },
      { id: 'beat_02_any_style', startFrame: 170, durationInFrames: 110, text: '任意文稿，任意风格，自动进入流程。', linkedSubjectIds: ['style_a', 'style_b'] },
      { id: 'beat_03_need_you', startFrame: 280, durationInFrames: 80, text: '而这个调优过程，需要各位的参与。', linkedSubjectIds: ['viewer'] },
      { id: 'beat_04_limited', startFrame: 360, durationInFrames: 70, text: '我的能力有限，只能抛砖引玉。', linkedSubjectIds: ['creator'] },
    ],
    layout: 'left-right-contrast',
    background: 'abstract',
    subjects: [
      { id: 'document', type: 'markdown-file', position: { x: 24, y: 52 }, size: { w: 250, h: 340 }, colorToken: 'white', label: 'Draft' },
      { id: 'pipeline', type: 'arrow', position: { x: 49, y: 52 }, size: { w: 260, h: 120 }, colorToken: 'ink' },
      { id: 'style_a', type: 'index-card', position: { x: 72, y: 40 }, size: { w: 240, h: 150 }, colorToken: 'yellow', label: 'Style A' },
      { id: 'style_b', type: 'index-card', position: { x: 72, y: 64 }, size: { w: 240, h: 150 }, colorToken: 'purple', label: 'Style B' },
      { id: 'viewer', type: 'human', position: { x: 48, y: 74 }, size: { w: 160, h: 210 }, colorToken: 'sky', label: 'You' },
      { id: 'creator', type: 'human', position: { x: 32, y: 74 }, size: { w: 160, h: 210 }, colorToken: 'green', label: 'Author' },
    ],
    texts: [
      { id: 'top', text: '任意文稿 → 任意风格视频', position: 'top', emphasis: true },
      { id: 'bottom', text: '关键在调优与参与', position: 'bottom' },
    ],
    motion: [
      { targetId: 'document', type: 'slide-in', startFrame: 0, durationFrames: 32, direction: 'left' },
      { targetId: 'pipeline', type: 'connect', startFrame: 70, durationFrames: 90 },
      { targetId: 'style_a', type: 'pop-in', startFrame: 150, durationFrames: 28 },
      { targetId: 'style_b', type: 'pop-in', startFrame: 180, durationFrames: 28 },
      { targetId: 'viewer', type: 'fade-in', startFrame: 270, durationFrames: 36 },
      { targetId: 'creator', type: 'fade-in', startFrame: 330, durationFrames: 36 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'author_07_open_source',
    durationInFrames: 540,
    goal: '记录作者关于开源的个人立场。',
    concept: '极简宣言卡片，逐句压低信息密度。',
    narration: '最后，我想记录一些个人看法。不感兴趣的话，现在可以酌情关闭视频了。有朋友问我：这个项目这么有价值，还要坚持开源吗？我的回答是：开源。而且是一定要开源。就要狠狠打所谓大厂的脸。因为，正如群星必须回归轨道，“无产阶级”的铡刀也终将落下。',
    narrationBeats: [
      { id: 'beat_01_personal_view', startFrame: 0, durationInFrames: 80, text: '最后，我想记录一些个人看法。', linkedSubjectIds: ['note'] },
      { id: 'beat_02_can_close', startFrame: 80, durationInFrames: 80, text: '不感兴趣的话，现在可以酌情关闭视频了。', linkedSubjectIds: ['note'] },
      { id: 'beat_03_question', startFrame: 160, durationInFrames: 110, text: '有朋友问我：这个项目这么有价值，还要坚持开源吗？', linkedSubjectIds: ['question'] },
      { id: 'beat_04_open_source', startFrame: 270, durationInFrames: 100, text: '我的回答是：开源。而且是一定要开源。', emphasis: true, linkedSubjectIds: ['open_source'] },
      { id: 'beat_05_face', startFrame: 370, durationInFrames: 70, text: '就要狠狠打所谓大厂的脸。', linkedSubjectIds: ['open_source'] },
      { id: 'beat_06_final_statement', startFrame: 440, durationInFrames: 90, text: '因为，正如群星必须回归轨道，“无产阶级”的铡刀也终将落下。', emphasis: true, linkedSubjectIds: ['final_card'] },
    ],
    layout: 'center-focus',
    background: 'plain',
    subjects: [
      { id: 'note', type: 'markdown-file', position: { x: 50, y: 52 }, size: { w: 520, h: 360 }, colorToken: 'white', label: 'Author Note' },
      { id: 'question', type: 'prompt-bubble', position: { x: 50, y: 42 }, size: { w: 560, h: 150 }, colorToken: 'sky', label: 'Open source?' },
      { id: 'open_source', type: 'manual', position: { x: 50, y: 54 }, size: { w: 420, h: 260 }, colorToken: 'yellow', label: 'OPEN SOURCE' },
      { id: 'final_card', type: 'index-card', position: { x: 50, y: 58 }, size: { w: 620, h: 230 }, colorToken: 'red', label: 'Declaration' },
    ],
    texts: [
      { id: 'top', text: '作者的话', position: 'top', emphasis: true },
      { id: 'bottom', text: '开源，而且一定要开源', position: 'bottom', emphasis: true },
    ],
    motion: [
      { targetId: 'note', type: 'fade-in', startFrame: 0, durationFrames: 30 },
      { targetId: 'question', type: 'pop-in', startFrame: 150, durationFrames: 30 },
      { targetId: 'open_source', type: 'scale-up', startFrame: 260, durationFrames: 42 },
      { targetId: 'final_card', type: 'pulse', startFrame: 420, durationFrames: 90 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'author_08_final_words',
    durationInFrames: 240,
    goal: '片尾收束项目名、方法和作者署名。',
    concept: '项目名、流程方法、作者署名依次出现。',
    narration: 'Skill Is All You Need。把流程写成手册，把手册交给 AI，把想法变成作品。作者：跳蛛先生。',
    narrationBeats: [
      { id: 'beat_01_title', startFrame: 0, durationInFrames: 70, text: 'Skill Is All You Need。', emphasis: true, linkedSubjectIds: ['title_card'] },
      { id: 'beat_02_method', startFrame: 70, durationInFrames: 100, text: '把流程写成手册，把手册交给 AI，把想法变成作品。', linkedSubjectIds: ['manual', 'creator'] },
      { id: 'beat_03_credit', startFrame: 170, durationInFrames: 60, text: '作者：跳蛛先生。', linkedSubjectIds: ['creator'] },
    ],
    layout: 'center-focus',
    background: 'space',
    subjects: [
      { id: 'title_card', type: 'abstract-shape', position: { x: 50, y: 40 }, size: { w: 520, h: 180 }, colorToken: 'yellow', label: 'Skill Is All You Need' },
      { id: 'manual', type: 'manual', position: { x: 42, y: 64 }, size: { w: 210, h: 170 }, colorToken: 'green', label: 'Manual' },
      { id: 'creator', type: 'human', position: { x: 60, y: 64 }, size: { w: 190, h: 230 }, colorToken: 'sky', label: 'Author' },
    ],
    texts: [
      { id: 'top', text: 'Skill Is All You Need', position: 'top', emphasis: true },
      { id: 'bottom', text: '跳蛛先生', position: 'bottom' },
    ],
    motion: [
      { targetId: 'title_card', type: 'scale-up', startFrame: 0, durationFrames: 40 },
      { targetId: 'manual', type: 'pop-in', startFrame: 70, durationFrames: 28 },
      { targetId: 'creator', type: 'fade-in', startFrame: 130, durationFrames: 40 },
    ],
    transitionOut: 'fade',
  },
];

export const TOTAL_FRAMES = sceneSpecs.reduce((sum, scene) => sum + scene.durationInFrames, 0);
