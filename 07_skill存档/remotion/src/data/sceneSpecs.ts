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

// v3.1（2026-06-16）。母题：助产(maieutic)↔尸检(postmortem)，《流浪地球2》"完整的一生"串联。
// 贯穿案例=真实双题复盘翻车。narrationBeats 的 durationInFrames 为估算值，仅作 motion 重锚的
// 估算域；真实时长来自 Eleven 生成的 fullFilmVoiceoverTiming，FullFilmVideo build 时自动重锚 motion。
export const sceneSpecs: SceneSpec[] = [
  {
    id: 'scene_00_two_partners',
    durationInFrames: 600,
    goal: '冷开场：用"助产士 + 法医"这对反差搭档，立刻抛出生死母题。',
    concept: '左暖助产、右冷尸检，中间是被托付一生的"作品"。',
    narration:
      '我给我的创作，配了俩搭档：一个助产士，一个法医。创作之前，助产士帮我把脑子里那团乱麻，接生成一个清楚的想法。作品做完，法医给它来一次冷静的尸检，不许自我美化。一头接生，一头验尸。我想给我做的每个东西，一个完整的一生。',
    narrationBeats: [
      { id: 'intro_01_two_partners', startFrame: 0, durationInFrames: 150, text: '我给我的创作，配了俩搭档：一个助产士，一个法医。', emphasis: true, linkedSubjectIds: ['midwife', 'coroner'] },
      { id: 'intro_02_midwife', startFrame: 150, durationInFrames: 160, text: '创作之前，助产士帮我把脑子里那团乱麻，接生成一个清楚的想法。', linkedSubjectIds: ['midwife', 'creation'] },
      { id: 'intro_03_coroner', startFrame: 310, durationInFrames: 140, text: '作品做完，法医给它来一次冷静的尸检，不许自我美化。', linkedSubjectIds: ['coroner'] },
      { id: 'intro_04_whole_life', startFrame: 450, durationInFrames: 150, text: '一头接生，一头验尸。我想给我做的每个东西，一个完整的一生。', emphasis: true, linkedSubjectIds: ['creation'] },
    ],
    layout: 'left-right-contrast',
    background: 'workspace',
    subjects: [
      { id: 'midwife', type: 'manual', position: { x: 24, y: 48 }, size: { w: 300, h: 220 }, colorToken: 'yellow', label: '助产' },
      { id: 'creation', type: 'abstract-shape', position: { x: 50, y: 52 }, size: { w: 240, h: 240 }, colorToken: 'green', label: '作品' },
      { id: 'coroner', type: 'manual', position: { x: 76, y: 48 }, size: { w: 300, h: 220 }, colorToken: 'sky', label: '尸检' },
    ],
    texts: [
      { id: 'top', text: '助产士 × 法医', position: 'top', emphasis: true },
      { id: 'bottom', text: '给创作，一个完整的一生', position: 'bottom' },
    ],
    motion: [
      { targetId: 'midwife', type: 'slide-in', startFrame: 8, durationFrames: 30, direction: 'left' },
      { targetId: 'creation', type: 'pop-in', startFrame: 160, durationFrames: 30 },
      { targetId: 'coroner', type: 'slide-in', startFrame: 312, durationFrames: 30, direction: 'right' },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'scene_01_what_is_skill',
    durationInFrames: 255,
    goal: '把两个搭档落地成同一个东西：Skill。',
    concept: '两本手册并列，合成一个发光的 SKILL。',
    narration: '这俩搭档，不是什么神秘 AI。说穿了，就是两份我写给 AI 的工作手册。这种手册，有个名字，叫 Skill。',
    narrationBeats: [
      { id: 'teaching_01_not_mystery', startFrame: 0, durationInFrames: 165, text: '这俩搭档，不是什么神秘 AI。说穿了，就是两份我写给 AI 的工作手册。', linkedSubjectIds: ['manual_a', 'manual_b'] },
      { id: 'teaching_02_called_skill', startFrame: 165, durationInFrames: 90, text: '这种手册，有个名字，叫 Skill。', emphasis: true, linkedSubjectIds: ['skill_block'] },
    ],
    layout: 'center-focus',
    background: 'space',
    subjects: [
      { id: 'manual_a', type: 'manual', position: { x: 30, y: 54 }, size: { w: 260, h: 200 }, colorToken: 'yellow', label: '助产' },
      { id: 'manual_b', type: 'manual', position: { x: 70, y: 54 }, size: { w: 260, h: 200 }, colorToken: 'sky', label: '尸检' },
      { id: 'skill_block', type: 'abstract-shape', position: { x: 50, y: 47 }, size: { w: 360, h: 250 }, colorToken: 'yellow', label: 'SKILL' },
    ],
    texts: [
      { id: 'top', text: '它们不是神秘 AI', position: 'top', emphasis: true },
      { id: 'bottom', text: '就是写给 AI 的工作手册 = Skill', position: 'bottom' },
    ],
    motion: [
      { targetId: 'manual_a', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'manual_b', type: 'fade-in', startFrame: 12, durationFrames: 24 },
      { targetId: 'skill_block', type: 'scale-up', startFrame: 165, durationFrames: 40 },
    ],
    transitionOut: 'zoom-in',
  },
  {
    id: 'scene_02_coroner_rule',
    durationInFrames: 190,
    goal: '聚焦法医，给出它唯一的铁律。',
    concept: '法医手册旁，浮出"先冻结事实，再写判断"。',
    narration: '篇幅原因，我们先来调研一下法医。它只有一条铁律：先冻结事实，再写判断。',
    narrationBeats: [
      { id: 'teaching_03_investigate_coroner', startFrame: 0, durationInFrames: 190, text: '篇幅原因，我们先来调研一下法医。它只有一条铁律：先冻结事实，再写判断。', emphasis: true, linkedSubjectIds: ['coroner', 'rule_card'] },
    ],
    layout: 'center-focus',
    background: 'plain',
    subjects: [
      { id: 'coroner', type: 'manual', position: { x: 38, y: 52 }, size: { w: 360, h: 280 }, colorToken: 'sky', label: '法医 Skill' },
      { id: 'rule_card', type: 'index-card', position: { x: 68, y: 46 }, size: { w: 420, h: 170 }, colorToken: 'red', label: '先冻结事实，再写判断' },
    ],
    texts: [
      { id: 'top', text: '法医的铁律', position: 'top', emphasis: true },
      { id: 'bottom', text: '先冻结事实，再写判断', position: 'bottom' },
    ],
    motion: [
      { targetId: 'coroner', type: 'scale-up', startFrame: 0, durationFrames: 30 },
      { targetId: 'rule_card', type: 'slide-in', startFrame: 60, durationFrames: 32, direction: 'right' },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'scene_03_crash_case',
    durationInFrames: 545,
    goal: '真实翻车：把偏爱的方案当成获胜的方案。',
    concept: '复盘记录被误标为"获奖"，AI 放大成 11 条假经验，最后被戳穿。',
    narration:
      '上个月我打了一场双题比赛，两道题的方案票数都靠前，但都没获奖。可我自己整理记录的时候，顺手就把它写成了“获奖图复盘”。AI 接着这份记录往下整合，真就当成获奖作品，给我分析出十一条“成功经验”。可它根本没获奖。我把我偏爱的方案，当成了获胜的方案。',
    narrationBeats: [
      { id: 'teaching_04_double_contest', startFrame: 0, durationInFrames: 250, text: '上个月我打了一场双题比赛，两道题的方案票数都靠前，但都没获奖。可我自己整理记录的时候，顺手就把它写成了“获奖图复盘”。', linkedSubjectIds: ['record', 'mislabel'] },
      { id: 'teaching_05_eleven_claims', startFrame: 250, durationInFrames: 165, text: 'AI 接着这份记录往下整合，真就当成获奖作品，给我分析出十一条“成功经验”。', linkedSubjectIds: ['claim_stack'] },
      { id: 'teaching_06_not_won', startFrame: 415, durationInFrames: 130, text: '可它根本没获奖。我把我偏爱的方案，当成了获胜的方案。', emphasis: true, linkedSubjectIds: ['verdict'] },
    ],
    layout: 'vertical-scale',
    background: 'data',
    subjects: [
      { id: 'record', type: 'markdown-file', position: { x: 26, y: 54 }, size: { w: 280, h: 380 }, colorToken: 'white', label: '复盘记录' },
      { id: 'mislabel', type: 'index-card', position: { x: 52, y: 64 }, size: { w: 320, h: 130 }, colorToken: 'yellow', label: '“获奖图复盘”' },
      { id: 'claim_stack', type: 'index-card', position: { x: 56, y: 38 }, size: { w: 340, h: 150 }, colorToken: 'green', label: '11 条成功经验' },
      { id: 'verdict', type: 'warning-icon', position: { x: 80, y: 52 }, size: { w: 300, h: 270 }, colorToken: 'red', label: '其实没获奖' },
    ],
    texts: [
      { id: 'top', text: '真实翻车', position: 'top', emphasis: true },
      { id: 'bottom', text: '把偏爱的方案，当成获胜的方案', position: 'bottom' },
    ],
    motion: [
      { targetId: 'record', type: 'slide-in', startFrame: 0, durationFrames: 30, direction: 'left' },
      { targetId: 'mislabel', type: 'pop-in', startFrame: 130, durationFrames: 26 },
      { targetId: 'claim_stack', type: 'scatter', startFrame: 250, durationFrames: 120 },
      { targetId: 'verdict', type: 'shake', startFrame: 420, durationFrames: 100 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'scene_04_freeze_facts',
    durationInFrames: 420,
    goal: '修复 + payoff：手册逼 AI 先冻结事实。',
    concept: '.md 顶部锁死"事实记录·不可修改区"，AI 被拦下来反问。',
    narration:
      '法医这份手册，逼 AI 动笔前，先在文档最顶上锁死一行事实：这东西到底获奖没有？这行填完，才准往下写。于是同一份记录，这次它先把我拦下来：先说清楚，它获奖了吗？那十一条自我表扬，从源头就没了。',
    narrationBeats: [
      { id: 'teaching_07_freeze_first', startFrame: 0, durationInFrames: 220, text: '法医这份手册，逼 AI 动笔前，先在文档最顶上锁死一行事实：这东西到底获奖没有？这行填完，才准往下写。', emphasis: true, linkedSubjectIds: ['md', 'freeze_block'] },
      { id: 'teaching_08_payoff', startFrame: 220, durationInFrames: 200, text: '于是同一份记录，这次它先把我拦下来：先说清楚，它获奖了吗？那十一条自我表扬，从源头就没了。', linkedSubjectIds: ['gate'] },
    ],
    layout: 'zoom-in-cross-section',
    background: 'plain',
    subjects: [
      { id: 'md', type: 'markdown-file', position: { x: 34, y: 52 }, size: { w: 340, h: 460 }, colorToken: 'white', label: 'SKILL.md' },
      { id: 'freeze_block', type: 'index-card', position: { x: 66, y: 38 }, size: { w: 440, h: 180 }, colorToken: 'red', label: '事实记录·不可修改区' },
      { id: 'gate', type: 'warning-icon', position: { x: 66, y: 64 }, size: { w: 300, h: 240 }, colorToken: 'orange', label: '获奖了吗？' },
    ],
    texts: [
      { id: 'top', text: '先冻结事实', position: 'top', emphasis: true },
      { id: 'bottom', text: '填完，才准往下写', position: 'bottom' },
    ],
    motion: [
      { targetId: 'md', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'freeze_block', type: 'slide-in', startFrame: 40, durationFrames: 32, direction: 'right' },
      { targetId: 'gate', type: 'pop-in', startFrame: 220, durationFrames: 30 },
    ],
    transitionOut: 'zoom-out',
  },
  {
    id: 'scene_05_markdown_form',
    durationInFrames: 270,
    goal: '解释 Skill 的物理形态：一个 Markdown 文件。',
    concept: 'SKILL.md = 触发条件 + 工作规矩（头一条禁止项）。',
    narration:
      '说穿了，这手册就是个 Markdown 文件。开头写它什么时候被调用，正文写它要守的规矩，头一条就是：禁止把你偏爱的方案，写成获胜的方案。',
    narrationBeats: [
      { id: 'teaching_09_markdown_form', startFrame: 0, durationInFrames: 270, text: '说穿了，这手册就是个 Markdown 文件。开头写它什么时候被调用，正文写它要守的规矩，头一条就是：禁止把你偏爱的方案，写成获胜的方案。', emphasis: true, linkedSubjectIds: ['md', 'yaml', 'body'] },
    ],
    layout: 'zoom-in-cross-section',
    background: 'plain',
    subjects: [
      { id: 'md', type: 'markdown-file', position: { x: 34, y: 52 }, size: { w: 340, h: 460 }, colorToken: 'white', label: 'SKILL.md' },
      { id: 'yaml', type: 'index-card', position: { x: 66, y: 38 }, size: { w: 420, h: 160 }, colorToken: 'cyan', label: '触发：何时调用' },
      { id: 'body', type: 'index-card', position: { x: 66, y: 62 }, size: { w: 460, h: 190 }, colorToken: 'green', label: '正文：禁止把偏爱当获胜' },
      { id: 'arrow', type: 'arrow', position: { x: 51, y: 52 }, size: { w: 170, h: 90 }, colorToken: 'ink' },
    ],
    texts: [
      { id: 'top', text: '它就是一个 Markdown 文件', position: 'top', emphasis: true },
      { id: 'bottom', text: '触发条件 + 工作规矩', position: 'bottom' },
    ],
    motion: [
      { targetId: 'md', type: 'fade-in', startFrame: 0, durationFrames: 24 },
      { targetId: 'arrow', type: 'connect', startFrame: 28, durationFrames: 44 },
      { targetId: 'yaml', type: 'slide-in', startFrame: 60, durationFrames: 32, direction: 'right' },
      { targetId: 'body', type: 'slide-in', startFrame: 120, durationFrames: 32, direction: 'right' },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'scene_06_three_mistakes',
    durationInFrames: 505,
    goal: '三个常见误区，快切清单。',
    concept: '当魔法 / 漏文件 / 不存版本。',
    narration:
      '用 Skill，最容易踩三个坑。一，把它当魔法。它不让烂内容变好，只让流程变稳。二，漏掉它引用的文件。点名的模板没带上，AI 照样抓瞎。三，不存版本。调好的手册被随手一改覆盖，连备份都没有。',
    narrationBeats: [
      { id: 'teaching_10_mistakes_intro', startFrame: 0, durationInFrames: 80, text: '用 Skill，最容易踩三个坑。', emphasis: true, linkedSubjectIds: ['m1', 'm2', 'm3'] },
      { id: 'teaching_11_not_magic', startFrame: 80, durationInFrames: 140, text: '一，把它当魔法。它不让烂内容变好，只让流程变稳。', linkedSubjectIds: ['m1'] },
      { id: 'teaching_12_missing_files', startFrame: 220, durationInFrames: 145, text: '二，漏掉它引用的文件。点名的模板没带上，AI 照样抓瞎。', linkedSubjectIds: ['m2'] },
      { id: 'teaching_13_no_backup', startFrame: 365, durationInFrames: 140, text: '三，不存版本。调好的手册被随手一改覆盖，连备份都没有。', linkedSubjectIds: ['m3'] },
    ],
    layout: 'left-right-contrast',
    background: 'data',
    subjects: [
      { id: 'm1', type: 'warning-icon', position: { x: 28, y: 52 }, size: { w: 260, h: 230 }, colorToken: 'red', label: '当魔法' },
      { id: 'm2', type: 'warning-icon', position: { x: 50, y: 52 }, size: { w: 260, h: 230 }, colorToken: 'orange', label: '漏文件' },
      { id: 'm3', type: 'warning-icon', position: { x: 72, y: 52 }, size: { w: 260, h: 230 }, colorToken: 'yellow', label: '不存版本' },
    ],
    texts: [
      { id: 'top', text: '三个坑', position: 'top', emphasis: true },
      { id: 'bottom', text: '别当魔法 / 别漏文件 / 要存版本', position: 'bottom' },
    ],
    motion: [
      { targetId: 'm1', type: 'shake', startFrame: 80, durationFrames: 80 },
      { targetId: 'm2', type: 'shake', startFrame: 220, durationFrames: 80 },
      { targetId: 'm3', type: 'shake', startFrame: 365, durationFrames: 80 },
    ],
    transitionOut: 'wipe',
  },
  {
    id: 'scene_07_whole_life_close',
    durationInFrames: 455,
    goal: '收束：回到"完整的一生"母题。',
    concept: '助产 → 创作者 → 尸检，出生与落幕连成闭环。',
    narration:
      '一个助产士，一个法医，一头一尾。中间那段创作，还是我自己来。但有了这两份手册，我不再是每次从零开始，AI 也不再是转头就忘的临时工。从一个念头出生，到一个作品落幕。这一回，有人替我认真对待了它的一生。',
    narrationBeats: [
      { id: 'teaching_14_two_ends', startFrame: 0, durationInFrames: 145, text: '一个助产士，一个法医，一头一尾。中间那段创作，还是我自己来。', linkedSubjectIds: ['midwife', 'creator', 'coroner'] },
      { id: 'teaching_15_not_from_zero', startFrame: 145, durationInFrames: 160, text: '但有了这两份手册，我不再是每次从零开始，AI 也不再是转头就忘的临时工。', linkedSubjectIds: ['midwife', 'coroner'] },
      { id: 'teaching_16_life_loop', startFrame: 305, durationInFrames: 150, text: '从一个念头出生，到一个作品落幕。这一回，有人替我认真对待了它的一生。', emphasis: true, linkedSubjectIds: ['birth', 'end'] },
    ],
    layout: 'circular-system',
    background: 'workspace',
    subjects: [
      { id: 'creator', type: 'human', position: { x: 50, y: 56 }, size: { w: 230, h: 300 }, colorToken: 'sky' },
      { id: 'midwife', type: 'manual', position: { x: 30, y: 40 }, size: { w: 210, h: 170 }, colorToken: 'yellow', label: '助产' },
      { id: 'coroner', type: 'manual', position: { x: 70, y: 40 }, size: { w: 210, h: 170 }, colorToken: 'sky', label: '尸检' },
      { id: 'birth', type: 'index-card', position: { x: 32, y: 72 }, size: { w: 200, h: 130 }, colorToken: 'green', label: '出生' },
      { id: 'end', type: 'index-card', position: { x: 68, y: 72 }, size: { w: 200, h: 130 }, colorToken: 'purple', label: '落幕' },
    ],
    texts: [
      { id: 'top', text: '一头接生，一头验尸', position: 'top', emphasis: true },
      { id: 'bottom', text: '认真对待它的一生', position: 'bottom', emphasis: true },
    ],
    motion: [
      { targetId: 'creator', type: 'pop-in', startFrame: 0, durationFrames: 30 },
      { targetId: 'midwife', type: 'zoom', startFrame: 20, durationFrames: 70 },
      { targetId: 'coroner', type: 'zoom', startFrame: 40, durationFrames: 70 },
      { targetId: 'birth', type: 'pulse', startFrame: 305, durationFrames: 90 },
      { targetId: 'end', type: 'pulse', startFrame: 340, durationFrames: 90 },
    ],
    transitionOut: 'fade',
  },
  {
    id: 'scene_08_author_note',
    durationInFrames: 450,
    goal: '作者的话（压缩版）：不会剪辑也能表达，代码开源。',
    concept: '画面/配音/剪辑都来自 AI，最后落到开源。',
    narration:
      '一句私心：我自己不会剪辑，这条片子从画面、配音到剪辑，全是 AI 按 Skill 做的。我想验证的就是，只要把流程写清楚，不会剪辑的人，也能把想法变成作品。代码会开源，欢迎一起来调试。',
    narrationBeats: [
      { id: 'author_01_cant_edit', startFrame: 0, durationInFrames: 190, text: '一句私心：我自己不会剪辑，这条片子从画面、配音到剪辑，全是 AI 按 Skill 做的。', emphasis: true, linkedSubjectIds: ['ai_core', 'image', 'voice', 'edit'] },
      { id: 'author_02_validate', startFrame: 190, durationInFrames: 170, text: '我想验证的就是，只要把流程写清楚，不会剪辑的人，也能把想法变成作品。', linkedSubjectIds: ['ai_core'] },
      { id: 'author_03_open_source', startFrame: 360, durationInFrames: 90, text: '代码会开源，欢迎一起来调试。', emphasis: true, linkedSubjectIds: ['opensource'] },
    ],
    layout: 'network-map',
    background: 'data',
    subjects: [
      { id: 'ai_core', type: 'ai-assistant', position: { x: 50, y: 50 }, size: { w: 260, h: 260 }, colorToken: 'cyan', label: 'AI' },
      { id: 'image', type: 'index-card', position: { x: 28, y: 38 }, size: { w: 220, h: 130 }, colorToken: 'yellow', label: '画面' },
      { id: 'voice', type: 'index-card', position: { x: 28, y: 66 }, size: { w: 220, h: 130 }, colorToken: 'green', label: '配音' },
      { id: 'edit', type: 'index-card', position: { x: 72, y: 38 }, size: { w: 220, h: 130 }, colorToken: 'purple', label: '剪辑' },
      { id: 'opensource', type: 'manual', position: { x: 72, y: 66 }, size: { w: 220, h: 170 }, colorToken: 'orange', label: '开源' },
    ],
    texts: [
      { id: 'top', text: '画面 / 配音 / 剪辑，全是 AI 做的', position: 'top', emphasis: true },
      { id: 'bottom', text: '代码会开源', position: 'bottom' },
    ],
    motion: [
      { targetId: 'ai_core', type: 'scale-up', startFrame: 0, durationFrames: 36 },
      { targetId: 'image', type: 'pop-in', startFrame: 60, durationFrames: 24 },
      { targetId: 'voice', type: 'pop-in', startFrame: 90, durationFrames: 24 },
      { targetId: 'edit', type: 'pop-in', startFrame: 120, durationFrames: 24 },
      { targetId: 'opensource', type: 'pop-in', startFrame: 360, durationFrames: 30 },
    ],
    transitionOut: 'fade',
  },
];

export const TOTAL_FRAMES = sceneSpecs.reduce((sum, scene) => sum + scene.durationInFrames, 0);
