export type Scene04VoiceoverTimingBeat = {
  id: string;
  text: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

export const scene04VoiceoverTiming = {
  hasGeneratedAudio: true,
  fps: 30,
  totalFrames: 251,
  beats: [
    {
        "id": "scene04_beat01_repeated_input",
        "text": "重复输入，不是经验",
        "audioSrc": "audio/scene_04/scene04_beat01_repeated_input.mp3",
        "startFrame": 0,
        "durationInFrames": 76,
        "durationSeconds": 2.24
    },
    {
        "id": "scene04_beat02_compress_to_process",
        "text": "经过压缩，才变成流程",
        "audioSrc": "audio/scene_04/scene04_beat02_compress_to_process.mp3",
        "startFrame": 76,
        "durationInFrames": 92,
        "durationSeconds": 2.8
    },
    {
        "id": "scene04_beat03_skill_manual",
        "text": "Skill 是可复用的工作手册",
        "audioSrc": "audio/scene_04/scene04_beat03_skill_manual.mp3",
        "startFrame": 168,
        "durationInFrames": 83,
        "durationSeconds": 2.48
    }
] satisfies Scene04VoiceoverTimingBeat[],
};
