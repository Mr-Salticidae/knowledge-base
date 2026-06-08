import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { NarrationBeat, TextSpec } from '../data/sceneSpecs';
import { theme } from '../styles/palette';

type Props = {
  beats?: NarrationBeat[];
  fallbackTexts: TextSpec[];
};

const getActiveBeat = (frame: number, beats?: NarrationBeat[]) =>
  beats?.find((beat) => frame >= beat.startFrame && frame <= beat.startFrame + beat.durationInFrames);

const getFallbackText = (texts: TextSpec[]) => texts.find((text) => text.emphasis) ?? texts[0];

export const NarrationCaption: React.FC<Props> = ({ beats, fallbackTexts }) => {
  const frame = useCurrentFrame();
  const activeBeat = getActiveBeat(frame, beats);
  const fallback = beats?.length ? undefined : getFallbackText(fallbackTexts);
  const text = activeBeat?.text ?? fallback?.text;
  const emphasis = activeBeat?.emphasis ?? fallback?.emphasis ?? false;

  if (!text) {
    return null;
  }

  const localFrame = activeBeat ? frame - activeBeat.startFrame : frame - (fallback?.delayFrames ?? 0);
  const opacity = interpolate(localFrame, [0, 10, Math.max(16, (activeBeat?.durationInFrames ?? 90) - 12), activeBeat?.durationInFrames ?? 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const translateY = interpolate(localFrame, [0, 14], [10, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        bottom: 54,
        transform: `translateX(-50%) translateY(${translateY}px)`,
        zIndex: 30,
        maxWidth: '68%',
        padding: emphasis ? '18px 34px' : '16px 32px',
        borderRadius: 28,
        background: '#FFFFFF',
        border: `6px solid ${theme.border}`,
        boxShadow: '12px 12px 0 rgba(24, 35, 58, 0.14)',
        color: theme.darkText,
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: emphasis ? 42 : 34,
        fontWeight: emphasis ? 900 : 750,
        lineHeight: 1.25,
        textAlign: 'center',
        whiteSpace: 'normal',
        opacity,
      }}
    >
      {text}
    </div>
  );
};
