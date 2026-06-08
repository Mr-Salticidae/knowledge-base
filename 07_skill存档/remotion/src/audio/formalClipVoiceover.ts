export type FormalClipVoiceoverBeat = {
  id: string;
  sceneId: string;
  caption: string;
  ttsText: string;
};

export const formalClipVoiceoverBeats: FormalClipVoiceoverBeat[] = [
  {
    id: 'formal_clip_01_ai_forgets',
    sceneId: 'ai_forgets',
    caption: 'AI 很聪明，但每次新对话，它都会忘记你刚教过的规则。',
    ttsText: '[calm] AI 很聪明，但每次新对话，它都会忘记你刚教过的规则。',
  },
  {
    id: 'formal_clip_02_compress_to_skill',
    sceneId: 'compress_to_skill',
    caption: '所以，反复输入的内容，不该继续堆 prompt，而要压缩成流程。',
    ttsText: '[slight pause] 所以，反复输入的内容，不该继续堆 prompt，而要压缩成流程。',
  },
  {
    id: 'formal_clip_03_markdown_structure',
    sceneId: 'markdown_structure',
    caption: 'Skill 本质上，是一份可读的工作手册，写清角色、步骤和避坑。',
    ttsText: 'Skill 本质上，是一份可读的工作手册，写清角色、步骤和避坑。',
  },
  {
    id: 'formal_clip_04_skill_index',
    sceneId: 'skill_index',
    caption: '技能索引像目录，告诉 AI 什么时候调用哪一本手册。',
    ttsText: '技能索引像目录，告诉 AI 什么时候调用哪一本手册。',
  },
  {
    id: 'formal_clip_05_tool_loop',
    sceneId: 'tool_loop',
    caption: '最后，MJ 建视觉锚，Seedance 让机制动起来，Remotion 负责时间线和字幕。',
    ttsText: '[confident] 最后，MJ 建视觉锚，Seedance 让机制动起来，Remotion 负责时间线和字幕。',
  },
];

export const formalClipVoiceoverText = formalClipVoiceoverBeats.map((beat) => beat.ttsText).join('\n\n');

export const formalClipVoiceover = {
  id: 'formal_clip_20260608_voiceover',
  audioPublicDir: 'audio/formal_clip_20260608',
  audioPublicPath: 'audio/formal_clip_20260608/voiceover.mp3',
  manifestPublicPath: 'audio/formal_clip_20260608/voiceover.manifest.json',
  text: formalClipVoiceoverText,
  lineCount: formalClipVoiceoverBeats.length,
};
