import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { NarrationBeat, TextSpec } from '../data/sceneSpecs';

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
        bottom: 56,
        transform: `translateX(-50%) translateY(${translateY}px)`,
        zIndex: 30,
        maxWidth: '76%',
        padding: emphasis ? '16px 34px' : '14px 30px',
        borderRadius: 999,
        background: 'rgba(16, 24, 39, 0.84)',
        border: '1px solid rgba(255,255,255,0.16)',
        boxShadow: '0 16px 36px rgba(2, 6, 23, 0.18)',
        color: '#F8FAFC',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: emphasis ? 40 : 32,
        fontWeight: emphasis ? 800 : 680,
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
