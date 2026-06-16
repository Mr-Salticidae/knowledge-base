import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fullFilmVoiceover, fullFilmVoiceoverBeats } from '../src/audio/fullFilmVoiceover';

/**
 * 写一份 **provisional（估算）** 的 fullFilmVoiceoverTiming，用于在没有真实 Eleven 音频时
 * 预览新文稿/新视觉的节奏。每个 beat 的时长按可见字符数估算，hasGeneratedAudio=false
 * （FullFilmVoiceoverAudio 会据此静音）。真实音频生成后由 generate-full-film-voiceover.ts 覆盖。
 *
 * 用法：npx.cmd tsx scripts/estimate-full-film-timing.ts
 */

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const timingPath = path.join(projectRoot, 'src', 'audio', 'generated', 'fullFilmVoiceoverTiming.ts');

const fps = 30;
const playbackRate = Number(process.env.FULL_FILM_VOICEOVER_PLAYBACK_RATE ?? '1.05');
const tailHoldFrames = 45;

// 经验估算：中文播报约 5 字/秒，标点带停顿。0.19s/字 + 0.3s 基底。
const SECONDS_PER_CHAR = 0.19;
const BASE_SECONDS = 0.3;

const estimateSeconds = (text: string) => {
  const visible = text.replace(/\s/g, '').length;
  return Math.max(1, visible * SECONDS_PER_CHAR + BASE_SECONDS);
};

type GeneratedBeat = {
  id: string;
  section: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

const beats: GeneratedBeat[] = [];
let startFrame = 0;

for (const item of fullFilmVoiceoverBeats) {
  const durationSeconds = estimateSeconds(item.ttsText);
  // 与 generate-full-film-voiceover.ts 同一套帧公式，保证估算 → 真实切换时结构一致。
  const durationInFrames = Math.max(45, Math.ceil((durationSeconds * fps) / playbackRate) + 12);
  beats.push({
    id: item.id,
    section: item.section,
    sceneId: item.sceneId,
    caption: item.caption,
    audioSrc: `${fullFilmVoiceover.audioPublicDir}/${item.id}.mp3`,
    startFrame,
    durationInFrames,
    durationSeconds: Number(durationSeconds.toFixed(6)),
  });
  startFrame += durationInFrames;
}

const totalFrames = startFrame + tailHoldFrames;

const content = `export type FullFilmVoiceoverTimingBeat = {
  id: string;
  section: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

// PROVISIONAL（估算 timing，无真实音频）。由 scripts/estimate-full-film-timing.ts 生成。
// 真实音频生成后会被 scripts/generate-full-film-voiceover.ts 覆盖（hasGeneratedAudio=true）。
export const fullFilmVoiceoverTiming = {
  hasGeneratedAudio: false,
  fps: ${fps},
  playbackRate: ${playbackRate},
  totalFrames: ${totalFrames},
  beats: ${JSON.stringify(beats, null, 4)} satisfies FullFilmVoiceoverTimingBeat[],
};
`;

writeFileSync(timingPath, content);

console.log(
  JSON.stringify(
    { status: 'estimated', timingPath: 'src/audio/generated/fullFilmVoiceoverTiming.ts', beatCount: beats.length, totalFrames, approxSeconds: Number((totalFrames / fps).toFixed(1)) },
    null,
    2,
  ),
);
