export type Scene04VoiceoverBeat = {
  id: string;
  text: string;
  ttsText: string;
};

export type PronunciationFix = {
  match: string;
  replacement: string;
  note: string;
};

export const pronunciationFixes: PronunciationFix[] = [
  {
    match: '调用',
    replacement: '调 用',
    note: '降低 ElevenLabs 把 调用 读成 tiao yong 的概率；字幕仍保留 调用。',
  },
];

export const applyPronunciationFixes = (text: string) =>
  pronunciationFixes.reduce((current, fix) => current.replaceAll(fix.match, fix.replacement), text);

export const scene04VoiceoverBeats: Scene04VoiceoverBeat[] = [
  {
    id: 'scene04_beat01_repeated_input',
    text: '重复输入，不是经验',
    ttsText: '[calm] 重复输入，不是经验。',
  },
  {
    id: 'scene04_beat02_compress_to_process',
    text: '经过压缩，才变成流程',
    ttsText: '[slight pause] 经过压缩，才变成流程。',
  },
  {
    id: 'scene04_beat03_skill_manual',
    text: 'Skill 是可复用的工作手册',
    ttsText: '[confident] Skill，是可复用的工作手册。',
  },
];

export const scene04AudioPublicDir = 'audio/scene_04';
