import type { CSSProperties } from 'react';
import { interpolate, spring } from 'remotion';
import type { MotionSpec } from '../data/sceneSpecs';

const clamp = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };

const progressFor = (frame: number, motion: MotionSpec) =>
  interpolate(frame, [motion.startFrame, motion.startFrame + motion.durationFrames], [0, 1], clamp);

const springFor = (frame: number, fps: number, motion: MotionSpec) =>
  spring({
    fps,
    frame: Math.max(0, frame - motion.startFrame),
    config: { damping: 18, stiffness: 110, mass: 0.9 },
    durationInFrames: motion.durationFrames,
  });

export const mergeMotionStyles = (frame: number, fps: number, motions: MotionSpec[]): CSSProperties => {
  const active = motions.find((motion) => {
    const endFrame = motion.startFrame + motion.durationFrames;
    return frame >= motion.startFrame && frame <= endFrame;
  });

  if (!active) {
    const first = motions[0];
    if (first && frame < first.startFrame) {
      return { opacity: 0 };
    }
    return {};
  }

  const progress = progressFor(frame, active);
  const sprung = springFor(frame, fps, active);
  const intensity = active.intensity ?? 1;

  switch (active.type) {
    case 'fade-in':
      return { opacity: progress };
    case 'pop-in':
      return { opacity: progress, transform: `scale(${interpolate(sprung, [0, 1], [0.55, 1], clamp)})` };
    case 'scale-up':
      return { opacity: progress, transform: `scale(${interpolate(sprung, [0, 1], [0.82, 1], clamp)})` };
    case 'slide-in': {
      const distance = 90 * intensity;
      const axis = active.direction === 'up' || active.direction === 'down' ? 'Y' : 'X';
      const sign = active.direction === 'right' || active.direction === 'down' ? 1 : -1;
      const value = interpolate(sprung, [0, 1], [distance * sign, 0], clamp);
      return { opacity: progress, transform: `translate${axis}(${value}px)` };
    }
    case 'pulse': {
      const scale = 1 + Math.sin((frame - active.startFrame) / 8) * 0.055 * intensity;
      return { opacity: 1, transform: `scale(${scale})` };
    }
    case 'shake': {
      const x = Math.sin((frame - active.startFrame) * 0.8) * 14 * intensity * (1 - progress);
      return { opacity: 1, transform: `translateX(${x}px)` };
    }
    case 'compress': {
      const scaleX = interpolate(sprung, [0, 1], [1.35, 1], clamp);
      const scaleY = interpolate(sprung, [0, 1], [0.72, 1], clamp);
      return { opacity: progress, transform: `scale(${scaleX}, ${scaleY})` };
    }
    case 'scatter': {
      const x = interpolate(progress, [0, 1], [0, 70 * intensity], clamp);
      const y = interpolate(progress, [0, 1], [0, -45 * intensity], clamp);
      return { opacity: interpolate(progress, [0, 0.25, 1], [1, 1, 0.36], clamp), transform: `translate(${x}px, ${y}px)` };
    }
    case 'connect': {
      const scaleX = interpolate(progress, [0, 1], [0.15, 1], clamp);
      return { opacity: progress, transform: `scaleX(${scaleX})` };
    }
    case 'zoom':
      return { opacity: progress, transform: `scale(${interpolate(sprung, [0, 1], [0.68, 1], clamp)})` };
    case 'wipe':
      return { opacity: progress, clipPath: `inset(0 ${interpolate(progress, [0, 1], [100, 0], clamp)}% 0 0)` };
    default:
      return {};
  }
};
