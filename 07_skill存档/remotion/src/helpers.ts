import { interpolate, spring } from 'remotion';
import { SPRING } from './design-tokens';

export const fadeUp = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const progress = spring({ fps, frame: f, config: SPRING.enter, durationInFrames: 20 });
  return {
    opacity: interpolate(progress, [0, 1], [0, 1]),
    transform: `translateY(${interpolate(progress, [0, 1], [24, 0])}px)`,
  };
};

export const fadeLeft = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const progress = spring({ fps, frame: f, config: SPRING.enter, durationInFrames: 18 });
  return {
    opacity: interpolate(progress, [0, 1], [0, 1]),
    transform: `translateX(${interpolate(progress, [0, 1], [-20, 0])}px)`,
  };
};

export const fade = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const opacity = interpolate(f, [0, 18], [0, 1], { extrapolateRight: 'clamp' });
  return { opacity };
};
