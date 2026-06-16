import { fullFilmVoiceoverTiming } from './generated/fullFilmVoiceoverTiming';
import {
  sceneSpecs,
  type MotionSpec,
  type NarrationBeat,
  type SceneSpec,
} from '../data/sceneSpecs';

/**
 * 以 fullFilmVoiceoverTiming（真实 Eleven 旁白时长）为唯一时间真相，
 * 重新推导全片时间线：scene 时长、逐字字幕 beat，以及 **重锚后的 motion**。
 *
 * 背景（2026-06-09 全片复盘「问题三：动画时长不能靠估算」）：
 * sceneSpecs 里的 motion.startFrame / durationFrames 当初是按「估算」的
 * narrationBeats 写的；后来才生成真实音频。旧版 FullFilmVideo 只用真实时长
 * 覆盖了 scene 时长和字幕，却把 motion 原样带过来，导致每个动画相对字幕错位
 * （subject 在首个 motion 触发前是隐藏的，错位尤其明显）。
 *
 * 这里把 motion 锚定到「真实 beat」上：
 * - 估算 beat 数 == 真实 beat 数：逐段线性映射，动画精确跟随每句口播。
 * - 数量不一致：退化为整场景比例映射，并标记 fallback 供人工审核。
 */

const sceneById = new Map(sceneSpecs.map((scene) => [scene.id, scene]));

type RealBeat = (typeof fullFilmVoiceoverTiming.beats)[number];

export type DerivedScene = SceneSpec & {
  /** motion 已按真实音频重锚 */
  motionReanchored: true;
  /** true 表示估算/真实 beat 数不一致，motion 用了整场景比例映射，需人工审核 */
  motionReanchorFallback: boolean;
};

type Segment = { start: number; dur: number };

const cumulativeSegments = (durations: number[]): Segment[] => {
  let cursor = 0;
  return durations.map((dur) => {
    const start = cursor;
    cursor += dur;
    return { start, dur };
  });
};

const reanchorMotion = (
  motions: MotionSpec[],
  estBeats: NarrationBeat[],
  realDurations: number[],
): { motions: MotionSpec[]; fallback: boolean } => {
  const realSegments = cumulativeSegments(realDurations);
  const realSceneDur = realDurations.reduce((sum, d) => sum + d, 0);

  const estSegments: Segment[] = estBeats.map((beat) => ({
    start: beat.startFrame,
    dur: beat.durationInFrames,
  }));
  const estDomainEnd = estSegments.length
    ? estSegments[estSegments.length - 1].start + estSegments[estSegments.length - 1].dur
    : 0;

  const perBeat = estSegments.length === realSegments.length && estSegments.length > 0;

  const remap = (frame: number): { frame: number; scale: number } => {
    if (!perBeat || estDomainEnd === 0) {
      const scale = estDomainEnd > 0 ? realSceneDur / estDomainEnd : 1;
      return { frame: frame * scale, scale };
    }
    // 找到包含该帧的估算 beat 段（超出末段则归到末段）
    let index = estSegments.findIndex((seg) => frame < seg.start + seg.dur);
    if (index === -1) {
      index = estSegments.length - 1;
    }
    const est = estSegments[index];
    const real = realSegments[index];
    const scale = est.dur > 0 ? real.dur / est.dur : 1;
    return { frame: real.start + (frame - est.start) * scale, scale };
  };

  const mapped = motions.map<MotionSpec>((motion) => {
    const { frame: rawStart, scale } = remap(motion.startFrame);
    const startFrame = Math.max(
      0,
      Math.min(Math.round(rawStart), Math.max(0, realSceneDur - 1)),
    );
    const durationFrames = Math.max(
      1,
      Math.min(Math.round(motion.durationFrames * scale), Math.max(1, realSceneDur - startFrame)),
    );
    return { ...motion, startFrame, durationFrames };
  });

  return { motions: mapped, fallback: !perBeat };
};

/** 把连续同 sceneId 的真实 beat 聚成一组（真实 beats 已按场景顺序排列） */
const groupRealBeatsByScene = (): { sceneId: string; beats: RealBeat[] }[] => {
  const groups: { sceneId: string; beats: RealBeat[] }[] = [];
  for (const beat of fullFilmVoiceoverTiming.beats) {
    const last = groups[groups.length - 1];
    if (last && last.sceneId === beat.sceneId) {
      last.beats.push(beat);
    } else {
      groups.push({ sceneId: beat.sceneId, beats: [beat] });
    }
  }
  return groups;
};

export const fullFilmTimeline: DerivedScene[] = groupRealBeatsByScene().flatMap((group) => {
  const source = sceneById.get(group.sceneId);
  if (!source) {
    return [];
  }

  const realDurations = group.beats.map((beat) => beat.durationInFrames);
  const sceneDuration = realDurations.reduce((sum, d) => sum + d, 0);

  let cursor = 0;
  const narrationBeats: NarrationBeat[] = group.beats.map((beat) => {
    const startFrame = cursor;
    cursor += beat.durationInFrames;
    return {
      id: beat.id,
      startFrame,
      durationInFrames: beat.durationInFrames,
      text: beat.caption,
    };
  });

  const { motions, fallback } = reanchorMotion(
    source.motion,
    source.narrationBeats ?? [],
    realDurations,
  );

  const derived: DerivedScene = {
    ...source,
    durationInFrames: sceneDuration,
    narration: group.beats.map((beat) => beat.caption).join(''),
    narrationBeats,
    motion: motions,
    motionReanchored: true,
    motionReanchorFallback: fallback,
  };

  return [derived];
});

export const FULL_FILM_FRAMES = fullFilmVoiceoverTiming.totalFrames;

export const fullFilmTimelineTailFrames = Math.max(
  0,
  FULL_FILM_FRAMES - fullFilmTimeline.reduce((sum, scene) => sum + scene.durationInFrames, 0),
);

/** 估算/真实 beat 数不一致、motion 用了比例 fallback 的场景，需人工审核动画落点 */
export const fullFilmMotionFallbackScenes = fullFilmTimeline
  .filter((scene) => scene.motionReanchorFallback)
  .map((scene) => scene.id);
