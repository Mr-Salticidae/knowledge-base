export type FormalClipVoiceoverTimingBeat = {
  id: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

export const formalClipVoiceoverTiming = {
  hasGeneratedAudio: true,
  fps: 30,
  totalFrames: 905,
  beats: [
    {
        "id": "formal_clip_01_ai_forgets",
        "sceneId": "ai_forgets",
        "caption": "AI 很聪明，但每次新对话，它都会忘记你刚教过的规则。",
        "audioSrc": "audio/formal_clip_20260608/formal_clip_01_ai_forgets.mp3",
        "startFrame": 0,
        "durationInFrames": 161,
        "durationSeconds": 4.96
    },
    {
        "id": "formal_clip_02_compress_to_skill",
        "sceneId": "compress_to_skill",
        "caption": "所以，反复输入的内容，不该继续堆 prompt，而要压缩成流程。",
        "audioSrc": "audio/formal_clip_20260608/formal_clip_02_compress_to_skill.mp3",
        "startFrame": 161,
        "durationInFrames": 164,
        "durationSeconds": 5.04
    },
    {
        "id": "formal_clip_03_markdown_structure",
        "sceneId": "markdown_structure",
        "caption": "Skill 本质上，是一份可读的工作手册，写清角色、步骤和避坑。",
        "audioSrc": "audio/formal_clip_20260608/formal_clip_03_markdown_structure.mp3",
        "startFrame": 325,
        "durationInFrames": 178,
        "durationSeconds": 5.52
    },
    {
        "id": "formal_clip_04_skill_index",
        "sceneId": "skill_index",
        "caption": "技能索引像目录，告诉 AI 什么时候调用哪一本手册。",
        "audioSrc": "audio/formal_clip_20260608/formal_clip_04_skill_index.mp3",
        "startFrame": 503,
        "durationInFrames": 156,
        "durationSeconds": 4.8
    },
    {
        "id": "formal_clip_05_tool_loop",
        "sceneId": "tool_loop",
        "caption": "最后，MJ 建视觉锚，Seedance 让机制动起来，Remotion 负责时间线和字幕。",
        "audioSrc": "audio/formal_clip_20260608/formal_clip_05_tool_loop.mp3",
        "startFrame": 659,
        "durationInFrames": 216,
        "durationSeconds": 6.8
    }
] satisfies FormalClipVoiceoverTimingBeat[],
};
